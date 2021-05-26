import pytest
import ckan.logic as logic
import ckan.plugins.toolkit as toolkit
from ckan import model
import ckan.tests.helpers as helpers
from ckan.tests import factories
from ckan.logic import _actions
from ckanext.url_shorten import plugin
import mock


@pytest.mark.usefixtures("clean_db", "with_request_context")
class TestUrlShortenPlugin:

    def setup(self):
        self.instance = plugin.UrlShortenMixinPlugin()

    def test_plugin_setup(self):
        assert len(self.instance.get_actions()) > 0
        assert len(self.instance.get_actions()) == 4
