#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of py-json-reader.
# https://github.com/socsieng/py-json-reader

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Socheat Sieng <socsieng@gmail.com>

from preggy import expect
from mock import Mock

from copy_code.tests.base import TestCase
from copy_code import commands

def mock_sys(platform = None):
    sys = Mock()
    sys.platform = platform
    return sys

def mock_sublime(region = None):
    sublime = Mock()
    sublime.Region = Mock(return_value = region)
    sublime.set_clipboard = Mock()
    return sublime

def mock_sublime_view(regions = None, substr = lambda sel: None):
    view = Mock()
    view.settings = Mock(return_value = mock_sublime_settings({
        'tab_size': 4
    }))

    view.sel = Mock(return_value = regions)
    view.substr = substr
    view.replace = Mock()
    return view

def mock_sublime_settings(dictionary):
    def setter(key, value):
        dictionary[key] = value
    settings = Mock()
    settings.get = lambda key, default_value = None: default_value if not key in dictionary else dictionary[key]
    settings.set = setter
    return settings

def mock_regions(contents):
    sublime_regions = []
    if contents:
        for str_value in contents:
            region = Mock(return_value = str_value)
            region.empty = lambda: len(str_value) == 0
            sublime_regions.append(region)

    return sublime_regions

def mock_sublime_edit():
    edit = Mock()
    return edit

def mock_os():
    os = Mock()
    os.system = Mock()
    return os

class CopySnippetTestCase(TestCase):
    def test_should_not_be_enabled_when_no_regions_selected(self):
        sublime = mock_sublime()
        view = mock_sublime_view([], lambda sel: sel())
        edit = mock_sublime_edit()

        command = commands.CopySnippetCommand(view, sublime)
        enabled = command.is_enabled()

        expect(enabled).to_equal(False)

    def test_should_be_enabled_when_one_region_selected(self):
        sublime = mock_sublime()
        regions = mock_regions(['{ }'])
        view = mock_sublime_view(regions, lambda sel: sel())
        edit = mock_sublime_edit()

        command = commands.CopySnippetCommand(view, sublime)
        enabled = command.is_enabled()

        expect(enabled).to_equal(True)

    def test_should_be_enabled_when_more_than_one_region_selected(self):
        sublime = mock_sublime()
        regions = mock_regions(['{ }', '[]'])
        view = mock_sublime_view(regions, lambda sel: sel())
        edit = mock_sublime_edit()

        command = commands.CopySnippetCommand(view, sublime)
        enabled = command.is_enabled()

        expect(enabled).to_equal(True)

    def test_should_match_comment_c(self):
        sublime = mock_sublime()
        regions = mock_regions(['{ }', '[]'])
        view = mock_sublime_view(regions, lambda sel: sel())

        command = commands.CopySnippetCommand(view, sublime)
        comment = command.get_comment_format('c')

        expect(comment).to_equal('// %s')

    def test_should_match_comment_sql(self):
        sublime = mock_sublime()
        regions = mock_regions(['{ }', '[]'])
        view = mock_sublime_view(regions, lambda sel: sel())

        command = commands.CopySnippetCommand(view, sublime)
        comment = command.get_comment_format('sql')

        expect(comment).to_equal('-- %s')

    def test_should_match_comment_python(self):
        sublime = mock_sublime()
        regions = mock_regions(['{ }', '[]'])
        view = mock_sublime_view(regions, lambda sel: sel())

        command = commands.CopySnippetCommand(view, sublime)
        comment = command.get_comment_format('python')

        expect(comment).to_equal('# %s')

    def test_should_match_comment_default(self):
        sublime = mock_sublime()
        regions = mock_regions(['{ }', '[]'])
        view = mock_sublime_view(regions, lambda sel: sel())

        command = commands.CopySnippetCommand(view, sublime)
        comment = command.get_comment_format('not sure')

        expect(comment).to_equal('# %s')

    def test_should_replace_tabs_with_spaces(self):
        sublime = mock_sublime()
        regions = mock_regions(['{ }', '[]'])
        view = mock_sublime_view(regions, lambda sel: sel())

        command = commands.CopySnippetCommand(view, sublime)
        normalized = command.normalize_indent('\t\thello\n\t    world\n    \tfoo', ' ', 4)

        expect(normalized).to_equal('        hello\n        world\n        foo')

    def test_should_spaces_with_tabs(self):
        sublime = mock_sublime()
        regions = mock_regions(['{ }', '[]'])
        view = mock_sublime_view(regions, lambda sel: sel())

        command = commands.CopySnippetCommand(view, sublime)
        normalized = command.normalize_indent('\t\thello\n\t    world\n\n    \tfoo', '\t', 4)

        expect(normalized).to_equal('\t\thello\n\t\tworld\n\n\t\tfoo')

    def test_should_extract_snippets_from_single_region_no_indent(self):
        sublime = mock_sublime()
        regions = mock_regions(['function () {\n\tdoSomething();\n}'])
        view = mock_sublime_view(regions, lambda sel: sel())

        command = commands.CopySnippetCommand(view, sublime)
        snippet = command.extract_snippet(' ', '// %s')

        expect(snippet).to_equal('function () {\n    doSomething();\n}')

    def test_should_extract_snippets_from_single_region_with_blank_lines(self):
        sublime = mock_sublime()
        regions = mock_regions(['\t\thello\n\t    world\n\n    \tfoo'])
        view = mock_sublime_view(regions, lambda sel: sel())

        command = commands.CopySnippetCommand(view, sublime)
        snippet = command.extract_snippet(' ', '// %s')

        expect(snippet).to_equal('hello\nworld\n\nfoo')

    def test_should_extract_snippets_from_single_region_tab_indent(self):
        sublime = mock_sublime()
        regions = mock_regions(['\tfunction () {\n\t\tdoSomething();\n\t}'])
        view = mock_sublime_view(regions, lambda sel: sel())

        command = commands.CopySnippetCommand(view, sublime)
        snippet = command.extract_snippet('\t', '// %s')

        expect(snippet).to_equal('function () {\n\tdoSomething();\n}')

    def test_should_extract_snippets_from_multiple_regions_no_indent(self):
        sublime = mock_sublime()
        regions = mock_regions(['function () {\n\tdoSomething();\n}', '\tfunction () {\n    \tdoSomething();\n    }'])
        view = mock_sublime_view(regions, lambda sel: sel())

        command = commands.CopySnippetCommand(view, sublime)
        snippet = command.extract_snippet(' ', '// %s')

        expect(snippet).to_equal('function () {\n    doSomething();\n}\n\n// code omitted\n\n    function () {\n        doSomething();\n    }')

    def test_should_copy_to_clipboard(self):
        sublime = mock_sublime()
        regions = mock_regions(['function () {\n\tdoSomething();\n}', '\tfunction () {\n    \tdoSomething();\n    }'])
        view = mock_sublime_view(regions, lambda sel: sel())
        edit = mock_sublime_edit()

        command = commands.CopySnippetCommand(view, sublime)
        snippet = command.run(edit)

        sublime.set_clipboard.assert_called_once_with('function () {\n\tdoSomething();\n}\n\n# code omitted\n\n\tfunction () {\n\t\tdoSomething();\n\t}')
