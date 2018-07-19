#!/usr/bin/python
# vim: et sw=4 ts=4:
# -*- coding: utf-8 -*-
#
# Domo - free/libre analytics platform
#
# by ebasso@ebasso.net
# @link https://ebasso.net
# @license https://www.gnu.org/licenses/gpl-3.0.html GPL v3 or later
# @version $Id$
#
# For more info see: https://ebasso.net/wiki
#
# Requires Python 2.6 or 2.7
#
import json
import yaml
import sys
from argparse import ArgumentParser

CONFIG_FILE = 'domo.json'
#WWW_ROOT_FULLPATH = 'wwwroot/pages/'
# Production
WWW_ROOT_FULLPATH = '/var/www/domo/pages/'

class Configuration(object):
    """
    Stores all the configuration options by reading sys.argv and parsing,
    if needed, the config.inc.php.

    It has 2 attributes: options and filenames.
    """

    class Error(Exception):
        pass

    def __init__(self, appname, appversion):
        self._app_name = appname
        self._app_version = appversion
        self.args = self._create_parser()
        self.main = self.loadConfigJson(CONFIG_FILE)
        self._templates_path = '/templates/'
        self._temp_dir = 'temp/'
        self._www_root = WWW_ROOT_FULLPATH

    def _create_parser(self):
        """
        Initialize and return the ArgumentParser instance.
        """
        parser = ArgumentParser(usage='%(prog)s',
                                description='description blablabla',
                                epilog='About Domo: https://'
                                '              Please send your suggestions or successful user story to ebasso@ebasso.net')

        # Basic auth user
        # option_parser.add_option(
        #    '--auth-user', dest='auth_user',
        #    help="Basic auth user",
        #)

        # option_parser.add_option(
        #    '--debug', '-d', dest='debug', action='count', default=0,
        #    help="Enable debug output (specify multiple times for more verbose)",
        #)

        # default_config = os.path.abspath(
        #    os.path.join(os.path.dirname(__file__),
        #    '../../config/config.ini.php'),
        #)

        # option_parser.add_option(
        #    '--config', dest='config_file', default=default_config,
        #    help=(
        #        "This is only used when --login and --password is not used. "
        #        "Piwik will read the configuration file (default: %default) to "
        #        "fetch the Super User token_auth from the config file. "
        #    )
        #)

        parser.add_argument('--version','-v', 
                            action='version', version='%(prog)s ' + self._app_version)

        #parser.add_argument('-p', '--port', type=int, metavar='PORT', dest='port', default=8080)
        #parser.add_argument('--host', type=str, metavar='HOST', dest='host', default='localhost')
        parser.add_argument('--collect', action='store_true',
                            help='Collect statistics from servers')
        parser.add_argument('--report_disks',  action='store_true',
                            help='Render report disks')
        parser.add_argument('--domino_statistics',  action='store_true',
                            help='Statistics from Domino')
        parser.add_argument('--domino_mail',  action='store_true',
                            help='Statistics from Domino')
        parser.add_argument('--traveler_statistics',  action='store_true',
                            help='Render report traveler')
        
        return parser.parse_args()

    def loadConfigJson(self, config_file):
        data = None
        with open(config_file) as json_data_file:
            data = json.load(json_data_file)
        return data

    def loadConfigYaml(self, config_file):
        data = None
        with open(config_file, 'r') as yaml_data_file:
            try:
                data = yaml.load(yaml_data_file)
            except yaml.YAMLError as exc:
                print(exc)
        return data

    def tempDir(self):
        return self._temp_dir

    def templatesPath(self):
        return self._templates_path

    def wwwRoot(self):
        return self._www_root

