#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import time
from collections import Iterable
from fasttest.common import Var, log_info, log_error
from fasttest.drivers.driver_base_app import DriverBaseApp
from fasttest.utils.opcv_utils import OpencvUtils


class ActionExecutorApp(object):

    def __from_scripts_file(self):

        file_list = []
        try:
            for rt, dirs, files in os.walk(os.path.join(Var.root, "Scripts")):
                for f in files:
                    if f == "__init__.py" or f.endswith(".pyc") or f.startswith(".") or not f.endswith('.py'):
                        continue
                    file_list.append(f'from Scripts.{f[:-3]} import *')

        except Exception as e:
            log_error(' {}'.format(e), False)

        return file_list

    def __out_result(self, key, result):
        '''
        input result
        '''
        if isinstance(result, list):
            log_info(f' <-- {key}: {type(result)}')
            for l in result:
                log_info(' - {}'.format(l))
        elif isinstance(result, dict):
            log_info(f' <-- {key}: {type(result)}')
            for k, v in result.items():
                log_info(' - {}: {}'.format(k, v))
        else:
            log_info(f' <-- {key}: {type(result)} {result}')

    def __get_element(self, key=None, index=0):
        '''
        :param action:
        :param index:
        :param is_return:
        :return:
        '''
        if Var.driver == 'appium':
            from appium.webdriver import WebElement
        if Var.driver == 'macaca':
            from macaca.webdriver import WebElement
        if isinstance(key, WebElement):
            element = key
        else:
            element = DriverBaseApp.find_elements_by_key(key=key, timeout=Var.time_out, interval=Var.interval, index=index)
        if not element:
            raise Exception("Can't find element {}".format(key))
        return element

    def __action_get_elements(self, action):
        '''
        :param action:
        :return:
        '''
        parms = action.parms
        if not isinstance(parms[0], str):
            raise TypeError('bad operand type: {}'.format(type(parms[0])))
        elements = DriverBaseApp.find_elements_by_key(key=parms[0], timeout=Var.time_out, interval=Var.interval, not_processing=True)
        if not elements:
            raise Exception("Can't find element {}".format(parms[0]))
        return elements

    def __get_value(self, action, index=0):
        '''
        :param action:
        :return:
        '''
        parms = action.parms
        if len(parms) <= index or not len(parms):
            raise TypeError('missing {} required positional argument'.format(index + 1))

        value = parms[index]
        return value

    def __action_start_app(self, action):
        """
        行为执行：start_app
        :param action:
        :return:
        """
        parms = action.parms
        if len(parms) == 1:
            DriverBaseApp.launch_app(parms[0])
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
            DriverBaseApp.close_app(Var.package)
        elif len(parms) == 1:
            DriverBaseApp.close_app(parms[0])
        else:
            raise TypeError('closeApp takes 1 positional argument but {} were giver'.format(len(parms)))

    def __action_install_app(self, action):
        """
        行为执行：install_app
        :param action:
        :return:
        """
        if len(action.parms) == 1:
            DriverBaseApp.install_app(action.parms[0])
        else:
            raise TypeError('installApp missing 1 required positional argument: app_path')

    def __action_uninstall_app(self, action):
        """
        行为执行：uninstall_app
        :param action:
        :return:
        """
        if len(action.parms) == 1:
            DriverBaseApp.uninstall_app(action.parms[0])
        else:
            raise TypeError('uninstallApp missing 1 required positional argument: package_info')

    def __action_adb(self, action):
        """
        行为执行：adb
        :param action:
        :return:
        """
        if len(action.parms) == 1:
            DriverBaseApp.adb_shell(action.parms[0])
        else:
            raise TypeError('adb missing 1 required positional argument')

    def __action_goback(self, action):
        """
        行为执行：goback
        :param action:
        :return:
        """
        DriverBaseApp.adb_shell('shell input keyevent 4')

    def __action_tap(self, action):
        """
        行为执行：tap
        :param action:
        :return:
        """
        if len(action.parms) == 2:
            DriverBaseApp.tap(float(action.parms[0]), float(action.parms[-1]))
        else:
            raise TypeError('tap missing 2 required positional argument: x, y')

    def __action_doubleTap(self, action):
        """
        行为执行：doubleTap
        :param action:
        :return:
        """
        if len(action.parms) == 2:
            DriverBaseApp.double_tap(float(action.parms[0]), float(action.parms[-1]))
        else:
            raise TypeError('doubleTap missing 2 required positional argument: x, y')

    def __action_press(self, action):
        """
        行为执行：press
        :param action:
        :return:
        """
        if len(action.parms) == 2:
            DriverBaseApp.press(float(action.parms[0]), float(action.parms[-1]))
        elif len(action.parms) == 3:
            DriverBaseApp.press(float(action.parms[0]), float(action.parms[1]), float(action.parms[-1]))
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
            DriverBaseApp.swipe_up()
        elif parms[0] == 'down':
            DriverBaseApp.swipe_down()
        elif parms[0] == 'left':
            DriverBaseApp.swipe_left()
        elif parms[0] == 'right':
            DriverBaseApp.swipe_right()
        elif len(parms) == 4:
            DriverBaseApp.swipe(float(action.parms[0]), float (action.parms[1]), float(action.parms[2]), float(action.parms[3]))
        elif len(action.parms) == 5:
            DriverBaseApp.swipe(float(action.parms[0]), float(action.parms[1]), float(action.parms[2]), float(action.parms[3]), int(action.parms[4]))
        else:
            raise TypeError('swipe takes 1 positional argument but {} were giver'.format(len(action.step)))

    def __action_getText(self, action):
        """
        行为执行：getText
        :param action:
        :return:
        """
        parms = action.parms
        if len(parms) == 1:
            element = self.__get_element(key=parms[0], index=0)
        elif len(parms) == 2:
            element = self.__get_element(key=parms[0], index=parms[-1])
        else:
            raise TypeError('getText missing 1 required positional argument: element')
        text = DriverBaseApp.get_text(element)
        return text

    def __action_click(self, action):
        """
        行为执行：click
        :param action:
        :return:
        """
        parms = action.parms
        if len(parms):
            image_name = '{}.png'.format(action.step)
            img_info = self.__ocr_analysis(image_name, parms[0], True)
            if img_info:
                Var.ocrimg = img_info['ocrimg']
                x = img_info['x']
                y = img_info['y']
                DriverBaseApp.tap(x, y)
            elif len(parms) == 1:
                element = self.__get_element(key=parms[0], index=0)
                DriverBaseApp.click(element)
            elif len(parms) == 2:
                element = self.__get_element(key=parms[0], index=parms[-1])
                DriverBaseApp.click(element)
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
            image_name = '{}.png'.format(action.step)
            img_info = self.__ocr_analysis(image_name, parms[0], True)
            if img_info:
                if img_info is not None:
                    Var.ocrimg = img_info['ocrimg']
                    check = True
                else:
                    check = False
                if not check:
                    raise Exception("Can't find element {}".format(parms[0]))
            elif len(parms) == 1:
                self.__get_element(key=parms[0], index=0)
            elif len(parms) == 2:
                self.__get_element(key=parms[0], index=parms[-1])
            else:
                raise TypeError('check takes 2 positional arguments but {} was given'.format(len(parms)))
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
            element = self.__get_element(key=parms[0], index=0)
        elif len(parms) == 3:
            element = self.__get_element(key=parms[0], index=parms[-1])
        else:
            raise TypeError('input missing 2 required positional argument: element, text')
        DriverBaseApp.input(element, parms[1])

    def __action_ifiOS(self, action):
        """
        行为执行：ifiOS
        :param action:
        :return:
        """
        if Var.desired_caps.platformName.lower() == 'ios':
            return True
        return False

    def __action_ifAndroid(self, action):
        """
        行为执行：ifAndroid
        :param action:
        :return:
        """
        if Var.desired_caps.platformName.lower() == 'android':
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

    def __ocr_analysis(self,image_name, match_image, israise):
        """
        :param match_image:
        :return:
        """
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
                return False
        except:
            return False

    def __action_getVar(self, action):
        '''
        :return:
        '''
        if action.key == '$.getText':
            result = self.__action_getText(action)
        elif action.key == '$.id':
            action.parms = action.parms.replace('\n', '')
            result = eval(action.parms)
        elif action.key == '$.getVar':
            if Var.global_var:
                if action.parms[0] in Var.global_var:
                    result = Var.global_var[action.parms[0]]
                else:
                    result = None
            else:
                result = None
        elif action.key == '$.getElement':
            parms = action.parms[0]
            result = self.__get_element(parms, index=0)
        elif action.key == '$.getElements':
            result = self.__action_get_elements(action)
        elif action.key:
            # 调用脚本
            result = self.new_action_executor(action, False)
        else:
            result = action.parms[0]

        self.__out_result(action.name, result)
        return result

    def __action_setVar(self, action):
        '''
        :return:
        '''
        key = self.__get_value(action, 0)
        values = self.__get_value(action, 1)
        Var.global_var[key] = values
        return

    def __action_call(self, action):
        '''
        :param action:
        :return:
        '''
        key = action.key
        parms = action.parms
        if  not key in Var.common_func.keys():
            raise NameError('name "{}" is not defined'.format(key))
        if len(Var.common_func[key].input) != len(parms):
            raise TypeError('{}() takes {} positional arguments but {} was given'.format(key, len(
                Var.common_func[key].input), len(parms)))
        common_var = dict(zip(Var.common_func[key].input, parms))

        try:
            from fasttest.runner.case_analysis import CaseAnalysis
            case = CaseAnalysis()
            case.iteration(Var.common_func[key].steps, f'{action.style}  ', common_var)
        except Exception as e:
            # call action中如果某一句step异常，此处会往上抛异常，导致call action也是失败状态，需要标记
            Var.exception_flag = True
            raise e
        return

    def __action_other(self, action):
        '''
        :return:
        '''
        key = action.key
        parms = action.parms
        try:
            parms = parms.replace('\n', '')
            result = eval(parms)
            if result:
                isTrue = True
            else:
                isTrue = False

            log_info(' <-- {}'.format(isTrue))
            if key == 'assert':
                assert result
            return isTrue
        except Exception as e:
            raise e

    def __action_for(self, action):
        '''
        :return:
        '''
        value = self.__get_value(action)
        var = action.var
        if not isinstance(value, Iterable):
            raise TypeError(f"'{value}' object is not iterable")
        return {'key': var, 'value': value}

    def new_action_executor(self, action, output=True):
        # 调用脚本
        if action.key:
            list = self.__from_scripts_file()
            for l in list:
                exec(l)
            parms = None
            for index, par in enumerate(action.parms):
                if not parms:
                    parms = 'action.parms[{}]'.format(index)
                    continue
                parms = '{}, action.parms[{}]'.format(parms, index)
            if not parms:
                result = eval('locals()[action.key]()')
            else:
                result = eval('locals()[action.key]({})'.format(parms))
            if result and output:
                self.__out_result(action.key, result)
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

        elif action.tag and action.tag == 'call':
            result = self.__action_call(action)

        elif action.tag and action.tag == 'other':
            result = self.__action_other(action)

        elif action.tag and action.tag == 'for':
            result = self.__action_for(action)

        elif action.key == 'setVar':
            result = self.__action_setVar(action)

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

        elif action.key == 'break':
            result = True

        elif action.key == 'else':
            result = True

        else:
            raise KeyError('The {} keyword is undefined!'.format(action.key))

        return result