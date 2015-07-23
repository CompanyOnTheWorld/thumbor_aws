# coding: utf-8

from setuptools import setup, find_packages

setup(
	name = 'tc_aws',
	version = "1",
	description = 'Thumbor AWS extensions',
	author = 'William King',
	author_email = 'willtrking@gmail.com',
	zip_safe = False,
	include_package_data = True,
	packages=find_packages(),
	install_requires=['python-dateutil','thumbor','boto','librato-metrics']
)
