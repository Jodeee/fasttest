#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import time
import traceback
import subprocess
from fasttest.common import *
from appium.webdriver.common.touch_action import TouchAction

class AndroidDriver(object):

    @staticmethod
    def adb_shell(cmd):
        '''
        :param cmd:
        :return:
        '''
        try:
            log_info('adb: {}'.format(cmd))
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
    def install_app(app_path):
        '''
        install app
        :param app_path:
        :return:
        '''
        try:
            Var.instance.install_app(app_path)
        except Exception as e:
            raise e

    @staticmethod
    def uninstall_app(package_info):
        '''
        uninstall app
        :param package_info: Android(package) or iOS(bundleId)
        :return:
        '''
        try:
            Var.instance.remove_app(package_info)
        except Exception as e:
            raise e

    @staticmethod
    def launch_app(package_info):
        '''
        launch app
        :param package_info: Android(package/activity) or iOS(bundleId)
        :return:
        '''
        try:
            if not package_info:
                Var.instance.launch_app()
            else:
                AndroidDriver.adb_shell('shell am start -W {}'.format(package_info))

        except Exception as e:
            raise e

    @staticmethod
    def close_app(package_info):
        '''
        close app
        :param package_info: Android(package) or iOS(bundleId)
        :return:
        '''
        try:
            if not package_info:
                Var.instance.close_app()
            else:
                AndroidDriver.adb_shell('shell am force-stop {}'.format(package_info))
        except Exception as e:
            raise e

    @staticmethod
    def background_app():
        '''
        only appium
        :return:
        '''
        try:
            Var.instance.background_app()
        except Exception as e:
            raise e

    @staticmethod
    def tap(x, y):
        '''
        :param x:
        :param y:
        :return:
        '''
        try:
            width = Var.instance.get_window_size()['width']
            height = Var.instance.get_window_size()['height']
            if x <= 1.0:
                x = x * width
            if y <= 1.0:
                y = y * height
            Var.instance.tap([(int(x), int(y))])
        except Exception as e:
            raise e

    @staticmethod
    def double_tap(x, y):
        '''
        :param x:
        :param y:
        :return:
        '''
        try:
            width = Var.instance.get_window_size()['width']
            height = Var.instance.get_window_size()['height']
            if x <= 1.0:
                x = x * width
            if y <= 1.0:
                y = y * height
            TouchAction(Var.instance).press(x=int(x), y=int(y), pressure=0.25).release().perform().wait(110). \
                press(x=int(x), y=int(y), pressure=0.25).release().perform()
        except Exception as e:
            raise e

    @staticmethod
    def press(x, y, duration=2):
        '''
        :param x:
        :param y:
        :param duration:
        :return:
        '''
        try:
            width = Var.instance.get_window_size()['width']
            height = Var.instance.get_window_size()['height']
            if x <= 1.0:
                x = x * width
            if y <= 1.0:
                y = y * height
            Var.instance.long_press(x=int(x), y=int(y), duration=duration)
        except Exception as e:
            raise e

    @staticmethod
    def press(element, duration=2):
        '''
        :param element:
        :param duration:
        :return:
        '''
        try:
            Var.instance.long_press(element=element, duration=duration)
        except Exception as e:
            raise e

    @staticmethod
    def swipe_up(duration=2):
        '''
        :param duration:
        :return:
        '''
        try:
            width = Var.instance.get_window_size()['width']
            height = Var.instance.get_window_size()['height']
            AndroidDriver.swipe(width / 2, height * 3 / 4, width / 2, height / 4, duration)
        except Exception as e:
            raise e

    @staticmethod
    def swipe_down(duration=2):
        '''
        :param duration:
        :return:
        '''
        try:
            width = Var.instance.get_window_size()['width']
            height = Var.instance.get_window_size()['height']
            AndroidDriver.swipe(width / 2, height / 4, width / 2, height * 3 / 4, duration)
        except Exception as e:
            raise e

    @staticmethod
    def swipe_left(duration=2):
        '''
        :param duration:
        :return:
        '''
        try:
            width = Var.instance.get_window_size()['width']
            height = Var.instance.get_window_size()['height']
            AndroidDriver.swipe(width * 3 / 4, height / 2, width / 4, height / 2, duration)
        except Exception as e:
            raise e

    @staticmethod
    def swipe_right(duration=2):
        '''
        :param duration:
        :return:
        '''
        try:
            width = Var.instance.get_window_size()['width']
            height = Var.instance.get_window_size()['height']
            AndroidDriver.swipe(width / 4, height / 2, width * 3 / 4, height / 2, duration)
        except Exception as e:
            raise e

    @staticmethod
    def swipe(from_x, from_y, to_x, to_y, duration=3):
        '''
        :param from_x:
        :param from_y:
        :param to_x:
        :param to_y:
        :param duration:
        :return:
        '''
        try:
            width = Var.instance.get_window_size()['width']
            height = Var.instance.get_window_size()['height']
            if from_x <= 1.0:
                from_x = from_x * width
            if from_y <= 1.0:
                from_y = from_y * height
            if to_x <= 1.0:
                to_x = to_x * width
            if to_y <= 1.0:
                to_y = to_y * height
            AndroidDriver.adb_shell(
                'shell input swipe {} {} {} {} {}'.format(from_x, from_y, to_x, to_y, duration * 100))
        except Exception as e:
            raise e

    @staticmethod
    def input(element, text, clear=True, hide_keyboard=True):
        '''
        :param element:
        :param text:
        :param clear:
        :param hide_keyboard:
        :return:
        '''
        try:
            # if clear:
            #     AndroidDriver.clear()
            # if hide_keyboard:
            #     AndroidDriver.hide_keyboard()
            element.send_keys(text)
        except Exception as e:
            raise e

    @staticmethod
    def get_text(element):
        '''
        :param element:
        :return:
        '''
        try:
            text = element.text
            return text
        except Exception as e:
            raise e

    @staticmethod
    def clear():
        '''
        :return:
        '''
        try:
            Var.instance.clear()
        except:
            traceback.print_exc()

    @staticmethod
    def hide_keyboard():
        '''
        :return:
        '''
        try:
            Var.instance.hide_keyboard()
        except:
            traceback.print_exc()

    @staticmethod
    def wait_for_elements_by_id(id, timeout=10, interval=1):
        '''
        :param id:
        :return:
        '''
        try:
            elements = Var.instance.find_elements_by_id(id)
            return elements
        except Exception as e:
            raise e

    @staticmethod
    def wait_for_elements_by_name(name, timeout=10, interval=1):
        '''
        :param name:
        :return:
        '''
        try:
            Var.instance.implicitly_wait(int(timeout)/2)
            elements = Var.instance.find_elements_by_accessibility_id(name)
            if not elements:
                elements = Var.instance.find_elements_by_android_uiautomator('new UiSelector().text("{}")'.format(name))
            Var.instance.implicitly_wait(timeout)
            return elements
        except Exception as e:
            raise e

    @staticmethod
    def wait_for_elements_by_xpath(xpath, timeout=10, interval=1):
        '''
        :param xpath:
        :return:
        '''
        try:
            elements = Var.instance.find_elements_by_xpath(xpath)
            return elements
        except Exception as e:
            raise e

    @staticmethod
    def wait_for_elements_by_classname(classname, timeout=10, interval=1):
        '''
        :param classname:
        :return:
        '''
        try:
            elements = Var.instance.find_elements_by_class_name(classname)
            return elements
        except Exception as e:
            raise e

