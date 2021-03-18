#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: owefsad@huoxian.cn
# datetime: 2021/3/18 下午4:13
# project: vulhub-compose
import os

from vulhub.plugin.huoxian_iast import LingZhi


class BaseCli(object):
    PLUGINS = {
        'lingzhi': LingZhi()
    }

    def __init__(self):
        pass

    def start(self, app, plugin, plugin_args):
        pass

    def stop(self, app, plugin, plugin_args):
        pass

    @staticmethod
    def get_yaml_path(path):
        #  检查是否存在
        yaml_path = BaseCli.normal_path(path)
        if yaml_path and os.path.exists(yaml_path):
            yaml_file = BaseCli.get_yaml_file(yaml_path)
            return os.path.join(yaml_path, yaml_file)
        else:
            raise FileNotFoundError(f'path:{yaml_path if path else path} not exists.')

    @staticmethod
    def get_yaml_file(yaml_path):
        """
        docker-compose.yml or docker-compose.yaml need in yaml_path
        :param yaml_path:
        :return:
        """
        files = os.listdir(yaml_path)
        if 'docker-compose.yml' in files:
            yaml_file = 'docker-compose.yml'
        elif 'docker-compose.yaml' in files:
            yaml_file = 'docker-compose.yaml'
        else:
            raise FileNotFoundError(f'path: docker-compose.yml or docker-compose.yaml not found in {yaml_path}')
        return yaml_file

    @staticmethod
    def normal_path(path):
        if path.startswith('/'):
            yaml_path = path
        else:
            # 获取当前路径
            base_path = os.path.abspath('.')
            yaml_path = os.path.normpath(os.path.join(base_path, path))
        return yaml_path
