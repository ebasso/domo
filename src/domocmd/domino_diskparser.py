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
import domocmd.utilities as utilities
import time

class DiskParser(object):

    def __init__(self, config, servers):
        self.config = config
        self.servers = servers

    def _parseDiskStatsFromFile(self, server):
        fileName = self.config.tempDir() + server['name']
        try:
            inputfile = open(fileName + '.tmp', 'rb')
            disks = []
            disk = {}
            for line in inputfile:
                line = line.strip()
                if (line.startswith('Disk.')):
                    line = line[5:]
                    if (line.startswith(server['notesdata'])):
                        k, v = line.split(' = ', 1)
                        f = k.find('.Free')
                        s = k.find('.Size')
                        b = v.replace(',', '')
                        if (b.count('+') == 0):
                            b = b.replace('.', '')
                        if (f > 0):
                            d, t = k.split('.', 1)
                            disk['label'] = d
                            disk['free'] = float(b)
                        elif (s > 0):
                            d, t = k.split('.', 1)
                            disk['size'] = float(b)
                            disks.append(disk)
                            disk = {}

                    elif (line.startswith('/opt')):
                        k, v = line.split(' = ', 1)
                        f = k.find('.Free')
                        s = k.find('.Size')
                        b = v.replace(',', '')
                        if (b.count('+') == 0):
                            b = b.replace('.', '')
                        if (f > 0):
                            d, t = k.split('.', 1)
                            disk['label'] = d
                            disk['free'] = float(b)
                        elif (s > 0):
                            d, t = k.split('.', 1)
                            disk['size'] = float(b)
                            disks.append(disk)
                            disk = {}
                    elif (line.startswith('/var/log')):
                        k, v = line.split(' = ', 1)
                        f = k.find('.Free')
                        s = k.find('.Size')
                        b = v.replace(',', '')
                        if (b.count('+') == 0):
                            b = b.replace('.', '')
                        if (f > 0):
                            d, t = k.split('.', 1)
                            disk['label'] = d
                            disk['free'] = float(b)
                        elif (s > 0):
                            d, t = k.split('.', 1)
                            disk['size'] = float(b)
                            disks.append(disk)
                            disk = {}

            inputfile.close()
            return disks
        except IOError as e:
            print('_parseDiskStatsFromFile: server.name', server['name'])
            print('_parseDiskStatsFromFile', e)
            return []

    def _doStatisticsByServer(self, server):

        size_total = 0
        used_total = 0
        for disk in server['disks']:
            size_total = size_total + disk['size']
            disk['used'] = disk['size'] - disk['free']
            used_total = used_total + disk['used']
            disk['size_human'] = utilities.formatKMBGT(float(disk['size']))
            disk['used_human'] = utilities.formatKMBGT(float(disk['used']))
            disk['used_perc'] = 1 * float(utilities.formatPercent(100 * float(disk['used']) / float(disk['size'])))
        server['disks_size_total'] = size_total
        server['disks_used_total'] = used_total
        server['disks_size_total_human'] = utilities.formatKMBGT(size_total)
        server['disks_used_total_human'] = utilities.formatKMBGT(used_total)
        dutp = 100 * float(used_total) / float(size_total)
        server['disks_used_total_perc'] = 1 * float(utilities.formatPercent(dutp))
        return server

    def parse(self):
        environment_size_total = 0
        environment_used_total = 0
        server_count = 0
        for server in self.servers:
            disks = self._parseDiskStatsFromFile(server)
            if (disks):
                server_count = server_count + 1
                # print(disks)
                server['disks'] = disks
                server = self._doStatisticsByServer(server)
                environment_size_total = environment_size_total + server['disks_size_total']
                environment_used_total = environment_used_total + server['disks_used_total']

        environment_size_total_human = utilities.formatKMBGT(environment_size_total)
        environment_used_total_human = utilities.formatKMBGT(environment_used_total)
        environment_used_total_perc = 100 * float(environment_used_total) / float(environment_size_total)
        environment_used_total_perc_human = 1 * float(utilities.formatPercent(environment_used_total_perc))

        now =  time.strftime("%Y-%m-%d %H:%M")
        context = {'title': 'Disk Report',
                   'now': now,
                   'server_count': server_count,
                   'environment_size_total_human':  environment_size_total_human,
                   'environment_used_total_human':  environment_used_total_human,
                   'environment_used_total_perc': environment_used_total_perc_human,
                   'servers': self.servers
                   }
        return context
