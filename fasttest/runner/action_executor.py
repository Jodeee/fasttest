#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
from fasttest.common import Var, log_info
from fasttest.drivers.driver_base import DriverBase
from fasttest.utils.opcv_utils import OpencvUtils
from fasttest.runner.action_keyword import ActionKeyWord

try:
    from Scripts import *
except Exception:
    pass


class ActionExecutor(object):

    def __action_start_app(self, step):
        """
        行为执行：start_app
        :param step:
        :return:
        """
        params = step.params
        if len(params) == 1:
            DriverBase.launch_app(params[0])
        else:
            raise TypeError('launchApp missing 1 required positional argument: package_info')

    def __action_stop_app(self, step):
        """
        行为执行：stop_app
        :param step:
        :return:
        """
        params = step.params
        if params is None:
            DriverBase.close_app(Var.package)
        elif len(params) == 1:
            DriverBase.close_app(params[0])
        else:
            raise TypeError('closeApp takes 1 positional argument but {} were giver'.format(len(params)))


    def __action_install_app(self, step):
        """
        行为执行：install_app
        :param step:
        :return:
        """
        if len(step.params) == 1:
            DriverBase.install_app(step.params[0])
        else:
            raise TypeError('installApp missing 1 required positional argument: app_path')

    def __action_uninstall_app(self, step):
        """
        行为执行：uninstall_app
        :param step:
        :return:
        """
        if len(step.params) == 1:
            DriverBase.uninstall_app(step.params[0])
        else:
            raise TypeError('uninstallApp missing 1 required positional argument: package_info')

    def __action_adb(self, step):
        """
        行为执行：adb
        :param step:
        :return:
        """
        if len(step.params) == 1:
            DriverBase.adb_shell(step.params[0])
        else:
            raise TypeError('adb missing 1 required positional argument')

    def __action_goback(self, step):
        """
        行为执行：goback
        :param step:
        :return:
        """
        DriverBase.adb_shell('shell input keyevent 4')

    def __action_tap(self, step):
        """
        行为执行：tap
        :param step:
        :return:
        """
        if len(step.params) == 2:
            DriverBase.tap(float(step.params[0]), float(step.params[-1]))
        else:
            raise TypeError('tap missing 2 required positional argument: x, y')

    def __action_doubleTap(self, step):
        """
        行为执行：doubleTap
        :param step:
        :return:
        """
        if len(step.params) == 2:
            DriverBase.double_tap(float(step.params[0]), float(step.params[-1]))
        else:
            raise TypeError('doubleTap missing 2 required positional argument: x, y')

    def __action_press(self, step):
        """
        行为执行：press
        :param step:
        :return:
        """
        if len(step.params) == 2:
            DriverBase.press(float(step.params[0]), float(step.params[-1]))
        elif len(step.params) == 3:
            DriverBase.press(float(step.params[0]), float(step.params[1]), float(step.params[-1]))
        else:
            raise TypeError('press missing 2 required positional argument: x, y')

    def __action_swipe_up(self, step):
        """
        行为执行：swipe_up
        :param step:
        :return:
        """
        if step.params is None:
            DriverBase.swipe_up()
        else:
            DriverBase.swipe_up(float(step.params[0]))

    def __action_swipe_down(self, step):
        """
        行为执行：swipe_down
        :param step:
        :return:
        """
        if step.params is None:
            DriverBase.swipe_down()
        else:
            DriverBase.swipe_down(float(step.params[0]))

    def __action_swipe_left(self, step):
        """
        行为执行：swipe_left
        :param step:
        :return:
        """
        if step.params is None:
            DriverBase.swipe_left()
        else:
            DriverBase.swipe_left(float(step.params[0]))

    def __action_swipe_right(self, step):
        """
        行为执行：swipe_right
        :param step:
        :return:
        """
        if step.params is None:
            DriverBase.swipe_right()
        else:
            DriverBase.swipe_right(float(step.params[0]))

    def __action_swipe(self, step):
        """
        行为执行：swipe
        :param step:
        :return:
        """
        params = step.params
        if params is None:
            raise TypeError('swipe missing 4 required positional argument: from_x, from_y, to_x, to_y')
        elif len(params) == 4:
            DriverBase.swipe(float(step.params[0]), float(step.params[1]), float(step.params[2]), float(step.params[3]))
        elif len(step.params) == 5:
            DriverBase.swipe(float(step.params[0]), float(step.params[1]), float(step.params[2]), float(step.params[3]), float(step.params[4]))
        else:
            raise TypeError('swipe takes 1 positional argument but {} were giver'.format(len(step.action)))

    def _action_get_text(self, step):
        """
        行为执行：getText
        :param step:
        :return:
        """
        params = step.params
        if len(params) == 1:
            text = DriverBase.get_text(key=params[0], timeout=Var.timeout, interval=Var.interval, index=0)
        elif len(params) == 2:
            text = DriverBase.get_text(key=params[0], timeout=Var.timeout, interval=Var.interval, index=params[-1])
        else:
            raise TypeError('getText missing 1 required positional argument: element')
        return text

    def __action_click(self, step):
        """
        行为执行：click
        :param step:
        :return:
        """
        params = step.params
        if len(params) == 1:
            img_info = self.ocr_analysis(step.action, params[0], True)
            if not isinstance(img_info, bool):
                Var.ocrimg = img_info['ocrimg']
                x = img_info['x']
                y = img_info['y']
                DriverBase.tap(x, y)
            else:
                if params[0]:
                    DriverBase.click(key=params[0], timeout=Var.timeout, interval=Var.interval, index=step.index)
                else:
                    raise TypeError('click missing 1 required positional argument: element')
        else:
            raise TypeError('click missing 1 required positional argument: element')

    def __action_check(self, step):
        """
        行为执行：check
        :param step:
        :return:
        """
        params = step.params
        if len(params) == 1:
            img_info = self.ocr_analysis(step.action, params[0], False)
            if not isinstance(img_info, bool):
                if img_info is not None:
                    Var.ocrimg = img_info['ocrimg']
                    check = True
                else:
                    check = False
            else:
                if params[0]:
                    check = DriverBase.check(key=params[0], timeout=Var.timeout, interval=Var.interval,
                                             index=step.index)
                else:
                    raise TypeError('check missing 1 required positional argument: element')

            if not check:
                raise Exception("Can't find element {}".format(step.element))
            return check
        else:
            raise TypeError('check missing 1 required positional argument: element')

    def __action_input(self, step):
        """
        行为执行：input
        :param step:
        :return:
        """
        params = step.params
        if len(params) == 2:

            if params[0]:
                DriverBase.input(key=params[0], text=params[1], timeout=Var.timeout, interval=Var.interval,
                                 index=step.index)
            else:
                raise TypeError('input missing 2 required positional argument: element, text')
        else:
            raise TypeError('input missing 2 required positional argument: element, text')


    def __action_if(self, step):
        """
        行为执行：if
        :param step:
        :return:
        """
        params = step.params
        if params:
            try:
                object_if = eval(params)
            except Exception as e:
                raise e
            if object_if:
                log_info('{} {}: True'.format(step.action, params))
            else:
                log_info('{} {}: False'.format(step.action, params))
            return object_if
        else:
            raise TypeError('{} missing 1 required positional argument'.format(step.action))

    def __action_ifcheck(self, step):
        """
        行为执行：ifcheck
        :param step:
        :return:
        """
        params = step.params
        if len(params) == 1:
            img_info = self.ocr_analysis(step.action, params[0], False)
            if not isinstance(img_info, bool):
                if img_info is not None:
                    Var.ocrimg = img_info['ocrimg']
                    check = True
                else:
                    check = False
            else:
                if params[0]:
                    check = DriverBase.check(key=params[0], timeout=Var.timeout, interval=Var.interval,
                                             index=step.index)
                else:
                    raise TypeError('{} missing 1 required positional argument: element'.format(step.action))
            return check
        else:
            raise TypeError('{} missing 1 required positional argument: element'.format(step.action))

    def __action_ifiOS(self, step):
        """
        行为执行：ifiOS
        :param step:
        :return:
        """
        if Var.platformName.lower() == 'ios':
            return True
        return False

    def __action_ifAndroid(self, step):
        """
        行为执行：ifAndroid
        :param step:
        :return:
        """
        if Var.platformName.lower() == 'android':
            return True
        return False

    def __action_else(self, step):
        """
        行为执行：else
        :param step:
        :return:
        """
        return True

    def __action_sleep(self, step):
        """
        行为执行
        :param step:
        :return:
        """
        params = step.params
        if params is None:
            raise TypeError('sleep missing 1 required positional argument')
        elif len(params) == 1:
            time.sleep(float(params[0]))

    def __action_assert(self, step):
        """
        行为解析：Assert
        :param step:
        :return:
        """
        params = step.params
        if params:
            try:
                result = eval(params)
                if result:
                    log_info('assert {}: True'.format(params))
                else:
                    log_info('assert {}: False'.format(params))
                assert result
            except AssertionError as e:
                raise AssertionError(params)
            except Exception as e:
                raise e
        else:
            raise TypeError('assert missing 1 required positional argument')


    def __action_while(self, step):
        """
        行为解析：while
        :param step:
        :return:
        """
        params = step.params
        if params:
            try:
                object_while = eval(params)
            except Exception as e:
                raise e
            if object_while:
                log_info('while {}: True'.format(params))
            else:
                log_info('while {}: False'.format(params))
            return object_while
        else:
            raise TypeError('where missing 1 required positional argument')


    def __action_break(self, step):
        """
        :param step:
        :return:
        """
        return True

    def __action_call(self, step):
        """
        行为执行：call
        :param step:
        :return:
        """
        if step.type == 'Scripts':
            try:
                eval(step.func)
            except Exception as e:
                raise e
        elif step.type == 'Common':
            from fasttest.runner.case_analysis import CaseAnalysis
            case = CaseAnalysis()
            case.iteration(Var.common_func[step.func].steps)
            Var.common_var = {}

    def __action_step(self, step):
        '''
        :return:
        '''

    def ocr_analysis(self, action, element, israise):
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

    def action_executor(self, step):
        """
        行为执行
        :param step:
        :return:
        """
        if len(step.keys()) == 1:
            action = self.__action_step(step)

        elif step.action == ActionKeyWord.INSTALLAPP:
            action = self.__action_install_app(step)

        elif step.action == ActionKeyWord.UNINSTALLAPP:
            action = self.__action_uninstall_app(step)

        elif step.action == ActionKeyWord.LAUNCHAPP:
            action = self.__action_start_app(step)

        elif step.action == ActionKeyWord.CLOSEAPP:
            action = self.__action_stop_app(step)

        elif step.action == ActionKeyWord.TAP:
            action = self.__action_tap(step)

        elif step.action == ActionKeyWord.DOUBLETAP:
            action = self.__action_doubleTap(step)

        elif step.action == ActionKeyWord.PRESS:
            action = self.__action_press(step)

        elif step.action == ActionKeyWord.ADB:
            action = self.__action_adb(step)

        elif step.action == ActionKeyWord.GOBACK:
            action = self.__action_goback(step)

        elif step.action == ActionKeyWord.SWIPEUP:
            action = self.__action_swipe_up(step)

        elif step.action == ActionKeyWord.SWIPEDOWN:
            action = self.__action_swipe_down(step)

        elif step.action == ActionKeyWord.SWIPELEFT:
            action = self.__action_swipe_left(step)

        elif step.action == ActionKeyWord.SWIPERIGHT:
            action = self.__action_swipe_right(step)

        elif step.action == ActionKeyWord.SWIPE:
            action = self.__action_swipe(step)

        elif step.action == ActionKeyWord.CLICK:
            action = self.__action_click(step)

        elif step.action == ActionKeyWord.CHECKT:
            action = self.__action_check(step)

        elif step.action == ActionKeyWord.INPUT:
            action = self.__action_input(step)

        elif step.action == ActionKeyWord.IF:
            action = self.__action_if(step)

        elif step.action == ActionKeyWord.ELIF:
            action = self.__action_if(step)

        elif step.action == ActionKeyWord.ELSE:
            action = self.__action_else(step)

        elif step.action == ActionKeyWord.IFCHECK:
            action = self.__action_ifcheck(step)

        elif step.action == ActionKeyWord.ELIFCHECK:
            action = self.__action_ifcheck(step)

        elif step.action == ActionKeyWord.IFIOS:
            action = self.__action_ifiOS(step)

        elif step.action == ActionKeyWord.IFANDROID:
            action = self.__action_ifAndroid(step)

        elif step.action == ActionKeyWord.SLEEP:
            action = self.__action_sleep(step)

        elif step.action == ActionKeyWord.ASSERT:
            action = self.__action_assert(step)

        elif step.action == ActionKeyWord.WHILE:
            action = self.__action_while(step)

        elif step.action == ActionKeyWord.BREAK:
            action = self.__action_break(step)

        elif step.action == ActionKeyWord.CALL:
            action = self.__action_call(step)
        else:
            raise SyntaxError(step)
        return action