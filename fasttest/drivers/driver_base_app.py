#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
from fasttest.common import *

class DriverBaseApp(object):


    @staticmethod
    def init():
        try:
            global driver
            if Var.driver.lower() == 'appium':
                from fasttest.drivers.appium import AndroidDriver, iOSDriver
            else:
                from fasttest.drivers.macaca import AndroidDriver, iOSDriver

            if Var.desired_caps.platformName.lower() == "ios":
                driver = iOSDriver
            elif Var.desired_caps.platformName.lower() == "android":
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
    def click(element):
        '''
        :param element:
        :return:
        '''
        element.click()

    @staticmethod
    def check(element):
        '''
        :param element:
        :return:
        '''
        if not element:
            return False
        return True

    @staticmethod
    def input(element, text='', clear=True):
        '''
        :param element:
        :param text:
        :param clear:
        :return:
        '''
        driver.input(element, text)

    @staticmethod
    def get_text(element, index=0):
        '''
        :param element:
        :param index:
        :return:
        '''
        text = driver.get_text(element)
        return text

    @staticmethod
    def find_elements_by_key(key, timeout=10, interval=1, index=0, not_processing=False):
        '''
        :param key:
        :param timeout:
        :param interval:
        :param index:
        :param not_processing: 不处理数据
        :return:
        '''
        if not interval:
            interval = 0.5
        dict = {
            'element': key,
            'timeout': timeout,
            'interval': interval,
            'index': index,
            'not_processing': not_processing
        }
        if Var.desired_caps.platformName.lower() == 'android':
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
        return DriverBaseApp.wait_for_elements_by_key(dict)

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
        not_processing = elements_info['not_processing']
        log_info(" --> body: {'using': '%s', 'value': '%s', 'index': %s, 'timeout': %s}" % (element_type, element, index, timeout))
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

        if elements:
            log_info(' <-- result:')
            for e in elements:
                log_info(' - {}'.format(e))
            if len(elements) <= int(index):
                log_error('elements exists, but cannot find index({}) position'.format(index), False)
                raise Exception('list index out of range, index:{}'.format(index))
            if not_processing:
                return elements
            return elements[index]
        return None
