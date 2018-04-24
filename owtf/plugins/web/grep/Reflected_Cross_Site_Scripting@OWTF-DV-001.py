"""
GREP Plugin for XSS
NOTE: GREP plugins do NOT send traffic to the target and only grep the HTTP Transaction Log
"""
from owtf.plugin.plugin_api import plugin_api

DESCRIPTION = "Searches transaction DB for XSS protections"


def run(PluginInfo):
    # Background: http://jeremiahgrossman.blogspot.com/2010/01/to-disable-ie8s-xss-filter-or-not.html
    title = "This plugin looks for server-side protection headers against XSS (TODO: Check vuln scanners' output!)<br/>"
    Content = plugin_api.HtmlString(title)
    Content += plugin_api.FindResponseHeaderMatchesForRegexpName('HEADERS_FOR_XSS_PROTECTION')
    return Content
