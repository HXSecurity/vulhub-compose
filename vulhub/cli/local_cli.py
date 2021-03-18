#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: owefsad@huoxian.cn
# datetime: 2021/3/18 下午4:14
# project: vulhub-compose

from vulhub.cli.base_cli import BaseCli
from vulhub.cli.command import dispatch


class Local(BaseCli):

    def __init__(self):
        super().__init__()

    def start(self, app, plugin=None, plugin_args=None):
        yaml_file = self.get_yaml_path(app)
        if plugin:
            plugin = self.PLUGINS.get(plugin)
            plugin.args = plugin_args
            yaml_file = plugin.attach(yaml_file)

        command_func = dispatch(['-f', yaml_file, 'up', '-d'])
        command_func()
        if plugin:
            plugin.detach(yaml_file)

    def stop(self, app, plugin=None, plugin_args=None):
        yaml_file = self.get_yaml_path(app)
        if plugin:
            plugin = self.PLUGINS.get(plugin)
            yaml_file = plugin.attach(yaml_file)

        command_func = dispatch(['-f', yaml_file, 'down'])
        command_func()

        if plugin:
            plugin.detach(yaml_file)
