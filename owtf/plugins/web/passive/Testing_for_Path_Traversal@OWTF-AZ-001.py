"""
PASSIVE Plugin
"""
from owtf.plugin.plugin_api import plugin_api

DESCRIPTION = "Panoptic, a tool for testing local file inclusion vulnerabilities"


def run(PluginInfo):
    Content = plugin_api.SuggestedCommandBox(PluginInfo, [['All', 'Testing_for_Path_Traversal_All']],
                                             'Testing_for_Path_Traversal - Potentially useful commands')
    return Content
