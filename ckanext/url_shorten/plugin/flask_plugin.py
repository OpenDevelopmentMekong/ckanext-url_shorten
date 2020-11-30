import ckan.plugins as plugins
from ckanext.url_shorten.views import url_shortner


class UrlShortenMixinFlask(plugins.SingletonPlugin):
    plugins.implements(plugins.IBlueprint)

    # IBlueprint
    def get_blueprint(self):
        # blueprint for this extension
        return [url_shortner]
