#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: owefsad@huoxian.cn
# datetime: 2021/3/16 下午3:45
# project: vulhub-compose

import fire as fire

from vulhub.cli.local_cli import Local
from vulhub.cli.remote_cli import Remote


def main():
    fire.Fire({
        'remote': Remote,
        'local': Local
    })
