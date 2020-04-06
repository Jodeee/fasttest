#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
from concurrent import futures
from fasttest.common import *

class DriverBase(object):


    @staticmethod
    def init():
        try:
            global driver
            if Var.driver.lower() == 'appium':
                from fasttest.drivers.appium import AndroidDriver, iOSDriver
            else:
                from fasttest.drivers.macaca import AndroidDriver, iOSDriver

            if Var.platformName.lower() == "ios":
                driver = iOSDriver
            elif Var.platformName.lower() == "android":
                driver = AndroidDriver
            Var.driver_instance = driver
        except Exception as e:
            raise e

    @staticmethod
    def adb_shell(cmd):
        """onlu Android
        Args:
            command
        Usage:
            adbshell 'adb devices'
        Returns:
            None
        """
        driver.adb_shell(cmd)

    @staticmethod
    def install_app(app_path):
        '''
        install app
        :param app_path:
        :return:
        '''
        driver.install_app(app_path)

    @staticmethod
    def uninstall_app(package_info):
        '''
        uninstall app
        :param package_info: Android(package) or iOS(bundleId)
        :return:
        '''
        driver.uninstall_app(package_info)

    @staticmethod
    def launch_app(package_info):
        '''
        launch app
        :param package_info: Android(package/activity) or iOS(bundleId)
        :return:
        '''
        driver.launch_app(package_info)

    @staticmethod
    def close_app(package_info):
        '''
        close app
        :param package_info: Android(package) or iOS(bundleId)
        :return:
        '''
        driver.close_app(package_info)

    @staticmethod
    def background_app():
        '''
        only appium
        :return:
        '''
        driver.background_app()

    @staticmethod
    def tap(x, y):
        '''
        :param x:
        :param y:
        :return:
        '''
        driver.tap(x, y)

    @staticmethod
    def double_tap(x, y):
        '''
        :param x:
        :param y:
        :return:
        '''
        driver.double_tap(x, y)

    @staticmethod
    def press(x, y, duration=2):
        '''
        :param x:
        :param y:
        :param duration:
        :return:
        '''
        driver.press(x, y, duration)

    @staticmethod
    def press(element, duration=2):
        '''
        :param element:
        :param duration:
        :return:
        '''
        driver.press(element, duration)

    @staticmethod
    def swipe_up(duration=2):
        '''
        :param duration:
        :return:
        '''
        driver.swipe_up(duration)

    @staticmethod
    def swipe_down(duration=2):
        '''
        :param duration:
        :return:
        '''
        driver.swipe_down(duration)

    @staticmethod
    def swipe_left(duration=2):
        '''
        :param duration:
        :return:
        '''
        driver.swipe_left(duration)

    @staticmethod
    def swipe_right(duration=2):
        '''
        :param duration:
        :return:
        '''
        driver.swipe_right(duration)

    @staticmethod
    def swipe(from_x, from_y, to_x, to_y, duration=2):
        '''
        :param from_x:
        :param from_y:
        :param to_x:
        :param to_y:
        :param duration:
        :return:
        '''
        driver.swipe(from_x, from_y, to_x, to_y, duration)

    @staticmethod
    def move_to(x, y):
        '''
        :param x:
        :param y:
        :return:
        '''
        driver.move_to(x, y)

    @staticmethod
    def click(key, timeout=10, interval=1, index=0):
        '''
        :param element:
        :param timeout:
        :param interval:
        :param index:
        :return:
        '''
        element = DriverBase.find_elements_by_key(key=key, timeout=timeout, interval=interval, index=index)
        if not element:
            raise Exception("Can't find element {}".format(key))
        element.click()

    @staticmethod
    def check(key, timeout=10, interval=1, index=0):
        '''
        :param key:
        :param timeout:
        :param interval:
        :param index:
        :return:
        '''
        element = DriverBase.find_elements_by_key(key=key, timeout=timeout, interval=interval, index=index)
        if not element:
            return False
        return True

    @staticmethod
    def input(key, text='', timeout=10, interval=1, index=0, clear=True):
        '''
        :param text:
        :param timeout:
        :param interval:
        :param index:
        :param clear:
        :return:
        '''
        element = DriverBase.find_elements_by_key(key=key, timeout=timeout, interval=interval, index=index)
        if not element:
            raise Exception("Can't find element {}".format(key))
        driver.input(element, text)

    @staticmethod
    def get_text(key, timeout=10, interval=1, index=0):
        '''
        :param key:
        :param timeout:
        :param interval:
        :param index:
        :return:
        '''
        element = DriverBase.find_elements_by_key(key=key, timeout=timeout, interval=interval, index=index)
        if not element:
            raise Exception("Can't find element {}".format(key))
        text = driver.get_text(element)
        return text

    @staticmethod
    def find_elements_by_key(key, timeout=10, interval=1, index=0):
        '''
        :param key:
        :param timeout:
        :param interval:
        :param index:
        :return:
        '''
        if not timeout:
            timeout = 10
        if not interval:
            interval = 1
        dict = {
            'element': key,
            'timeout': timeout,
            'interval': interval,
            'index': index
        }
        if Var.platformName.lower() == 'android':
            if re.match(r'[a-zA-Z]+\.[a-zA-Z]+[\.\w]+:id/\S+', key):
                dict['element_type'] = 'id'
            elif re.match(r'android\.[a-zA-Z]+[\.(a-zA-Z)]+', key) or re.match(r'[a-zA-Z]+\.[a-zA-Z]+[\.(a-zA-Z)]+', key):
                dict['element_type'] = 'classname'
            elif re.match('//\*\[@\S+=\S+\]', key) or re.match('//[a-zA-Z]+\.[a-zA-Z]+[\.(a-zA-Z)]+\[\d+\]', key):
                dict['element_type'] = 'xpath'
            else:
                dict['element_type'] = 'name'
        else:
            if re.match(r'XCUIElementType', key):
                dict['element_type'] = 'classname'
            elif re.match(r'//XCUIElementType', key):
                dict['element_type'] = 'xpath'
            elif re.match(r'//\*\[@\S+=\S+\]', key):
                dict['element_type'] = 'xpath'
            else:
                dict['element_type'] = 'name'
        return DriverBase.wait_for_elements_by_key(dict)

    @staticmethod
    def wait_for_elements_by_key(elements_info):
        '''
        :param elements_info:
        :return:
        '''

        element_type = elements_info['element_type']
        element = elements_info['element']
        timeout = elements_info['timeout']
        interval = elements_info['interval']
        index = elements_info['index']
        log_info("find elements: Body: {'using': '%s', 'value': '%s', 'index': %s}" % (element_type, element, index))
        if element_type == 'name':
            elements = driver.wait_for_elements_by_name(name=element, timeout=timeout, interval=interval)
        elif element_type == 'id':
            elements = driver.wait_for_elements_by_id(id=element, timeout=timeout, interval=interval)
        elif element_type == 'xpath':
            elements = driver.wait_for_elements_by_xpath(xpath=element, timeout=timeout, interval=interval)
        elif element_type == 'classname':
            elements = driver.wait_for_elements_by_classname(classname=element, timeout=timeout, interval=interval)
        else:
            elements = None

        log_info('return elements: {}'.format(elements))
        if elements:
            if len(elements) <= int(index):
                log_error('elements exists, but cannot find index({}) position'.format(index), False)
                raise Exception('list index out of range, index:{}'.format(index))
            return elements[index]
        return None
