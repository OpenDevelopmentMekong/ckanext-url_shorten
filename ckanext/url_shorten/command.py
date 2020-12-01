from ckan.lib.cli import CkanCommand
from ckanext.url_shorten import model as url_model
import sys
import logging

log = logging.getLogger(__name__)


class UrlShortenCommand(CkanCommand):
    """
    URL shorten database table setup
    """
    summary = __doc__.split('\n')[0]
    usage = __doc__
    min_args = 0
    max_args = 2

    def command(self):
        if not self.args or self.args[0] in ['--help', '-h', 'help']:
            print("This command class is used to setup database table for UrlShoten extension ")
            return

        cmd = self.args[0]
        self._load_config()

        if cmd == 'initdb':
            url_model.init_table()
        else:
            log.error("Given command does not exists")
