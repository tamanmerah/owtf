from owtf.plugin.plugin_api import plugin_api

DESCRIPTION = "Plugin to assist manual testing"


def run(PluginInfoz):
    Content = plugin_api.HtmlString("Intended to show helpful info in the future")
    return Content
