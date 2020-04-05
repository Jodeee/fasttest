#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class ActionKeyWord(object):

    INSTALLAPP = 'installApp'
    UNINSTALLAPP = 'uninstallApp'
    LAUNCHAPP = 'launchApp'
    CLOSEAPP = 'closeApp'
    TAP = 'tap'
    DOUBLETAP = 'doubleTap'
    PRESS = 'press'
    # only Android
    GOBACK = 'goBack'
    ADB = 'adb'
    SWIPEUP = 'swipeUp'
    SWIPEDOWN = 'swipeDown'
    SWIPELEFT = 'swipeLeft'
    SWIPERIGHT = 'swipeRight'
    SWIPE = 'swipe'
    GETTEXT = 'getText'
    CLICK = 'click'
    CHECKT = 'check'
    INPUT = 'input'
    IF = 'if'
    ELIF = 'elif'
    ELSE = 'else'
    IFCHECK = 'ifcheck'
    ELIFCHECK = 'elifcheck'
    IFIOS = 'ifiOS'
    IFANDROID = 'ifAndroid'
    SLEEP = 'sleep'
    ASSERT = 'assert'
    WHILE = 'while'
    BREAK = 'break'

    # 全局
    SETGV = r'\$\.setGv'
    # 变量
    VARIABLES = r'\$\{\w+\}'
    # 调用模块
    CALL = 'call'
