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
from domocmd.render import Render

class DiskRender(object):

    def __init__(self, config, context):
        self.config = config
        self.context = context

    def render(self):
        myrender = Render(self.config.templatesPath(), 'report-disks-html.tpl', self.config.wwwRoot() + 'report-disks.html')
        myrender.render(self.context)
        myrender = Render(self.config.templatesPath(), 'json', self.config.wwwRoot() + 'report-disks.json')
        myrender.render(self.context)
        myrender = Render(self.config.templatesPath(), 'txt-tree.tpl', self.config.wwwRoot() + 'report-disks.txt')
        myrender.render(self.context)
        myrender = Render(self.config.templatesPath(), 'csv.tpl', self.config.wwwRoot() + 'report-disks.csv')
        myrender.render(self.context)
        myrender = Render(self.config.templatesPath(), 'sql.tpl', self.config.wwwRoot() + 'report-disks.sql')
        myrender.render(self.context)
        myrender = Render(self.config.templatesPath(),'report-disks-2-html.tpl', self.config.wwwRoot() + 'report-disks-2.html')
        myrender.render(self.context)
