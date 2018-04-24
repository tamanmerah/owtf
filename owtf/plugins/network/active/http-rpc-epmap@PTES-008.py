"""
Plugin for probing HTTP Rpc
"""
from owtf.managers.resource import get_resources
from owtf.plugin.plugin_api import plugin_api

DESCRIPTION = " HTTP Rpc Probing "


def run(PluginInfo):
    resource = get_resources('HttpRpcProbeMethods')
    # No previous output
    return plugin_api.CommandDump('Test Command', 'Output', resource, PluginInfo, [])
