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

    def _get_element_info(self, action, index=0, is_return=False):
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

    def _action_open_url(self, action):
        """
        openUrl
        :param action:
        :return:
        """
        url = self._get_value(action)
        DriverBaseWeb.open_url(url)

    def _action_close(self, action):
        """
        close
        :param action:
        :return:
        """
        DriverBaseWeb.close()

    def _action_quit(self, action):
        """
        行为执行：quit
        :param action:
        :return:
        """
        DriverBaseWeb.quit()

    def _action_back(self, action):
        '''
        back
        :param action:
        :return:
        '''
        DriverBaseWeb.back()

    def _action_forward(self, action):
        '''
        forward
        :param action:
        :return:
        '''
        DriverBaseWeb.forward()

    def _action_refresh(self, action):
        '''
        refresh
        :param action:
        :return:
        '''
        DriverBaseWeb.refresh()

    def _action_set_timeout(self, action):
        """
        行为执行：setTimeout
        :param action:
        :return:
        """
        time = self._get_value(action)
        Var.time_out = int(time)

    def _action_maximize_window(self, action):
        '''
        maxWindow
        :return:
        '''
        DriverBaseWeb.maximize_window()

    def _action_minimize_window(self, action):
        '''
        minWindow
        :return:
        '''
        DriverBaseWeb.minimize_window()

    def _action_fullscreen_window(self, action):
        '''
        fullscreenWindow
        :return:
        '''
        DriverBaseWeb.fullscreen_window()

    def _action_delete_all_cookies(self, action):
        '''
        deleteAllCookies
        :return:
        '''
        DriverBaseWeb.delete_all_cookies()

    def _action_delete_cookie(self, action):
        '''
        deleteCookie
        :return:
        '''
        key = self._get_value(action)
        DriverBaseWeb.delete_cookie(key)

    def _action_add_cookie(self, action):
        '''
        addCookie
        :return:
        '''
        key = self._get_value(action)
        DriverBaseWeb.add_cookie(key)

    @check
    def _action_clear(self, action):
        '''
        clear
        :return:
        '''
        element = self._get_element_info(action)
        DriverBaseWeb.clear(element)

    @check
    def _action_submit(self, action):
        '''
        submit
        :param action:
        :return:
        '''
        element = self._get_element_info(action)
        DriverBaseWeb.submit(element)

    @check
    def _action_click(self, action):
        '''
        click
        :param action:
        :return:
        '''
        element = self._get_element_info(action)
        DriverBaseWeb.click(element)

    @check
    def _action_context_click(self, action):
        '''
        contextClick
        :param action:
        :return:
        '''
        element = self._get_element_info(action)
        DriverBaseWeb.context_click(element)

    @check
    def _action_double_click(self, action):
        '''
        doubleClick
        :param action:
        :return:
        '''
        element = self._get_element_info(action)
        DriverBaseWeb.double_click(element)

    @check
    def _action_click_and_hold(self, action):
        '''
        holdClick
        :param action:
        :return:
        '''
        element = self._get_element_info(action)
        DriverBaseWeb.click_and_hold(element)

    @check
    def _action_drag_and_drop(self, action):
        '''
        dragDrop
        :param action:
        :return:
        '''
        element = self._get_element_info(action, 0)
        target = self._get_element_info(action, 1)
        DriverBaseWeb.drag_and_drop(element, target)

    @check
    def _action_drag_and_drop_by_offset(self, action):
        '''
        dragDropByOffset
        :param action:
        :return:
        '''
        element = self._get_element_info(action)
        xoffset = self._get_value(action, 1)
        yoffset = self._get_value(action, 2)
        DriverBaseWeb.drag_and_drop_by_offse(element, float(xoffset), float(yoffset))

    def _action_move_by_offset(self, action):
        '''
        moveByOffset
        :param action:
        :return:
        '''
        xoffset = self._get_value(action, 0)
        yoffset = self._get_value(action, 1)
        DriverBaseWeb.move_by_offset(float(xoffset), float(yoffset))

    @check
    def _action_move_to_element(self, action):
        '''
        moveToElement
        :param action:
        :return:
        '''
        element = self._get_element_info(action)
        DriverBaseWeb.move_to_element(element)

    @check
    def _action_move_to_element_with_offset(self, action):
        '''
        moveToElementWithOffset
        :param action:
        :return:
        '''
        element = self._get_element_info(action)
        xoffset = self._get_value(action, 1)
        yoffset = self._get_value(action, 2)
        DriverBaseWeb.move_to_element_with_offset(element, float(xoffset), float(yoffset))

    def _action_switch_to_frame(self, action):
        '''
        switchToFrame
        :param action:
        :return:
        '''
        frame_reference = self._get_value(action)
        DriverBaseWeb.switch_to_frame(frame_reference)

    def _action_switch_to_default_content(self, action):
        '''
        switchToDefaultContent
        :param action:
        :return:
        '''
        DriverBaseWeb.switch_to_default_content()

    def _action_switch_to_parent_frame(self, action):
        '''
        switchToParentFrame
        :param action:
        :return:
        '''
        DriverBaseWeb.switch_to_parent_frame()

    def _action_switch_to_window(self, action):
        '''
        switchToWindow
        :param action:
        :return:
        '''
        handle = self._get_value(action)
        DriverBaseWeb.switch_to_window(handle)

    @check
    def _action_send_keys(self, action):
        '''
        sendKeys
        :param action:
        :return:
        '''
        element = self._get_element_info(action)
        text_list = []
        if len(action.parms) == 2:
            text_list.append(self._get_value(action, 1))
        elif len(action.parms) == 3:
            text_list.append(self._get_value(action, 1))
            text_list.append(self._get_value(action, 2))
        else:
            raise TypeError('missing 1 required positional argument')
        DriverBaseWeb.send_keys(element, text_list)

    @check
    def _action_check(self, action):
        '''
        check
        :param action:
        :return:
        '''
        self._get_element_info(action)

    def _action_query_displayed(self, action):
        '''
        queryDisplayed
        :param action:
        :return:
        '''
        parms = self._get_value(action)
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

    def _action_query_not_displayed(self, action):
        '''
        queryNotDisplayed
        :param action:
        :return:
        '''
        parms = self._get_value(action)
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
    def _action_save_screenshot(self, action):
        '''
        saveScreenshot
        :param action:
        :return:
        '''
        if len(action.parms) == 1:
            element = None
            name = self._get_value(action)
        else:
            element = self._get_element_info(action)
            name = self._get_value(action, 1)
        return DriverBaseWeb.save_screenshot(element, name)

    @check
    def _action_is_selected(self, action):
        '''
        isSelected
        :param action:
        :return:
        '''
        element = self._get_element_info(action)
        return DriverBaseWeb.is_selected(element)

    @check
    def _action_is_displayed(self, action):
        '''
        isDisplayed
        :param action:
        :return:
        '''
        element = self._get_element_info(action)
        return DriverBaseWeb.is_displayed(element)

    @check
    def _action_is_enabled(self, action):
        '''
        isEnabled
        :param action:
        :return:
        '''
        element = self._get_element_info(action)
        return DriverBaseWeb.is_enabled(element)

    @check
    def _action_get_size(self, action):
        '''
        getSize
        :param action:
        :return:
        '''
        element = self._get_element_info(action)
        return DriverBaseWeb.get_size(element)

    @check
    def _action_get_attribute(self, action):
        '''
        getAttribute
        :param action:
        :return:
        '''
        element = self._get_element_info(action)
        attribute = self._get_value(action, 1)
        return DriverBaseWeb.get_attribute(element, attribute)

    @check
    def _action_get_text(self, action):
        '''
        getText
        :param action:
        :return:
        '''
        element = self._get_element_info(action)
        return DriverBaseWeb.get_text(element)

    @check
    def _action_get_tag_name(self, action):
        '''
        getTagName
        :param action:
        :return:
        '''
        element = self._get_element_info(action)
        return DriverBaseWeb.get_tag_name(element)

    @check
    def _action_get_css_property(self, action):
        '''
        getCssProperty
        :param action:
        :return:
        '''
        element = self._get_element_info(action)
        css_value = self._get_value(action, 1)
        return DriverBaseWeb.get_css_property(element, css_value)

    @check
    def _action_get_location(self, action):
        '''
        getLocation
        :param action:
        :return:
        '''
        element = self._get_element_info(action)
        return DriverBaseWeb.get_location(element)

    @check
    def _action_get_rect(self, action):
        '''
        getRect
        :param action:
        :return:
        '''
        element = self._get_element_info(action)
        return DriverBaseWeb.get_rect(element)

    def _action_get_name(self, action):
        '''
        getName
        :param :
        :return:
        '''
        return DriverBaseWeb.get_name()

    def _action_get_title(self, action):
        '''
        getTitle
        :param action:
        :return:
        '''
        return DriverBaseWeb.get_title()

    def _action_get_current_url(self, action):
        '''
        getTitle
        :param :
        :return:
        '''
        return DriverBaseWeb.get_current_url()

    def _action_get_current_window_handle(self, action):
        '''
        getCurrentWindowHandle
        :param :
        :return:
        '''
        return DriverBaseWeb.get_current_window_handle()

    def _action_get_window_handles(self, action):
        '''
        getWindowHandles
        :param :
        :return:
        '''
        return DriverBaseWeb.get_window_handles()

    def _action_get_cookies(self, action):
        '''
        getCookies
        :param :
        :return:
        '''
        return DriverBaseWeb.get_cookies()

    def _action_get_cookie(self, action):
        '''
        getCookie
        :param :
        :return:
        '''
        key = self._get_value(action)
        return DriverBaseWeb.get_cookie(key)

    def _action_get_window_position(self, action):
        '''
        getWindowPosition
        :param :
        :return:
        '''
        return DriverBaseWeb.get_window_position()

    def _action_set_window_position(self, action):
        '''
        setWindowPosition
        :param :
        :return:
        '''
        x = self._get_value(action)
        y = self._get_value(action, 1)
        DriverBaseWeb.set_window_position(float(x), float(y))

    def _action_execute_script(self, action):
        '''
        executeScript
        :param :
        :return:
        '''
        endTime = datetime.datetime.now() + datetime.timedelta(seconds=int(Var.time_out))
        while True:
            try:
                js_value = self._get_value(action)
                return DriverBaseWeb.execute_script(js_value)
            except JavascriptException as e:
                if datetime.datetime.now() >= endTime:
                    raise e
                time.sleep(0.1)
            except Exception as e:
                raise e

    def _action_match_image(self, action):
        '''
        matchImage
        :param :
        :return:
        '''
        base_image = self._get_value(action)
        match_image = self._get_value(action,1)
        if not os.path.isfile(match_image):
            raise FileNotFoundError("No such file: {}".format(match_image))
        if not os.path.isfile(base_image):
            raise FileNotFoundError("No such file: {}".format(base_image))
        height = Var.instance.get_window_size()['height']
        orc_img = OpencvUtils(base_image, match_image, height)
        img_info = orc_img.extract_minutiae()
        if img_info:
            Var.ocrimg = img_info['ocrimg']
        else:
            raise Exception("Can't find image {}".format(match_image))

    def _action_get_window_size(self, action):
        '''
        getWindowSize
        :param :
        :return:
        '''
        return DriverBaseWeb.get_window_size()

    def _action_set_window_size(self, action):
        '''
        setWindowSize
        :param :
        :return:
        '''
        width = self._get_value(action)
        height = self._get_value(action)
        DriverBaseWeb.set_window_size(float(width), float(height))

    def _action_get_elements(self, action):
        '''
        :param action:
        :return:
        '''
        parms = action.parms
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
        parms = action.parms
        if not len(parms):
            raise TypeError('missing 1 required positional argument')
        if not re.match(r'^(id|name|class|tag_name|link_text|partial_link_text|xpath|css_selector)\s*=.+',
                        parms[0].strip(), re.I):
            raise TypeError('input parameter format error:{}'.format(parms[0]))
        key = parms[0].strip().split('=', 1)[0]
        value = parms[0].strip().split('=', 1)[-1]
        elements = DriverBaseWeb.get_elements(key, value, Var.time_out)
        return bool(elements)

    def _action_is_not_exist(self, action):
        '''
        :param action:
        :return:
        '''
        parms = action.parms
        if not len(parms):
            raise TypeError('missing 1 required positional argument')
        if not re.match(r'^(id|name|class|tag_name|link_text|partial_link_text|xpath|css_selector)\s*=.+',
                        parms[0].strip(), re.I):
            raise TypeError('input parameter format error:{}'.format(parms[0]))
        key = parms[0].strip().split('=', 1)[0]
        value = parms[0].strip().split('=', 1)[-1]
        elements = DriverBaseWeb.get_elements(key, value, 0)
        return not bool(elements)

    def _action_sleep(self, action):
        """
        行为执行
        :param action:
        :return:
        """
        sleep = self._get_value(action)
        time.sleep(float(sleep))

    def _action_getVar(self, action):
        '''
        :return:
        '''
        if action.key == '$.isSelected':
            result = self._action_is_selected(action)
        elif action.key == '$.isDisplayed':
            result = self._action_is_displayed(action)
        elif action.key == '$.isEnabled':
            result = self._action_is_enabled(action)
        elif action.key == '$.saveScreenshot':
            result = self._action_save_screenshot(action)
        elif action.key == '$.executeScript':
            result = self._action_execute_script(action)
        elif action.key == '$.getText':
            result = self._action_get_text(action)
        elif action.key == '$.getSize':
            result = self._action_get_size(action)
        elif action.key == '$.getAttribute':
            result = self._action_get_attribute(action)
        elif action.key == '$.getText':
            result = self._action_get_text(action)
        elif action.key == '$.getTagName':
            result = self._action_get_tag_name(action)
        elif action.key == '$.getCssProperty':
            result = self._action_get_css_property(action)
        elif action.key == '$.getLocation':
            result = self._action_get_location(action)
        elif action.key == '$.getRect':
            result = self._action_get_rect(action)
        elif action.key == '$.getName':
            result = self._action_get_name(action)
        elif action.key == '$.getTitle':
            result = self._action_get_title(action)
        elif action.key == '$.getCurrentUrl':
            result = self._action_get_current_url(action)
        elif action.key == '$.getCurrentWindowHandle':
            result = self._action_get_current_window_handle(action)
        elif action.key == '$.getWindowHandles':
            result = self._action_get_window_handles(action)
        elif action.key == '$.getCookies':
            result = self._action_get_cookies(action)
        elif action.key == '$.getCookie':
            result = self._action_get_cookie(action)
        elif action.key == '$.getWindowPosition':
            result = self._action_get_window_position(action)
        elif action.key == '$.getWindowSize':
            result = self._action_get_window_size(action)
        elif action.key == '$.getElement':
            result = self._get_element_info(action)
        elif action.key == '$.getElements':
            result = self._action_get_elements(action)
        elif action.key == '$.id':
            action.parms = action.parms.replace('\n', '')
            result = eval(action.parms)
        elif action.key == '$.getLen':
            result = self._action_get_len(action)
        elif action.key == '$.isExist':
            result = self._action_is_exist(action)
        elif action.key == '$.isNotExist':
            result = self._action_is_not_exist(action)
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

        self._out_result(action.name, result)
        return result

    def _action_set_var(self, action):
        '''
        setVar
        :return:
        '''
        key = self._get_value(action, 0)
        values = self._get_value(action, 1)
        Var.global_var[key] = values

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
            result = self._action_set_var(action)

        elif action.key == 'openUrl':
            result = self._action_open_url(action)

        elif action.key == 'close':
            result = self._action_close(action)

        elif action.key == 'quit':
            result = self._action_quit(action)

        elif action.key == 'setTimeout':
            result = self._action_set_timeout(action)

        elif action.key == 'back':
            result = self._action_back(action)

        elif action.key == 'forward':
            result = self._action_forward(action)

        elif action.key == 'refresh':
            result = self._action_refresh(action)

        elif action.key == 'maxWindow':
            result = self._action_maximize_window(action)

        elif action.key == 'minWindow':
            result = self._action_minimize_window(action)

        elif action.key == 'fullscreenWindow':
            result = self._action_fullscreen_window(action)

        elif action.key == 'deleteAllCookies':
            result = self._action_delete_all_cookies(action)

        elif action.key == 'deleteCookie':
            result = self._action_delete_cookie(action)

        elif action.key == 'addCookie':
            result = self._action_add_cookie(action)

        elif action.key == 'clear':
            result = self._action_clear(action)

        elif action.key == 'submit':
            result = self._action_submit(action)

        elif action.key == 'click':
            result = self._action_click(action)

        elif action.key == 'contextClick':
            result = self._action_context_click(action)

        elif action.key == 'doubleClick':
            result = self._action_double_click(action)

        elif action.key == 'holdClick':
            result = self._action_click_and_hold(action)

        elif action.key == 'dragDrop':
            result = self._action_drag_and_drop(action)

        elif action.key == 'dragDropByOffset':
            result = self._action_drag_and_drop_by_offset(action)

        elif action.key == 'moveByOffset':
            result = self._action_move_by_offset(action)

        elif action.key == 'moveToElement':
            result = self._action_move_to_element(action)

        elif action.key == 'moveToElementWithOffset':
            result = self._action_move_to_element_with_offset(action)

        elif action.key == 'switchToFrame':
            result = self._action_switch_to_frame(action)

        elif action.key == 'switchToDefaultContent':
            result = self._action_switch_to_default_content(action)

        elif action.key == 'switchToParentFrame':
            result = self._action_switch_to_parent_frame(action)

        elif action.key == 'switchToWindow':
            result = self._action_switch_to_window(action)

        elif action.key == 'setWindowSize':
            result = self._action_set_window_size(action)

        elif action.key == 'setWindowPosition':
            result = self._action_set_window_position(action)

        elif action.key == 'executeScript':
            result = self._action_execute_script(action)

        elif action.key == 'matchImage':
            result = self._action_match_image(action)

        elif action.key == 'sendKeys':
            result = self._action_send_keys(action)

        elif action.key == 'check':
            result = self._action_check(action)

        elif action.key == 'queryDisplayed':
            result = self._action_query_displayed(action)

        elif action.key == 'queryNotDisplayed':
            result = self._action_query_not_displayed(action)

        elif action.key == 'sleep':
            result = self._action_sleep(action)

        elif action.key == 'break':
            result = True

        elif action.key == 'else':
            result = True

        else:
            raise KeyError('The {} keyword is undefined!'.format(action.key))

        return result