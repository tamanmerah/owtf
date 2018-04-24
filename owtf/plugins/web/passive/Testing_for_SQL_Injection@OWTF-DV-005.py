"""
PASSIVE Plugin for Testing for SQL Injection (OWASP-DV-005)
https://www.owasp.org/index.php/Testing_for_SQL_Injection_%28OWASP-DV-005%29
"""
from owtf.managers.resource import get_resources
from owtf.plugin.plugin_api import plugin_api

DESCRIPTION = "Google Hacking for SQLi"


def run(PluginInfo):
    resource = get_resources('PassiveSQLInjectionLnk')
    Content = plugin_api.resource_linklist('Online Resources', resource)
    return Content
