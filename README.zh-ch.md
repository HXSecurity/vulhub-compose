# vulhub-compose
[![license](https://img.shields.io/github/license/huoxianclub/vulhub-compose.svg)](https://github.com/huoxianclub/vulhub-compose/blob/main/LICENSE)
[![build](https://github.com/huoxianclub/vulhub-compose/actions/workflows/python-publish.yml/badge.svg)](https://github.com/huoxianclub/vulhub-compose/actions/workflows/python-publish.yml)

vulhub-compose是一款屏蔽docker-compose的命令行工具，目的是降低火线平台社区用户使用vulhub靶场的难度，减少学习docker-compose的时间成本；同时，支持直接安装洞态IAST（原灵芝IAST）到vulhub靶场，用于漏洞复现、漏洞挖掘。

[English](https://github.com/huoxianclub/vulhub-compose/blob/main/README.md)

## 快速开始
vulhub项目的前置安装步骤依然需要完成，请自行前往[vulhub项目](https://github.com/vulhub/vulhub)安装docker及其它部分。
```shell script
# 下载vulhub项目
$ wget https://github.com/vulhub/vulhub/archive/master.zip -O vulhub-master.zip
$ unzip vulhub-master.zip
$ cd vulhub-master

# 安装vulhub-cli工具
$ pip install vulhub-cli

# 创建靶场环境
$ vulhub-cli start --path ./fastjson/1.2.24-rce

# 停止并销毁靶场
$ vulhub-cli stop --path ./fastjson/1.2.24-rce

# 创建靶场并自动安装洞态IAST（原灵芝IAST）
$ vulhub-cli start --path fastjson/1.2.24-rce --iast=true

# 停止并销毁带IAST的靶场环境
$ vulhub-cli stop --path=./flask/ssti --iast=true
```

## 洞态IAST
洞态IAST推出代码审计版本，在Java WEB应用中安装agent后可用于收集污点调用链，包括组件级数据，只需要编写对应的hook策略即可实现部分**0 Day**漏洞的挖掘，教程可在[官方文档](https://huoxianclub.github.io/LingZhi/#/README)中查看。



