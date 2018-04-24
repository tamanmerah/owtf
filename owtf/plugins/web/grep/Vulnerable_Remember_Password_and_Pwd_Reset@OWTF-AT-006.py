"""
GREP Plugin for Vulnerable Remember Password and Pwd Reset (OWASP-AT-006)
NOTE: GREP plugins do NOT send traffic to the target and only grep the HTTP Transaction Log
"""
from owtf.plugin.plugin_api import plugin_api

DESCRIPTION = "Searches transaction DB for autocomplete protections"


def run(PluginInfo):
    title = "This plugin looks for password and form tags to review the autocomplete attribute<br />"
    Content = plugin_api.HtmlString(title)
    Content += plugin_api.FindResponseBodyMatchesForRegexpName('RESPONSE_REGEXP_FOR_AUTOCOMPLETE')
    return Content
