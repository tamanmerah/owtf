"""
ACTIVE Plugin for Testing for HTTP Methods and XST (OWASP-CM-008)
"""
from owtf.managers.resource import get_resources
from owtf.managers.target import target_manager
from owtf.plugin.plugin_api import plugin_api

DESCRIPTION = "Active probing for HTTP methods"


def run(PluginInfo):
    URL = target_manager.get_val('top_url')
    # TODO: PUT not working right yet
    Content = plugin_api.TransactionTableForURL(True, URL, Method='TRACE')
    Content += plugin_api.CommandDump('Test Command', 'Output', get_resources('ActiveHTTPMethods'), PluginInfo, Content)
    return Content
