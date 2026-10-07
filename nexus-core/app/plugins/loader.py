from app.plugins.base import Plugin


class PluginLoader:
    def __init__(self):
        self.plugins: list[Plugin] = []

    def register(self, plugin: Plugin):
        self.plugins.append(plugin)

    def initialize_all(self):
        for plugin in self.plugins:
            plugin.initialize()


plugin_loader = PluginLoader()