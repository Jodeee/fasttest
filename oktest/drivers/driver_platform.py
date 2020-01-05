#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import traceback
import subprocess
from oktest.common import *


class DriverAndroid(object):

    @staticmethod
    def shell(cmd):
        '''
        :param cmd:
        :return:
        '''
        try:
            log_info(cmd)
            if cmd.startswith('shell'):
                cmd = ["adb", "-s", Var.udid, "shell", "{}".format(cmd.lstrip('shell').strip())]
                pipe = subprocess.Popen(cmd, stdin=subprocess.PIPE,
                                        stdout=subprocess.PIPE)
                out = pipe.communicate()
            else:
                cmd = ["adb", "-s", Var.udid, "{}".format(cmd)]
                os.system(' '.join(cmd))
        except:
            raise Exception(traceback.format_exc())

    @staticmethod
    def tap(x,y):
        '''
        :param element:
        :return:
        '''
        try:
            Var.driver.touch('tap', { 'x': x, 'y': y})
        except:
            raise Exception(traceback.format_exc())

    @staticmethod
    def doubleTap(x,y):
        '''
        :param element:
        :return:
        '''
        try:
            Var.driver.touch('doubleTap', { 'x': x, 'y': y})
        except:
            raise Exception(traceback.format_exc())

    @staticmethod
    def press(element,duration=2):
        '''
        :param element:
        :param duration:
        :return:
        '''
        try:
            element.touch('press', {'duration': duration})
        except:
            raise Exception(traceback.format_exc())

    @staticmethod
    def pinch_open(element,percent=0.8,steps=200):
        '''
        :param element:
        :param percent:
        :param steps:
        :return:
        '''
        try:
            element.touch('pinch', {'direction': 'in', 'percent': percent, 'steps': steps})
        except:
            raise Exception(traceback.format_exc())

    @staticmethod
    def pinch_close(element,percent=0.8,steps=200):
        '''
        :param element:
        :param percent:
        :param steps:
        :return:
        '''
        try:
            element.touch('pinch', {'direction': 'out', 'percent': percent, 'steps': steps})
        except:
            raise Exception(traceback.format_exc())


    @staticmethod
    def swipe_up(during=3):
        '''
        :param during:
        :return:
        '''
        try:
            width = Var.driver.get_window_size()['width']
            height = Var.driver.get_window_size()['height']
            DriverAndroid.shell(
                'shell input swipe {} {} {} {} {}'.format(width / 2, height * 3 / 4, width / 2, height / 4, during * 100))
        except:
            raise Exception(traceback.format_exc())

    @staticmethod
    def swipe_down(during=3):
        '''
        :param during:
        :return:
        '''
        try:
            width = Var.driver.get_window_size()['width']
            height = Var.driver.get_window_size()['height']
            DriverAndroid.shell(
                'shell input swipe {} {} {} {} {}'.format(width / 2, height / 4, width / 2, height * 3 / 4, during * 100))
        except:
            raise Exception(traceback.format_exc())


    @staticmethod
    def swipe_left(during=3):
        '''
        :param during:
        :return:
        '''
        try:
            width = Var.driver.get_window_size()['width']
            height = Var.driver.get_window_size()['height']
            DriverAndroid.shell(
                'shell input swipe {} {} {} {} {}'.format(width * 3 / 4, height / 2, width / 4, height / 2, during * 100))
        except:
            raise Exception(traceback.format_exc())

    @staticmethod
    def swipe_right(during=3):
        '''
        :param during:
        :return:
        '''
        try:
            width = Var.driver.get_window_size()['width']
            height = Var.driver.get_window_size()['height']
            DriverAndroid.shell(
                'shell input swipe {} {} {} {} {}'.format(width / 4, height / 2, width * 3 / 4, height / 2, during * 100))
        except:
            raise Exception(traceback.format_exc())

    @staticmethod
    def swipe(fromX,fromY,toX,toY,during=3):
        '''
        :param x:
        :param y:
        :param to_x:
        :param to_y:
        :param during:
        :return:
        '''
        try:
            DriverAndroid.shell('shell input swipe {} {} {} {} {}'.format(fromX, fromY, toX, toY, during * 100))
        except:
            raise Exception(traceback.format_exc())

    @staticmethod
    def wait_for_elements_by_id(id,timeout=10,interval=1):
        '''
        :param id:
        :param timeout:
        :param interval:
        :return:
        '''
        try:
            elements = Var.driver.wait_for_elements_by_id(id,int(timeout)*1000,int(interval)*1000)
            return elements
        except:
            return None

    @staticmethod
    def wait_for_elements_by_name(name,timeout=10,interval=1):
        '''
        :param name:
        :param timeout:
        :param interval:
        :return:
        '''
        try:
            elements = Var.driver.wait_for_elements_by_name(name,int(timeout)*1000,int(interval)*1000)
            return elements
        except:
            return None

    @staticmethod
    def wait_for_elements_by_xpath(xpath,timeout=10,interval=1):
        '''
        :param xpath:
        :param timeout:
        :param interval:
        :return:
        '''
        try:
            elements = Var.driver.wait_for_elements_by_xpath(xpath,int(timeout)*1000,int(interval)*1000)
            return elements
        except:
            return None

    @staticmethod
    def wait_for_elements_by_class_name(classname,timeout=10,interval=1):
        '''
        :param classname:
        :param timeout:
        :param interval:
        :return:
        '''
        try:
            elements = Var.driver.wait_for_elements_by_class_name(classname,int(timeout)*1000,int(interval)*1000)
            return elements
        except:
            return None

    @staticmethod
    def input(element, text="", clear=True):
        '''
        :param element:
        :param text:
        :param clear:
        :return:
        '''
        try:
            if clear:
                DriverAndroid.clear()
            element.click()
            element.send_keys(text)
        except:
            raise Exception(traceback.format_exc())

    @staticmethod
    def clear():
        '''
        :param text:
        :return:
        '''
        try:
            Var.driver.clear()
        except:
            pass


    @staticmethod
    def text(element):
        '''
        :param element:
        :return:
        '''
        try:
            return element.text
        except:
            return None

    @staticmethod
    def hide_keyboard():
        '''
        :return:
        '''
        try:
            DriverAndroid.shell('shell input keyevent 111')
        except:
            raise Exception(traceback.format_exc())


