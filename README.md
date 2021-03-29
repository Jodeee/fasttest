`fasttest` 在`macaca`、`appium`、`selenium`的基础上做了一层关键字的封装与解析，通过`yaml`编写自动化用例，即使无代码基础的同学也已可以很快上手自动化测试

![](https://img.shields.io/badge/python-3.7-green) 

#### 我能做什么
- 支持`IDEA`关键字联想输入，在`yaml`文件上写用例像写代码一样舒畅
- 支持在线实时`debug`用例步骤，无需重复运行验证
- 支持现有关键字组合、自定义关键字，拥有无限扩展性
- 支持`PO`模式、支持`iOS`、`Android`两端共用一份用例
- 支持`if`、`while`、`for`等语法用于构造复杂场景
- 支持`CLI`命令，支持`Jenkins`持续集成
- 支持多设备并行执行

更多介绍请点击[fasttest](https://www.yuque.com/jodeee/vt6gkg/oue9xb)

#### 运行示例
```
module: OpenAlipay
skip: false
description: 打开支付宝小程序
steps:
    - click('我的小程序')
    - click('奈雪点单')
    - ${modules} = [
        {'key':'自取', 'value':'霸气玉油柑'},
        {'key':'外卖', 'value':'新增地址'}
        ]
    - for ${module} in ${modules}:
        - click(${module}['key'])
        - check(${module}['value'])
        - if ${module}['key'] == '自取':
            - click('首页')
          else:
            - goBack
    - click('订单')
    - click('去点餐')
```
