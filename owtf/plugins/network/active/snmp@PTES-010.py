"""
Plugin for probing snmp
"""
from owtf.managers.resource import get_resources
from owtf.plugin.plugin_api import plugin_api

DESCRIPTION = " SNMP Probing "


def run(PluginInfo):
    resource = get_resources('SnmpProbeMethods')
    return plugin_api.CommandDump('Test Command', 'Output', resource, PluginInfo, [])
