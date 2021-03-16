#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: owefsad@huoxian.cn
# datetime: 2021/3/16 下午3:54
# project: vulhub-compose

import os

import yaml

from vulhub import IAST_SERVICE_NAME


def normal_path(path):
    yaml_path = None
    if path.startswith('/'):
        yaml_path = path
    else:
        # 获取当前路径
        base_path = os.path.abspath('.')
        yaml_path = os.path.normpath(os.path.join(base_path, path))
    return yaml_path


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


def get_yaml_path(path):
    #  检查是否存在
    yaml_path = normal_path(path)
    if yaml_path and os.path.exists(yaml_path):
        yaml_file = get_yaml_file(yaml_path)
        return os.path.join(yaml_path, yaml_file)
    else:
        raise FileNotFoundError(f'path:{yaml_path if path else path} not exists.')


def get_iast_service():
    return {
        'image': 'webhubforiast/iast_lingzhi_agent:latest',
        'container_name': 'volumn_with_iast_agent',
        'volumes': ['/tmp']
    }


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

    data['services'][IAST_SERVICE_NAME] = get_iast_service()
    return data


def get_iast_file(yaml_file):
    data = get_iast_yaml_content(yaml_file)
    # 提取yaml_file的目录
    # 写入payload
    path = os.path.dirname(yaml_file)
    iast_yaml = os.path.join(path, 'iast.yml')
    with open(iast_yaml, 'w') as f:
        yaml.safe_dump(data=data, stream=f)
    # yaml.safe_dump(data, fp)
    return iast_yaml


def remove_iast_yaml_file(yaml_file):
    if os.path.exists(yaml_file):
        os.remove(yaml_file)
