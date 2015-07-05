#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of sublime-copy-code-snippet.
# https://github.com/socsieng/sublime-copy-code-snippet

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Socheat Sieng <socsieng@gmail.com>

import os
import sys
import sublime
import sublime_plugin
import imp

sys.path.append(os.path.dirname(os.path.realpath(__file__)))

reloader_name = 'copy_code.package_util.reloader'

try:
    if reloader_name in sys.modules:
        imp.reload(sys.modules[reloader_name])
    else:
        import copy_code.package_util.reloader
except:
    pass

from copy_code import commands

class CopySnippetCommand(sublime_plugin.TextCommand):
    def __init__(self, view):
        sublime_plugin.TextCommand.__init__(self, view)
        self.command = commands.CopySnippetCommand(self.view, sublime)

    def is_enabled(self):
        return self.command.is_enabled()

    def run(self, edit):
        self.command.run(edit)
