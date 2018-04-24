"""
Plugin for probing ftp
"""

from owtf.managers.resource import get_resources
from owtf.plugin.plugin_api import plugin_api

DESCRIPTION = " FTP Probing "


def run(PluginInfo):
    resource = get_resources('BruteFtpProbeMethods')
    return plugin_api.CommandDump('Test Command', 'Output', resource, PluginInfo, [])
