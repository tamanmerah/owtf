"""
PASSIVE Plugin for Testing for Error Code (OWASP-IG-006)
https://www.owasp.org/index.php/Testing_for_Error_Code_%28OWASP-IG-006%29
"""
from owtf.managers.resource import get_resources
from owtf.plugin.plugin_api import plugin_api

DESCRIPTION = "Google Hacking for Error codes"


def run(PluginInfo):
    resource = get_resources('PassiveErrorMessagesLnk')
    Content = plugin_api.resource_linklist('Online Resources', resource)
    return Content
