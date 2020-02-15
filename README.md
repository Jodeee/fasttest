## 框架介绍

`fasttest` 在`macaca`的基础上做了一层关键字的封装与解析，极大得简化了测试用例描述。我们有丰富的行为关键字，而且支持关键字模块级复用，自定义关键字等操作

![](https://img.shields.io/badge/python-3.7-green) ![](https://img.shields.io/badge/macaca-2.2.0-lightgrey)


## 运行示例
测试用例
```
module: OpenWebView
skip: false
description: 打开饿了么
steps:
  - input '搜索或输入网站名称' 'tb.ele.me/m?from=taobaoapp'
  - click '定位失败'
  - input '请输入地址' '西湖'
  - click '西湖文化广场'
  - check '美食'
```

运行示例

![image](http://47.110.43.11/media/image/demo1.gif)


## 更多帮助

[框架介绍](https://www.yuque.com/docs/share/7efcf004-b9d1-40e0-80a0-e87c6d901f9e?#)

[环境配置](https://www.yuque.com/docs/share/8f55e1ba-b699-4f40-addd-dfaa0605148d?#)

[快速上手](https://www.yuque.com/docs/share/2d091bf1-e2c5-45a9-9bd4-cd5c6836660f?#)

[参数配置](https://www.yuque.com/docs/share/8d805c9c-bb78-4575-a493-6d785c5e65cc?#)

[关键字库](https://www.yuque.com/docs/share/63caf5f1-4091-48ff-8ea6-1b1b3bb4cf65?#)


## 问题收集

[issues](https://github.com/Jodeee/OKTest/issues)
