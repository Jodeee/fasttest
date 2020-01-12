## 框架介绍

`OKTest`在`macaca`的基础上做了一层关键字的封装与解析。同时支持`Android`、`iOS`两个平台，支持`自定义关键字模块`、`自定义函数`等。目的在于保证执行效率的同时更加灵活的简化用例描述。

![](https://img.shields.io/badge/python-3.7-green) ![](https://img.shields.io/badge/node-10.16.3-blue) ![](https://img.shields.io/badge/macaca-2.2.0-lightgrey)


## 项目结构

    ├── Common           // 自定义关键字库  
    |   ├── Android      // Android关键字库  
    |   ├── iOS          // iOS关键字库   
    ├── oktest           // 框架核心代码  
    ├── Report           // 结果报告  
    ├── Images           // ocr图片目录
    ├── Scripts          // 自定义脚本函数  
    ├── TestCase         // 用例  
    ├── config           // 项目配置  
    ├── data             // 扩展数据  
    ├── runtest          // 项目入口  
   
   
## 快速开始

``` #yaml
module: search
description: 淘宝首页随机搜索手机品牌
steps:
  - ${mobilephone} = Scripts.get_mobile_phone()
  - call Taobao_Search(${mobilephone})
  - click '搜索'
```

## 更多帮助

[框架介绍](https://www.yuque.com/jodeee/kb/ywq037)


## 环境配置

[Macaca环境配置](https://macacajs.github.io/zh/guide/environment-setup.html)

[Macaca环境配置常见问题](https://www.yuque.com/jodeee/kb/ggz606)


## 问题收集

[issues](https://github.com/Jodeee/OKTest/issues)
