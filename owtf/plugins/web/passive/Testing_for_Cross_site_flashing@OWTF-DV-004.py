"""
PASSIVE Plugin for Testing for Cross site flashing (OWASP-DV-004)
"""
from owtf.managers.resource import get_resources
from owtf.plugin.plugin_api import plugin_api

DESCRIPTION = "Google Hacking for Cross Site Flashing"


def run(PluginInfo):
    resource = get_resources('PassiveCrossSiteFlashingLnk')
    Content = plugin_api.resource_linklist('Online Resources', resource)
    return Content
