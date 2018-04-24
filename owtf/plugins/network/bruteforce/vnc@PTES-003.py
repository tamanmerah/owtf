"""
Plugin for probing vnc
"""
from owtf.managers.resource import get_resources
from owtf.plugin.plugin_api import plugin_api

DESCRIPTION = " VNC Probing "


def run(PluginInfo):
    resource = get_resources('BruteVncProbeMethods')
    return plugin_api.CommandDump('Test Command', 'Output', resource, PluginInfo, [])
