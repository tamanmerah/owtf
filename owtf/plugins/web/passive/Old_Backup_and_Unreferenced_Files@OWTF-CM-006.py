"""
PASSIVE Plugin for Old, Backup and Unreferenced Files (OWASP-CM-006)
https://www.owasp.org/index.php/Testing_for_Old,_Backup_and_Unreferenced_Files_(OWASP-CM-006)
"""
from owtf.managers.resource import get_resources
from owtf.plugin.plugin_api import plugin_api

DESCRIPTION = "Google Hacking for juicy files"


def run(PluginInfo):
    resource = get_resources('PassiveOldBackupUnreferencedFilesLnk')
    return plugin_api.resource_linklist('Online Resources', resource)
