#!/usr/bin/env python

from setuptools import setup

setup(name='tap-appointment-plus',
      version='0.0.1',
      description='Singer.io tap for Appointment Plus (appointment-plus.com)',
      author='Fishtown Analytics',
      url='http://fishtownanalytics.com',
      classifiers=['Programming Language :: Python :: 3 :: Only'],
      py_modules=['tap_appointment_plus'],
      install_requires=[
          'funcy>=1.8',
          'singer-python>=1.5.0',
          'voluptuous>=0.10.5',
          'requests>=2.18.3',
      ],
      entry_points='''
          [console_scripts]
          tap-appointment-plus=tap_appointment_plus:main
      ''',
      packages=['tap_appointment_plus'])
