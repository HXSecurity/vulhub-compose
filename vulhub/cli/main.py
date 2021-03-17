#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: owefsad@huoxian.cn
# datetime: 2021/3/16 下午3:45
# project: vulhub-compose
import logging
import os
import queue
import tempfile
from urllib.parse import urljoin

import fire as fire
import requests

from vulhub.cli.command import dispatch
from vulhub.plugin.huoxian_iast import LingZhi

logger = logging.getLogger(__name__)


def main():
    fire.Fire({
        'remote': Remote,
        'local': Local
    })


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


class Remote(BaseCli):
    GITHUB_API = 'https://api.github.com/repos/{repo}/contents/{app}'
    VULHUB_APP = 'vulhub/vulhub'
    BASE_URLS = ('https://gitee.com/vulhub/vulhub/raw/master/',)
    TEMPLATES_YAML = ('docker-compose.yml', 'docker-compose.yaml')

    def __init__(self):
        super().__init__()

    def start(self, app, plugin=None, plugin_args=None):
        app = self.normalize_app(app)
        yaml_path = self.download_app(app)
        if yaml_path:
            Local().start(app=yaml_path, plugin=plugin, plugin_args=plugin_args)
        else:
            logger.error(f'[*] Failure: vulhub app[{app}] download failure')

    def stop(self, app, plugin=None, plugin_args=None):
        app = self.normalize_app(app)
        yaml_path = self.download_app(app)
        if yaml_path:
            Local().stop(app=yaml_path, plugin=plugin, plugin_args=plugin_args)
        else:
            logger.error(f'[*] Failure: vulhub app[{app}] download failure')

    @staticmethod
    def normalize_app(app):
        if app.startswith('/'):
            app = app[1:]
        return app

    def download_app(self, app):
        url = self.GITHUB_API.format(repo=self.VULHUB_APP, app=app)
        app_contents = None
        try:
            resp = requests.get(url)
            if resp.status_code == 200:
                app_contents = resp.json()
        except Exception as e:
            pass

        app_path = None
        if app_contents and len(app_contents) > 0:
            app_path = self.create_app_path(app=app)
            print(f'[+] download vulapp[{app}] to {app_path}')
            for app_content in app_contents:
                name = app_content.get('name')
                download_url = app_content.get('download_url')
                self.download_file(app=app, name=name, download_url=download_url, app_path=app_path)
        return app_path

    @staticmethod
    def download_file(app, name, download_url, app_path):
        download_queue = queue.Queue()

        def generate_download_urls():
            download_queue.put(download_url)
            for BASE_URL in Remote.BASE_URLS:
                url = urljoin(BASE_URL, f'{app}/{name}')
                download_queue.put(url)

        def download():
            while download_queue.empty() is False:
                url = download_queue.get()
                try:
                    # fixme 使用head方法可以提升效率，但是这里使用head时出现了错误
                    resp = requests.get(url, headers={'User-Agent': 'curl/7.64.1'}, timeout=(6, 6))
                    if resp.status_code == 200:
                        Remote.write_file(app_path=app_path, name=name, content=resp.content)
                        break
                except Exception as e:
                    logger.debug(f'[-] Failure: download {name} from {url}')
                    pass

        generate_download_urls()
        download()

    @staticmethod
    def create_app_path(app):
        temp_dir = tempfile.gettempdir()
        path = os.path.join(temp_dir, app)
        if os.path.exists(path) is False:
            os.makedirs(path)
        return path

    @staticmethod
    def write_file(app_path, name, content):
        with open(f'{app_path}/{name}', 'wb') as f:
            f.write(content)


class Local(BaseCli):

    def __init__(self):
        super().__init__()

    def start(self, app, plugin=None, plugin_args=None):
        yaml_file = self.get_yaml_path(app)
        if plugin:
            plugin = self.PLUGINS.get(plugin)
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


class VulHubCli(BaseCli):
    def __init__(self):
        super().__init__()
        self.local = Local()
        self.remote = Remote()

    def start(self, app, plugin=None, plugin_args=None):
        self.local.start(app=app, plugin=plugin, plugin_args=plugin_args)
        self.remote.start(app=app, plugin=plugin, plugin_args=plugin_args)

    def stop(self, app, plugin=None, plugin_args=None):
        self.local.stop(app=app, plugin=plugin, plugin_args=plugin_args)
        self.remote.stop(app=app, plugin=plugin, plugin_args=plugin_args)
