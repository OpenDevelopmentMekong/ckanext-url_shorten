from ckan.lib.base import BaseController
from ckan.plugins import toolkit
import ckan.model as model
from ckan.lib import helpers as h
from ckan.common import c
import sys
import urllib
import traceback
import logging

log = logging.getLogger(__name__)


class ShortUrlController(BaseController):

    def short_url_redirect(self, id=None):
        """
        Redirect url to the long url as given
        :param id: str (short url id)
        :return: redirect
        """
        context = {
            u'model': model,
            u'session': model.Session,
            u'user': c.user
        }
        long_url = toolkit.config.get('ckan.site_url')
        try:
            long_url = toolkit.get_action(u'get_short_url')(context, {u'id': id})[u'long_url']
        except toolkit.ObjectNotFound:
            toolkit.abort(404, toolkit._(u"Url not found"))
        except Exception as e:
            log.error(e)
            toolkit.abort(404, toolkit._(u"Something went wrong"))

        toolkit.response.headers['location'] = long_url
        return toolkit.abort(302)

