"""
PASSIVE Plugin for Testing for Captcha (OWASP-AT-008)
"""
from owtf.managers.resource import get_resources
from owtf.plugin.plugin_api import plugin_api

DESCRIPTION = "Google Hacking for CAPTCHA"


def run(PluginInfo):
    resource = get_resources('PassiveCAPTCHALnk')
    Content = plugin_api.resource_linklist('Online Resources', resource)
    return Content
