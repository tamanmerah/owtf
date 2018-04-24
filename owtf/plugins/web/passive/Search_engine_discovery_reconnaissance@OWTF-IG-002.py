"""
PASSIVE Plugin for Search engine discovery/reconnaissance (OWASP-IG-002)
"""
from owtf.managers.resource import get_resources
from owtf.plugin.plugin_api import plugin_api

DESCRIPTION = "General Google Hacking/Email harvesting, etc"
ATTR = {'INTERNET_RESOURCES': True}


def run(PluginInfo):
    resource = get_resources('PassiveSearchEngineDiscoveryCmd')
    resource_online = get_resources('PassiveSearchEngineDiscoveryLnk')
    Content = plugin_api.CommandDump('Test Command', 'Output', resource, PluginInfo, [])
    Content += plugin_api.resource_linklist('Online Resources', resource_online)
    return Content
