"""
GREP Plugin for Testing for Web Application Fingerprint (OWASP-IG-004)
NOTE: GREP plugins do NOT send traffic to the target and only grep the HTTP Transaction Log
"""
from owtf.plugin.plugin_api import plugin_api

DESCRIPTION = "Searches transaction DB for fingerprint traces"


def run(PluginInfo):
    Content = plugin_api.ResearchFingerprintInlog()
    return Content
