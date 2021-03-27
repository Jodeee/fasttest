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

    def _from_scripts_file(self):

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

    def _out_result(self, key, result):
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


    def _get_value(self, action, index=0):
        '''
        :param action:
        :return:
        '''
        parms = action.parms
        if len(parms) <= index or not len(parms):
            raise TypeError('missing {} required positional argument'.format(index + 1))

        value = parms[index]
        return value


    def _get_element(self, action):
        '''
        :param action:
        :return:
        '''
        parms = self._get_value(action, 0)
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

    def _action_get_elements(self, action):
        '''
        :param action:
        :return:
        '''
        parms = self._get_value(action, 0)
        if not isinstance(parms, str):
            raise TypeError('bad operand type: {}'.format(type(parms)))
        elements = DriverBaseApp.find_elements_by_key(key=parms, timeout=Var.time_out, interval=Var.interval, not_processing=True)
        if not elements:
            raise Exception("Can't find element {}".format(parms))
        return elements

    def _action_get_len(self, action):
        """
        len
        :param action:
        :return:
        """
        value = self._get_value(action)
        if value:
            return len(value)
        return 0

    def _action_is_exist(self, action):
        '''
        :param action:
        :return:
        '''
        parms = self._get_value(action, 0)
        image_name = '{}.png'.format(action.step)
        img_info = self._ocr_analysis(image_name, parms, True)
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

    def _action_is_not_exist(self, action):
        '''
        :param action:
        :return:
        '''
        parms = self._get_value(action, 0)
        image_name = '{}.png'.format(action.step)
        img_info = self._ocr_analysis(image_name, parms, True)
        result = False
        if not isinstance(img_info, bool):
            if img_info is not None:
                Var.ocrimg = img_info['ocrimg']
                result = True
        else:
            elements = DriverBaseApp.find_elements_by_key(key=parms, timeout=0, interval=Var.interval, not_processing=True)
            result = bool(elements)
        return not result

    def _action_start_app(self, action):
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

    def _action_stop_app(self, action):
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

    def _action_install_app(self, action):
        """
        行为执行：install_app
        :param action:
        :return:
        """
        if len(action.parms) == 1:
            DriverBaseApp.install_app(action.parms[0])
        else:
            raise TypeError('installApp missing 1 required positional argument: app_path')

    def _action_uninstall_app(self, action):
        """
        行为执行：uninstall_app
        :param action:
        :return:
        """
        if len(action.parms) == 1:
            DriverBaseApp.uninstall_app(action.parms[0])
        else:
            raise TypeError('uninstallApp missing 1 required positional argument: package_info')

    def _action_adb(self, action):
        """
        行为执行：adb
        :param action:
        :return:
        """
        if len(action.parms) == 1:
            DriverBaseApp.adb_shell(action.parms[0])
        else:
            raise TypeError('adb missing 1 required positional argument')

    def _action_goback(self, action):
        """
        行为执行：goback
        :param action:
        :return:
        """
        DriverBaseApp.adb_shell('shell input keyevent 4')

    def _action_tap(self, action):
        """
        行为执行：tap
        :param action:
        :return:
        """
        if len(action.parms) == 2:
            DriverBaseApp.tap(float(action.parms[0]), float(action.parms[-1]))
        else:
            raise TypeError('tap missing 2 required positional argument: x, y')

    def _action_doubleTap(self, action):
        """
        行为执行：doubleTap
        :param action:
        :return:
        """
        if len(action.parms) == 2:
            DriverBaseApp.double_tap(float(action.parms[0]), float(action.parms[-1]))
        else:
            raise TypeError('doubleTap missing 2 required positional argument: x, y')

    def _action_press(self, action):
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

    def _action_swipe(self, action):
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

    def _action_getText(self, action):
        """
        行为执行：getText
        :param action:
        :return:
        """
        element = self._get_element(action)
        text = DriverBaseApp.get_text(element)
        return text

    def _action_click(self, action):
        """
        行为执行：click
        :param action:
        :return:
        """
        parms = self._get_value(action, 0)
        image_name = '{}.png'.format(action.step)
        img_info = self._ocr_analysis(image_name, parms, True)
        if not isinstance(img_info, bool):
            if img_info is not None:
                Var.ocrimg = img_info['ocrimg']
                x = img_info['x']
                y = img_info['y']
                DriverBaseApp.tap(x, y)
            else:
                raise Exception("Can't find element {}".format(parms))
        else:
            element = self._get_element(action)
            DriverBaseApp.click(element)

    def _action_check(self, action):
        """
        行为执行：check
        :param action:
        :return:
        """
        parms = self._get_value(action, 0)
        image_name = '{}.png'.format(action.step)
        img_info = self._ocr_analysis(image_name, parms, True)
        if not isinstance(img_info, bool):
            if img_info is not None:
                Var.ocrimg = img_info['ocrimg']
            else:
                raise Exception("Can't find element {}".format(parms))
        else:
            self._get_element(action)

    def _action_input(self, action):
        """
        行为执行：input
        :param action:
        :return:
        """
        text = self._get_value(action, -1)
        element = self._get_element(action)
        DriverBaseApp.input(element, text)

    def _action_ifiOS(self, action):
        """
        行为执行：ifiOS
        :param action:
        :return:
        """
        if Var.desired_caps.platformName.lower() == 'ios':
            return True
        return False

    def _action_ifAndroid(self, action):
        """
        行为执行：ifAndroid
        :param action:
        :return:
        """
        if Var.desired_caps.platformName.lower() == 'android':
            return True
        return False

    def _action_sleep(self, action):
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

    def _action_set_timeout(self, action):
        """
        行为执行：setTimeout
        :param action:
        :return:
        """
        time = self._get_value(action)
        Var.time_out = int(time)

    def _ocr_analysis(self,image_name, match_image, israise):
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
                return None
        except:
            return False

    def _action_getVar(self, action):
        '''
        :return:
        '''
        if action.key == '$.getText':
            result = self._action_getText(action)
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
            result = self._get_element(action)
        elif action.key == '$.getElements':
            result = self._action_get_elements(action)
        elif action.key == '$.getLen':
            result = self._action_get_len(action)
        elif action.key == '$.isExist':
            result = self._action_is_exist(action)
        elif action.key == '$.isNotExist':
            result = self._action_is_not_exist(action)
        elif action.key:
            # 调用脚本
            result = self.new_action_executor(action, False)
        else:
            result = action.parms[0]

        self._out_result(action.name, result)
        return result

    def _action_setVar(self, action):
        '''
        :return:
        '''
        key = self._get_value(action, 0)
        values = self._get_value(action, 1)
        Var.global_var[key] = values
        return

    def _action_call(self, action):
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

    def _action_other(self, action):
        '''
        :return:
        '''
        key = action.key
        parms = action.parms
        try:
            parms = parms.replace('\n', '')
            result = eval(parms)
            log_info(' <-- {}'.format(bool(result)))
            if key == 'assert':
                assert result
            return bool(result)
        except Exception as e:
            raise e

    def _action_for(self, action):
        '''
        :return:
        '''
        value = self._get_value(action)
        var = action.var
        if not isinstance(value, Iterable):
            raise TypeError(f"'{value}' object is not iterable")
        return {'key': var, 'value': value}

    def new_action_executor(self, action, output=True):
        # 调用脚本
        if action.key:
            list = self._from_scripts_file()
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
                self._out_result(action.key, result)
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
            result = self._action_getVar(action)

        elif action.tag and action.tag == 'call':
            result = self._action_call(action)

        elif action.tag and action.tag == 'other':
            result = self._action_other(action)

        elif action.tag and action.tag == 'for':
            result = self._action_for(action)

        elif action.key == 'setVar':
            result = self._action_setVar(action)

        elif action.key == 'installApp':
            result = self._action_install_app(action)

        elif action.key == 'uninstallApp':
            result = self._action_uninstall_app(action)

        elif action.key == 'launchApp':
            result = self._action_start_app(action)

        elif action.key == 'closeApp':
            result = self._action_stop_app(action)

        elif action.key == 'tap':
            result = self._action_tap(action)

        elif action.key == 'doubleTap':
            result = self._action_doubleTap(action)

        elif action.key == 'press':
            result = self._action_press(action)

        elif action.key == 'goBack':
            result = self._action_goback(action)

        elif action.key == 'adb':
            result = self._action_adb(action)

        elif action.key == 'swipe':
            result = self._action_swipe(action)

        elif action.key == 'click':
            result = self._action_click(action)

        elif action.key == 'check':
            result = self._action_check(action)

        elif action.key == 'input':
            result = self._action_input(action)

        elif action.key == 'sleep':
            result = self._action_sleep(action)

        elif action.key == 'setTimeout':
            result = self._action_set_timeout(action)

        elif action.key == 'ifiOS':
            result = self._action_ifiOS(action)

        elif action.key == 'ifAndroid':
            result = self._action_ifAndroid(action)

        elif action.key == 'break':
            result = True

        elif action.key == 'else':
            result = True

        else:
            raise KeyError('The {} keyword is undefined!'.format(action.key))

        return result