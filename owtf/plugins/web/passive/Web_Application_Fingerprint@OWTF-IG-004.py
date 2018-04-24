"""
PASSIVE Plugin for Testing for Web Application Fingerprint (OWASP-IG-004)
"""
from owtf.managers.resource import get_resources
from owtf.plugin.plugin_api import plugin_api

DESCRIPTION = "Third party resources and fingerprinting suggestions"


def run(PluginInfo):
    mapping = [['All', 'CMS_FingerPrint_All'], ['WordPress', 'CMS_FingerPrint_WordPress'],
               ['Joomla', 'CMS_FingerPrint_Joomla'], ['Drupal',
                                                      'CMS_FingerPrint_Drupal'], ['Mambo', 'CMS_FingerPrint_Mambo']]
    # Vuln search box to be built in core and reused in different plugins:
    Content = plugin_api.VulnerabilitySearchBox('')
    resource = get_resources('PassiveFingerPrint')
    Content += plugin_api.resource_linklist('Online Resources', resource)
    Content += plugin_api.SuggestedCommandBox(PluginInfo, mapping, 'CMS Fingerprint - Potentially useful commands')
    return Content
