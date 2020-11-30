from ckan.plugins import toolkit
import logging
log = logging.getLogger(__name__)
try:
    # python2
    from urlparse import urlparse
except:
    # python3
    from urllib.parse import urlparse


def validate_url(url):
    """
    Validate url
    :param url: str url
    :return:
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        raise toolkit.ValidationError("Not a valid url")
