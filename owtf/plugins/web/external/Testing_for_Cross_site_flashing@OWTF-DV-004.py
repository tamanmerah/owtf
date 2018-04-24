from owtf.managers.resource import get_resources
from owtf.plugin.plugin_api import plugin_api

DESCRIPTION = "Cross Site Flashing Plugin to assist manual testing"


def run(PluginInfo):
    resource = get_resources('ExternalCrossSiteFlashing')
    Content = plugin_api.resource_linklist('Online Resources', resource)
    return Content
