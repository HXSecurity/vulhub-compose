# vulhub-compose
[![license](https://img.shields.io/github/license/huoxianclub/vulhub-compose.svg)](https://github.com/huoxianclub/vulhub-compose/blob/main/LICENSE)
[![build](https://github.com/huoxianclub/vulhub-compose/actions/workflows/python-publish.yml/badge.svg)](https://github.com/huoxianclub/vulhub-compose/actions/workflows/python-publish.yml)

vulhub-compose是一款屏蔽docker-compose的命令行工具，目的是降低火线平台社区用户使用vulhub靶场的难度，减少学习docker-compose的时间成本；同时，支持直接安装洞态IAST（原灵芝IAST）到vulhub靶场，用于漏洞复现、漏洞挖掘。

[English](https://github.com/huoxianclub/vulhub-compose/blob/main/README.md)

## 快速开始
如果要下载vulnhub项目或已经下载了vulnhub项目，则可以直接使用本地模式。 如果您不想下载，可以使用远程模式。vulhub项目的前置安装步骤依然需要完成，请自行前往[vulhub项目](https://github.com/vulhub/vulhub)安装docker及其它部分。

#### 下载vulhub-cli
```shell script
$ pip install vulhub-cli
```

#### 本地模式
```shell script
# 使用相对路径启动靶场环境
$ vulhub-cli local start --app fastjson/1.2.24-rce
$ vulhub-cli local start --app ./fastjson/1.2.24-rce

# 使用绝对路径启动靶场环境
$ vulhub-cli local start --app /opt/vulhub/fastjson/1.2.24-rce

# 停止并销毁靶场环境
$ vulhub-cli local stop --app fastjson/1.2.24-rce
```

#### 远程模式
```shell script
# 指定vulhub app的名称，如: fastjson/1.2.24-rce
$ vulhub-cli remote start --app fastjson/1.2.24-rce

# 停止并销毁靶场环境
$ vulhub-cli remote stop --app fastjson/1.2.24-rce
```


## Plugin System
`vulhub-cli` provides plug-in functions, which can support custom plug-ins to achieve specific functions.

### Plugin: dongtai
灵芝IAST推出代码审计版本，在Java WEB应用中安装agent后可用于收集污点调用链，包括组件级数据，只需要编写对应的hook策略即可实现部分**0 Day**漏洞的挖掘，教程可在[官方文档](https://huoxianclub.github.io/LingZhi/#/README)中查看。

#### 使用方法
启动方法与正常启动方法相同，只需要增加`plugin`参数指定使用`dongtai`插件即可，如需在靶场中安装**私有**agent，需要前往[洞态](http://aws.iast.huoxian.cn:8000/)的**部署页面**获取并指定token
```shell script
# 启动靶场并安装公共的灵芝IAST agent
$ vulhub-cli remote start --app fastjson/1.2.24-rce --plugin dongtai

# 启动靶场并安装个人灵芝IAST agent，token可前往"部署IAST"页面获取
$ vulhub-cli remote start --app fastjson/1.2.24-rce --plugin dongtai --plugin-args "token=<dongtai iast token>"

# 停止并销毁预装IAST的靶场环境
$ vulhub-cli remote stop --app fastjson/1.2.24-rce --plugin dongtai
```