class DriveriOS(object):

    @staticmethod
    def tap(x, y):
        '''
        :param element:
        :return:
        '''
        try:
            Var.driver.touch('tap', {'x': x, 'y': y})
        except:
            raise Exception(traceback.format_exc())

    @staticmethod
    def doubleTap(x, y):
        '''
        :param element:
        :return:
        '''
        try:
            Var.driver.touch('doubleTap', {'x': x, 'y': y})
        except:
            raise Exception(traceback.format_exc())

    @staticmethod
    def press(element, duration=2):
        '''
        :param element:
        :param duration:
        :return:
        '''
        try:
            element.touch('press', {'duration': duration})
        except:
            raise Exception(traceback.format_exc())

    @staticmethod
    def pinch_open(element, percent=0.8, steps=200):
        '''
        :param element:
        :param percent:
        :param steps:
        :return:
        '''
        try:
            element.touch('pinch', {'scale': percent, 'velocity': steps})
        except:
            raise Exception(traceback.format_exc())

    @staticmethod
    def pinch_close(element, percent=0.8, steps=200):
        '''
        :param element:
        :param percent:
        :param steps:
        :return:
        '''
        try:
            element.touch('pinch', {'scale': percent, 'velocity': steps})
        except:
            raise Exception(traceback.format_exc())

    @staticmethod
    def swipe_up(during=3):
        '''
        :param during:
        :return:
        '''
        try:
            width = Var.driver.get_window_size()['width']
            height = Var.driver.get_window_size()['height']
            Var.driver.touch('drag', {'fromX': width / 2, 'fromY': height * 3 / 4, 'toX': width / 2, 'toY': height / 4,
                                      'duration': during})
        except:
            raise Exception(traceback.format_exc())

    @staticmethod
    def swipe_down(during=3):
        '''
        :param during:
        :return:
        '''
        try:
            width = Var.driver.get_window_size()['width']
            height = Var.driver.get_window_size()['height']
            Var.driver.touch('drag', {'fromX': width / 2, 'fromY': height / 4, 'toX': width / 2, 'toY': height * 3 / 4,
                                      'duration': during})
        except:
            raise Exception(traceback.format_exc())

    @staticmethod
    def swipe_left(during=3):
        '''
        :param during:
        :return:
        '''
        try:
            width = Var.driver.get_window_size()['width']
            height = Var.driver.get_window_size()['height']
            Var.driver.touch('drag', {'fromX': width * 3 / 4, 'fromY': height / 2, 'toX': width / 4, 'toY': 100,
                                      'duration': during})
        except:
            raise Exception(traceback.format_exc())

    @staticmethod
    def swipe_right(during=3):
        '''
        :param during:
        :return:
        '''
        try:
            width = Var.driver.get_window_size()['width']
            height = Var.driver.get_window_size()['height']
            Var.driver.touch('drag', {'fromX': 100, 'fromY': height / 2, 'toX': width * 3 / 4, 'toY': height / 2,
                                      'duration': during})
        except:
            raise Exception(traceback.format_exc())

    @staticmethod
    def swipe(fromX, fromY, toX, toY, during=3):
        '''
        :param x:
        :param y:
        :param to_x:
        :param to_y:
        :param during:
        :return:
        '''
        try:
            Var.driver.touch('drag', {'fromX': fromX, 'fromY': fromY, 'toX': toX, 'toY': toY, 'duration': during})
        except:
            raise Exception(traceback.format_exc())

    @staticmethod
    def wait_for_elements_by_id(id, timeout=10, interval=1):
        '''
        :param id:
        :param timeout:
        :param interval:
        :return:
        '''
        try:
            elements = Var.driver.wait_for_elements_by_id(id, int(timeout) * 1000, int(interval) * 1000)
            return elements
        except:
            return None

    @staticmethod
    def wait_for_elements_by_name(name, timeout=10, interval=1):
        '''
        :param name:
        :param timeout:
        :param interval:
        :return:
        '''
        try:
            elements = Var.driver.wait_for_elements_by_name(name, int(timeout) * 1000, int(interval) * 1000)
            return elements
        except:
            return None

    @staticmethod
    def wait_for_elements_by_xpath(xpath, timeout=10, interval=1):
        '''
        :param xpath:
        :param timeout:
        :param interval:
        :return:
        '''
        try:
            elements = Var.driver.wait_for_elements_by_xpath(xpath, int(timeout) * 1000, int(interval) * 1000)
            return elements
        except:
            return None

    @staticmethod
    def wait_for_elements_by_class_name(classname, timeout=10, interval=1):
        '''
        :param classname:
        :param timeout:
        :param interval:
        :return:
        '''
        try:
            elements = Var.driver.wait_for_elements_by_class_name(classname, int(timeout) * 1000, int(interval) * 1000)
            return elements
        except:
            return None

    @staticmethod
    def input(element, text="", clear=True):
        '''
        :param element:
        :param text:
        :param clear:
        :return:
        '''
        try:
            if clear:
                DriveriOS.clear()
            element.click()
            element.send_keys(text)
        except:
            raise Exception(traceback.format_exc())

    @staticmethod
    def clear():
        '''
        :param text:
        :return:
        '''
        try:
            Var.driver.clear()
        except:
            pass

    @staticmethod
    def text(element):
        '''
        :param element:
        :return:
        '''
        try:
            return element.text
        except:
            return None

    @staticmethod
    def hide_keyboard():
        '''
        :return:
        '''
        try:
            pass
        except:
            raise Exception(traceback.format_exc())