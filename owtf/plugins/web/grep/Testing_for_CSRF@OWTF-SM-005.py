"""
GREP Plugin for Testing for CSRF (OWASP-SM-005)
https://www.owasp.org/index.php/Testing_for_CSRF_%28OWASP-SM-005%29
NOTE: GREP plugins do NOT send traffic to the target and only grep the HTTP Transaction Log
"""
from owtf.plugin.plugin_api import plugin_api

DESCRIPTION = "Searches transaction DB for CSRF protections"


def run(PluginInfo):
    return plugin_api.FindResponseBodyMatchesForRegexpName('RESPONSE_REGEXP_FOR_HIDDEN')
