#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from selenium import webdriver
from fasttest.common import *



class ServerUtilsWeb(object):

    def __getattr__(self, item):
        try:
            return self.__getattribute__(item)
        except:
            return None

    def __init__(self, desired_capabilities):

        self.instance = None
        self.driver = desired_capabilities.driver
        self.time_out = desired_capabilities.timeOut
        self.desired_capabilities = desired_capabilities.desired
        self.browser =  self.desired_capabilities.browser
        self.max_window =  self.desired_capabilities.maxWindow
        self.remote =  self.desired_capabilities.remote
        if 'driver' in self.desired_capabilities[self.browser][0].keys():
            self.driver_path = self.desired_capabilities[self.browser][0]['driver']
        else:
            self.driver_path = None
        if 'options' in self.desired_capabilities[self.browser][0].keys():
            self.options = self.desired_capabilities[self.browser][0]['options']
        else:
            self.driver_path = None
        if self.remote is None:
            self.remote = False

    def start_server(self):

        try:
            if not os.path.isfile(self.driver_path):
                self.driver_path = None

            if self.browser == 'chrome':
                options = webdriver.ChromeOptions()
                if self.options:
                    for opt in self.options:
                        options.add_argument(opt)
                if self.remote:
                    self.instance = webdriver.Remote(command_executor=self.remote,
                                                     desired_capabilities={
                                                         'platform': 'ANY',
                                                         'browserName': self.browser,
                                                         'version': '',
                                                         'javascriptEnabled': True
                                                     },
                                                     options=options)
                else:
                    if self.driver_path:
                        self.instance = webdriver.Chrome(executable_path=self.driver_path,
                                                     chrome_options=options)
                    else:
                        self.instance = webdriver.Chrome(chrome_options=options)
            elif self.browser == 'firefox':
                options = webdriver.FirefoxOptions()
                if self.options:
                    for opt in self.options:
                        options.add_argument(opt)
                if self.remote:
                    self.instance = webdriver.Remote(command_executor=self.remote,
                                                     desired_capabilities={
                                                         'platform': 'ANY',
                                                         'browserName': self.browser,
                                                         'version': '',
                                                         'javascriptEnabled': True
                                                     },
                                                     options=options)
                else:
                    if self.driver_path:
                        self.instance = webdriver.Firefox(executable_path=self.driver_path,
                                                        firefox_options=options)
                    else:
                        self.instance = webdriver.Firefox(firefox_options=options)
            elif self.browser == 'edge':
                if self.driver_path:
                    self.instance = webdriver.Edge(executable_path=self.driver_path)
                else:
                    self.instance = webdriver.Edge()
            elif self.browser == 'safari':
                self.instance = webdriver.Safari()
            elif self.browser == 'ie':
                if self.driver_path:
                    self.instance = webdriver.Ie(executable_path=self.driver_path)
                else:
                    self.instance = webdriver.Ie()
            elif self.browser == 'opera':
                if self.driver_path:
                    self.instance = webdriver.Opera(executable_path=self.driver_path)
                else:
                    self.instance = webdriver.Opera()
            elif self.browser == 'phantomjs':
                if self.driver_path:
                    self.instance = webdriver.PhantomJS(executable_path=self.driver_path)
                else:
                    self.instance = webdriver.PhantomJS()

            if self.max_window:
                self.instance.maximize_window()
            return self.instance
        except Exception as e:
            raise e

    def stop_server(self, instance):

        try:
            instance.quit()
        except:
            pass

