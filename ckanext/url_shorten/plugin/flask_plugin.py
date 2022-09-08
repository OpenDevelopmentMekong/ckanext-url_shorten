import ckan.plugins as plugins
from ckanext.url_shorten.views import url_shortner
import click
from ..model import init_table

class UrlShortenMixinFlask(plugins.SingletonPlugin):
    plugins.implements(plugins.IBlueprint)
    plugins.implements(plugins.IClick)

    # IBlueprint
    def get_blueprint(self):
        # blueprint for this extension
        return [url_shortner]

    def get_commands(self):
        @click.group('urlshortener')
        def urlshortener():
            pass

        @urlshortener.command('initdb')
        def initdb():
            init_table()

        return [urlshortener]
