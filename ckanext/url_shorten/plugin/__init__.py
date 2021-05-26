import ckan.plugins as plugins
from ckan.plugins import toolkit
from ckanext.url_shorten.logic import action


if toolkit.check_ckan_version(min_version='2.9.0'):
    from ckanext.url_shorten.plugin.flask_plugin import UrlShortenMixinFlask as UrlShorten
else:
    from ckanext.url_shorten.plugin.pylons_plugin import UrlShortenMixinPylons as UrlShorten
    

class UrlShortenMixinPlugin(UrlShorten):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IActions)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, '../templates')
        toolkit.add_public_directory(config_, '../public')
        toolkit.add_resource('../fanstatic', 'url_shorten')

    ## IActions
    def get_actions(self):
        return {
            u'get_short_url': action.get_short_url,
            u'create_short_url': action.create_short_url,
            u'update_short_url': action.update_short_url,
            u'delete_short_url': action.delete_short_url
        }
