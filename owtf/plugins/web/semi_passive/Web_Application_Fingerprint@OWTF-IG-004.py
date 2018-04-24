"""
SEMI-PASSIVE Plugin for Testing for Web Application Fingerprint (OWASP-IG-004)
"""
from owtf.managers.resource import get_resources
from owtf.managers.target import get_targets_as_list
from owtf.plugin.plugin_api import plugin_api

DESCRIPTION = "Normal requests to gather fingerprint info"


def run(PluginInfo):
    # True = Use Transaction Cache if possible: Visit the start URLs if not already visited
    TransactionTable = plugin_api.TransactionTableForURLList(True, get_targets_as_list(['target_url', 'top_url']))
    resource = get_resources('SemiPassiveFingerPrint')
    Content = plugin_api.ResearchFingerprintInlog() + TransactionTable
    Content += plugin_api.CommandDump('Test Command', 'Output', resource, PluginInfo, Content)
    return Content
