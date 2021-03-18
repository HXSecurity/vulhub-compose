#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: owefsad@huoxian.cn
# datetime: 2021/3/17 下午12:09
# project: vulhub-compose
import logging
import os

import requests
import yaml

from vulhub.plugin import BasePlugin

logger = logging.getLogger(__name__)
"""
todo: 
1. 支持设置自定义token，安装agent
2. 根据环境版本自动选择下载的agent版本（以前根据选择，现在自行判断）
"""


class LingZhi(BasePlugin):
    @staticmethod
    def get_iast_service():
        return {
            'image': 'webhubforiast/iast_lingzhi_agent:latest',
            'container_name': 'volumn_with_iast_agent',
            'volumes': ['/tmp']
        }

    @staticmethod
    def get_iast_yaml_content(yaml_file):
        with open(yaml_file, 'r') as f:
            data = yaml.safe_load(f)

        services = data['services']
        for service_name, service_value in services.items():
            # 添加环境变量
            if 'environment' not in service_value:
                service_value['environment'] = ['JAVA_TOOL_OPTIONS=-javaagent:/tmp/agent.jar']
            else:
                service_value['environment'].append('JAVA_TOOL_OPTIONS=-javaagent:/tmp/agent.jar')

            if 'volumes' not in service_value:
                service_value['volumes'] = ['./agent.jar:/tmp/agent.jar']
            else:
                service_value['volumes'].append('./agent.jar:/tmp/agent.jar')

        return data

    @staticmethod
    def get_iast_file(yaml_file):
        data = LingZhi.get_iast_yaml_content(yaml_file)
        path = os.path.dirname(yaml_file)
        iast_yaml = os.path.join(path, 'iast.yml')
        with open(iast_yaml, 'w') as f:
            yaml.safe_dump(data=data, stream=f)
        return iast_yaml

    @staticmethod
    def remove_iast_yaml_file(yaml_file):
        if os.path.exists(yaml_file):
            os.remove(yaml_file)

    @staticmethod
    def download_agent():
        pass

    def parse_args(self):
        args = dict()

        def _parse():
            if self.args:
                _args = self.args.split(';')
                for arg in _args:
                    name, value = arg.split('=')
                    args[name] = value

        _parse()
        url = 'http://openapi.aws.iast.huoxian.cn:8000/api/v1/agent/download?url=http://openapi.aws.iast.huoxian.cn:8000&jdk.version=Java%201.8'
        headers = {
            'Authorization': f'Token {args["token"] if "token" in args else "88d2f0096662335d42580cbd03d8ddea745fdfab"}'
        }
        try:
            # fixme 使用head方法可以提升效率，但是这里使用head时出现了错误
            resp = requests.get(url, headers=headers, timeout=(10, 30))
            if resp.status_code == 200:
                with open(f'{self.base_path}/agent.jar', 'wb') as f:
                    f.write(resp.content)
            return True
        except Exception as e:
            logger.debug(f'[-] Failure: download agent failed. Token: {args["token"]}\nReason: {e}')

    def attach(self, yaml_file):
        self.base_path = os.path.dirname(yaml_file)
        if self.parse_args():
            return self.get_iast_file(yaml_file)
        return yaml_file

    def detach(self, yaml_file):
        self.remove_iast_yaml_file(yaml_file)
