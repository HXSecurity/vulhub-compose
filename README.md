# vulhub-compose
[![license](https://img.shields.io/github/license/huoxianclub/vulhub-compose.svg)](https://github.com/huoxianclub/vulhub-compose/blob/main/LICENSE)
[![build](https://github.com/huoxianclub/vulhub-compose/actions/workflows/python-publish.yml/badge.svg)](https://github.com/huoxianclub/vulhub-compose/actions/workflows/python-publish.yml)

`vulhub-cli` is a command line tool of the vulhub project, which makes the operation of `docker-compose` transparent and reduces the difficulty of using the vulhub shooting range. Vulhub-cli supports local mode and remote mode. The remote mode can directly start the related shooting range without downloading the complete vulhub project, which is more convenient to use.

[中文文档](https://github.com/huoxianclub/vulhub-compose/blob/main/README.zh-ch.md)

## Quick start
If you want to download the vulhub project or have already downloaded the vulhub project, you can directly use the local mode; if you don’t want to download, you can use the remote mode

#### download vulhub-cli
```shell script
$ pip install vulhub-cli
```

#### local mode
```shell script
# Specify relative path
$ vulhub-cli local start --app fastjson/1.2.24-rce
$ vulhub-cli local start --app ./fastjson/1.2.24-rce

# Specify absolute path
$ vulhub-cli local start --app /opt/vulhub/fastjson/1.2.24-rce

# Stop environment use vulhub-cli
$ vulhub-cli local stop --app fastjson/1.2.24-rce

# Stop environment with agent use vulhub-cli
$ vulhub-cli local stop --app fastjson/1.2.24-rce
```

#### remote mode
```shell script
# Specify vulhub app's name, eg: fastjson/1.2.24-rce
$ vulhub-cli remote start --app fastjson/1.2.24-rce

# Stop environment with agent use vulhub-cli
$ vulhub-cli remote stop --app fastjson/1.2.24-rce
```


## Plugin System
`vulhub-cli` provides plug-in functions, which can support custom plug-ins to achieve specific functions.

### Plugin: lingzhi
Lingzhi IAST is an interactive application security testing tool independently developed by [FireWire platform](https://www.huoxian.cn/) to detect vulnerabilities in application systems; lingzhi IAST supports the detection of some 0 Day vulnerabilities. Now, you can use the vulhub-cli tool to quickly create a shooting range and install lingzhi IAST to experience the vulnerability detection function.

#### Usage
The startup method is the same as the normal startup method, just add the `plugin` parameter to specify the use of the `lingzhi` plugin.
```shell script
# Start the vulhub's app with public Lingzhi IAST agent
$ vulhub-cli remote start --app fastjson/1.2.24-rce --plugin lingzhi

# Start the vulhub's app with your own Lingzhi IAST agent
$ vulhub-cli remote start --app fastjson/1.2.24-rce --plugin lingzhi --plugin-args "token=<lingzhi iast token>"

# Stop the vulhub's app with Lingzhi IAST
$ vulhub-cli remote stop --app fastjson/1.2.24-rce --plugin lingzhi
```
