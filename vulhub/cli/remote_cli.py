#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: owefsad@huoxian.cn
# datetime: 2021/3/18 下午4:13
# project: vulhub-compose
import logging
import os
import queue
import tempfile
from urllib.parse import urljoin

import requests
import platform

from vulhub.cli.base_cli import BaseCli
from vulhub.cli.local_cli import Local

logger = logging.getLogger(__name__)

IS_WINDOWS = False
IS_LINUX = False
IS_MAC = False

if (platform.system() == 'Windows'):
    IS_WINDOWS = True
elif (platform.system() == 'Linux'):
    IS_LINUX = True
elif platform.system() == 'Darwin':
    IS_MAC = True


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
            print(f'[+] download vulapp [ {app} ] to {app_path}')
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
        if IS_MAC or IS_LINUX:
            temp_dir = os.path.join(os.path.expanduser('~'), '.vulhpp')
        else:
            temp_dir = tempfile.gettempdir()
        path = os.path.join(temp_dir, app)
        if os.path.exists(path) is False:
            os.makedirs(path)
        return path

    @staticmethod
    def write_file(app_path, name, content):
        with open(f'{app_path}/{name}', 'wb') as f:
            f.write(content)
