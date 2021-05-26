from ckanext.url_shorten.logic import action
from ckanext.url_shorten import model as url_shorten_model
from ckan.plugins import toolkit
from ckan.tests import factories
import ckan.tests.helpers as helpers
from ckan import model
from ckan import logic
from ckan.logic import _actions
import pytest
import mock
import requests


@pytest.mark.usefixtures("clean_db", "with_request_context")
class TestUrlShortenACtions:

    def setup(self):
        """
        # create dataset
        # create resource
        # create user
        # create sysadmin
        :return:
        """
        url_shorten_model.init_table()
        self._user = factories.User()
        self.context = {
            'user': self._user['name'],
            'model': model,
            'ignore_auth': False
        }


    def test_create_short_url_authorization(self):
        """
        Test create url authorization
        :return:
        """
        with pytest.raises(toolkit.NotAuthorized):
            __ = helpers.call_action(
                "create_short_url",
                context=self.context,
                name="test-create-url",
                long_url="https://github.com/ckan/ckan"
            )

    def test_create_short_url(self):
        """
        Test url shorten create
        :return:
        """
        res = helpers.call_action(
            "create_short_url",
            context=self.context,
            name="test-create-url",
            long_url="https://github.com/ckan/ckan",
            token_key="test-xxx-key"
        )
        assert isinstance(res, dict)
        assert "long_url" in res and res.get('long_url', '') == "https://github.com/ckan/ckan"

    def test_get_short_url(self):
        """
        Test url shorten
        :return:
        """
        create_url = helpers.call_action(
            "create_short_url",
            context=self.context,
            name="test-create-url-get",
            long_url="https://github.com/ckan/ckan/ckan",
            token_key="test-xxx-key"
        )
        shorten_url = helpers.call_action(
            "get_short_url",
            context=self.context,
            id=create_url.get('id', ''),
            token_key="test-xxx-key"
        )

        assert isinstance(shorten_url, dict)
        assert 'short_url' in shorten_url
        assert 'test-create-url-get' in shorten_url.get('short_url')

    def test_update_short_url(self):
        """
       Test url shorten update
       :return:
       """
        create_url = helpers.call_action(
            "create_short_url",
            context=self.context,
            name="test-update-url",
            long_url="https://github.com/ckan/test-update-url",
            token_key="test-xxx-key"
        )
        updated_url = helpers.call_action(
            "update_short_url",
            context=self.context,
            id=create_url.get('id', ''),
            name='test-update-url-success',
            token_key="test-xxx-key"
        )
        shorten_url = helpers.call_action(
            "get_short_url",
            context=self.context,
            id=create_url.get('id', ''),
            token_key="test-xxx-key"
        )

        assert 'test-update-url-success' in updated_url.get('short_url')
        assert 'test-update-url-success' in shorten_url.get('short_url')

        updated_url = helpers.call_action(
            "update_short_url",
            context=self.context,
            id=create_url.get('id', ''),
            long_url='https://github.com/ckan/test-update-url-long',
            token_key="test-xxx-key"
        )
        shorten_url = helpers.call_action(
            "get_short_url",
            context=self.context,
            id=create_url.get('id', ''),
            token_key="test-xxx-key"
        )
        assert shorten_url.get('long_url', '') == updated_url.get('long_url', '')

    def test_delete_short_url(self):
        """
        test delete url
        :return:
        """
        create_url = helpers.call_action(
            "create_short_url",
            context=self.context,
            name="test-update-url-delete",
            long_url="https://github.com/ckan/test-delete-url",
            token_key="test-xxx-key"
        )
        helpers.call_action(
            "delete_short_url",
            context=self.context,
            id=create_url.get('id', ''),
            token_key="test-xxx-key"
        )
        with pytest.raises(toolkit.ObjectNotFound):
            __ = helpers.call_action(
                "get_short_url",
                context=self.context,
                id=create_url.get('id', ''),
                token_key="test-xxx-key"
            )


@pytest.mark.usefixtures("clean_db", "with_request_context")
class TestUrlShortenViews:

    def setup(self):
        """
        # create user
        :return:
        """
        url_shorten_model.init_table()
        self._user = factories.User()
        self.context = {
            'user': self._user['name'],
            'model': model,
            'ignore_auth': False
        }
        self.create_url = helpers.call_action(
            "create_short_url",
            context=self.context,
            name="test-update-url-test",
            long_url="https://github.com/ckan/test",
            token_key="test-xxx-key"
        )
        self.app = helpers._get_test_app()

    def test_short_url_redirect(self):
        """
        Test redirect
        :return:
        """
        with pytest.raises(RuntimeError) as e:
            __ = self.app.get("/odm-short-url/{}".format(self.create_url['id']))
            assert "Following external redirects is not supported." in e
