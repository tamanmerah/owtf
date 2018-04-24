"""
GREP Plugin for Cookies Attributes
NOTE: GREP plugins do NOT send traffic to the target and only grep the HTTP Transaction Log
"""
from owtf.plugin.plugin_api import plugin_api

DESCRIPTION = "Searches transaction DB for Cookie attributes"


def run(PluginInfo):
    title = "This plugin looks for cookie setting headers (TODO: Check vuln scanners' output!)<br />"
    Content = plugin_api.HtmlString(title)
    Content += plugin_api.FindResponseHeaderMatchesForRegexpName('HEADERS_FOR_COOKIES')
    # TODO: Fix up
    return Content
