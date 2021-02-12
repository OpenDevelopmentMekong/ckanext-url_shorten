from ckan.plugins import toolkit
from ckanext.url_shorten.model import UrlShorten
import logging

log = logging.getLogger(__name__)


@toolkit.side_effect_free
def get_short_url(context, data_dict):
    """
    Fetch the record by id or name. If not found raise error
    :param context:
    :param data_dict:
    :return:
    """

    rec = UrlShorten.get_entry(id=data_dict.get(u'id', u''))
    if not rec:
        raise toolkit.ObjectNotFound(u"Given id: {} not found".format(data_dict.get(u'id', u'')))

    result = rec.as_dict()
    if data_dict.get(u'additional_url_params', {}):
        url_params = u"&".join([u"{}={}".format(k, v) for k, v in data_dict[u'additional_url_params'].items()])
        result[u'long_url'] = result.get(u'long_url', u'') + u'&'+url_params

    return result


def create_short_url(context, data_dict):
    """
    Create a short url. Raises validation error if any
    :param context:
    :param data_dict:
    :return:
    """
    if toolkit.config.get('ckanext.url_shortner_key', None) != data_dict.get('token_key', '').strip():
        raise toolkit.NotAuthorized("No token_key parameter provided")
    _ = data_dict.pop(u'id', u'')
    md = UrlShorten.create_entry(**data_dict)
    return md.as_dict()


def update_short_url(context, data_dict):
    """
    Update a short url. Raises validation error if any
    :param context:
    :param data_dict:
    :return:
    """
    if toolkit.config.get('ckanext.url_shortner_key', None) != data_dict.get('token_key', '').strip():
        raise toolkit.NotAuthorized("No token_key parameter provided")
    md = UrlShorten.update_entry(**data_dict)
    return md.as_dict()


def delete_short_url(context, data_dict):
    """
    Delete an entry (soft delete) or raises validation error if any
    :param context:
    :param data_dict:
    :return:
    """
    if toolkit.config.get('ckanext.url_shortner_key', None) != data_dict.get('token_key', '').strip():
        raise toolkit.NotAuthorized("No token_key parameter provided")
    _ = UrlShorten.delete_entry(**data_dict)
    return {
        u"msg": u"Entry {} deleted".format(data_dict.get(u'id', ''))
    }
