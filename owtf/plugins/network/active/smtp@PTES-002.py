"""
Plugin for probing smtp
"""
from owtf.managers.resource import get_resources
from owtf.plugin.plugin_api import plugin_api

DESCRIPTION = " SMTP Probing "


def run(PluginInfo):
    resource = get_resources('SmtpProbeMethods')
    return plugin_api.CommandDump('Test Command', 'Output', resource, PluginInfo, [])
