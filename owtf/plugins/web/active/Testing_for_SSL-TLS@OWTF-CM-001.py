"""
ACTIVE Plugin for Testing for SSL-TLS (OWASP-CM-001)
"""
from owtf.managers.resource import get_resources
from owtf.plugin.plugin_api import plugin_api

DESCRIPTION = "Active probing for SSL configuration"


def run(PluginInfo):
    resource = get_resources('ActiveSSLCmds')
    Content = plugin_api.CommandDump('Test Command', 'Output', resource, PluginInfo, [])  # No previous output
    return Content
