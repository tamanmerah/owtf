"""
owtf.plugin.plugin_api
~~~~~~~~~~~~~~~~~~~~~~

This module contains helper functions to make plugins simpler to read and write,
centralising common functionality easy to reuse
"""
import cgi
import logging
import os
import re

from tornado.template import Template

from owtf.db.session import get_scoped_session
from owtf.http.requester import requester
from owtf.lib.exceptions import FrameworkAbortException, PluginAbortException
from owtf.managers.config import config_handler
from owtf.managers.target import target_manager
from owtf.managers.url import add_url, get_urls_to_visit, import_urls
from owtf.plugin.runner import plugin_runner
from owtf.shell.base import shell
from owtf.utils.file import FileOperations
from owtf.utils.strings import multi_replace
from owtf.utils.timer import timer

__all__ = ['plugin_api']

PLUGIN_OUTPUT = {"type": None, "output": None}  # This will be json encoded and stored in db as string


class PluginAPI(object):

    lines_to_show = 25

    def __init__(self):
        self.runner = plugin_runner
        self.requester = requester
        self.shell = shell
        self.timer = timer
        self.session = get_scoped_session()
        # Compile regular expressions only once on init:
        self.robots_allow_regex = re.compile("Allow: ([^\n  #]+)")
        self.robots_disallow_regex = re.compile("Disallow: ([^\n #]+)")
        self.robots_sitemap = re.compile("Sitemap: ([^\n #]+)")

    def multi_replace(self, text, replace_dict):
        """ This redundant method is here so that plugins can use it

        :param text: Text to replace with
        :type text: `str`
        :param replace_dict: Dict to modify
        :type replace_dict: `dict`
        :return: Replaced dict
        :rtype: `dict`
        """
        return multi_replace(text, replace_dict)

    def request_link_list(self, resource_list_name, resource_list, plugin_info):
        link_list = []
        for name, resource in resource_list:
            Chunks = resource.split('###POST###')
            URL = Chunks[0]
            POST = None
            Method = 'GET'
            if len(Chunks) > 1:  # POST
                Method = 'POST'
                POST = Chunks[1]
                Transaction = self.requester.get_transaction(True, URL, Method, POST)
                if Transaction is not None and Transaction.found:
                    RawHTML = Transaction.get_raw_response_body()
                    FilteredHTML = cgi.escape(RawHTML)
                    NotSandboxedPath = self.runner.dump_output_file("NOT_SANDBOXED_%s.html" % name, FilteredHTML,
                                                                    plugin_info)
                    logging.info("File: NOT_SANDBOXED_%s.html saved to: %s", name, NotSandboxedPath)
                    iframe_template = Template("""
                        <iframe src="{{ NotSandboxedPath }}" sandbox="" security="restricted"  frameborder='0'
                        style="overflow-y:auto; overflow-x:hidden;width:100%;height:100%;" >
                        Your browser does not support iframes
                        </iframe>
                        """)
                    iframe = iframe_template.generate(NotSandboxedPath=NotSandboxedPath.split('/')[-1])
                    SandboxedPath = self.runner.dump_output_file("SANDBOXED_%s.html" % name, iframe, plugin_info)
                    logging.info("File: SANDBOXED_%s.html saved to: %s", name, SandboxedPath)
                    link_list.append((name, SandboxedPath))
        output = dict(PLUGIN_OUTPUT)
        output["type"] = "Requestlink_list"
        output["output"] = {"ResourceListName": resource_list_name, "link_list": link_list}
        return ([output])

    def SuggestedCommandBox(self, PluginInfo, CommandCategoryList, Header=''):
        output = dict(PLUGIN_OUTPUT)
        PluginOutputDir = self.init_plugin_output_dir(PluginInfo)
        output["type"] = "SuggestedCommandBox"
        output["output"] = {
            "PluginOutputDir": PluginOutputDir,
            "CommandCategoryList": CommandCategoryList,
            "Header": Header
        }
        return ([output])

    def set_plugin_output_dir(self, plugin_info):
        plugin_output_dir = self.runner.get_plugin_output_dir(plugin_info)
        # FULL output path for plugins to use
        target_manager.set_path('plugin_output_dir', "{}/{}".format(os.getcwd(), plugin_output_dir))
        self.shell.refresh_replacements()  # Get dynamic replacement, i.e. plugin-specific output directory
        return plugin_output_dir

    def init_plugin_output_dir(self, plugin_info):
        plugin_output_dir = self.set_plugin_output_dir(plugin_info)
        FileOperations.create_missing_dirs(plugin_output_dir)  # Create output dir so that scripts can cd to it :)
        return plugin_output_dir

    def run_command(self, command, plugin_info, plugin_output_dir):
        framework_abort = plugin_abort = False
        if not plugin_output_dir:
            plugin_output_dir = self.init_plugin_output_dir(plugin_info)
        timer.start_timer('FormatCommandAndOutput')
        modified_command = shell.get_modified_shell_cmd(command, plugin_output_dir)

        try:
            raw_output = shell.shell_exec_monitor(self.session, modified_command, plugin_info)
        except PluginAbortException as e:
            raw_output = str(e.parameter)  # Save Partial Output
            plugin_abort = True
        except FrameworkAbortException as e:
            raw_output = str(e.parameter)  # Save Partial Output
            framework_abort = True
        time_str = timer.get_elapsed_time_as_str('FormatCommandAndOutput')
        logging.info("Time=%s", time_str)
        out = [modified_command, framework_abort, plugin_abort, time_str, raw_output, plugin_output_dir]
        return out

    def get_cmd_output_extension(self, input_name):
        output_name = input_name
        output_extension = "txt"
        if input_name.split('.')[-1] in ['html']:
            output_name = input_name[0:-5]
            output_extension = "html"
        return [output_name, output_extension]

    def command_dump(self, cmd_intro, output_intro, resource_list, plugin_info, prev_output):
        output_list = []
        plugin_output_dir = self.init_plugin_output_dir(plugin_info)
        resource_list = sorted(resource_list, key=lambda x: x[0] == "Extract URLs")
        for name, command in resource_list:
            dump_file_name = "{}.txt".format(os.path.splitext(name)[0])  # Add txt extension to avoid wrong mimetypes
            output = dict(PLUGIN_OUTPUT)
            modified_command, framework_abort, plugin_abort, time_str, raw_output, plugin_output_dir = self.run_command(
                command, plugin_info, plugin_output_dir)
            output["type"] = "CommandDump"
            output["output"] = {
                "Name":
                self.get_cmd_output_extension(name)[0],
                "CommandIntro":
                cmd_intro,
                "ModifiedCommand":
                modified_command,
                "RelativeFilePath":
                self.runner.dump_output_file(dump_file_name, raw_output, plugin_info, relative_path=True),
                "OutputIntro":
                output_intro,
                "TimeStr":
                time_str
            }
            plugin_output = [output]
            # This command returns URLs for processing
            if name == config_handler.get_val('EXTRACT_URLS_RESERVED_RESOURCE_NAME'):
                #  The plugin_output output dict will be remade if the resource is of this type
                plugin_output = self.log_urls_from_str(raw_output)
            # TODO: Look below to handle streaming report
            if plugin_abort:  # Pass partial output to external handler:
                raise PluginAbortException(prev_output + plugin_output)
            if framework_abort:
                raise FrameworkAbortException(prev_output + plugin_output)
            output_list += plugin_output
        return output_list

    def log_urls_from_str(self, raw_output):
        plugin_output = dict(PLUGIN_OUTPUT)
        self.timer.start_timer('LogURLsFromStr')
        # Extract and classify URLs and store in DB
        url_list = import_urls(raw_output.strip().split("\n"))
        num_found = 0
        visit_urls = False
        # TODO: Whether or not active testing will depend on the user profile ;). Have cool ideas for profile names
        if True:
            visit_urls = True
            # Visit all URLs if not in Cache
            for Transaction in self.requester.get_transactions(True, get_urls_to_visit()):
                if Transaction is not None and Transaction.found:
                    num_found += 1
        TimeStr = self.timer.get_elapsed_time_as_str('LogURLsFromStr')
        logging.info("Spider/URL scraper time=%s", TimeStr)
        plugin_output["type"] = "URLsFromStr"
        plugin_output["output"] = {
            "TimeStr": TimeStr,
            "VisitURLs": visit_urls,
            "URLList": url_list,
            "NumFound": num_found
        }
        return [plugin_output]

    def DumpFile(self, Filename, Contents, PluginInfo, LinkName=''):
        save_path = self.runner.dump_output_file(Filename, Contents, PluginInfo)
        if not LinkName:
            LinkName = save_path
        logging.info("File: %s saved to: %s", Filename, save_path)
        template = Template("""
            <a href="{{ Link }}" target="_blank">
                {{ LinkName }}
            </a>
            """)

        return [save_path, template.generate(LinkName=LinkName, Link="../../../{!s}".format(save_path))]

    def DumpFileGetLink(self, Filename, Contents, PluginInfo, LinkName=''):
        return self.DumpFile(Filename, Contents, PluginInfo, LinkName)[1]

    def AnalyseRobotsEntries(self, Contents):  # Find the entries of each kind and count them
        num_lines = len(Contents.split("\n"))  # Total number of robots.txt entries
        AllowedEntries = list(set(
            self.robots_allow_regex.findall(Contents)))  # list(set()) is to avoid repeated entries
        num_allow = len(AllowedEntries)  # Number of lines that start with "Allow:"
        DisallowedEntries = list(set(self.robots_disallow_regex.findall(Contents)))
        num_disallow = len(DisallowedEntries)  # Number of lines that start with "Disallow:"
        SitemapEntries = list(set(self.robots_sitemap.findall(Contents)))
        num_sitemap = len(SitemapEntries)  # Number of lines that start with "Sitemap:"
        RobotsFound = True
        if 0 == num_allow and 0 == num_disallow and 0 == num_sitemap:
            RobotsFound = False
        return [
            num_lines, AllowedEntries, num_allow, DisallowedEntries, num_disallow, SitemapEntries, num_sitemap,
            RobotsFound
        ]

    def process_robots(self, PluginInfo, Contents, LinkStart, LinkEnd, Filename='robots.txt'):
        plugin_output = dict(PLUGIN_OUTPUT)
        plugin_output["type"] = "Robots"
        num_lines, AllowedEntries, num_allow, DisallowedEntries, num_disallow, SitemapEntries, num_sitemap, NotStr = \
            self.AnalyseRobotsEntries(Contents)
        SavePath = self.runner.dump_output_file(Filename, Contents, PluginInfo, True)
        TopURL = target_manager.get_val('top_url')
        EntriesList = []
        # robots.txt contains some entries, show browsable list! :)
        if num_disallow > 0 or num_allow > 0 or num_sitemap > 0:
            for Display, Entries in [['Disallowed Entries', DisallowedEntries], ['Allowed Entries', AllowedEntries],
                                     ['Sitemap Entries', SitemapEntries]]:
                Links = []  # Initialise category-specific link list
                for Entry in Entries:
                    if 'Sitemap Entries' == Display:
                        URL = Entry
                        add_url(self.session, URL)  # Store real links in the DB
                        Links.append([Entry, Entry])  # Show link in defined format (passive/semi_passive)
                    else:
                        URL = TopURL + Entry
                        add_url(self.session, URL)  # Store real links in the DB
                        # Show link in defined format (passive/semi_passive)
                        Links.append([Entry, LinkStart + Entry + LinkEnd])
                EntriesList.append((Display, Links))
                plugin_output["output"] = {
                    "NotStr": NotStr,
                    "NumLines": num_lines,
                    "NumAllow": num_allow,
                    "NumDisallow": num_disallow,
                    "NumSitemap": num_sitemap,
                    "SavePath": SavePath,
                    "EntriesList": EntriesList
                }
                return ([plugin_output])


plugin_api = PluginAPI()
