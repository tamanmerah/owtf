"""
Plugin for probing mssql
"""
from owtf.managers.resource import get_resources
from owtf.plugin.plugin_api import plugin_api

DESCRIPTION = " MsSql Probing "


def run(PluginInfo):
    resource = get_resources('BruteMsSqlProbeMethods')
    return plugin_api.CommandDump('Test Command', 'Output', resource, PluginInfo, [])
