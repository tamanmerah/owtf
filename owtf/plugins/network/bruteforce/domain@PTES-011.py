"""
Plugin for probing DNS
"""
from owtf.managers.resource import get_resources
from owtf.plugin.plugin_api import plugin_api

DESCRIPTION = " DNS Probing "


def run(PluginInfo):
    return plugin_api.CommandDump('Test Command', 'Output', get_resources('DomainBruteForcing'), PluginInfo, "")
