"""
PASSIVE Plugin for Testing for Application Discovery (OWASP-IG-005)
"""
from owtf.managers.resource import get_resources
from owtf.plugin.plugin_api import plugin_api

DESCRIPTION = "Third party discovery resources"


def run(PluginInfo):
    Content = plugin_api.Tabbedresource_linklist([['DNS', get_resources('PassiveAppDiscoveryDNS')], [
        'WHOIS', get_resources('PassiveAppDiscoveryWHOIS')
    ], ['DB Lookups', get_resources('PassiveAppDiscoveryDbLookup')], ['Ping',
                                                                      get_resources('PassiveAppDiscoveryPing')],
                                                  ['Traceroute',
                                                   get_resources('PassiveAppDiscoveryTraceroute')],
                                                  ['Misc', get_resources('PassiveAppDiscoveryMisc')]])
    return Content
