#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from fasttest.common import Var
from fasttest.drivers.driver_base_app import DriverBaseApp
from fasttest.utils.opcv_utils import OpencvUtils
from fasttest.runner.action_executor_base import ActionExecutorBase


class ActionExecutorApp(ActionExecutorBase):

    def _installApp(self, action):
        '''
        :param action:
        :return:
        '''
        parms = self._getParms(action, 0)
        DriverBaseApp.install_app(parms)

    def _uninstallApp(self, action):
        '''
        :param action:
        :return:
        '''
        parms = self._getParms(action, 0)
        DriverBaseApp.uninstall_app(parms)

    def _launchApp(self, action):
        '''
        :param action:
        :return:
        '''
        parms = self._getParms(action, 0)
        DriverBaseApp.launch_app(parms)

    def _closeApp(self, action):
        '''
        :param action:
        :return:
        '''
        parms = self._getParms(action, 0, ignore=True)
        if parms:
            DriverBaseApp.close_app(parms)
        else:
            package = Var.desired_caps.package if Var.desired_caps.package else Var.desired_caps.appPackage
            DriverBaseApp.close_app(package)

    def _tap(self, action):
        '''
        :param action:
        :return:
        '''
        parms_x = self._getParms(action, 0)
        parms_y = self._getParms(action, 1)
        DriverBaseApp.tap(parms_x, parms_y)

    def _doubleTap(self, action):
        '''
        :param action:
        :return:
        '''
        parms_x = self._getParms(action, 0)
        parms_y = self._getParms(action, 1)
        DriverBaseApp.double_tap(parms_x, parms_y)

    def _press(self, action):
        '''
        :param action:
        :return:
        '''
        parms_x = self._getParms(action, 0)
        parms_y = self._getParms(action, 1)
        parms_s = self._getParms(action, 2, ignore=True)
        if not parms_s:
            DriverBaseApp.press(parms_x, parms_y)
        else:
            DriverBaseApp.press(parms_x, parms_y, parms_s)

    def _goBack(self, action):
        '''
        :param action:
        :return:
        '''
        DriverBaseApp.adb_shell('shell input keyevent 4')

    def _adb(self, action):
        '''
        :param action:
        :return:
        '''
        parms = self._getParms(action, 0)
        DriverBaseApp.adb_shell(parms)

    def _swipe(self, action):
        '''
        :param action:
        :return:
        '''
        parms_fx = self._getParms(action, 0)
        parms_fy = self._getParms(action, 1, ignore=True)
        parms_tx = self._getParms(action, 2, ignore=True)
        parms_ty = self._getParms(action, 3, ignore=True)
        parms_s = self._getParms(action, 4, ignore=True)
        try:
            if len(action.parms) == 1:
                swipe_f = getattr(DriverBaseApp, 'swipe_{}'.format(parms_fx.lower()))
                swipe_f()
            elif len(action.parms) == 2:
                swipe_f = getattr(DriverBaseApp, 'swipe_{}'.format(parms_fx.lower()))
                swipe_f(parms_fy)
            elif len(action.parms) == 4:
                DriverBaseApp.swipe(parms_fx, parms_fy, parms_tx, parms_ty)
            elif len(action.parms) == 5:
                DriverBaseApp.swipe(parms_fx, parms_fy, parms_tx, parms_ty, parms_s)
            else:
                raise
        except:
            raise TypeError('swipe takes 1 positional argument but {} were giver'.format(len(action.step)))

    def _input(self, action):
        '''
        :param action:
        :return:
        '''
        text = self._getParms(action, 1)
        element = self._getElement(action)
        DriverBaseApp.input(element, text)

    def _click(self, action):
        '''
        :param action:
        :return:
        '''
        parms = self._getParms(action, 0)
        image_name = '{}.png'.format(action.step)
        img_info = self._ocrAnalysis(image_name, parms)
        if not isinstance(img_info, bool):
            if img_info is not None:
                Var.ocrimg = img_info['ocrimg']
                x = img_info['x']
                y = img_info['y']
                DriverBaseApp.tap(x, y)
            else:
                raise Exception("Can't find element {}".format(parms))
        else:
            element = self._getElement(action)
            DriverBaseApp.click(element)

    def _check(self, action):
        '''
        :param action:
        :return:
        '''
        parms = self._getParms(action, 0)
        image_name = '{}.png'.format(action.step)
        img_info = self._ocrAnalysis(image_name, parms)
        if not isinstance(img_info, bool):
            if img_info is not None:
                Var.ocrimg = img_info['ocrimg']
            else:
                raise Exception("Can't find element {}".format(parms))
        else:
            self._getElement(action)

    def _ifiOS(self, action):
        '''
        :param action:
        :return:
        '''
        if Var.desired_caps.platformName.lower() == 'ios':
            return True
        return False

    def _ifAndroid(self, action):
        '''
        :param action:
        :return:
        '''
        if Var.desired_caps.platformName.lower() == 'android':
            return True
        return False

    def _getText(self, action):
        '''
        :param action:
        :return:
        '''
        element = self._getElement(action)
        text = DriverBaseApp.get_text(element)
        return text

    def _getElement(self, action):
        '''
        :param action:
        :return:
        '''
        parms = self._getParms(action, 0)
        if Var.driver == 'appium':
            from appium.webdriver import WebElement
        if Var.driver == 'macaca':
            from macaca.webdriver import WebElement
        if isinstance(parms, WebElement):
            element = parms
        else:
            element = DriverBaseApp.find_elements_by_key(key=parms, timeout=Var.time_out, interval=Var.interval)
        if not element:
            raise Exception("Can't find element {}".format(parms))
        return element

    def _getElements(self, action):
        '''
        :param action:
        :return:
        '''
        parms = self._getParms(action, 0)
        elements = DriverBaseApp.find_elements_by_key(key=parms, timeout=Var.time_out, interval=Var.interval,
                                                      not_processing=True)
        if not elements:
            raise Exception("Can't find element {}".format(parms))
        return elements

    def _isExist(self, action):
        '''
        :param action:
        :return:
        '''
        parms = self._getParms(action, 0)
        image_name = '{}.png'.format(action.step)
        img_info = self._ocrAnalysis(image_name, parms)
        result = True
        if not isinstance(img_info, bool):
            if img_info is not None:
                Var.ocrimg = img_info['ocrimg']
            else:
                result = False
        else:
            elements = DriverBaseApp.find_elements_by_key(key=parms, timeout=Var.time_out, interval=Var.interval, not_processing=True)
            result = bool(elements)
        return result

    def _isNotExist(self, action):
        '''
        :param action:
        :return:
        '''
        parms = self._getParms(action, 0)
        image_name = '{}.png'.format(action.step)
        img_info = self._ocrAnalysis(image_name, parms)
        result = False
        if not isinstance(img_info, bool):
            if img_info is not None:
                Var.ocrimg = img_info['ocrimg']
                result = True
        else:
            elements = DriverBaseApp.find_elements_by_key(key=parms, timeout=0, interval=Var.interval, not_processing=True)
            result = bool(elements)
        return not result

    def _ocrAnalysis(self,image_name, match_image):
        '''
        :param image_name:
        :param match_image:
        :return:
        '''
        try:
            if not isinstance(match_image, str):
                return False
            if not os.path.isfile(match_image):
                return False

            image_dir = os.path.join(Var.snapshot_dir, 'screenshot')
            if not os.path.exists(image_dir):
                os.makedirs(image_dir)
            base_image = os.path.join(image_dir, '{}'.format(image_name))
            Var.instance.save_screenshot(base_image)
            height = Var.instance.get_window_size()['height']

            orcimg = OpencvUtils(base_image, match_image, height)
            img_info = orcimg.extract_minutiae()
            if img_info:
                return img_info
            else:
                return None
        except:
            return False