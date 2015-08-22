#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of sublime-copy-code-snippet.
# https://github.com/socsieng/sublime-copy-code-snippet

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Socheat Sieng <socsieng@gmail.com>

if __name__ == '__main__':
    import imp

    try:
        imp.find_module('setuptools')

        from setuptools import setup, find_packages

        tests_require = [
            'mock',
            'nose',
            'coverage',
            'yanc',
            'preggy',
            'tox',
            'ipdb',
            'coveralls',
            'sphinx',
        ]

        setup(
            name='sublime-copy-code-snippet',
            version='0.0.1',
            description='Forgiving document indenter',
            long_description='''
        A forgiving document indenter for Sublime Text 3.
        ''',
            keywords='indent xml tolerant forgiving',
            author='Socheat Sieng',
            author_email='socsieng@gmail.com',
            url='https://github.com/socsieng/sublime-copy-code-snippet',
            license='MIT',
            classifiers=[
                'Development Status :: 4 - Beta',
                'Intended Audience :: Developers',
                'License :: OSI Approved :: MIT License',
                'Natural Language :: English',
                'Operating System :: Unix',
                'Programming Language :: Python :: 3.4',
                'Programming Language :: Python :: Implementation :: PyPy',
                'Operating System :: OS Independent',
            ],
            packages=find_packages(),
            include_package_data=False,
            install_requires=[
                # add your dependencies here
                # remember to use 'package-name>=x.y.z,<x.y+1.0' notation (this way you get bugfixes)
            ],
            extras_require={
                'tests': tests_require,
            },
            entry_points={
                'console_scripts': [
                    # add cli scripts here in this form:
                    # 'sublime-copy-code-snippet=sublime-copy-code-snippet.cli:main',
                ],
            },
        )
    except ImportError:
        print('Could not find setuptools. Make sure that setuptools is installed (https://pypi.python.org/pypi/setuptools)')
