"""
SEMI-PASSIVE Plugin for Search engine discovery/reconnaissance (OWASP-IG-002)
"""
from owtf.managers.resource import get_resources
from owtf.plugin.plugin_api import plugin_api

DESCRIPTION = "Metadata analysis"
ATTR = {'INTERNET_RESOURCES': True}


def run(PluginInfo):
    resource = get_resources('SemiPassiveSearchEngineDiscoveryCmd')
    Content = plugin_api.CommandDump('Test Command', 'Output', resource, PluginInfo, [])  # No previous output
    return Content
