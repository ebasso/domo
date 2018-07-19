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
import time
from domocmd.render import Render


class TravelerStatistics(object):

    def __init__(self, config):
        self.config = config
        self.now = time.strftime("%Y-%m-%d %H:%M")
        self.context = {'title': 'Traveler Statistics',
                        'now': self.now
                        }
        self.loadServers()
        self.loadDevices()

    def loadServers(self):
        count = 3
        self.context['servers'] = [
            {'name': 'SRCBSA01086/BancodoBrasil',
             'status': 'Green',
             'ai': '97',
             'user': '35',
             'devices': '78'
             },
            {'name': 'SRCBSA01087/BancodoBrasil',
             'status': 'Yellow',
             'ai': '100',
             'user': '0',
             'devices': '0'
             },
            {'name': 'SRCBSA01084/BancodoBrasil',
             'status': 'Yellow',
             'ai': '100',
             'user': '31',
             'devices': '53'
             },
            {'name': 'SRCBSA01085/BancodoBrasil',
             'status': 'Red',
             'ai': '100',
             'user': '1',
             'devices': '2'
             }]
        self.server_count = count

    def loadDevices(self):
        countDevices = 125
        countDevicesGreen = 80
        countDevicesYellow = 7
        countDevicesRed = 7
        countDevicesGray = 31
        percDevicesGreen = 64
        percDevicesYellow = 5
        percDevicesRed = 5
        percDevicesGray = 24
        self.context['devices'] = [{
            'deviceId': '9LQVJU6HRT3CVARA18HNKBM44C',
            'username': 'F8176197 Paulo Roberto Lopes Ricci',
            'deviceProvider': 'iPhone 7',
            'lastSynctime': '2017-02-06 16:20:02',
            'lastPushtime': '2017-02-06 16:16:13',
            'httpStatus': '200'
        },
            {
            'deviceId': 'FTGSPUIRRH7PLABNP1RRA0Q730',
            'username': 'F8859855 Rudinei dos Santos',
            'deviceProvider': 'iPad Air 2',
            'lastSynctime': '2017-02-06 16:19:58',
            'lastPushtime': '2017-02-06 16:09:35',
            'httpStatus': '499'
        },
            {
            'deviceId': 'IM9OQD64B56E3BFE7J8FG64RE8',
            'username': 'F8859855 Rudinei dos Santos',
            'deviceProvider': 'iPhone 6',
            'lastSynctime': '2017-02-06 16:19:57',
            'lastPushtime': '2017-02-06 16:16:31',
            'httpStatus': '499'
        }]
        self.context['countDevices'] = countDevices
        self.context['countDevicesGreen'] = countDevicesGreen
        self.context['countDevicesYellow'] = countDevicesYellow
        self.context['countDevicesRed'] = countDevicesRed
        self.context['countDevicesGray'] = countDevicesGray
        self.context['percDevicesGreen'] = percDevicesGreen
        self.context['percDevicesYellow'] = percDevicesYellow
        self.context['percDevicesRed'] = percDevicesRed
        self.context['percDevicesGray'] = percDevicesGray

    def render(self):

        myrender = Render(self.config.templatesPath(), 'traveler-servers-html.tpl',
                          self.config.wwwRoot() + 'traveler-servers.html')
        myrender.render(self.context)
        myrender = Render(self.config.templatesPath(), 'json',
                          self.config.wwwRoot() + 'traveler-statistics.json')
        myrender.render(self.context)
