"""
GREP Plugin for CORS
NOTE: GREP plugins do NOT send traffic to the target and only grep the HTTP Transaction Log
"""
from owtf.plugin.plugin_api import plugin_api

DESCRIPTION = "Searches transaction DB for Cross Origin Resource Sharing headers"


def run(PluginInfo):
    title = "This plugin looks for HTML 5 Cross Origin Resource Sharing (CORS) headers<br/>"
    Content = plugin_api.HtmlString(title)
    Content += plugin_api.FindResponseHeaderMatchesForRegexpName('HEADERS_FOR_CORS')
    Content += plugin_api.FindResponseHeaderMatchesForRegexpName('HEADERS_REGEXP_FOR_CORS_METHODS')
    return Content
