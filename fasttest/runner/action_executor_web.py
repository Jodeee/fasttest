#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
import time
import datetime
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import JavascriptException
from fasttest.common import Var
from fasttest.common.check import check
from fasttest.drivers.driver_base_web import DriverBaseWeb
from fasttest.utils.opcv_utils import OpencvUtils
from fasttest.runner.action_executor_base import ActionExecutorBase


class ActionExecutorWeb(ActionExecutorBase):

    def _openUrl(self, action):
        '''
        :param action:
        :return:
        '''
        url = self._getParms(action, 0)
        DriverBaseWeb.open_url(url)

    def _close(self, action):
        '''
        :param action:
        :return:
        '''
        DriverBaseWeb.close()

    def _quit(self, action):
        '''
        :param action:
        :return:
        '''
        DriverBaseWeb.quit()

    @check
    def _submit(self, action):
        '''
        :param action:
        :return:
        '''
        element = self._getElement(action)
        DriverBaseWeb.submit(element)

    def _back(self, action):
        '''
        :param action:
        :return:
        '''
        DriverBaseWeb.back()

    def _forward(self, action):
        '''
        :param action:
        :return:
        '''
        DriverBaseWeb.forward()

    def _refresh(self, action):
        '''
        :param action:
        :return:
        '''
        DriverBaseWeb.refresh()

    def _queryDisplayed(self, action):
        '''
        :param action:
        :return:
        '''
        parms = self._getParms(action, 0)
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

    def _queryNotDisplayed(self, action):
        '''
        :param action:
        :return:
        '''
        parms = self._getParms(action, 0)
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
    def _click(self, action):
        '''
        :param action:
        :return:
        '''
        element = self._getElement(action)
        DriverBaseWeb.click(element)

    @check
    def _check(self, action):
        '''
        :param action:
        :return:
        '''
        self._getElement(action)

    @check
    def _contextClick(self, action):
        '''
        :param action:
        :return:
        '''
        element = self._getElement(action)
        DriverBaseWeb.context_click(element)

    @check
    def _doubleClick(self, action):
        '''
        :param action:
        :return:
        '''
        element = self._getElement(action)
        DriverBaseWeb.double_click(element)

    @check
    def _holdClick(self, action):
        '''
        :param action:
        :return:
        '''
        element = self._getElement(action)
        DriverBaseWeb.click_and_hold(element)

    @check
    def _dragDrop(self, action):
        '''
        :param action:
        :return:
        '''
        element = self._getElement(action, 0)
        target = self._getElement(action, 1)
        DriverBaseWeb.drag_and_drop(element, target)

    @check
    def _dragDropByOffset(self, action):
        '''
        :param action:
        :return:
        '''
        element = self._getElement(action)
        xoffset = self._getParms(action, 1)
        yoffset = self._getParms(action, 2)
        DriverBaseWeb.drag_and_drop_by_offse(element, float(xoffset), float(yoffset))

    def _moveByOffset(self, action):
        '''
        :param action:
        :return:
        '''
        xoffset = self._getParms(action, 0)
        yoffset = self._getParms(action, 1)
        DriverBaseWeb.move_by_offset(float(xoffset), float(yoffset))

    @check
    def _moveToElement(self, action):
        '''
        :param action:
        :return:
        '''
        element = self._getElement(action)
        DriverBaseWeb.move_to_element(element)

    @check
    def _moveToElementWithOffset(self, action):
        '''
        :param action:
        :return:
        '''
        element = self._getElement(action)
        xoffset = self._getParms(action, 1)
        yoffset = self._getParms(action, 2)
        DriverBaseWeb.move_to_element_with_offset(element, float(xoffset), float(yoffset))

    @check
    def _sendKeys(self, action):
        '''
        :param action:
        :return:
        '''
        element = self._getElement(action)
        text_list = []
        if len(action.parms) == 2:
            text_list.append(self._getParms(action, 1))
        elif len(action.parms) == 3:
            text_list.append(self._getParms(action, 1))
            text_list.append(self._getParms(action, 2))
        else:
            raise TypeError('missing 1 required positional argument')
        DriverBaseWeb.send_keys(element, text_list)

    @check
    def _clear(self, action):
        '''
        :param action:
        :return:
        '''
        element = self._getElement(action)
        DriverBaseWeb.clear(element)

    def _maxWindow(self, action):
        '''
        :param action:
        :return:
        '''
        DriverBaseWeb.maximize_window()

    def _minWindow(self, action):
        '''
        :param action:
        :return:
        '''
        DriverBaseWeb.minimize_window()

    def _fullscreenWindow(self, action):
        '''
        :param action:
        :return:
        '''
        DriverBaseWeb.fullscreen_window()

    def _deleteAllCookies(self, action):
        '''
        :param action:
        :return:
        '''
        DriverBaseWeb.delete_all_cookies()

    def _deleteCookie(self, action):
        '''
        :param action:
        :return:
        '''
        key = self._getParms(action, 0)
        DriverBaseWeb.delete_cookie(key)

    def _addCookie(self, action):
        '''
        :param action:
        :return:
        '''
        key = self._getParms(action, 0)
        DriverBaseWeb.add_cookie(key)

    def _switchToFrame(self, action):
        '''
        :param action:
        :return:
        '''
        frame_reference = self._getParms(action)
        DriverBaseWeb.switch_to_frame(frame_reference)

    def _switchToDefaultContent(self, action):
        '''
        :param action:
        :return:
        '''
        DriverBaseWeb.switch_to_default_content()

    def _switchToParentFrame(self, action):
        '''
        :param action:
        :return:
        '''
        DriverBaseWeb.switch_to_parent_frame()

    def _switchToWindow(self, action):
        '''
        :param action:
        :return:
        '''
        handle = self._getParms(action)
        DriverBaseWeb.switch_to_window(handle)

    def _setWindowSize(self, action):
        '''
        :param action:
        :return:
        '''
        width = self._getParms(action, 0)
        height = self._getParms(action, 0)
        DriverBaseWeb.set_window_size(float(width), float(height))

    def _setWindowPosition(self, action):
        '''
        :param action:
        :return:
        '''
        x = self._getParms(action, 0)
        y = self._getParms(action, 1)
        DriverBaseWeb.set_window_position(float(x), float(y))

    def _executeScript(self, action):
        '''
        :param action:
        :return:
        '''
        endTime = datetime.datetime.now() + datetime.timedelta(seconds=int(Var.time_out))
        while True:
            try:
                js_value = self._getParms(action)
                return DriverBaseWeb.execute_script(js_value)
            except JavascriptException as e:
                if datetime.datetime.now() >= endTime:
                    raise e
                time.sleep(0.1)
            except Exception as e:
                raise e

    def _matchImage(self, action):
        '''
        :param action:
        :return:
        '''
        base_image = self._getParms(action, 0)
        match_image = self._getParms(action, 1)
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

    @check
    def _saveScreenshot(self, action):
        '''
        :param action:
        :return:
        '''
        if len(action.parms) == 1:
            element = None
            name = self._getParms(action, 0)
        else:
            element = self._getElement(action)
            name = self._getParms(action, 1)
        return DriverBaseWeb.save_screenshot(element, name)

    @check
    def _isSelected(self, action):
        '''
        :param action:
        :return:
        '''
        element = self._getElement(action)
        return DriverBaseWeb.is_selected(element)

    @check
    def _isDisplayed(self, action):
        '''
        :param action:
        :return:
        '''
        element = self._getElement(action)
        return DriverBaseWeb.is_displayed(element)

    @check
    def _isEnabled(self, action):
        '''
        :param action:
        :return:
        '''
        element = self._getElement(action)
        return DriverBaseWeb.is_enabled(element)

    @check
    def _getSize(self, action):
        '''
        :param action:
        :return:
        '''
        element = self._getElement(action)
        return DriverBaseWeb.get_size(element)

    @check
    def _getLocation(self, action):
        '''
        :param action:
        :return:
        '''
        element = self._getElement(action)
        return DriverBaseWeb.get_location(element)

    @check
    def _getRect(self, action):
        '''
        :param action:
        :return:
        '''
        element = self._getElement(action)
        return DriverBaseWeb.get_rect(element)

    @check
    def _getAttribute(self, action):
        '''
        :param action:
        :return:
        '''
        element = self._getElement(action)
        attribute = self._getParms(action, 1)
        return DriverBaseWeb.get_attribute(element, attribute)

    @check
    def _getTagName(self, action):
        '''
        :param action:
        :return:
        '''
        element = self._getElement(action)
        return DriverBaseWeb.get_tag_name(element)

    @check
    def _getCssProperty(self, action):
        '''
        :param action:
        :return:
        '''
        element = self._getElement(action)
        css_value = self._getParms(action, 1)
        return DriverBaseWeb.get_css_property(element, css_value)

    def _getName(self, action):
        '''
        :param action:
        :return:
        '''
        return DriverBaseWeb.get_name()

    def _getTitle(self, action):
        '''
        :param action:
        :return:
        '''
        return DriverBaseWeb.get_title()

    def _getCurrentUrl(self, action):
        '''
        :param action:
        :return:
        '''
        return DriverBaseWeb.get_current_url()

    def _getCurrentWindowHandle(self, action):
        '''
        :param action:
        :return:
        '''
        return DriverBaseWeb.get_current_window_handle()

    def _getWindowHandles(self, action):
        '''
        :param action:
        :return:
        '''
        return DriverBaseWeb.get_window_handles()

    def _getCookies(self, action):
        '''
        :param action:
        :return:
        '''
        return DriverBaseWeb.get_cookies()

    def _getCookie(self, action):
        '''
        :param action:
        :return:
        '''
        key = self._getParms(action)
        return DriverBaseWeb.get_cookie(key)

    def _getWindowPosition(self, action):
        '''
        :param action:
        :return:
        '''
        return DriverBaseWeb.get_window_position()

    def _getWindowSize(self, action):
        '''
        :param action:
        :return:
        '''
        return DriverBaseWeb.get_window_size()

    @check
    def _getText(self, action):
        '''
        :param action:
        :return:
        '''
        element = self._getElement(action)
        return DriverBaseWeb.get_text(element)

    def _getElement(self, action, index=0):
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
            if not re.match(r'^(id|name|class|tag_name|link_text|partial_link_text|xpath|css_selector)\s*=.+',
                            parms[index].strip(), re.I):
                raise TypeError('input parameter format error:{}'.format(parms[index]))
            key = parms[index].split('=', 1)[0].strip()
            value = parms[index].split('=', 1)[-1].strip()
            element = DriverBaseWeb.get_element(key, value, Var.time_out)
        else:
            raise TypeError('the parms type must be: WebElement or str')

        if not element:
            raise Exception("Can't find element: {}".format(parms[index]))
        return element

    def _getElements(self, action):
        '''
        :param action:
        :return:
        '''
        parms = self._getParms(action, 0)
        if not re.match(r'^(id|name|class|tag_name|link_text|partial_link_text|xpath|css_selector)\s*=.+',
                        parms.strip(), re.I):
            raise TypeError('input parameter format error:{}'.format(parms))
        key = parms.strip().split('=', 1)[0]
        value = parms.strip().split('=', 1)[-1]
        elements = DriverBaseWeb.get_elements(key, value, Var.time_out)
        if not elements:
            raise Exception("Can't find elements: {}".format(parms))
        return elements

    def _isExist(self, action):
        '''
        :param action:
        :return:
        '''
        parms = self._getParms(action, 0)
        if not re.match(r'^(id|name|class|tag_name|link_text|partial_link_text|xpath|css_selector)\s*=.+',
                        parms.strip(), re.I):
            raise TypeError('input parameter format error:{}'.format(parms))
        key = parms.strip().split('=', 1)[0]
        value = parms.strip().split('=', 1)[-1]
        elements = DriverBaseWeb.get_elements(key, value, Var.time_out)
        return bool(elements)

    def _isNotExist(self, action):
        '''
        :param action:
        :return:
        '''
        parms = self._getParms(action, 0)
        if not re.match(r'^(id|name|class|tag_name|link_text|partial_link_text|xpath|css_selector)\s*=.+',
                        parms.strip(), re.I):
            raise TypeError('input parameter format error:{}'.format(parms))
        key = parms.strip().split('=', 1)[0]
        value = parms.strip().split('=', 1)[-1]
        elements = DriverBaseWeb.get_elements(key, value, 0)
        return not bool(elements)