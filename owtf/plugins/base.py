from abc import ABCMeta, abstractmethod

from owtf.plugin.plugin_api import PluginAPI


class Plugin(object):
    """Abstract base class definition for plugins.
    Plugins must be a subclass of Plugin and
    must define the following members.
    """
    __metaclass__ = ABCMeta

    name = None
    description = None
    code = None
    # Type is a tuple of tags.
    # For example, ('web', 'grep')
    type = None

    def __init__(self):
        self.plugin_api = PluginAPI()

    @abstractmethod
    def run(self):
        pass
