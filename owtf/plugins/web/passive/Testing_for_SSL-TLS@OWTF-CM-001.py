"""
PASSIVE Plugin for Testing_for_SSL-TLS_(OWASP-CM-001)
"""
from owtf.plugin.plugin_api import plugin_api

DESCRIPTION = "Third party resources"


def run(PluginInfo):
    # Vuln search box to be built in core and resued in different plugins:
    resource = get_resources('PassiveSSL')
    Content = plugin_api.resource_linklist('Online Resources', resource)
    return Content
