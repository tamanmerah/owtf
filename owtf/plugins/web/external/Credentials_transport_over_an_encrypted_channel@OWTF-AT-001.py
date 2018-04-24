from owtf.managers.resource import get_resources
from owtf.plugin.plugin_api import plugin_api

DESCRIPTION = "Tools to assist credential transport vulnerability exploitation"


def run(PluginInfo):
    resource = get_resources('ExternalCredentialsTransport')
    Content = plugin_api.resource_linklist('Online Resources', resource)
    return Content
