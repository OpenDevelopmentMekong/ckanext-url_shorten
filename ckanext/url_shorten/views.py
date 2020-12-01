from flask import Blueprint, redirect, url_for
from ckan.plugins import toolkit
import ckan.model as model
from ckan.common import c
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
    context = {
        u'model': model,
        u'session': model.Session,
        u'user': c.user
    }
    long_url = toolkit.config.get('ckan.site_url')
    try:
        long_url = toolkit.get_action(u'get_short_url')(context, {u'id': id})[u'long_url']
    except toolkit.NotFound as e:
        toolkit.abort(404, toolkit._(u"Url not found"))
    except Exception as e:
        log.error(e)
        toolkit.abort(404, toolkit._(u"Something went wrong"))

    return redirect(long_url)


url_shortner.add_url_rule(
    u'/<id>',
    view_func=short_url_redirect,
    methods=[u'GET']
)