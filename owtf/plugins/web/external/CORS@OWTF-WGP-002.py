"""
Plugin for manual/external CORS testing
"""
from owtf.managers.resource import get_resources
from owtf.plugin.plugin_api import plugin_api

DESCRIPTION = "CORS Plugin to assist manual testing"


def run(PluginInfo):
    resource = get_resources('ExternalCORS')
    Content = plugin_api.resource_linklist('Online Resources', resource)
    return Content
