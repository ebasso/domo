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
# Requires Python 2.7
#
import sys
import json
import copy
import domocmd

#if sys.version_info >= (3, 0):
#    from http.server import BaseHTTPRequestHandler, HTTPServer
#else:
#    from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

from domocmd.configuration import Configuration
from domocmd.dashboard import Dashboard
from domocmd.collector import Collector
from domocmd.domino_diskparser import DiskParser
from domocmd.domino_health_general import DominoHealthGeneral
from domocmd.domino_health_cluster import DominoHealthCluster
from domocmd.domino_health_http import DominoHealthHttp
from domocmd.domino_health_mail import DominoHealthMail
from domocmd.domino_health_platform import DominoHealthPlatform
from domocmd.domino_mail import DominoMail
from domocmd.render import Render
from domocmd.disk_render import DiskRender
from domocmd.traveler_statistics import TravelerStatistics

APP_NAME = 'domo.py'
APP_VERSION = '0.0.1'
DOMINO_CONFIG_FILE = './configs/domino_config.json'

def renderDashboard():
    dsb = Dashboard(config)
    dsb.render()

if __name__ == '__main__':

    config = Configuration(APP_NAME,APP_VERSION)
    domcfg = config.loadConfigJson(DOMINO_CONFIG_FILE)
    servers = copy.deepcopy(domcfg['servers'])   # Copy Deep
    servers2 = copy.deepcopy(domcfg['servers'])
    servers3 = copy.deepcopy(domcfg['servers'])
    serversCluster = copy.deepcopy(domcfg['servers'])
    serversHttp = copy.deepcopy(domcfg['servers'])
    serversMail = copy.deepcopy(domcfg['servers'])
    if (servers is None):
        print('Could not load config file')
        sys.exit(1)

    if (config.args.collect):
        print('collect - start')
        mycollector = Collector(config, servers)
        mycollector.collect()
        print('collect - end')

    if (config.args.report_disks):
        print('report_disks - start')
        myparser = DiskParser(config, servers)
        context = myparser.parse()
        mydr = DiskRender(config, context)
        mydr.render()
        print('report_disks - end')

    if (config.args.domino_statistics):
        print('domino - start')
        domstats = DominoHealthGeneral(config, servers2)
        #domstats.alerts()
        domstats.render()
        domstats = DominoHealthCluster(config, serversCluster)
        domstats.render()
        domstats = DominoHealthHttp(config, serversHttp)
        domstats.render()
        domstats = DominoHealthMail(config, serversMail)
        domstats.render()
        domstats = DominoHealthPlatform(config, serversMail)
        domstats.render()
        print('domino - end')

    if (config.args.domino_mail):
        print('domino.mail - start')
        mailstats = DominoMail(config, servers3)
        #domstats.alerts()
        mailstats.render()
        print('domino.mail - end')

    if (config.args.traveler_statistics):
        print('traveler - start')
        trvstats = TravelerStatistics(config)
        trvstats.render()
        print('traveler - end')

    renderDashboard()
