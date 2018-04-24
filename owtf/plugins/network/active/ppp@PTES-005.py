"""
Plugin for probing emc
"""
from owtf.managers.resource import get_resources
from owtf.plugin.plugin_api import plugin_api

DESCRIPTION = " EMC Probing "


def run(PluginInfo):
    resource = get_resources('EmcProbeMethods')
    return plugin_api.CommandDump('Test Command', 'Output', resource, PluginInfo, [])
