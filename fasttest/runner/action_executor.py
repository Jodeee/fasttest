#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import time
from fasttest.common import Var, log_info
from fasttest.drivers.driver_base import DriverBase
from fasttest.utils.opcv_utils import OpencvUtils
try:
    from Scripts import *
except Exception:
    pass


class ActionExecutor(object):

    def __action_start_app(self, action):
        """
        行为执行：start_app
        :param action:
        :return:
        """
        parms = action.parms
        if len(parms) == 1:
            DriverBase.launch_app(parms[0])
        else:
            raise TypeError('launchApp missing 1 required positional argument: package_info')

    def __action_stop_app(self, action):
        """
        行为执行：stop_app
        :param action:
        :return:
        """
        parms = action.parms
        if parms is None:
            DriverBase.close_app(Var.package)
        elif len(parms) == 1:
            DriverBase.close_app(parms[0])
        else:
            raise TypeError('closeApp takes 1 positional argument but {} were giver'.format(len(parms)))

    def __action_install_app(self, action):
        """
        行为执行：install_app
        :param action:
        :return:
        """
        if len(action.parms) == 1:
            DriverBase.install_app(action.parms[0])
        else:
            raise TypeError('installApp missing 1 required positional argument: app_path')

    def __action_uninstall_app(self, action):
        """
        行为执行：uninstall_app
        :param action:
        :return:
        """
        if len(action.parms) == 1:
            DriverBase.uninstall_app(action.parms[0])
        else:
            raise TypeError('uninstallApp missing 1 required positional argument: package_info')

    def __action_adb(self, action):
        """
        行为执行：adb
        :param action:
        :return:
        """
        if len(action.parms) == 1:
            DriverBase.adb_shell(action.parms[0])
        else:
            raise TypeError('adb missing 1 required positional argument')

    def __action_goback(self, action):
        """
        行为执行：goback
        :param action:
        :return:
        """
        DriverBase.adb_shell('shell input keyevent 4')

    def __action_tap(self, action):
        """
        行为执行：tap
        :param action:
        :return:
        """
        if len(action.parms) == 2:
            DriverBase.tap(float(action.parms[0]), float(action.parms[-1]))
        else:
            raise TypeError('tap missing 2 required positional argument: x, y')

    def __action_doubleTap(self, action):
        """
        行为执行：doubleTap
        :param action:
        :return:
        """
        if len(action.parms) == 2:
            DriverBase.double_tap(float(action.parms[0]), float(action.parms[-1]))
        else:
            raise TypeError('doubleTap missing 2 required positional argument: x, y')

    def __action_press(self, action):
        """
        行为执行：press
        :param action:
        :return:
        """
        if len(action.parms) == 2:
            DriverBase.press(float(action.parms[0]), float(action.parms[-1]))
        elif len(action.parms) == 3:
            DriverBase.press(float(action.parms[0]), float(action.parms[1]), float(action.parms[-1]))
        else:
            raise TypeError('press missing 2 required positional argument: x, y')

    def __action_swipe(self, action):
        """
        行为执行：swipe
        :param action:
        :return:
        """
        parms = action.parms
        if parms is None:
            raise TypeError('swipe missing 4 required positional argument: from_x, from_y, to_x, to_y')
        if parms[0] == 'up':
            DriverBase.swipe_up()
        elif parms[0] == 'down':
            DriverBase.swipe_down()
        elif parms[0] == 'left':
            DriverBase.swipe_left()
        elif parms[0] == 'right':
            DriverBase.swipe_right()
        elif len(parms) == 4:
            DriverBase.swipe(float(action.parms[0]), float (action.parms[1]), float(action.parms[2]), float(action.parms[3]))
        elif len(action.parms) == 5:
            DriverBase.swipe(float(action.parms[0]), float(action.parms[1]), float(action.parms[2]), float(action.parms[3]), int(action.parms[4]))
        else:
            raise TypeError('swipe takes 1 positional argument but {} were giver'.format(len(action.action)))

    def __action_getText(self, action):
        """
        行为执行：getText
        :param action:
        :return:
        """
        parms = action.parms
        if len(parms) == 1:
            text = DriverBase.get_text(key=parms[0], timeout=Var.timeout, interval=Var.interval, index=0)
        elif len(parms) == 2:
            text = DriverBase.get_text(key=parms[0], timeout=Var.timeout, interval=Var.interval, index=parms[-1])
        else:
            raise TypeError('getText missing 1 required positional argument: element')
        return text

    def __action_click(self, action):
        """
        行为执行：click
        :param action:
        :return:
        """
        parms = action.parms
        if len(parms):
            img_info = self.__ocr_analysis(action.action, parms[0], True)
            if not isinstance(img_info, bool):
                Var.ocrimg = img_info['ocrimg']
                x = img_info['x']
                y = img_info['y']
                DriverBase.tap(x, y)
            elif len(parms) == 1:
                DriverBase.click(key=parms[0], timeout=Var.timeout, interval=Var.interval, index=0)
            elif len(parms) == 2:
                DriverBase.click(key=parms[0], timeout=Var.timeout, interval=Var.interval, index=parms[1])
        else:
            raise TypeError('click missing 1 required positional argument: element')

    def __action_check(self, action):
        """
        行为执行：check
        :param action:
        :return:
        """
        parms = action.parms
        if len(parms):
            img_info = self.__ocr_analysis(action.action, parms[0], True)
            if not isinstance(img_info, bool):
                if img_info is not None:
                    Var.ocrimg = img_info['ocrimg']
                    check = True
                else:
                    check = False
            elif len(parms) == 1:
                check = DriverBase.check(key=parms[0], timeout=Var.timeout, interval=Var.interval, index=0)
            elif len(parms) == 2:
                check = DriverBase.check(key=parms[0], timeout=Var.timeout, interval=Var.interval, index=parms[1])
            else:
                raise TypeError('check takes 2 positional arguments but {} was given'.format(len(parms)))

            if not check:
                raise Exception("Can't find element {}".format(parms[0]))
            return check
        else:
            raise TypeError('click missing 1 required positional argument: element')

    def __action_input(self, action):
        """
        行为执行：input
        :param action:
        :return:
        """
        parms = action.parms
        if len(parms) == 2:
            DriverBase.input(key=parms[0], text=parms[1], timeout=Var.timeout, interval=Var.interval,
                             index=0)
        elif len(parms) == 3:
            DriverBase.input(key=parms[0], text=parms[1], timeout=Var.timeout, interval=Var.interval,
                             index=parms[2])
        else:
            raise TypeError('input missing 2 required positional argument: element, text')

    def __action_ifcheck(self, action):
        """
        行为执行：ifcheck
        :param action:
        :return:
        """
        parms = action.parms
        if len(parms):
            img_info = self.__ocr_analysis(action.action, parms[0], True)
            if not isinstance(img_info, bool):
                if img_info is not None:
                    Var.ocrimg = img_info['ocrimg']
                    check = True
                else:
                    check = False
            elif len(parms) == 1:
                check = DriverBase.check(key=parms[0], timeout=Var.timeout, interval=Var.interval, index=0)
            elif len(parms) == 2:
                check = DriverBase.check(key=parms[0], timeout=Var.timeout, interval=Var.interval, index=parms[1])
            else:
                raise TypeError('check takes 2 positional arguments but {} was given'.format(len(parms)))

            return check
        else:
            raise TypeError('click missing 1 required positional argument: element')

    def __action_ifiOS(self, action):
        """
        行为执行：ifiOS
        :param action:
        :return:
        """
        if Var.platformName.lower() == 'ios':
            return True
        return False

    def __action_ifAndroid(self, action):
        """
        行为执行：ifAndroid
        :param action:
        :return:
        """
        if Var.platformName.lower() == 'android':
            return True
        return False

    def __action_sleep(self, action):
        """
        行为执行
        :param action:
        :return:
        """
        parms = action.parms
        if parms is None:
            raise TypeError('sleep missing 1 required positional argument')
        elif len(parms) == 1:
            time.sleep(float(parms[0]))

    def __ocr_analysis(self, action, element, israise):
        """
        :param action:
        :param element:
        :return:
        """
        if element not in Var.extensions_var['images_file'].keys():
            return False
        time.sleep(5)
        img_file = Var.extensions_var['images_file'][element]
        orcimg = OpencvUtils(action, img_file)
        orcimg.save_screenshot()
        img_info = orcimg.extract_minutiae()
        if img_info:
            return img_info
        else:
            if israise:
                raise Exception("Can't find element {}".format(element))
            else:
                return None

    def __action_getVar(self, action):
        '''
        :return:
        '''
        if action.key == '$.getText':
            result = self.__action_getText(action)
        elif action.key == '$.id':
            result = eval(action.parms)
        elif action.key == '$.getVar':
            if Var.global_var:
                if action.parms[0] in Var.global_var:
                    result = Var.global_var[action.parms[0]]
                else:
                    result = None
            else:
                result = None
        elif action.key:
            func = f'{action.key}({action.parms})'
            result = eval(func)
            log_info(f'{action.key}: {result}')
        else:
           result = action.parms[0]
        return result

    def __action_setVar(self, action):
        '''
        :return:
        '''
        key = action.parms[0]
        values = action.parms[1]
        Var.global_var[key] = values
        return

    def __action_call(self, action):
        '''
        :param action:
        :return:
        '''
        Var.common_var = {}
        key = action.key
        parms = action.parms
        if  not key in Var.common_func.keys():
            raise NameError('name "{}" is not defined'.format(key))
        if len(Var.common_func[key].input) != len(parms):
            raise TypeError('{}() takes {} positional arguments but {} was given'.format(key, len(
                Var.common_func[key].input), len(parms)))
        Var.common_var = dict(zip(Var.common_func[key].input, parms))

        from fasttest.runner.case_analysis import CaseAnalysis
        case = CaseAnalysis()
        case.iteration(Var.common_func[key].steps, f'{action.style}  ')
        Var.common_var = {}
        return

    def __action_other(self, action):
        '''
        :return:
        '''
        key = action.key
        parms = action.parms
        try:
            result = eval(parms)
            log_info('{}: {}'.format(action.parms, result))
            if key == 'assert':
                assert result
            return result
        except Exception as e:
            raise e

    def new_action_executor(self, action):

        if action.key:
            func = f'{action.key}({action.parms})'
            result = eval(func)
            log_info(f'{action.key} return: {result}')
            return result
        else:
            raise KeyError('The {} keyword is undefined!'.format(action.step))

    def action_executor(self, action):
        """
        行为执行
        :param action:
        :return:
        """
        if action.tag and action.tag == 'getVar':
            result = self.__action_getVar(action)

        elif action.tag and action.tag == 'setVar':
            result = self.__action_setVar(action)

        elif action.tag and action.tag == 'call':
            result = self.__action_call(action)

        elif action.tag and action.tag == 'other':
            result = self.__action_other(action)

        elif action.key == 'installApp':
            result = self.__action_install_app(action)

        elif action.key == 'uninstallApp':
            result = self.__action_uninstall_app(action)

        elif action.key == 'launchApp':
            result = self.__action_start_app(action)

        elif action.key == 'closeApp':
            result = self.__action_stop_app(action)

        elif action.key == 'tap':
            result = self.__action_tap(action)

        elif action.key == 'doubleTap':
            result = self.__action_doubleTap(action)

        elif action.key == 'press':
            result = self.__action_press(action)

        elif action.key == 'goBack':
            result = self.__action_goback(action)

        elif action.key == 'adb':
            result = self.__action_adb(action)

        elif action.key == 'swipe':
            result = self.__action_swipe(action)

        elif action.key == 'click':
            result = self.__action_click(action)

        elif action.key == 'check':
            result = self.__action_check(action)

        elif action.key == 'input':
            result = self.__action_input(action)

        elif action.key == 'sleep':
            result = self.__action_sleep(action)

        elif action.key == 'ifiOS':
            result = self.__action_ifiOS(action)

        elif action.key == 'ifAndroid':
            result = self.__action_ifAndroid(action)

        elif action.key == 'ifcheck':
            result = self.__action_ifcheck(action)

        elif action.key == 'elifcheck':
            result = self.__action_ifcheck(action)

        elif action.key == 'break':
            result = None

        elif action.key == 'else':
            result = None

        else:
            raise KeyError('The {} keyword is undefined!'.format(action.key))

        return result