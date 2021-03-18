#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fasttest_selenium.common import Var

class WebDriver(object):

    def __init__(self):
        self.driver = None

    def __getattribute__(self, item):
        try:
            if item == 'driver':
                self.driver = Var.instanc
                return Var.instance
            else:
                return None
        except:
            return None

wd = WebDriver()
