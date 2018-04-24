"""
GREP Plugin for Logout and Browse cache management
NOTE: GREP plugins do NOT send traffic to the target and only grep the HTTP Transaction Log
"""
from owtf.plugin.plugin_api import plugin_api

DESCRIPTION = "Searches transaction DB for Cache snooping protections"


def run(PluginInfo):
    title = "This plugin looks for server-side protection headers and tags against cache snooping<br />"
    Content = plugin_api.HtmlString(title)
    Content += plugin_api.FindResponseHeaderMatchesForRegexpName('HEADERS_FOR_CACHE_PROTECTION')
    Content += plugin_api.FindResponseBodyMatchesForRegexpName('RESPONSE_REGEXP_FOR_CACHE_PROTECTION')
    return Content
