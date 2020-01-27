#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class ActionKeyWord(object):

    # 变量
    VARIABLES = r'\$\{\w+\}'

    # 脚本
    SCRIPTS = 'Scripts'

    # call
    CALL = 'call'

    # 公用
    COMMON = 'Common'

    # 启动app
    STARTAPP = 'startApp'

    # 关闭app
    STOPAPP = 'stopApp'

    # 点击
    TAP = 'tap'

    # 双击
    DOUBLETAP = 'doubleTap'

    # 长按
    PRESS = 'press'

    # 旋转 待实现
    ROTATE = 'rotate'

    # 拖动
    DRAG = 'drag'

    # 返回  only Android
    GOBACK = 'goBack'

    # adb  only Android
    ADB = 'adb'

    # shell  only Android
    ADBSHELL = 'adbShell'

    # 上滑
    SWIPEUP = 'swipeUp'

    # 下滑
    SWIPEDOWN = 'swipeDown'

    # 左滑
    SWIPELEFT = 'swipeLeft'

    # 右滑
    SWIPERIGHT = 'swipeRight'

    # 滑动
    SWIPE = 'swipe'

    # 获取文案
    GETTEXT = 'getText'

    # 点击
    CLICK = 'click'

    # 检查
    CHECKT = 'check'

    # 输入
    INPUT = 'input'

    # if
    IF = 'if'

    ELIF = 'elif'

    ELSE = 'else'

    # 是否存在
    IFCHECK = 'ifcheck'

    ELIFCHECK = 'elifcheck'

    # 是否iOS
    IFIOS = 'ifiOS'

    # 是否Android
    IFANDROID = 'ifAndroid'

    # 等待
    SLEEP = 'sleep'

    # 断言
    ASSERT = 'assert'

    # 循环
    WHILE = 'while'

    BREAK = 'break'

    # 全局
    SETGV = r'\$\.setGV'