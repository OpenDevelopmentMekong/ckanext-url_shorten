from ckan.plugins import toolkit
from ckanext.url_shorten.model import UrlShorten
import logging

log = logging.getLogger(__name__)


def get_short_url(context, data_dict):
    """
    Fetch the record by id or name. If not found raise error
    :param context:
    :param data_dict:
    :return:
    """
    rec = UrlShorten.get_entry(id=data_dict.get(u'id', u''))
    if not rec:
        raise toolkit.NotFound(u"Given id: {} not found".format(data_dict.get(u'id', u'')))
    return rec.as_dict()


def create_short_url(context, data_dict):
    """
    Create a short url. Raises validation error if any
    :param context:
    :param data_dict:
    :return:
    """
    toolkit.check_access(u'sysadmin', context, data_dict)
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
    toolkit.check_access(u'sysadmin', context, data_dict)
    md = UrlShorten.update_entry(**data_dict)
    return md.as_dict()


def delete_short_url(context, data_dict):
    """
    Delete an entry (soft delete) or raises validation error if any
    :param context:
    :param data_dict:
    :return:
    """
    toolkit.check_access(u'sysadmin', context, data_dict)
    _ = UrlShorten.delete_entry(**data_dict)
    return {
        u"msg": u"Entry {} deleted".format(data_dict.get(u'id', ''))
    }
