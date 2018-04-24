"""
GREP Plugin for SSL protection
NOTE: GREP plugins do NOT send traffic to the target and only grep the HTTP Transaction Log
"""
from owtf.plugin.plugin_api import plugin_api

DESCRIPTION = "Searches transaction DB for SSL protections"


def run(PluginInfo):
    title = "This plugin looks for server-side protection headers to enforce SSL<br />"
    Content = plugin_api.HtmlString(title)
    Content += plugin_api.FindResponseHeaderMatchesForRegexpName('HEADERS_FOR_SSL_PROTECTION')
    return Content
