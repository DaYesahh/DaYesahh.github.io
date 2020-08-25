---
title: puppeteer
date: 2020-07-05 01:42:27
tags:
---
## 简介

这是一款前端自动化测试工具，是黑盒测试，可以模仿用户操作。

## 下载以及安装
先摆上各种链接：
- 官方github链接：https://github.com/puppeteer/puppeteer
- 官方答疑链接：https://github.com/puppeteer/puppeteer/blob/main/docs/troubleshooting.md
- 好用的中文版api网站：https://zhaoqize.github.io/puppeteer-api-zh_CN/#?product=Puppeteer&version=v3.0.0&show=api-error-handling

看官方介绍知道如果使用puppeteer可以有两种东西需要下载，一种是puppeteer-core，一个是puppeteer，具体介绍可以看上述中文api网站，不过大体可以看出来puppeteer-core是精简版的puppeteer。鉴于本人没用过puppeteer-core，本文只讲puppeteer。
- 首先可以直接用npm或者cnpm下载：`cnpm i puppeteer@版本号 -g`，这里给的例子为什么是cnpm而不是npm，当然是npm不好使，详情如下：
 + 首先`npm`比较慢，咱都懂，而且puppeteer能用，除了下载本身以外，还会下载chromium，因为puppeteer会单独启动一个浏览器，默认会启动下载的这个。
 + 本人采用npm没下载成功过chromium，cnpm虽然也有点慢，但能下载成功。
 + 当然也可以配置其他浏览器，但是chromium最好用。
 + 当然也可以通过单独下载chromium，但是本人没试过，通过cnpm在下载puppeteer的时候下载chromium是最简单的了。
- 首次下载安装后，可能会报错，详细报错信息为缺少共享库，不要慌张，也不要去网上乱搜，直接去上述网站上找，需要下载非常多。


## 语法
语法非常简单，调用各种api即可。不过学习这个需要有js同步异步事件执行机制和es6的基础，尤其是promise await/async 还要对dom操作比较熟悉。

### 运行环境
本人亲测，在win10 虚拟机上运行比较ok，不过在虚拟机上会出现一些问题，渲染元素慢，导致找不到元素等等，后续会讲。但是在windows的虚拟子系统中运行会出现各种问题，100%运行失败。需要再寻找解决方案，但是本人没有解决此问题。

多看一下相关知识会发现，puppeteer是需要运行在async/await下的，因为很多api的返回值是promise函数。


