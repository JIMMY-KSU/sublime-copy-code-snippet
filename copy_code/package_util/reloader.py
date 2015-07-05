#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of sublime-copy-code-snippet.
# https://github.com/socsieng/sublime-copy-code-snippet

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Socheat Sieng <socsieng@gmail.com>

import sys
import imp

modules_name = 'copy_code.package_util.modules'
if modules_name in sys.modules:
    imp.reload(sys.modules[modules_name])

from copy_code.package_util.modules import module_order

mods_load_order = module_order

for mod in mods_load_order:
    if mod in sys.modules:
        try:
            imp.reload(sys.modules[mod])
            print('reloaded %s' % mod)
        except (ImportError) as e:
            print('Error reloading %s\n%s' % (mod, e.message))
