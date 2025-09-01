from mkdocs.plugins import BasePlugin


class HelloWorldPlugin(BasePlugin):
    def on_config(self, config):
        print("Hello World from MkDocs plugin!")
        return config
