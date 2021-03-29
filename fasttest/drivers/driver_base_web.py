#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import os
import pdb
import time
import datetime
from concurrent import futures
from fasttest.utils import *
from fasttest.common import *
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, NoSuchWindowException, InvalidSessionIdException, TimeoutException

class DriverBaseWeb(object):


    @staticmethod
    def init():
        try:
            global by
            by = Dict({
                'id': By.ID,
                'name': By.NAME,
                'xpath': By.XPATH,
                'class': By.CLASS_NAME,
                'tag_name': By.TAG_NAME,
                'link_text': By.LINK_TEXT,
                'css_selector': By.CSS_SELECTOR,
                'partial_link_text': By.PARTIAL_LINK_TEXT,
            })
        except Exception as e:
            raise e

    @staticmethod
    def open_url(url):
        '''
        open url
        :param url:
        :return:
        '''
        try:
            Var.instance.get(url)
        except NoSuchWindowException:
            handles = DriverBaseWeb.get_window_handles()
            # 如果浏览器未关闭打开新窗口触发该异常，提示用户切换窗口
            if handles:
                raise NoSuchWindowException('no such window, execute the switchToWindow method to switch the window')
            DriverBaseWeb.createSession()
            Var.instance.get(url)
        except InvalidSessionIdException:
            DriverBaseWeb.createSession()
            Var.instance.get(url)

    @staticmethod
    def close():
        '''
        close
        :param:
        :return:
        '''
        Var.instance.close()

    @staticmethod
    def createSession():
        server_web = ServerUtilsWeb(Var.desired_capabilities)
        Var.instance = server_web.start_server()
        DriverBaseWeb.init()

    @staticmethod
    def quit():
        '''
        quit
        :param:
        :return:
        '''
        Var.instance.quit()

    @staticmethod
    def back():
        '''
        back
        :param
        :return:
        '''
        Var.instance.back()

    @staticmethod
    def forward():
        '''
        forward
        :param
        :return:
        '''
        Var.instance.forward()

    @staticmethod
    def refresh():
        '''
        refresh
        :param
        :return:
        '''
        Var.instance.refresh()

    @staticmethod
    def maximize_window():
        '''
        maxWindow
        :param:
        :return:
        '''
        Var.instance.maximize_window()

    @staticmethod
    def minimize_window():
        '''
        minWindow
        :param:
        :return:
        '''
        Var.instance.minimize_window()

    @staticmethod
    def fullscreen_window():
        '''
        fullscreenWindow
        :param:
        :return:
        '''
        Var.instance.fullscreen_window()

    @staticmethod
    def delete_all_cookies():
        '''
        deleteAllCookies
        :param:
        :return:
        '''
        Var.instance.delete_all_cookies()

    @staticmethod
    def delete_cookie(name):
        '''
        deleteCookie
        :param name
        :return:
        '''
        Var.instance.delete_cookie(name)

    @staticmethod
    def add_cookie(cookie_dict):
        '''
        addCookie
        :param cookie_dict
        :return:
        '''
        Var.instance.add_cookie(cookie_dict)

    @staticmethod
    def submit(element):
        '''
        submit
        :param: element
        :return:
        '''
        element.submit()

    @staticmethod
    def clear(element):
        '''
        element
        :param:
        :return:
        '''
        element.clear()

    @staticmethod
    def click(element):
        '''
        click
        :param: element
        :return:
        '''
        element.click()


    @staticmethod
    def context_click(element):
        '''
        contextClick
        :param: element
        :return:
        '''
        ActionChains(Var.instance).context_click(element).perform()

    @staticmethod
    def double_click(element):
        '''
        doubleClick
        :param: element
        :return:
        '''
        ActionChains(Var.instance).double_click(element).perform()

    @staticmethod
    def click_and_hold(element):
        '''
        holdClick
        :param: element
        :return:
        '''
        ActionChains(Var.instance).click_and_hold(element).perform()

    @staticmethod
    def drag_and_drop(element, target):
        '''
        dragDrop
        :param element:鼠标按下的源元素
        :param target:鼠标释放的目标元素
        :return:
        '''
        ActionChains(Var.instance).drag_and_drop(element, target).perform()

    @staticmethod
    def drag_and_drop_by_offse(element, xoffset, yoffset):
        '''
        dragDropByOffset
        :param element:
        :param xoffset:
        :param yoffset:
        :return:
        '''
        ActionChains(Var.instance).drag_and_drop_by_offset(element, xoffset, yoffset).perform()

    @staticmethod
    def move_by_offset(xoffset, yoffset):
        '''
        moveByOffset
        :param xoffset:
        :param yoffset:
        :return:
        '''
        ActionChains(Var.instance).move_by_offset(xoffset, yoffset).perform()

    @staticmethod
    def move_to_element(element):
        '''
        moveToElement
        :param element
        :return:
        '''
        ActionChains(Var.instance).move_to_element(element).perform()

    @staticmethod
    def move_to_element_with_offset(element, xoffset, yoffset):
        '''
        moveToElementWithOffset
        :param element
        :param xoffset:
        :param yoffset:
        :return:
        '''
        ActionChains(Var.instance).move_to_element_with_offset(element, xoffset, yoffset).perform()

    @staticmethod
    def key_down_and_key_up(value):
        '''
        keyDownAndkeyUp
        :param element
        :param value:
        :return:
        '''
        try:
            action = 'ActionChains(Var.instance)'
            for k, v in value.items():
                if k.lower() == 'keydown':
                    for k_down in v:
                        action = '{}.key_down({})'.format(action, k_down)
                elif k.lower() == 'sendkeys':
                    action = '{}.send_keys("{}")'.format(action, v)
                elif k.lower() == 'keyup':
                    for k_up in v:
                        action = '{}.key_up({})'.format(action, k_up)
            action = '{}.perform()'.format(action)
            log_info(action)
            eval(action)
        except Exception as e:
            raise e

    @staticmethod
    def key_up(element, value):
        '''
        keyUp
        :param element
        :param value:
        :return:
        '''
        ActionChains(Var.instance).key_up(value, element).perform()

    @staticmethod
    def switch_to_frame(frame_reference):
        '''
        switchToFrame
        :param frame_reference:
        :return:
        '''
        Var.instance.switch_to.frame(frame_reference)

    @staticmethod
    def switch_to_default_content():
        '''
        switchToDefaultContent
        :return:
        '''
        Var.instance.switch_to.default_content()

    @staticmethod
    def switch_to_parent_frame():
        '''
        switchToParentFrame
        :return:
        '''
        Var.instance.switch_to.parent_frame()

    @staticmethod
    def switch_to_window(handle):
        '''
        switchToWindow
        :return:
        '''
        Var.instance.switch_to.window(handle)

    @staticmethod
    def execute_script(js):
        '''
        executeScript
        :return:
        '''
        return Var.instance.execute_script(js)

    @staticmethod
    def send_keys(element, text):
        '''
        sendKeys
        :param element:
        :param text:
        :return:
        '''
        try:
            str_list = []
            for t_str in text:
                if t_str is None:
                    raise TypeError("the parms can'not be none")
                if re.match(r'Keys\.\w+', t_str):
                    try:
                        t_str = eval(t_str)
                    except:
                        t_str = t_str
                str_list.append(t_str)
            if len(str_list) == 1:
                element.send_keys(str_list[0])
            elif len(str_list) == 2:
                element.send_keys(str_list[0], str_list[1])
        except Exception as e:
            raise e

    @staticmethod
    def is_selected(element):
        '''
        isSelected
        :param element:
        :return:
        '''
        return element.is_selected()

    @staticmethod
    def is_displayed(element):
        '''
        isDisplayed
        :param element:
        :return:
        '''
        return element.is_displayed()

    @staticmethod
    def is_enabled(element):
        '''
        isEnabled
        :param element:
        :return:
        '''
        return element.is_enabled()

    @staticmethod
    def get_size(element):
        '''
        getSize
        :param element:
        :return:
        '''
        return element.size

    @staticmethod
    def get_attribute(element, attribute):
        '''
        getAttribute
        :param element
        :param attribute
        :return:
        '''
        return element.get_attribute(attribute)

    @staticmethod
    def get_text(element):
        '''
        getText
        :param element:
        :return:
        '''
        return element.text

    @staticmethod
    def get_tag_name(element):
        '''
        getTagName
        :param element:
        :return:
        '''
        return element.tag_name

    @staticmethod
    def get_css_property(element, css):
        '''
        getCssProperty
        :param element:
        :return:
        '''
        return element.value_of_css_property(css)

    @staticmethod
    def get_location(element):
        '''
        getLocation
        :param element:
        :return:
        '''
        return element.location

    @staticmethod
    def get_rect(element):
        '''
        getRect
        '''
        return element.rect

    @staticmethod
    def get_name():
        '''
        getName
        :return:
        '''
        return Var.instance.name

    @staticmethod
    def get_title():
        '''
        getTitle
        :return:
        '''
        return Var.instance.title

    @staticmethod
    def get_current_url():
        '''
        getCurrentUrl
        :return:
        '''
        return Var.instance.current_url

    @staticmethod
    def get_current_window_handle():
        '''
        getCurrentWindowHandle
        :return:
        '''
        return Var.instance.current_window_handle

    @staticmethod
    def get_window_handles():
        '''
        getWindowHandles
        :return:
        '''
        return Var.instance.window_handles

    @staticmethod
    def get_cookies():
        '''
        getCookies
        :return:
        '''
        return Var.instance.get_cookies()

    @staticmethod
    def get_cookie(name):
        '''
        getCookie
        :param name
        :return:
        '''
        return Var.instance.get_cookie(name)

    @staticmethod
    def get_window_position():
        '''
        getWindowPosition
        :return:
        '''
        return Var.instance.get_window_position()

    @staticmethod
    def set_window_position(x, y):
        '''
        setWindowPosition
        :return:
        '''
        return Var.instance.set_window_position(x, y)

    @staticmethod
    def get_window_size():
        '''
        getWindowSize
        :return:
        '''
        return Var.instance.get_window_size()

    @staticmethod
    def set_window_size(width, height):
        '''
        setWindowSize
        :return:
        '''
        return Var.instance.set_window_size(width, height)

    @staticmethod
    def save_screenshot(element, name):
        '''
        saveScreenshot
        :return:
        '''
        try:
            image_dir = os.path.join(Var.snapshot_dir, 'screenshot')
            if not os.path.exists(image_dir):
                os.makedirs(image_dir)
            image_path = os.path.join(image_dir, '{}'.format(name))
            if element:
                element.screenshot(image_path)
            else:
                Var.instance.save_screenshot(image_path)
        except Exception as e:
            raise e
        return image_path

    @staticmethod
    def query_displayed(type='', text='',element='' , timeout=10):
        '''
        queryDisplayed
        :param type:
        :param text:
        :return:
        '''
        if element:
            try:
                WebDriverWait(Var.instance, int(timeout)).until(
                    EC.visibility_of(element)
                )
            except Exception as e:
                raise e
        else:
            try:
                type = type.lower()
                WebDriverWait(Var.instance, int(timeout)).until(
                    EC.visibility_of_element_located((by[type], text))
                )
            except Exception as e:
                raise e

    @staticmethod
    def query_not_displayed(type='', text='', element='', timeout=10):
        '''
        queryNotDisplayed
        :param type:
        :param text:
        :return:
        '''
        if element:
            try:
                WebDriverWait(Var.instance, int(timeout)).until(
                    EC.invisibility_of_element(element)
                )
            except Exception as e:
                raise e
        else:
            try:
                type = type.lower()
                WebDriverWait(Var.instance, int(timeout)).until(
                    EC.invisibility_of_element_located((by[type], text))
                )
            except Exception as e:
                raise e

    @staticmethod
    def get_element(type, text, timeout=10):
        '''
        getElement
        :param type:
        :param text:
        :return:
        '''
        type = type.lower()
        endTime = datetime.datetime.now() + datetime.timedelta(seconds=int(timeout))
        index = 3
        while True:
            try:
                element = Var.instance.find_element(by[type], text)
                if element.is_enabled():
                    return element
                elif element.is_displayed():
                    index -= 1
                    if index < 0:
                        return element
                if datetime.datetime.now() >= endTime:
                    return element
            except NoSuchElementException:
                if datetime.datetime.now() >= endTime:
                    return None
            except Exception as e:
                raise e

    @staticmethod
    def get_elements(type, text, timeout=10):
        '''
        getElements
        :param type:
        :param text:
        :return:
        '''
        type = type.lower()
        try:
            element = DriverBaseWeb.get_element(type, text, timeout)
            if not element:
                return []
            elements = Var.instance.find_elements(by[type], text)
            return elements
        except NoSuchElementException:
            return []
        except Exception as e:
            raise e