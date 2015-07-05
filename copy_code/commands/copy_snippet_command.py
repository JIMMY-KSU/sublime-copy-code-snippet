#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of sublime-copy-code-snippet.
# https://github.com/socsieng/sublime-copy-code-snippet

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Socheat Sieng <socsieng@gmail.com>

import re
import os

leading_space_exp = re.compile(r'^[\t ]*(?=\S)', re.M)

comment_styles = {
    '// %s': ['actionscript', 'c#', 'c++', 'c', 'd', 'go', 'java', 'json', 'javascript', 'objective-c++', 'objective-c', 'pascal', 'scala'],
    '# %s': ['makefile', 'php', 'perl', 'python', 'r', 'ruby on rails', 'ruby', 'shell-unix-generic', 'tcl', 'yaml'],
    '-- %s': ['applescript', 'haskell', 'literate haskell', 'lua', 'sql'],
    '%% %s': ['erlang', 'bibtex', 'latex beamer', 'latex log', 'latex memoir', 'latex', 'tex math', 'tex', 'matlab'],
    '; %s': ['clojure', 'lisp'],
    '<!-- %s -->': ['html', 'xml', 'xsl'],
    'REM %s': ['batch file'],
    '/* %s */': ['css', 'less', 'sass'],
    '(* %s *)': ['ocaml', 'ocamllex', 'ocamlyacc', 'camlp4']
}

class CopySnippetCommand:
    def __init__(self, view, sublime):
        self.view = view
        self.sublime = sublime
        self.command_name = ''

    def run(self, edit):
        indent_character = '\t'
        settings = self.view.settings()

        if settings.get('translate_tabs_to_spaces'):
            indent_character = ' '

        comment_style = self.get_comment_format(self.get_language())

        output = self.extract_snippet(indent_character, comment_style)

        self.sublime.set_clipboard(output)

    def extract_snippet(self, indent_character, comment_format):
        settings = self.view.settings()
        regions = []
        output = ''

        for selection in self.view.sel():
            text = self.view.substr(selection)
            regions.append(self.normalize_indent(self.view.substr(selection), indent_character, settings.get('tab_size')))

        self.trim_indent(regions, indent_character)

        for region in regions:
            if output != '':
                output += '\n\n'
                output += comment_format % 'code omitted'
                output += '\n\n'

            output += region

        return output

    def normalize_indent(self, text, indent_character, tab_size):
        def replacer(match):
            if indent_character == ' ':
                return match.group(0).replace('\t', ' ' * tab_size)
            else:
                return match.group(0).replace(' ' * tab_size, '\t')

        return leading_space_exp.sub(replacer, text)

    def trim_indent(self, regions, indent_character):
        min_indent = -1

        def indent_replacer(match):
            if len(match.group(0)) >= min_indent:
                return match.group(0)[min_indent:]
            return match.group(0)

        for region in regions:
            matches = leading_space_exp.finditer(region)

            for match in matches:
                if len(match.group(0)) < min_indent or min_indent == -1:
                    min_indent = len(match.group(0))

        if min_indent > -1:
            for i in range(0, len(regions)):
                regions[i] = leading_space_exp.sub(indent_replacer, regions[i])

    def is_enabled(self):
        return len(self.view.sel()) > 0

    def get_comment_format(self, language):
        for comment in comment_styles.keys():
            if language in comment_styles[comment]:
                return comment
        return '# %s'

    def get_language(self):
        syntax_file = self.view.settings().get('syntax')
        language = os.path.basename(syntax_file).replace('.tmLanguage', '').lower() if syntax_file != None else 'plain text'
        return language
