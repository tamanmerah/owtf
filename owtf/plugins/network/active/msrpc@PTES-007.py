"""
Plugin for probing MsRpc
"""
from owtf.managers.resource import get_resources
from owtf.plugin.plugin_api import plugin_api

DESCRIPTION = " MsRpc Probing "


def run(PluginInfo):
    resource = get_resources('MsRpcProbeMethods')
    # No previous output
    return plugin_api.CommandDump('Test Command', 'Output', resource, PluginInfo, [])
