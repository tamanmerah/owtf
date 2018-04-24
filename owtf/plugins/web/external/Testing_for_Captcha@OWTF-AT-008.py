"""
EXTERNAL Plugin for CAPTCHA assistance
"""
from owtf.managers.resource import get_resources
from owtf.plugin.plugin_api import plugin_api

DESCRIPTION = "Plugin to assist manual testing"


def run(PluginInfo):
    Content = plugin_api.VulnerabilitySearchBox('')
    resource = get_resources('ExternalCAPTCHA')
    Content += plugin_api.resource_linklist('Tools', resource)
    return Content
