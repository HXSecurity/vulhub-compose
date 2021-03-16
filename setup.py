#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: owefsad@huoxian.cn
# datetime: 2021/3/16 下午7:33
# project: vulhub-compose
import codecs
import os
import re

from setuptools import find_packages
from setuptools import setup


def read(*parts):
    path = os.path.join(os.path.dirname(__file__), *parts)
    with codecs.open(path, encoding='utf-8') as fobj:
        return fobj.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


install_requires = [
    'docker-compose >= 1.28.5',
    'fire >= 0.4.0',
]

extras_require = {
    ':python_version < "3.5"': ['backports.ssl_match_hostname >= 3.5, < 4'],
    ':sys_platform == "win32"': ['colorama >= 0.4, < 1'],
}

setup(
    name='vulhub-cli',
    version=find_version("vulhub", "__init__.py"),
    description='easy command tool for vulhub',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    url='https://www.huoxian.cn/',
    project_urls={
        'Source': 'https://github.com/huoxianclub/vulhub-compose',
        'Tracker': 'https://github.com/huoxianclub/vulhub-compose/issues',
    },
    author='Owefsad, Inc.',
    license='MIT License',
    packages=find_packages(exclude=['tests.*', 'tests']),
    include_package_data=True,
    install_requires=install_requires,
    extras_require=extras_require,
    python_requires='>=3.4',
    entry_points={
        'console_scripts': ['vulhub-cli=vulhub.cli.main:main'],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
