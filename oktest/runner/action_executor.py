#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
from oktest.common import Var
from oktest.drivers.driver_base import DriverBase
from oktest.common.decorator import keywords
from oktest.utils.opcv_utils import OpencvUtils
try:
    from Scripts import *
except Exception:
    pass


class Action(object):
    VARIABLES = 'variables'
    SCRIPTS = 'Scripts'
    CALL = 'call'
    COMMON = 'Common'

    # APP 操作
    STARTAPP = 'startApp'
    STOPAPP = 'stopApp'

    # 手势
    TAP = 'tap'
    DOUBLETAP = 'doubleTap'
    PRESS = 'press'
    PINCHOPEN = 'pinchOpen'  # 待实现
    PINCHCLOSE = 'pinchClose'  # 待实现
    ROTATE = 'rotate'  # 待实现
    DRAG = 'drag'  # 待实现

    # only Android
    GOBACK = 'goBack'
    ADB = 'adb'
    ADBSHELL = 'adbShell'  # 待实现

    # 滑动
    SWIPEUP = 'swipeUp'
    SWIPEDOWN = 'swipeDown'
    SWIPELEFT = 'swipeLeft'
    SWIPERIGHT = 'swipeRight'
    SWIPE = 'swipe'

    # 元素操作
    RECT = 'rect'  # 待实现
    GETTEXT = 'getText'
    CLICK = 'click'
    CHECKT = 'check'
    INPUT = 'input'

    # 逻辑判断
    IF = 'if'
    ELIF = 'elif'
    ELSE = 'else'
    IFCHECK = 'ifcheck'
    ELIFCHECK = 'elifcheck'
    IFIOS = 'ifiOS'
    IFANDROID = 'ifAndroid'

    # 等待
    SLEEP = 'sleep'

    # 断言
    ASSERT = 'assert'

    # 循环
    WHILE = 'while'

    BREAK = 'break'

    SETGV = 'setGV'

