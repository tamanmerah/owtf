"""
Plugin for probing x11
"""
from owtf.managers.resource import get_resources
from owtf.plugin.plugin_api import plugin_api

DESCRIPTION = " x11 Probing "


def run(PluginInfo):
    resource = get_resources('X11ProbeMethods')
    return plugin_api.CommandDump('Test Command', 'Output', resource, PluginInfo, [])  # No previous output
