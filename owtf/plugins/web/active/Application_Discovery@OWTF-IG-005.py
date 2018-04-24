"""
ACTIVE Plugin for Testing for Application Discovery (OWASP-IG-005)
"""
from owtf.managers.resource import get_resources
from owtf.plugin.plugin_api import plugin_api

DESCRIPTION = "Active probing for app discovery"


def run(PluginInfo):
    resource = get_resources('ActiveDiscovery')
    # No previous output
    return plugin_api.CommandDump('Test Command', 'Output', resource, PluginInfo, [])
