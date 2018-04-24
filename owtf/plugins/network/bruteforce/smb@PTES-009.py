"""
Plugin for probing SMB
"""
from owtf.managers.resource import get_resources
from owtf.plugin.plugin_api import plugin_api

DESCRIPTION = " SMB Probing "


def run(PluginInfo):
    resource = get_resources('BruteSmbProbeMethods')
    return plugin_api.CommandDump('Test Command', 'Output', resource, PluginInfo, [])
