#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from utest.common import Var
from utest.common.decorator import therading
from utest.drivers.driver_platform import DriveriOS
from utest.drivers.driver_platform import DriverAndroid

class DriverBase(object):

    @staticmethod
    def init():
        try:
            global driver
            if Var.platformName in "ios":
                driver = DriveriOS
            elif Var.platformName in "android":
                driver = DriverAndroid
        except:
            driver = DriverAndroid

    @staticmethod
    def startApp(activity=Var.activity):
        """
        启动app
        :param activity:
        :return:
        """
        if Var.platformName in "ios":
            Var.driver.init()
        elif Var.platformName in "android":
            DriverAndroid.shell('shell am start -S {}'.format(activity))

    @staticmethod
    def stopApp(package=Var.package):
        """
        关闭app
        :param package:
        :return:
        """
        if Var.platformName in "ios":
            Var.driver.init()
        elif Var.platformName in "android":
            DriverAndroid.shell('shell am force-stop {}'.format(package))

    @staticmethod
    def adb(cmd):
        """
        adb 命令
        :param cmd:
        :return:
        """
        if Var.platformName in "ios":
            pass
        elif Var.platformName in "android":
            DriverAndroid.shell(cmd)

    @staticmethod
    def tap(x, y):
        """
        单击
        :param x:
        :param y:
        :return:
        """
        driver.tap(x, y)

    @staticmethod
    def doubleTap(x, y):
        """
        双击
        :param x:
        :param y:
        :return:
        """
        driver.doubleTap(x, y)

    @staticmethod
    def press(x, y, duration=2):
        """
        长按
        :param x:
        :param y:
        :param duration:
        :return:
        """
        Var.driver.touch('press', {'x': int(x), 'y': int(y), 'duration': duration})

    @staticmethod
    def swipe_up(during=3):
        """
        上滑
        :param during:
        :return:
        """
        driver.swipe_up(during)

    @staticmethod
    def swipe_down(during=3):
        """
        下拉
        :param during:
        :return:
        """
        driver.swipe_down(during)

    @staticmethod
    def swipe_left(during=3):
        """
        左滑
        :param during:
        :return:
        """
        driver.swipe_left(during)

    @staticmethod
    def swipe_right(during=3):
        """
        右滑
        :param during:
        :return:
        """
        driver.swipe_right(during)

    @staticmethod
    def swipe(fromx, fromy, tox, toy, during=3):
        """
        滑动
        :param fromx:
        :param fromy:
        :param tox:
        :param toy:
        :param during:
        :return:
        """
        driver.swipe(fromx, fromy, tox, toy, during)

    @staticmethod
    @therading
    def wait_element(name='', id='', xpath='', classname='', timeout=5, interval=1, index=0):
        """
        等待元素
        :param name:
        :param id:
        :param xpath:
        :param classname:
        :param timeout:
        :param interval:
        :param index:
        :return:
        """
        if name:
            elements = driver.wait_for_elements_by_name(name, timeout, interval)
        elif id:
            elements = driver.wait_for_elements_by_id(id, timeout, interval)
        elif xpath:
            elements = driver.wait_for_elements_by_xpath(xpath, timeout, interval)
        elif classname:
            elements = driver.wait_for_elements_by_class_name(classname, timeout, interval)
        else:
            raise TypeError('element() missing 1 required positional argument')

        if elements:
            if len(elements) <= int(index):
                raise Exception('list index out of range, index:{}'.format(index))
            return elements[index]
        return None

    @staticmethod
    def rect(element, timeout=10, interval=1, index=0):
        """
        获取元素坐标
        :param element:
        :param timeout:
        :param interval:
        :param index:
        :return:
        """
        element_rect = DriverBase.get_element(element=element, timeout=timeout, interval=interval, index=index)
        if element_rect:
            return element_rect.rect
        else:
            raise Exception("Can't find element {}".format(element))

    @staticmethod
    def click(element, timeout=10, interval=1, index=0):
        """
        点击元素
        :param element:
        :param timeout:
        :param interval:
        :param index:
        :return:
        """
        element_click = DriverBase.get_element(element=element, timeout=timeout, interval=interval, index=index)
        if element_click:
            element_click.click()
        else:
            raise Exception("Can't find element {}".format(element))

    @staticmethod
    def check(element, timeout=10, interval=1, index=0):
        """
        检查元素
        :param element:
        :param timeout:
        :param interval:
        :param index:
        :return:
        """
        element_check = DriverBase.get_element(element=element, timeout=timeout, interval=interval, index=index)
        if element_check:
            return True
        else:
            return False

    @staticmethod
    def input(element, text='', timeout=10, interval=1, index=0, clear=True):
        """
        输入
        :param element:
        :param text:
        :param timeout:
        :param interval:
        :param index:
        :param clear:
        :return:
        """
        element_input = DriverBase.get_element(element=element, timeout=timeout, interval=interval, index=index)
        if element_input:
            driver.input(element_input, text=text, clear=clear)
        else:
            raise Exception("Can't find element {}".format(element))

    @staticmethod
    def text(element, timeout=10, interval=1, index=0):
        """
        获取文案
        :param element:
        :param timeout:
        :param interval:
        :param index:
        :return:
        """

        element_text = DriverBase.get_element(element=element, timeout=timeout, interval=interval, index=index)
        if element_text:
            text = driver.text(element_text)
            if text:
                return text
            else:
                return ''
        else:
            raise Exception("Can't find element {}".format(element))

    @staticmethod
    def get_element(element, timeout=5, interval=1, index=0):
        """
        等待元素
        :param element:
        :param timeout:
        :param interval:
        :param index:
        :return:
        """
        element_name = DriverBase.wait_element(name=element, timeout=timeout, interval=interval, index=index)
        element_id = DriverBase.wait_element(id=element, timeout=timeout, interval=interval, index=index)
        element_xpath = DriverBase.wait_element(xpath=element, timeout=timeout, interval=interval, index=index)
        element_classname = DriverBase.wait_element(classname=element, timeout=timeout, interval=interval, index=index)
        while True:
            if not element_name.isAlive():
                return element_name.get()
            elif not element_id.isAlive():
                return element_id.get()
            elif not element_xpath.isAlive():
                return element_xpath.get()
            elif not element_classname.isAlive():
                return element_classname.get()

