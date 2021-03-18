#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import time
import json
import inspect
import unittest
import threading
from fasttest.common import *
from fasttest.utils import *
from fasttest.keywords import keywords
from fasttest.runner.run_case import RunCase
from fasttest.drivers.driver_base import DriverBase
from fasttest.result.test_runner import TestRunner

class Project(object):

    def __init__(self):

        self.__init_project()
        self.__init_config()
        self.__init_logging()
        self.__analytical_testcase_file()
        self.__analytical_common_file()
        self.__init_data()
        self.__init_keywords()
        self.__init_resource()
        self.__init_testcase_suite()

    def __init_project(self):

        # Var.root= os.getcwd()
        Var.root = '/Users/xiongjunjie/code/fasttest'
        sys.path.append(Var.root)
        sys.path.append(os.path.join(Var.root, 'Scripts'))
        Var.global_var = {}
        Var.extensions_var = {}
        Var.common_var = {}

    def __init_config(self):

        self.__config = analytical_file(os.path.join(Var.root, 'config.yaml'))
        driver = self.__config.driver
        browser = self.__config.browser

        if not driver or driver.lower() not in ['appium', 'macaca', 'selenium']:
            raise ValueError('Missing/incomplete configuration file: config.yaml, No driver type specified.')
        if driver == 'selenium' and (not browser or browser not in ['chrome', 'safari', 'firefox', 'ie', 'opera', 'phantomjs']):
            raise ValueError('browser parameter is illegal!')
        for configK, configV in self.__config.items():
            if configK == 'desiredCapabilities':
                Var.desired_caps = configV[0]
            else:
                Var[configK] = configV
        # 默认时间
        if not Var.timeOut or not isinstance(Var.timeOut, int):
            Var.timeOut = 10

        if driver != 'selenium':
            if 'platformName' not in Var.desired_caps:
                raise ValueError('Missing/incomplete configuration file: config.yaml, No platformName type specified.')
            if 'udid' not in Var.desired_caps:
                Var.desired_caps['udid'] = None
            DriverBase.init()


    def __init_data(self):

        if os.path.exists(os.path.join(Var.root, 'data.json')):
            with open(os.path.join(Var.root, 'data.json'), 'r', encoding='utf-8') as f:
                dict = Dict(json.load(fp=f))
                if dict:
                    log_info('******************* analytical data *******************')
                for extensionsK, extensionsV in dict.items():
                    log_info(' {}: {}'.format(extensionsK, extensionsV))
                    Var.extensions_var[extensionsK] = extensionsV
        if not Var.extensions_var:
            Var.extensions_var = {}
        if 'variable' not in Var.extensions_var:
            Var.extensions_var['variable'] = {}

    def __init_keywords(self):

        Var.default_keywords_data = keywords.return_keywords(Var.driver)

        if 'keywords' not in  Var.extensions_var.keys():
            Var.new_keywords_data = []
            return
        Var.new_keywords_data = Var.extensions_var['keywords']

    def __init_resource(self):

        log_info('******************* analytical resource *******************')
        if 'resource' not in Var.extensions_var.keys():
            Var.extensions_var['resource'] = {}

        for resource, path in Var.extensions_var['resource'].items():
            resource_file = os.path.join(Var.root, path)
            if not os.path.isfile(resource_file):
                log_error('No such file or directory: {}'.format(resource_file), False)
                continue
            Var.extensions_var['resource'][resource] = resource_file
            log_info(' {}: {}'.format(resource, resource_file))

    def __init_logging(self):

        if Var.driver != 'selenium':
            devices = DevicesUtils(Var.desired_caps['platformName'], Var.desired_caps['udid'])
            Var.desired_caps['udid'], info = devices.device_info()
        else:
            info = Var.browser

        thr_name = threading.currentThread().getName()
        report_time = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
        report_child = "{}_{}_{}".format(info, report_time, thr_name)
        Var.report = os.path.join(Var.root, "Report", report_child)

        if not os.path.exists(Var.report):
            os.makedirs(Var.report)
            os.makedirs(os.path.join(Var.report, 'resource'))

    def __analytical_testcase_file(self):

        log_info('******************* analytical config *******************')
        for configK, configV in self.__config.items():
            log_info(' {}: {}'.format(configK, configV))
        log_info('******************* analytical testcase *******************')
        testcase = TestCaseUtils()
        self.__testcase = testcase.testcase_path(Var.root, Var.testcase)
        log_info(' case: {}'.format(len(self.__testcase)))
        for case in self.__testcase:
            log_info(' {}'.format(case))

    def __analytical_common_file(self):

        log_info('******************* analytical common *******************')
        Var.common_func = Dict()
        common_dir = os.path.join(Var.root, "Common")
        for rt, dirs, files in os.walk(common_dir):
            if rt == common_dir:
                self.__load_common_func(rt, files)
            elif Var.driver != 'selenium':
                if rt.split(os.sep)[-1].lower() == Var.desired_caps['platformName'].lower():
                    self.__load_common_func(rt, files)

    def __load_common_func(self,rt ,files):

        for f in files:
            if not f.endswith('yaml'):
                continue
            for commonK, commonV in analytical_file(os.path.join(rt, f)).items():
                Var.common_func[commonK] = commonV
                log_info(' {}: {}'.format(commonK, commonV))


    def __init_testcase_suite(self):

        self.__suite = []
        for case_path in self.__testcase:
            testcase = analytical_file(case_path)
            testcase['testcase_path'] = case_path
            Var.testcase = testcase
            subsuite = unittest.TestLoader().loadTestsFromTestCase(RunCase)
            self.__suite.append(subsuite)
            Var.testcase = None

    def start(self):
        log_info('******************* analytical desired capabilities *******************')
        desired_capabilities = Dict({
            'driver': Var.driver.lower(),
            'timeOut': Var.timeOut,
            'browser': Var.browser,
            'desired': Var.desired_caps
        })
        if Var.driver != 'selenium':
            self.server_mobile = ServerUtils(desired_capabilities)
            Var.instance = self.server_mobile.start_server()
        elif not Var.reStart:
            self.server_web = ServerUtilsSelenium(desired_capabilities)
            Var.instance = self.server_web.start_server()
            DriverBase.init()

        suite = unittest.TestSuite(tuple(self.__suite))
        runner = TestRunner()
        runner.run(suite)

        if Var.driver != 'selenium':
            self.server_mobile.stop_server()
        elif not Var.reStart:
            self.server_web.stop_server()

        if Var.all_result:
            if Var.all_result.errorsList:
                log_info(' Error case:')
            for error in Var.all_result.errorsList:
                log_error(error, False)

            if Var.all_result.failuresList:
                log_info(' Failed case:')
            for failure in Var.all_result.failuresList:
                log_error(failure, False)
        return Var.all_result