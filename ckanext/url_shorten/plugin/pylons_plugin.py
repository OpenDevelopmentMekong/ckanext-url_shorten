import ckan.plugins as plugins
from ckan.plugins import toolkit


class UrlShortenMixinPylons(plugins.SingletonPlugin):
    plugins.implements(plugins.IRoutes, inherit=True)

    ## IRoutes
    def before_map(self, map):

        map.connect(u'url_shorten',
                    u'/'+toolkit.config.get(u'ckanext.url_shorten.url_prefix', u'odm-short-url')+u'/{id}',
                    controller=u'ckanext.url_shorten.controller:ShortUrlController',
                    action=u'short_url_redirect')
        return map
