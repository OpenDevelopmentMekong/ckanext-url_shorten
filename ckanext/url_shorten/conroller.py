from ckan.lib.base import BaseController
from ckan.plugins import toolkit
import ckan.model as model
from ckan.common import c
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
        try:
            res = toolkit.get_action(u'get_short_url')(context, {u'id': id})
            return toolkit.redirect_to(res[u'long_url'])
        except toolkit.NotFound as e:
            toolkit.abort(404, toolkit._(u"Url not found"))
