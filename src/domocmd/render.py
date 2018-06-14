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
import os
import json
from jinja2 import Environment, FileSystemLoader

class Render:

    def __init__(self, tpl_path, tpl_filename, outputfile):
        self.tpl_filename = tpl_filename
        self.tpl_dir = os.path.dirname(os.path.abspath(__file__)) + tpl_path
        self.outputfile = outputfile
        # TODO: Check if file exists

    def _render_jinja2(self, context):
        j2_env = Environment(loader=FileSystemLoader(self.tpl_dir), trim_blocks=True)
        return j2_env.get_template(self.tpl_filename).render(context)

    # def _render_py(self, hosts, vars={}):
    #    module = imp.load_source('r', self.tpl_file)
    #    return module.render(hosts, vars=vars, tpl_dirs=self.tpl_dirs)

    def render(self, context):
        """
        Render a jinja2 or .py file.
        """
        if self.tpl_filename.endswith('.tpl'):
            with open(self.outputfile, 'w') as f:
                html = self._render_jinja2(context)
                f.write(html)
                f.close()
        elif self.tpl_filename.endswith('json'):
            with open(self.outputfile, 'w') as f:
                json.dump(context, f, indent=3, encoding="latin-1")
                f.close()
        # elif self.tpl_file.endswith(".py"):
        #    return self._render_py(hosts, vars)
        else:
            raise ValueError("Don't know how to handle '{0}'".format(self.tpl_file))
