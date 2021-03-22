#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
import time
import datetime
from collections import Iterable
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import JavascriptException
from fasttest.common import Var, log_info, log_error
from fasttest.common.check import check
from fasttest.drivers.driver_base_web import DriverBaseWeb
from fasttest.utils.opcv_utils import OpencvUtils


class ActionExecutorWeb(object):

    def __from_scripts_file(self):

        file_list = []
        try:
            for rt, dirs, files in os.walk(os.path.join(Var.ROOT, "Scripts")):
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

    def __get_element_info(self, action, index=0, is_return=False):
        '''
        :param action:
        :return:
        '''
        parms = action.parms
        if len(parms) <= index or not len(parms):
            raise TypeError('missing {} required positional argument'.format(index + 1))
        if isinstance(parms[index], WebElement):
            element = parms[index]
        elif isinstance(parms[index], str):
            if not re.match(r'^(id|name|class|tag_name|link_text|partial_link_text|xpath|css_selector)\s*=.+', parms[index].strip(), re.I):
                raise TypeError('input parameter format error:{}'.format(parms[index]))
            key = parms[index].split('=', 1)[0].strip()
            value = parms[index].split('=', 1)[-1].strip()
            element = DriverBaseWeb.get_element(key, value, Var.time_out)
        else:
            raise TypeError('the parms type must be: WebElement or str')

        if not element and not is_return:
            raise Exception("Can't find element: {}".format(parms[index]))
        return element


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

    def __action_open_url(self, action):
        """
        openUrl
        :param action:
        :return:
        """
        url = self.__get_value(action)
        DriverBaseWeb.open_url(url)

    def __action_close(self, action):
        """
        close
        :param action:
        :return:
        """
        DriverBaseWeb.close()

    def __action_quit(self, action):
        """
        行为执行：quit
        :param action:
        :return:
        """
        DriverBaseWeb.quit()

    def __action_back(self, action):
        '''
        back
        :param action:
        :return:
        '''
        DriverBaseWeb.back()

    def __action_forward(self, action):
        '''
        forward
        :param action:
        :return:
        '''
        DriverBaseWeb.forward()

    def __action_refresh(self, action):
        '''
        refresh
        :param action:
        :return:
        '''
        DriverBaseWeb.refresh()

    def __action_set_timeout(self, action):
        """
        行为执行：setTimeout
        :param action:
        :return:
        """
        time = self.__get_value(action)
        Var.time_out = int(time)

    def __action_maximize_window(self, action):
        '''
        maxWindow
        :return:
        '''
        DriverBaseWeb.maximize_window()

    def __action_minimize_window(self, action):
        '''
        minWindow
        :return:
        '''
        DriverBaseWeb.minimize_window()

    def __action_fullscreen_window(self, action):
        '''
        fullscreenWindow
        :return:
        '''
        DriverBaseWeb.fullscreen_window()

    def __action_delete_all_cookies(self, action):
        '''
        deleteAllCookies
        :return:
        '''
        DriverBaseWeb.delete_all_cookies()

    def __action_delete_cookie(self, action):
        '''
        deleteCookie
        :return:
        '''
        key = self.__get_value(action)
        DriverBaseWeb.delete_cookie(key)

    def __action_add_cookie(self, action):
        '''
        addCookie
        :return:
        '''
        key = self.__get_value(action)
        DriverBaseWeb.add_cookie(key)

    @check
    def __action_clear(self, action):
        '''
        clear
        :return:
        '''
        element = self.__get_element_info(action)
        DriverBaseWeb.clear(element)

    @check
    def __action_submit(self, action):
        '''
        submit
        :param action:
        :return:
        '''
        element = self.__get_element_info(action)
        DriverBaseWeb.submit(element)

    @check
    def __action_click(self, action):
        '''
        click
        :param action:
        :return:
        '''
        element = self.__get_element_info(action)
        DriverBaseWeb.click(element)

    @check
    def __action_context_click(self, action):
        '''
        contextClick
        :param action:
        :return:
        '''
        element = self.__get_element_info(action)
        DriverBaseWeb.context_click(element)

    @check
    def __action_double_click(self, action):
        '''
        doubleClick
        :param action:
        :return:
        '''
        element = self.__get_element_info(action)
        DriverBaseWeb.double_click(element)

    @check
    def __action_click_and_hold(self, action):
        '''
        holdClick
        :param action:
        :return:
        '''
        element = self.__get_element_info(action)
        DriverBaseWeb.click_and_hold(element)

    @check
    def __action_drag_and_drop(self, action):
        '''
        dragDrop
        :param action:
        :return:
        '''
        element = self.__get_element_info(action, 0)
        target = self.__get_element_info(action, 1)
        DriverBaseWeb.drag_and_drop(element, target)

    @check
    def __action_drag_and_drop_by_offset(self, action):
        '''
        dragDropByOffset
        :param action:
        :return:
        '''
        element = self.__get_element_info(action)
        xoffset = self.__get_value(action, 1)
        yoffset = self.__get_value(action, 2)
        DriverBaseWeb.drag_and_drop_by_offse(element, float(xoffset), float(yoffset))

    def __action_move_by_offset(self, action):
        '''
        moveByOffset
        :param action:
        :return:
        '''
        xoffset = self.__get_value(action, 0)
        yoffset = self.__get_value(action, 1)
        DriverBaseWeb.move_by_offset(float(xoffset), float(yoffset))

    @check
    def __action_move_to_element(self, action):
        '''
        moveToElement
        :param action:
        :return:
        '''
        element = self.__get_element_info(action)
        DriverBaseWeb.move_to_element(element)

    @check
    def __action_move_to_element_with_offset(self, action):
        '''
        moveToElementWithOffset
        :param action:
        :return:
        '''
        element = self.__get_element_info(action)
        xoffset = self.__get_value(action, 1)
        yoffset = self.__get_value(action, 2)
        DriverBaseWeb.move_to_element_with_offset(element, float(xoffset), float(yoffset))

    def __action_switch_to_frame(self, action):
        '''
        switchToFrame
        :param action:
        :return:
        '''
        frame_reference = self.__get_value(action)
        DriverBaseWeb.switch_to_frame(frame_reference)

    def __action_switch_to_default_content(self, action):
        '''
        switchToDefaultContent
        :param action:
        :return:
        '''
        DriverBaseWeb.switch_to_default_content()

    def __action_switch_to_parent_frame(self, action):
        '''
        switchToParentFrame
        :param action:
        :return:
        '''
        DriverBaseWeb.switch_to_parent_frame()

    def __action_switch_to_window(self, action):
        '''
        switchToWindow
        :param action:
        :return:
        '''
        handle = self.__get_value(action)
        DriverBaseWeb.switch_to_window(handle)

    @check
    def __action_send_keys(self, action):
        '''
        sendKeys
        :param action:
        :return:
        '''
        element = self.__get_element_info(action)
        text_list = []
        if len(action.parms) == 2:
            text_list.append(self.__get_value(action, 1))
        elif len(action.parms) == 3:
            text_list.append(self.__get_value(action, 1))
            text_list.append(self.__get_value(action, 2))
        else:
            raise TypeError('missing 1 required positional argument')
        DriverBaseWeb.send_keys(element, text_list)

    @check
    def __action_check(self, action):
        '''
        check
        :param action:
        :return:
        '''
        self.__get_element_info(action)

    def __action_query_displayed(self, action):
        '''
        queryDisplayed
        :param action:
        :return:
        '''
        parms = self.__get_value(action)
        if isinstance(parms, WebElement):
            element = parms
            DriverBaseWeb.query_displayed(element=element, timeout=Var.time_out)
        elif isinstance(parms, str):
            if not re.match(r'^(id|name|class|tag_name|link_text|partial_link_text|xpath|css_selector)\s*=.+',
                            parms.strip(), re.I):
                raise TypeError('input parameter format error:{}'.format(parms))
            key = parms.split('=', 1)[0].strip()
            value = parms.split('=', 1)[-1].strip()
            DriverBaseWeb.query_displayed(type=key, text=value, timeout=Var.time_out)
        else:
            raise TypeError('the parms type must be: WebElement or str')

    def __action_query_not_displayed(self, action):
        '''
        queryNotDisplayed
        :param action:
        :return:
        '''
        parms = self.__get_value(action)
        if isinstance(parms, WebElement):
            element = parms
            DriverBaseWeb.query_not_displayed(element=element, timeout=Var.time_out)
        elif isinstance(parms, str):
            if not re.match(r'^(id|name|class|tag_name|link_text|partial_link_text|xpath|css_selector)\s*=.+',
                            parms.strip(), re.I):
                raise TypeError('input parameter format error:{}'.format(parms))
            key = parms.split('=', 1)[0].strip()
            value = parms.split('=', 1)[-1].strip()
            DriverBaseWeb.query_not_displayed(type=key, text=value, timeout=Var.time_out)
        else:
            raise TypeError('the parms type must be: WebElement or str')

    @check
    def __action_save_screenshot(self, action):
        '''
        saveScreenshot
        :param action:
        :return:
        '''
        if len(action.parms) == 1:
            element = None
            name = self.__get_value(action)
        else:
            element = self.__get_element_info(action)
            name = self.__get_value(action, 1)
        return DriverBaseWeb.save_screenshot(element, name)

    @check
    def __action_is_selected(self, action):
        '''
        isSelected
        :param action:
        :return:
        '''
        element = self.__get_element_info(action)
        return DriverBaseWeb.is_selected(element)

    @check
    def __action_is_displayed(self, action):
        '''
        isDisplayed
        :param action:
        :return:
        '''
        element = self.__get_element_info(action)
        return DriverBaseWeb.is_displayed(element)

    @check
    def __action_is_enabled(self, action):
        '''
        isEnabled
        :param action:
        :return:
        '''
        element = self.__get_element_info(action)
        return DriverBaseWeb.is_enabled(element)

    @check
    def __action_get_size(self, action):
        '''
        getSize
        :param action:
        :return:
        '''
        element = self.__get_element_info(action)
        return DriverBaseWeb.get_size(element)

    @check
    def __action_get_attribute(self, action):
        '''
        getAttribute
        :param action:
        :return:
        '''
        element = self.__get_element_info(action)
        attribute = self.__get_value(action, 1)
        return DriverBaseWeb.get_attribute(element, attribute)

    @check
    def __action_get_text(self, action):
        '''
        getText
        :param action:
        :return:
        '''
        element = self.__get_element_info(action)
        return DriverBaseWeb.get_text(element)

    @check
    def __action_get_tag_name(self, action):
        '''
        getTagName
        :param action:
        :return:
        '''
        element = self.__get_element_info(action)
        return DriverBaseWeb.get_tag_name(element)

    @check
    def __action_get_css_property(self, action):
        '''
        getCssProperty
        :param action:
        :return:
        '''
        element = self.__get_element_info(action)
        css_value = self.__get_value(action, 1)
        return DriverBaseWeb.get_css_property(element, css_value)

    @check
    def __action_get_location(self, action):
        '''
        getLocation
        :param action:
        :return:
        '''
        element = self.__get_element_info(action)
        return DriverBaseWeb.get_location(element)

    @check
    def __action_get_rect(self, action):
        '''
        getRect
        :param action:
        :return:
        '''
        element = self.__get_element_info(action)
        return DriverBaseWeb.get_rect(element)

    def __action_get_name(self, action):
        '''
        getName
        :param :
        :return:
        '''
        return DriverBaseWeb.get_name()

    def __action_get_title(self, action):
        '''
        getTitle
        :param action:
        :return:
        '''
        return DriverBaseWeb.get_title()

    def __action_get_current_url(self, action):
        '''
        getTitle
        :param :
        :return:
        '''
        return DriverBaseWeb.get_current_url()

    def __action_get_current_window_handle(self, action):
        '''
        getCurrentWindowHandle
        :param :
        :return:
        '''
        return DriverBaseWeb.get_current_window_handle()

    def __action_get_window_handles(self, action):
        '''
        getWindowHandles
        :param :
        :return:
        '''
        return DriverBaseWeb.get_window_handles()

    def __action_get_cookies(self, action):
        '''
        getCookies
        :param :
        :return:
        '''
        return DriverBaseWeb.get_cookies()

    def __action_get_cookie(self, action):
        '''
        getCookie
        :param :
        :return:
        '''
        key = self.__get_value(action)
        return DriverBaseWeb.get_cookie(key)

    def __action_get_window_position(self, action):
        '''
        getWindowPosition
        :param :
        :return:
        '''
        return DriverBaseWeb.get_window_position()

    def __action_set_window_position(self, action):
        '''
        setWindowPosition
        :param :
        :return:
        '''
        x = self.__get_value(action)
        y = self.__get_value(action, 1)
        DriverBaseWeb.set_window_position(float(x), float(y))

    def __action_execute_script(self, action):
        '''
        executeScript
        :param :
        :return:
        '''
        timeout = Var.time_out
        if not timeout:
            timeout = 10
        endTime = datetime.datetime.now() + datetime.timedelta(seconds=int(timeout))
        while True:
            try:
                js_value = self.__get_value(action)
                return DriverBaseWeb.execute_script(js_value)
            except JavascriptException as e:
                if datetime.datetime.now() >= endTime:
                    raise e
                time.sleep(1)
            except Exception as e:
                raise e

    def __action_match_image(self, action):
        '''
        matchImage
        :param :
        :return:
        '''
        base_image = self.__get_value(action)
        match_image = self.__get_value(action,1)
        if not os.path.isfile(match_image):
            raise FileNotFoundError("No such file: {}".format(match_image))
        if not os.path.isfile(base_image):
            raise FileNotFoundError("No such file: {}".format(base_image))
        orc_img = OpencvUtils(base_image, match_image)
        img_info = orc_img.extract_minutiae()
        if img_info:
            Var.ocrimg = img_info['ocrimg']
        else:
            raise Exception("Can't find image {}".format(match_image))

    def __action_get_window_size(self, action):
        '''
        getWindowSize
        :param :
        :return:
        '''
        return DriverBaseWeb.get_window_size()

    def __action_set_window_size(self, action):
        '''
        setWindowSize
        :param :
        :return:
        '''
        width = self.__get_value(action)
        height = self.__get_value(action)
        DriverBaseWeb.set_window_size(float(width), float(height))

    def __action_get_elements(self, action):
        '''
        :param action:
        :return:
        '''
        parms = action.parms
        step = action.step
        if not len(parms):
            raise TypeError('missing 1 required positional argument')
        if not re.match(r'^(id|name|class|tag_name|link_text|partial_link_text|xpath|css_selector)\s*=.+',
                        parms[0].strip(), re.I):
            raise TypeError('input parameter format error:{}'.format(parms[0]))
        key = parms[0].strip().split('=', 1)[0]
        value = parms[0].strip().split('=', 1)[-1]
        elements = DriverBaseWeb.get_elements(key, value, Var.time_out)
        if not elements:
            raise Exception("Can't find elements: {}".format(parms[0]))
        return elements

    @check
    def __action_ifcheck(self, action):
        """
        行为执行：ifcheck
        :param action:
        :return:
        """
        element = self.__get_element_info(action, is_return=True)
        if not element:
            return False
        return True

    def __action_len(self, action):
        """
        len
        :param action:
        :return:
        """
        value = self.__get_value(action)
        if value:
            return len(value)
        return 0

    def __action_sleep(self, action):
        """
        行为执行
        :param action:
        :return:
        """
        sleep = self.__get_value(action)
        time.sleep(float(sleep))

    def __action_getVar(self, action):
        '''
        :return:
        '''
        if action.key == '$.isSelected':
            result = self.__action_is_selected(action)
        elif action.key == '$.isDisplayed':
            result = self.__action_is_displayed(action)
        elif action.key == '$.isEnabled':
            result = self.__action_is_enabled(action)
        elif action.key == '$.saveScreenshot':
            result = self.__action_save_screenshot(action)
        elif action.key == '$.executeScript':
            result = self.__action_execute_script(action)
        elif action.key == '$.getText':
            result = self.__action_get_text(action)
        elif action.key == '$.getSize':
            result = self.__action_get_size(action)
        elif action.key == '$.getAttribute':
            result = self.__action_get_attribute(action)
        elif action.key == '$.getText':
            result = self.__action_get_text(action)
        elif action.key == '$.getTagName':
            result = self.__action_get_tag_name(action)
        elif action.key == '$.getCssProperty':
            result = self.__action_get_css_property(action)
        elif action.key == '$.getLocation':
            result = self.__action_get_location(action)
        elif action.key == '$.getRect':
            result = self.__action_get_rect(action)
        elif action.key == '$.getName':
            result = self.__action_get_name(action)
        elif action.key == '$.getTitle':
            result = self.__action_get_title(action)
        elif action.key == '$.getCurrentUrl':
            result = self.__action_get_current_url(action)
        elif action.key == '$.getCurrentWindowHandle':
            result = self.__action_get_current_window_handle(action)
        elif action.key == '$.getWindowHandles':
            result = self.__action_get_window_handles(action)
        elif action.key == '$.getCookies':
            result = self.__action_get_cookies(action)
        elif action.key == '$.getCookie':
            result = self.__action_get_cookie(action)
        elif action.key == '$.getWindowPosition':
            result = self.__action_get_window_position(action)
        elif action.key == '$.getWindowSize':
            result = self.__action_get_window_size(action)
        elif action.key == '$.getElement':
            result = self.__get_element_info(action)
        elif action.key == '$.getElements':
            result = self.__action_get_elements(action)
        elif action.key == '$.id':
            action.parms = action.parms.replace('\n', '')
            result = eval(action.parms)
        elif action.key == '$.getLen':
            result = self.__action_len(action)
        elif action.key == '$.getVar':
            if Var.global_var:
                if action.parms[0] in Var.global_var:
                    result = Var.global_var[action.parms[0]]
                else:
                    result = None
            else:
                result = None
        elif action.key:
            # 调用脚本
            result = self.new_action_executor(action, False)
        else:
           result = action.parms[0]

        self.__out_result(action.name, result)
        return result

    def __action_set_var(self, action):
        '''
        setVar
        :return:
        '''
        key = self.__get_value(action, 0)
        values = self.__get_value(action, 1)
        Var.global_var[key] = values

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
            result = self.__action_set_var(action)

        elif action.key == 'openUrl':
            result = self.__action_open_url(action)

        elif action.key == 'close':
            result = self.__action_close(action)

        elif action.key == 'quit':
            result = self.__action_quit(action)

        elif action.key == 'setTimeout':
            result = self.__action_set_timeout(action)

        elif action.key == 'back':
            result = self.__action_back(action)

        elif action.key == 'forward':
            result = self.__action_forward(action)

        elif action.key == 'refresh':
            result = self.__action_refresh(action)

        elif action.key == 'maxWindow':
            result = self.__action_maximize_window(action)

        elif action.key == 'minWindow':
            result = self.__action_minimize_window(action)

        elif action.key == 'fullscreenWindow':
            result = self.__action_fullscreen_window(action)

        elif action.key == 'deleteAllCookies':
            result = self.__action_delete_all_cookies(action)

        elif action.key == 'deleteCookie':
            result = self.__action_delete_cookie(action)

        elif action.key == 'addCookie':
            result = self.__action_add_cookie(action)

        elif action.key == 'clear':
            result = self.__action_clear(action)

        elif action.key == 'submit':
            result = self.__action_submit(action)

        elif action.key == 'click':
            result = self.__action_click(action)

        elif action.key == 'contextClick':
            result = self.__action_context_click(action)

        elif action.key == 'doubleClick':
            result = self.__action_double_click(action)

        elif action.key == 'holdClick':
            result = self.__action_click_and_hold(action)

        elif action.key == 'dragDrop':
            result = self.__action_drag_and_drop(action)

        elif action.key == 'dragDropByOffset':
            result = self.__action_drag_and_drop_by_offset(action)

        elif action.key == 'moveByOffset':
            result = self.__action_move_by_offset(action)

        elif action.key == 'moveToElement':
            result = self.__action_move_to_element(action)

        elif action.key == 'moveToElementWithOffset':
            result = self.__action_move_to_element_with_offset(action)

        elif action.key == 'switchToFrame':
            result = self.__action_switch_to_frame(action)

        elif action.key == 'switchToDefaultContent':
            result = self.__action_switch_to_default_content(action)

        elif action.key == 'switchToParentFrame':
            result = self.__action_switch_to_parent_frame(action)

        elif action.key == 'switchToWindow':
            result = self.__action_switch_to_window(action)

        elif action.key == 'setWindowSize':
            result = self.__action_set_window_size(action)

        elif action.key == 'setWindowPosition':
            result = self.__action_set_window_position(action)

        elif action.key == 'executeScript':
            result = self.__action_execute_script(action)

        elif action.key == 'matchImage':
            result = self.__action_match_image(action)

        elif action.key == 'sendKeys':
            result = self.__action_send_keys(action)

        elif action.key == 'check':
            result = self.__action_check(action)

        elif action.key == 'queryDisplayed':
            result = self.__action_query_displayed(action)

        elif action.key == 'queryNotDisplayed':
            result = self.__action_query_not_displayed(action)

        elif action.key == 'sleep':
            result = self.__action_sleep(action)

        elif action.key == 'ifcheck':
            result = self.__action_ifcheck(action)

        elif action.key == 'elifcheck':
            result = self.__action_ifcheck(action)

        elif action.key == 'break':
            result = True

        elif action.key == 'else':
            result = True

        else:
            raise KeyError('The {} keyword is undefined!'.format(action.key))

        return result