from ckan.plugins import toolkit
import ckan.model as model
from ckan.lib import helpers as h
from ckanext.url_shorten.helpers import parse_request_parameters_to_dict
from ckan.common import request, c
import logging

log = logging.getLogger(__name__)


def get_long_url(id=None):
    """
    Get the long url given short url id.
    API Endpoint: get_short_url (this also contains long url)
    :param id: str
    :return: str
    """
    context = {
        u'model': model,
        u'session': model.Session,
        u'user': c.user
    }

    long_url = toolkit.config.get('ckan.site_url')
    data_dict = {
        u'id': id,
        u'additional_url_params': parse_request_parameters_to_dict(request.params)
    }
    try:
        long_url = toolkit.get_action(u'get_short_url')(context, data_dict)[u'long_url']
    except toolkit.ObjectNotFound:
        toolkit.abort(404, toolkit._(u"Url not found"))
    except Exception as e:
        log.error(e)
        toolkit.abort(404, toolkit._(u"Something went wrong"))

    return long_url