class iOSDriver(object):

    @staticmethod
    def install_app(app_path):
        '''
        install app
        :param app_path:
        :return:
        '''
        try:
            Var.instance.install_app(app_path)
        except Exception as e:
            raise e

    @staticmethod
    def uninstall_app(package_info):
        '''
        uninstall app
        :param package_info: Android(package) or iOS(bundleId)
        :return:
        '''
        try:
            Var.instance.remove_app(package_info)
        except Exception as e:
            raise e

    @staticmethod
    def launch_app(package_info):
        '''
        launch app
        :param package_info: Android(package/activity) or iOS(bundleId)
        :return:
        '''
        try:
            if not package_info:
                Var.instance.launch_app()
            else:
                pass  # todo 待补充
        except Exception as e:
            raise e

    @staticmethod
    def close_app(package_info):
        '''
        close app
        :param package_info: Android(package) or iOS(bundleId)
        :return:
        '''
        try:
            if not package_info:
                Var.instance.close_app()
            else:
                pass # todo 待补充
        except Exception as e:
            raise e

    @staticmethod
    def background_app():
        '''
        only appium
        :return:
        '''
        try:
            Var.instance.background_app()
        except Exception as e:
            raise e

    @staticmethod
    def tap(x, y):
        '''
        :param x:
        :param y:
        :return:
        '''
        try:
            width = Var.instance.get_window_size()['width']
            height = Var.instance.get_window_size()['height']
            if x <= 1.0:
                x = x * width
            if y <= 1.0:
                y = y * height
            Var.instance.tap([(int(x), int(y))])
        except Exception as e:
            raise e

    @staticmethod
    def double_tap(x, y):
        '''
        :param x:
        :param y:
        :return:
        '''
        try:
            width = Var.instance.get_window_size()['width']
            height = Var.instance.get_window_size()['height']
            if x <= 1.0:
                x = x * width
            if y <= 1.0:
                y = y * height
            TouchAction(Var.instance).press(x=int(x), y=int(y), pressure=0.25).release().perform().wait(110). \
                press(x=int(x), y=int(y), pressure=0.25).release().perform()
        except Exception as e:
            raise e

    @staticmethod
    def press(x, y, duration=2):
        '''
        :param x:
        :param y:
        :param duration:
        :return:
        '''
        try:
            width = Var.instance.get_window_size()['width']
            height = Var.instance.get_window_size()['height']
            if x <= 1.0:
                x = x * width
            if y <= 1.0:
                y = y * height
            Var.instance.long_press(x=int(x), y=int(y), duration=duration)
        except Exception as e:
            raise e

    @staticmethod
    def press(element, duration=2):
        '''
        :param element:
        :param duration:
        :return:
        '''
        try:
            Var.instance.long_press(element=element, duration=duration)
        except Exception as e:
            raise e

    @staticmethod
    def swipe_up(duration=2):
        '''
        :param duration:
        :return:
        '''
        try:
            width = Var.instance.get_window_size()['width']
            height = Var.instance.get_window_size()['height']
            iOSDriver.swipe(width / 2, height * 3 / 4, width / 2, height / 4, duration)
        except Exception as e:
            raise e

    @staticmethod
    def swipe_down(duration=2):
        '''
        :param duration:
        :return:
        '''
        try:
            width = Var.instance.get_window_size()['width']
            height = Var.instance.get_window_size()['height']
            iOSDriver.swipe(width / 2, height / 4, width / 2, height * 3 / 4, duration)
        except Exception as e:
            raise e

    @staticmethod
    def swipe_left(duration=2):
        '''
        :param duration:
        :return:
        '''
        try:
            width = Var.instance.get_window_size()['width']
            height = Var.instance.get_window_size()['height']
            iOSDriver.swipe(width * 3 / 4, height / 2, width / 4, height / 2, duration)
        except Exception as e:
            raise e

    @staticmethod
    def swipe_right(duration=2):
        '''
        :param duration:
        :return:
        '''
        try:
            width = Var.instance.get_window_size()['width']
            height = Var.instance.get_window_size()['height']
            iOSDriver.swipe(width / 4, height / 2, width * 3 / 4, height / 2, duration)
        except Exception as e:
            raise e

    @staticmethod
    def swipe(from_x, from_y, to_x, to_y, duration=3):
        '''
        :param from_x:
        :param from_y:
        :param to_x:
        :param to_y:
        :param duration:
        :return:
        '''
        try:
            width = Var.instance.get_window_size()['width']
            height = Var.instance.get_window_size()['height']
            if from_x <= 1.0:
                from_x = from_x * width
            if from_y <= 1.0:
                from_y = from_y * height
            if to_x <= 1.0:
                to_x = to_x * width
            if to_y <= 1.0:
                to_y = to_y * height
            Var.instance.swipe(int(from_x), int(from_y), int(to_x), int(to_y), duration * 100)
        except Exception as e:
            raise e

    @staticmethod
    def input(element, text, clear=True, hide_keyboard=True):
        '''
        :param element:
        :param text:
        :param clear:
        :param hide_keyboard:
        :return:
        '''
        try:
            # if clear:
            #     iOSDriver.clear()
            # if hide_keyboard:
            #     iOSDriver.hide_keyboard()
            element.send_keys(text)
        except Exception as e:
            raise e

    @staticmethod
    def get_text(element):
        '''
        :param element:
        :return:
        '''
        try:
            text = element.text
            return text
        except Exception as e:
            raise e

    @staticmethod
    def clear():
        '''
        :return:
        '''
        try:
            Var.instance.clear()
        except:
            traceback.print_exc()

    @staticmethod
    def hide_keyboard():
        '''
        :return:
        '''
        try:
            Var.instance.hide_keyboard()
        except:
            traceback.print_exc()

    @staticmethod
    def wait_for_elements_by_id(id, timeout=10, interval=1):
        '''
        :param id:
        :return:
        '''
        try:
            elements = Var.instance.find_elements_by_id(id)
            return elements
        except Exception as e:
            raise e

    @staticmethod
    def wait_for_elements_by_name(name, timeout=10, interval=1):
        '''
        :param name:
        :return:
        '''
        try:
            elements = Var.instance.find_elements_by_accessibility_id(name)
            return elements
        except Exception as e:
            raise e

    @staticmethod
    def wait_for_elements_by_xpath(xpath, timeout=10, interval=1):
        '''
        :param xpath:
        :return:
        '''
        try:
            elements = Var.instance.find_elements_by_xpath(xpath)
            return elements
        except Exception as e:
            raise e

    @staticmethod
    def wait_for_elements_by_classname(classname, timeout=10, interval=1):
        '''
        :param classname:
        :return:
        '''
        try:
            elements = Var.instance.find_elements_by_class_name(classname)
            return elements
        except Exception as e:
            raise e


