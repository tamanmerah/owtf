"""
ACTIVE Plugin for Generic Unauthenticated Web App Fuzzing via Skipfish
This will perform a "low-hanging-fruit" pass on the web app for easy to find (tool-findable) vulns
"""
from owtf.managers.resource import get_resources
from owtf.plugin.plugin_api import plugin_api

DESCRIPTION = "Active Vulnerability Scanning without credentials via Skipfish"


def run(PluginInfo):
    resource = get_resources('Skipfish_Unauth')
    return plugin_api.CommandDump('Test Command', 'Output', resource, PluginInfo, [])
