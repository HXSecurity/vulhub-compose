#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: owefsad@huoxian.cn
# datetime: 2021/3/17 下午12:09
# project: vulhub-compose
import os

import yaml
from vulhub import IAST_SERVICE_NAME

from vulhub.plugin import BasePlugin


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

            if 'depends_on' not in service_value:
                service_value['depends_on'] = [IAST_SERVICE_NAME]
            else:
                service_value['depends_on'].append(IAST_SERVICE_NAME)

            if 'volumes_from' not in service_value:
                service_value['volumes_from'] = [IAST_SERVICE_NAME]
            else:
                service_value['volumes_from'].append(IAST_SERVICE_NAME)

        data['services'][IAST_SERVICE_NAME] = LingZhi.get_iast_service()
        return data

    @staticmethod
    def get_iast_file(yaml_file):
        data = LingZhi.get_iast_yaml_content(yaml_file)
        # 提取yaml_file的目录
        # 写入payload
        path = os.path.dirname(yaml_file)
        iast_yaml = os.path.join(path, 'iast.yml')
        with open(iast_yaml, 'w') as f:
            yaml.safe_dump(data=data, stream=f)
        # yaml.safe_dump(data, fp)
        return iast_yaml

    @staticmethod
    def remove_iast_yaml_file(yaml_file):
        if os.path.exists(yaml_file):
            os.remove(yaml_file)

    def attach(self, yaml_file):
        return self.get_iast_file(yaml_file)

    def detach(self, yaml_file):
        self.remove_iast_yaml_file(yaml_file)
