from flask import Blueprint, redirect
from ckan.plugins import toolkit
from ckanext.url_shorten.helpers import parse_request_parameters_to_dict
from ckanext.url_shorten.utils import get_long_url
import logging

log = logging.getLogger(__name__)

url_shortner = Blueprint(
    u'url_shorten',
    __name__,
    url_prefix=u'/'+toolkit.config.get(u'ckanext.url_shorten.url_prefix', u'odm-short-url')
)


def short_url_redirect(id=None):
    """
    Redirect url to the long url as given
    :param id: str (short url id)
    :return: redirect
    """
    long_url = get_long_url(id)
    return redirect(long_url)


url_shortner.add_url_rule(
    u'/<id>',
    view_func=short_url_redirect,
    methods=[u'GET']
)
