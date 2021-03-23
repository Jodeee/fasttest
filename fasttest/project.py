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
from fasttest.drivers.driver_base_app import DriverBaseApp
from fasttest.drivers.driver_base_web import DriverBaseWeb
from fasttest.result.test_runner import TestRunner

class Project(object):

    def __init__(self):

        self.__init_project()
        self.__init_config()
        self.__init_logging()
        self.__analytical_testcase_file()
        self.__analytical_common_file()
        self.__init_data()
        self.__init_testcase_suite()

    def __init_project(self):

        Var.root= os.getcwd()
        sys.path.append(Var.root)
        sys.path.append(os.path.join(Var.root, 'Scripts'))
        Var.global_var = Dict()
        Var.extensions_var = Dict()
        Var.common_var = Dict()
        Var.common_func = Dict()

    def __init_config(self):

        self.__config = analytical_file(os.path.join(Var.root, 'config.yaml'))
        Var.driver = self.__config.driver
        Var.re_start = self.__config.reStart
        Var.save_screenshot = self.__config.saveScreenshot
        Var.time_out = self.__config.timeOut
        Var.test_case = self.__config.testcase
        Var.desired_caps = Dict()
        for configK, configV in self.__config.desiredCapabilities[0].items():
            Var.desired_caps[configK] = configV

        if not Var.driver or Var.driver.lower() not in ['appium', 'macaca', 'selenium']:
            raise ValueError('Missing/incomplete configuration file: config.yaml, No driver type specified.')

        if not Var.time_out or not isinstance(Var.time_out, int):
            Var.time_out = 10

        if Var.driver != 'selenium':
            if not Var.desired_caps.platformName:
                raise ValueError('Missing/incomplete configuration file: config.yaml, No platformName type specified.')
            DriverBaseApp.init()
        else:
            if not Var.desired_caps.browser or Var.desired_caps.browser not in ['chrome', 'safari', 'firefox', 'ie', 'opera', 'phantomjs']:
                raise ValueError('browser parameter is illegal!')

    def __init_logging(self):

        if Var.driver != 'selenium':
            devices = DevicesUtils(Var.desired_caps.platformName, Var.desired_caps.udid)
            Var.desired_caps['udid'], info = devices.device_info()
        else:
            info = Var.desired_caps.browser

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
        self.__testcase = testcase.test_case_path(Var.root, Var.test_case)
        log_info(' case: {}'.format(len(self.__testcase)))
        for case in self.__testcase:
            log_info(' {}'.format(case))

    def __analytical_common_file(self):

        log_info('******************* analytical common *******************')
        common_dir = os.path.join(Var.root, "Common")
        for rt, dirs, files in os.walk(common_dir):
            if rt == common_dir:
                self.__load_common_func(rt, files)
            elif Var.desired_caps.platformName and (rt.split(os.sep)[-1].lower() == Var.desired_caps.platformName.lower()):
                self.__load_common_func(rt, files)

    def __load_common_func(self,rt ,files):

        for f in files:
            if not f.endswith('yaml'):
                continue
            for commonK, commonV in analytical_file(os.path.join(rt, f)).items():
                Var.common_func[commonK] = commonV
                log_info(' {}: {}'.format(commonK, commonV))

    def __init_data(self):

        if os.path.exists(os.path.join(Var.root, 'data.json')):
            with open(os.path.join(Var.root, 'data.json'), 'r', encoding='utf-8') as f:
                dict = Dict(json.load(fp=f))
                Var.extensions_var['variable'] = dict.variable
                Var.extensions_var['resource'] = dict.resource
                Var.extensions_var['keywords'] = dict.keywords
                if not Var.extensions_var.variable:
                    Var.extensions_var['variable'] = Dict()
                if not Var.extensions_var.resource:
                    Var.extensions_var['resource'] = Dict()
                if not Var.extensions_var.keywords:
                    Var.extensions_var['keywords'] = Dict()
        # 注册全局变量
        log_info('******************* register variable *******************')
        for key, value in Var.extensions_var.variable.items():
            Var.extensions_var.variable[key] = value
            log_info(' {}: {}'.format(key, value))
        # 解析文件路径
        log_info('******************* register resource *******************')
        for resource, path in Var.extensions_var.resource.items():
            resource_file = os.path.join(Var.root, path)
            if not os.path.isfile(resource_file):
                log_error('No such file or directory: {}'.format(resource_file), False)
                continue
            Var.extensions_var.resource[resource] = resource_file
            log_info(' {}: {}'.format(resource, resource_file))
        # 注册关键字
        log_info('******************* register keywords *******************')
        Var.default_keywords_data = keywords.return_keywords(Var.driver)
        Var.new_keywords_data = Var.extensions_var.keywords
        for key in Var.extensions_var.keywords:
            log_info(' {}'.format(key))

    def __init_testcase_suite(self):

        self.__suite = []
        for case_path in self.__testcase:
            test_case = analytical_file(case_path)
            test_case['test_case_path'] = case_path
            Var.case_info = test_case
            subsuite = unittest.TestLoader().loadTestsFromTestCase(RunCase)
            self.__suite.append(subsuite)
            Var.case_info = None

    def start(self):
        log_info('******************* analytical desired capabilities *******************')
        Var.desired_capabilities = Dict({
            'driver': Var.driver.lower(),
            'timeOut': Var.time_out,
            'desired': Var.desired_caps
        })
        # 启动服务
        if Var.driver != 'selenium':
            server = ServerUtilsApp(Var.desired_capabilities)
            Var.instance = server.start_server()
        elif not Var.re_start:
            server = ServerUtilsWeb(Var.desired_capabilities)
            Var.instance = server.start_server()
            DriverBaseWeb.init()
        else:
            server = None
        # 用例运行
        suite = unittest.TestSuite(tuple(self.__suite))
        runner = TestRunner()
        runner.run(suite)

        # 结束服务
        if Var.driver != 'selenium':
            server.stop_server()
        elif not Var.re_start:
            server.stop_server(Var.instance)

        # 打印失败结果
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