from owtf.managers.resource import get_resources
from owtf.plugin.plugin_api import plugin_api

DESCRIPTION = "Cookie Attributes Plugin to assist manual testing"


def run(PluginInfo):
    resource = get_resources('ExternalCookiesAttributes')
    Content = plugin_api.resource_linklist('Online Hash Cracking Resources', resource)
    return Content
