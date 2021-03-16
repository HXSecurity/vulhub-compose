#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: owefsad@huoxian.cn
# datetime: 2021/3/16 下午3:45
# project: vulhub-compose

import fire as fire

from vulhub.cli.command import dispatch
from vulhub.utils import get_yaml_path, get_iast_file, remove_iast_yaml_file


def main():
    fire.Fire(component={
        'start': start,
        'stop': stop
    })


def start(path: str, iast: bool = False, iast_token: str = None):
    yaml_file = get_yaml_path(path)
    if iast:
        yaml_file = get_iast_file(yaml_file)

    command_func = dispatch(['-f', yaml_file, 'up', '-d'])
    command_func()
    if iast:
        remove_iast_yaml_file(yaml_file)


def stop(path: str, iast: bool = False, iast_token: str = None):
    yaml_file = get_yaml_path(path)
    if iast:
        yaml_file = get_iast_file(yaml_file)
    command_func = dispatch(['-f', yaml_file, 'down'])
    command_func()
    if iast:
        remove_iast_yaml_file(yaml_file)
