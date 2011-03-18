#!/usr/bin/env python

from distutils.core import setup

setup(name='codefest_sched',
        version='0.1',
        description='Generates codefest.ru schedule',
        author='Gleb Kanterov',
        author_email='gleb@kanterov.ru',
        packages=['codefest_sched',],
        package_dir={'': 'src'},
        install_requires=['lxml', 'leaf' ],
        entry_points=("""
                [console_scripts]
        """)
        )

