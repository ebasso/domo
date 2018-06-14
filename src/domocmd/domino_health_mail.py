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
# Requires Python 3.6
#
import json
import time
import domocmd.utilities as utilities
from domocmd.render import Render


class DominoHealthMail(object):

    def __init__(self, config, servers):
        self.config = config
        self.servers = servers
        self.server_count = 0
        self.loadStats()
        self.now = time.strftime("%Y-%m-%d %H:%M")
        self.context = {'title': 'Domino Statistics',
                        'now': self.now,
                        'servers': self.servers,
                        'server_count': self.server_count
                        }

    def _parseStatsFromFile(self, server):
        fileName = self.config.tempDir() + server['name']
        inputfile = open(fileName + '.tmp',mode='rb')

        aDict = {}

        for line in inputfile:
            line = line.strip()
            start = line.find(' = ')
            if (start > 0):
                k, v = line.split(' = ', 1)
                aDict[k] = v

        inputfile.close()
        return aDict

    def _getStatInt(self, stats, str):
        try:
            sout = stats[str]
            sout = sout.replace(',', '')
            return int(sout)
        except KeyError:
            return 0

    def _getStatFloat(self, stats, str):
        try:
            sout = stats[str]
            sout = sout.replace(',', '')
            return float(sout)
        except KeyError:
            return 0.0

    def _getStatPercentFloat(self, stats, str):
        try:
            B = float(stats[str])
            sout = '{0:.2f}'.format(B)
            sout = '{message:{fill}{align}{width}}'.format(message=sout, fill=' ', align='>', width=0)
            return float(sout)
        except KeyError:
            return 0

    def loadStats(self):
        #print('loadStats - start')
        count = 0
        for server in self.servers:
            #print 'parse from server: %s' % (server['name'])
            stats = self._parseStatsFromFile(server)
            if (stats):
                count += 1
                domstats = {
                    'Server.Name': stats['Server.Name'],
                    'Server.ElapsedTime': stats['Server.ElapsedTime'],
                    'Stats.Time.Current': stats['Stats.Time.Current'],
                    'Stats.Time.Start': stats['Stats.Time.Start'],
                }
                domstats = self._status_mailboxes(stats, domstats)
            server['statistics'] = domstats
        self.server_count = count
        #print('loadStats - end')

    def alerts(self):
        for server in self.servers:
            print('')
            print(server['name'])

    def _status_mailboxes(self, stats, domstats):

        mbac = self._getStatInt(stats, 'Mail.Mailbox.AccessConflicts')
        mba = self._getStatInt(stats, 'Mail.Mailbox.Accesses')
        count = 0
        if (mba > 0):
            count = mbac / mba * 100

        txt = 'Conflicts. Add mailboxes'
        if (count < 2):
            txt = 'Excelent'

        domstats['Mail.Mailbox.AccessConflicts'] = mbac
        domstats['Mail.Mailbox.Accesses'] = mba
        domstats['Mail.Mailbox.AccessConflicts.status'] = txt
        return domstats

    def _statistics_mail(self, stats, domstats):
        domstats['Mail.Delivered'] = self._getStatInt(stats, 'Mail.Delivered')
        domstats['Mail.DeliveredSize.Under_1KB'] = self._getStatInt(
            stats, 'Mail.DeliveredSize.Under_1KB')
        domstats['Mail.DeliveredSize.1KB_to_10KB'] = self._getStatInt(
            stats, 'Mail.DeliveredSize.1KB_to_10KB')
        domstats['Mail.DeliveredSize.10KB_to_100KB'] = self._getStatInt(
            stats, 'Mail.DeliveredSize.10KB_to_100KB')
        domstats['Mail.DeliveredSize.100KB_to_1MB'] = self._getStatInt(
            stats, 'Mail.DeliveredSize.100KB_to_1MB')
        domstats['Mail.DeliveredSize.1MB_to_10MB'] = self._getStatInt(
            stats, 'Mail.DeliveredSize.1MB_to_10MB')
        domstats['Mail.DeliveredSize.10MB_to_100MB'] = self._getStatInt(
            stats, 'Mail.DeliveredSize.10MB_to_100MB')
        domstats['Mail.DeliveredSize.Over_100MB'] = self._getStatInt(
            stats, 'Mail.DeliveredSize.Over_100MB')
        domstats['Mail.TotalRouted'] = self._getStatInt(
            stats, 'Mail.TotalRouted')
        domstats['Mail.TotalRouted.NRPC'] = self._getStatInt(
            stats, 'Mail.TotalRouted.NRPC')
        domstats['Mail.TotalRouted.SMTP'] = self._getStatInt(
            stats, 'Mail.TotalRouted.SMTP')
        domstats['Mail.Transferred'] = self._getStatInt(
            stats, 'Mail.Transferred')
        domstats['Mail.Transferred.NRPC'] = self._getStatInt(
            stats, 'Mail.Transferred.NRPC')
        domstats['Mail.Transferred.SMTP'] = self._getStatInt(
            stats, 'Mail.Transferred.SMTP')
        domstats['Mail.TransferredSize.Under_1KB'] = self._getStatInt(
            stats, 'Mail.TransferredSize.Under_1KB')
        domstats['Mail.TransferredSize.1KB_to_10KB'] = self._getStatInt(
            stats, 'Mail.TransferredSize.1KB_to_10KB')
        domstats['Mail.TransferredSize.10KB_to_100KB'] = self._getStatInt(
            stats, 'Mail.TransferredSize.10KB_to_100KB')
        domstats['Mail.TransferredSize.100KB_to_1MB'] = self._getStatInt(
            stats, 'Mail.TransferredSize.100KB_to_1MB')
        domstats['Mail.TransferredSize.1MB_to_10MB'] = self._getStatInt(
            stats, 'Mail.TransferredSize.1MB_to_10MB')
        domstats['Mail.TransferredSize.10MB_to_100MB'] = self._getStatInt(
            stats, 'Mail.TransferredSize.10MB_to_100MB')
        domstats['Mail.TransferredSize.Over_100MB'] = self._getStatInt(
            stats, 'Mail.TransferredSize.Over_100MB')

        return domstats

    def render(self):

        myrender = Render(self.config.templatesPath(), 'domino-health-mail-html.tpl',
                          self.config.wwwRoot() + 'domino-health-mail.html')
        myrender.render(self.context)
        myrender = Render(self.config.templatesPath(), 'json',
                          self.config.wwwRoot() + 'domino-health-mail.json')
        myrender.render(self.context)
        
