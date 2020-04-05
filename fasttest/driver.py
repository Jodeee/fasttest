#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from fasttest.common import *

class Driver(object):

    @staticmethod
    def press(element, duration=2):
        '''
        :param element:
        :param duration:
        :return:
        '''
        Var.driver_instance.press(element, duration)

    @staticmethod
    def clear(element):
        '''
        :param element:
        :return:
        '''
        try:
            element.clear()
        except:
            pass

    @staticmethod
    def wait_for_elements_by_id(id, timeout=10, interval=1):
        '''
        :param id:
        :return:
        '''
        try:
            return Var.driver_instance.wait_for_elements_by_id(id, timeout, interval)
        except Exception as e:
            raise e

    @staticmethod
    def wait_for_elements_by_name(name, timeout=10, interval=1):
        '''
        :param name:
        :return:
        '''
        try:
            return Var.driver_instance.wait_for_elements_by_name(name, timeout, interval)
        except Exception as e:
            raise e

    @staticmethod
    def wait_for_elements_by_xpath(xpath, timeout=10, interval=1):
        '''
        :param xpath:
        :return:
        '''
        try:
            return Var.driver_instance.wait_for_elements_by_xpath(xpath, timeout, interval)
        except Exception as e:
            raise e

    @staticmethod
    def wait_for_elements_by_class_name(classname, timeout=10, interval=1):
        '''
        :param classname:
        :return:
        '''
        try:
            return Var.driver_instance.wait_for_elements_by_classname(classname, timeout, interval)
        except Exception as e:
            raise e
