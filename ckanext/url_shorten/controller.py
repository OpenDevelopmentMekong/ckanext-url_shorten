from ckan.lib.base import BaseController
from ckan.plugins import toolkit
from ckanext.url_shorten.helpers import parse_request_parameters_to_dict
from ckanext.url_shorten.utils import get_long_url
import logging

log = logging.getLogger(__name__)


class ShortUrlController(BaseController):

    def short_url_redirect(self, id=None):
        """
        Redirect url to the long url as given
        :param id: str (short url id)
        :return: redirect
        """
        long_url = get_long_url(id)

        toolkit.response.headers['location'] = long_url
        return toolkit.abort(302)