class ActionExecutor(object):

    @keywords
    def __action_start_app(self, step):
        """
        行为执行：start_app
        :param step:
        :return:
        """
        if step.activity:
            DriverBase.startApp(step.activity)
        else:
            DriverBase.startApp(Var.activity)

    @keywords
    def __action_stop_app(self, step):
        """
        行为执行：stop_app
        :param step:
        :return:
        """
        if step.package:
            DriverBase.stopApp(step.package)
        else:
            DriverBase.stopApp(Var.package)

    @keywords
    def __action_adb(self, step):
        """
        行为执行：adb
        :param step:
        :return:
        """
        DriverBase.adb(step.cmd)

    @keywords
    def __action_goback(self, step):
        """
        行为执行：goback
        :param step:
        :return:
        """
        DriverBase.adb(step.cmd)

    @keywords
    def __action_tap(self, step):
        """
        行为执行：tap
        :param step:
        :return:
        """
        DriverBase.tap(int(step.location.x), int(step.location.y))

    @keywords
    def __action_doubleTap(self, step):
        """
        行为执行：doubleTap
        :param step:
        :return:
        """
        DriverBase.doubleTap(int(step.location.x), int(step.location.y))

    @keywords
    def __action_press(self, step):
        """
        行为执行：press
        :param step:
        :return:
        """
        DriverBase.press(int(step.location.x), int(step.location.y), int(step.duration))

    @keywords
    def __action_pinch_open(self, step):
        """
        行为执行：pinch_open
        :param step:
        :return:
        """

    @keywords
    def __action_pinch_close(self, step):
        """
        行为执行：pinch_close
        :param step:
        :return:
        """

    @keywords
    def __action_rotate(self, step):
        """
        行为执行：rotate
        :param step:
        :return:
        """

    @keywords
    def __action_drag(self, step):
        """
        行为执行：drag
        :param step:
        :return:
        """

    @keywords
    def __action_swipe_up(self, step):
        """
        行为执行：swipe_up
        :param step:
        :return:
        """
        DriverBase.swipe_up(int(step.during))

    @keywords
    def __action_swipe_down(self, step):
        """
        行为执行：swipe_down
        :param step:
        :return:
        """
        DriverBase.swipe_down(int(step.during))

    @keywords
    def __action_swipe_left(self, step):
        """
        行为执行：swipe_left
        :param step:
        :return:
        """
        DriverBase.swipe_left(int(step.during))

    @keywords
    def __action_swipe_right(self, step):
        """
        行为执行：swipe_right
        :param step:
        :return:
        """
        DriverBase.swipe_right(int(step.during))

    @keywords
    def __action_swipe(self, step):
        """
        行为执行：swipe
        :param step:
        :return:
        """
        fromx = step.location.fromx
        fromy = step.location.fromy
        tox = step.location.tox
        toy = step.location.toy
        DriverBase.swipe(int(fromx), int(fromy), int(tox), int(toy), int(step.during))

    @keywords
    def __action_rect(self, step):
        """
        行为执行：rect
        :param step:
        :return:
        """
        rect = DriverBase.rect(element=step.element, timeout=Var.timeout, interval=Var.interval, index=step.index)
        return rect

    def _action_getText(self, step):
        """
        行为执行：getText
        :param step:
        :return:
        """
        text = DriverBase.text(element=step.element, timeout=Var.timeout, interval=Var.interval, index=step.index)
        return text

    @keywords
    def __action_click(self, step):
        """
        行为执行：click
        :param step:
        :return:
        """
        img_info = self.ocr_analysis(step.action, step.element, True)
        if not isinstance(img_info, bool):
            Var.ocrimg = img_info['ocrimg']
            x = img_info['x']
            y = img_info['y']
            DriverBase.tap(x, y)
        else:
            DriverBase.click(element=step.element, timeout=Var.timeout, interval=Var.interval, index=step.index)

    @keywords
    def __action_check(self, step):
        """
        行为执行：check
        :param step:
        :return:
        """
        img_info = self.ocr_analysis(step.action, step.element, False)
        if not isinstance(img_info, bool):
            if img_info is not None:
                Var.ocrimg = img_info['ocrimg']
                check = True
            else:
                check = False
        else:
            check = DriverBase.check(element=step.element, timeout=Var.timeout, interval=Var.interval, index=step.index)
        if not check:
            raise Exception("Can't find element {}".format(step.element))
        return check

    @keywords
    def __action_input(self, step):
        """
        行为执行：input
        :param step:
        :return:
        """
        DriverBase.input(element=step.element, text=step.content, timeout=Var.timeout, interval=Var.interval,
                         index=step.index)

    @keywords
    def __action_call(self, step):
        """
        行为执行：call
        :param step:
        :return:
        """
        if step.type == 'Scripts':
            try:
                return eval(step.func)
            except Exception as e:
                raise e
        elif step.type == 'Common':
            from oktest.runner.case_analysis import CaseAnalysis
            case = CaseAnalysis()
            case.iteration(Var.common_func[step.func].steps)
            Var.common_var = {}

    @keywords
    def __action_var(self, step):
        """
        行为执行：赋值
        :param step:
        :return:
        """

    @keywords
    def __action_ifcheck(self, step):
        """
        行为执行：ifcheck
        :param step:
        :return:
        """
        img_info = self.ocr_analysis(step.action, step.element, False)
        if not isinstance(img_info, bool):
            if img_info is not None:
                Var.ocrimg = img_info['ocrimg']
                check = True
            else:
                check = False
        else:
            check = DriverBase.check(element=step.element, timeout=Var.timeout, interval=Var.interval, index=step.index)
        return check

    @keywords
    def __action_elifcheck(self, step):
        """
        行为执行：elifcheck
        :param step:
        :return:
        """
        img_info = self.ocr_analysis(step.action, step.element, False)
        if not isinstance(img_info, bool):
            if img_info is not None:
                Var.ocrimg = img_info['ocrimg']
                check = True
            else:
                check = False
        else:
            check = DriverBase.check(element=step.element, timeout=Var.timeout, interval=Var.interval, index=step.index)
        return check

    @keywords
    def __action_if(self, step):
        """
        行为执行：if
        :param step:
        :return:
        """
        try:
            object_if = eval(step.content)
            if not object_if:
                object_if = False
        except Exception as e:
            raise e
        return object_if

    @keywords
    def __action_elif(self, step):
        """
        行为执行：elif
        :param step:
        :return:
        """
        try:
            object_else = eval(step.content)
            if not object_else:
                object_else = False
        except Exception as e:
            raise e
        return object_else

    @keywords
    def __action_ifiOS(self, step):
        """
        行为执行：ifiOS
        :param step:
        :return:
        """
        if Var.platformName.lower() == 'ios':
            return True
        return False

    @keywords
    def __action_ifAndroid(self, step):
        """
        行为执行：ifAndroid
        :param step:
        :return:
        """
        if Var.platformName.lower() == 'android':
            return True
        return False

    @keywords
    def __action_else(self, step):
        """
        行为执行：else
        :param step:
        :return:
        """
        return True

    @keywords
    def __action_sleep(self, step):
        """
        行为执行
        :param step:
        :return:
        """
        time.sleep(int(step.duration))

    @keywords
    def __action_assert(self, step):
        """
        行为解析：Assert
        :param step:
        :return:
        """
        try:
            assert eval(step.content)
        except AssertionError as e:
            raise AssertionError(step.originStep)
        except Exception as e:
            raise e

    @keywords
    def __action_while(self, step):
        """
        行为解析：while
        :param step:
        :return:
        """
        try:
            object_else = eval(step.content)
            if not object_else:
                object_else = False
        except Exception as e:
            raise e
        return object_else

    @keywords
    def __action_setGV(self, step):
        """
        设置全局变量
        :param step:
        :return:
        """
        return True

    @keywords
    def __action_break(self, step):
        """
        :param step:
        :return:
        """
        return True

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
        if step.action == Action.STARTAPP:
            action = self.__action_start_app(step)
        elif step.action == Action.STOPAPP:
            action = self.__action_stop_app(step)
        elif step.action == Action.ADB:
            action = self.__action_adb(step)
        elif step.action == Action.GOBACK:
            action = self.__action_goback(step)
        elif step.action == Action.TAP:
            action = self.__action_tap(step)
        elif step.action == Action.DOUBLETAP:
            action = self.__action_doubleTap(step)
        elif step.action == Action.PRESS:
            action = self.__action_press(step)
        elif step.action == Action.PINCHOPEN:
            action = self.__action_pinch_open(step)
        elif step.action == Action.PINCHCLOSE:
            action = self.__action_pinch_close(step)
        elif step.action == Action.ROTATE:
            action = self.__action_rotate(step)
        elif step.action == Action.DRAG:
            action = self.__action_drag(step)
        elif step.action == Action.SWIPEUP:
            action = self.__action_swipe_up(step)
        elif step.action == Action.SWIPEDOWN:
            action = self.__action_swipe_down(step)
        elif step.action == Action.SWIPELEFT:
            action = self.__action_swipe_left(step)
        elif step.action == Action.SWIPERIGHT:
            action = self.__action_swipe_right(step)
        elif step.action == Action.SWIPE:
            action = self.__action_swipe(step)
        elif step.action == Action.RECT:
            action = self.__action_rect(step)
        elif step.action == Action.CLICK:
            action = self.__action_click(step)
        elif step.action == Action.CHECKT:
            action = self.__action_check(step)
        elif step.action == Action.INPUT:
            action = self.__action_input(step)
        elif step.action == Action.CALL:
            action = self.__action_call(step)
        elif step.action == Action.VARIABLES:
            action = self.__action_var(step)
        elif step.action == Action.IFCHECK:
            action = self.__action_ifcheck(step)
        elif step.action == Action.ELIFCHECK:
            action = self.__action_elifcheck(step)
        elif step.action == Action.IFIOS:
            action = self.__action_ifiOS(step)
        elif step.action == Action.IFANDROID:
            action = self.__action_ifAndroid(step)
        elif step.action == Action.IF:
            action = self.__action_if(step)
        elif step.action == Action.ELIF:
            action = self.__action_elif(step)
        elif step.action == Action.ELSE:
            action = self.__action_else(step)
        elif step.action == Action.SLEEP:
            action = self.__action_sleep(step)
        elif step.action == Action.ASSERT:
            action = self.__action_assert(step)
        elif step.action == Action.WHILE:
            action = self.__action_while(step)
        elif step.action == Action.BREAK:
            action = self.__action_break(step)
        elif step.action == Action.SETGV:
            action = self.__action_setGV(step)
        else:
            raise SyntaxError(step)
        return action