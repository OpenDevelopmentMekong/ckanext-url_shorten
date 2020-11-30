from sqlalchemy import Column
from sqlalchemy import types
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import exc as orm_exceptions
from sqlalchemy import or_, and_
from ckan.plugins import toolkit
import ckan.model as model
from ckanext.url_shorten import validators
import datetime
import uuid
import os
import logging
log = logging.getLogger(__name__)
Base = declarative_base()


def get_uuid():
    return unicode(uuid.uuid4())


def convert_to_name(val):
    """
    convert to name. Remove all spaces
    :param val:
    :return:
    """
    if not val:
        return ''

    return val.sptrip().lower().replace(" ", "-")


class UrlShorten(Base):
    """
    URL shorten table to hold long url and respective id or name
    """
    __tablename__ = 'url_shorten'

    id = Column(types.UnicodeText, primary_key=True, default=get_uuid)
    name = Column(types.UnicodeText, nullable=False, unique=True)
    is_active = Column(types.Boolean, default=True, nullable=False)
    long_url = Column(types.UnicodeText, nullable=False)
    created = Column(types.DateTime, default=datetime.datetime.utcnow)
    updated = Column(types.DateTime, onupdate=datetime.datetime.utcnow)

    @classmethod
    def create_entry(cls, **kwargs):
        """
        Create entry
        :return:
        """
        long_url = kwargs.get('url', '')
        name = kwargs.get('')
        validators.validate_url(url)

        rec = cls.get_entry(url=long_url)

        if not rec:
            rec = cls()
            rec.id = get_uuid
            rec.name = convert_to_name(name or _uuid)
            rec.long_url = long_url
            model.Session.add(rec)
            try:
                model.Session.commit()
            except orm_exceptions.IntegrityError as e:
                log.error(e)
                model.Session.flush()
                raise toolkit.ValidationError(u"Something wrong while saving the record")

        return rec

    @classmethod
    def update_entry(cls, **kwargs):
        """
        Update name or long_url for the existing entry
        :param kwargs:
        :return:
        """
        _id = kwargs.get(u'id', u'')
        rec = cls.get_entry(id=_id)
        if not rec:
            raise toolkit.NotFound(u"Given record not found")

        if u'name' in kwargs:
            rec.name = convert_to_name(kwargs[u'name'])

        if u'long_url' in kwargs:
            validators.validate_url(kwargs[u'url'])
            rec.long_url = kwargs[u'url']

        try:
            model.Session.commit()
        except orm_exceptions.IntegrityError as e:
            log.error(e)
            model.Session.flush()
            raise toolkit.ValidationError(u"Another Record with same name or url exists")

        return rec

    @classmethod
    def delete_entry(cls, id):
        """
        Delete record (or set is_active as false)
        :return:
        """
        if not id:
            raise toolkit.ValidationError(u"No id is given to delete record")
        rec = cls.get_entry(id=id)
        if not rec:
            raise toolkit.NotFound(u"Given record not found")

        rec.is_active = False
        model.Session.commit()
        return True

    @classmethod
    def get_entry(cls, id=id, url=none):
        """
        Get an entry given id or name
        :param id:
        :param url:
        :return:
        """
        if url.strip():
            return model.Session.query(cls)\
                .filter(and_(cls.long_url == url, cls.is_active is True))\
                .one_or_none()

        if not id:
            raise toolkit.ValidationError(u"No id or name given")

        return model.Session.query(cls) \
            .filter(and_(or_(cls.id == id, cls.name == id), cls.is_active is True))\
            .one_or_none()

    def as_dict(self):
        """
        Convert instance to dict
        :return:
        """
        _site_url = toolkit.config.get(u'ckan.site_url')
        _url_path = toolkit.config.get(u'ckanext.url_shorten.url_prefix', u'odm-short-url')
        res = {
            column.key: getattr(self, column.key)
            for column in self.__table__.columns if not column.key.startswith(u"_")
        }

        res[u'short_url'] = os.path.join(_site_url, _url_path, res[u'name'])

        return res


def init_table(engine):
    Base.metadata.create_all(engine)
    log.info('Stetting up url shortner table')
