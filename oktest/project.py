#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import time
import json
import inspect
import unittest
import traceback
from macaca.webdriver import WebDriver
from oktest.common import *
from oktest.utils import *
from oktest.runner.run_case import RunCase
from oktest.common.logging import log_init
from oktest.drivers.driver_base import DriverBase
from oktest.result.test_runner import TestRunner

class Project(object):

    def __init__(self):
        self.__init_project()
        self.__init_config()
        self.__init_logging()
        self.__analytical_testcase_file()
        self.__analytical_common_file()
        self.__init_extensions()
        self.__init_images()
        self.__init_testcase_suite()

    def __init_project(self):
        for path in [path  for path in inspect.stack() if str(path[1]).endswith("runtest.py")]:
            self.ROOT = os.path.dirname(path[1])
            sys.path.append(self.ROOT)
            Var.ROOT = self.ROOT
            Var.global_var = {} # 全局变量
            Var.extensions_var = {} # 扩展数据变量
            Var.common_var = {} # common临时变量，call执行完后重置

    def __init_config(self):
        self.config = analytical_file(os.path.join(self.ROOT, 'config.yaml'))
        for configK, configV in self.config.items():
            if configK == 'desiredcaps':
                Var.desired_caps = configV[0]
                for desiredcapsK, desiredcapsV in Var.desired_caps.items():
                    if desiredcapsK == 'platformName':
                        Var[desiredcapsK] = desiredcapsV.lower()
                    else:
                        Var[desiredcapsK] = desiredcapsV
            else:
                Var[configK] = configV
        DriverBase.init()


    def __init_extensions(self):
        if os.path.exists(os.path.join(Var.ROOT,'data.json')):
            with open(os.path.join(Var.ROOT, 'data.json'), 'r', encoding='utf-8') as f:
                dict = Dict(json.load(fp=f))
                if dict:
                    log_info('******************* analytical extensions *******************')
                for extensionsK, extensionsV in dict.items():
                    log_info('{}:{}'.format(extensionsK, extensionsV))
                    Var.extensions_var[extensionsK] = extensionsV

    def __init_images(self):
        if Var.extensions_var and Var.extensions_var['images']:
            images_dict = {}
            for images in Var.extensions_var['images']:
                images_file = os.path.join(Var.ROOT, 'images/{}'.format(images))
                if os.path.isfile(images_file):
                    images_dict[images] = images_file
                else:
                    raise FileNotFoundError('No such file or directory: {}'.format(images_file))
            Var.extensions_var['images_file'] = images_dict
            log_info('image path:{}'.format(Var.extensions_var['images_file']))

    def __init_logging(self):
        devices = DevicesUtils(Var.platformName, Var.udid)
        Var.udid, deviceinfo = devices.device_info()
        report_time = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
        report_child = "{}_{}".format(deviceinfo, report_time)
        Var.report = os.path.join(Var.ROOT, "Report", report_child)

        if not os.path.exists(Var.report):
            os.makedirs(Var.report)
            os.makedirs(os.path.join(Var.report, 'resource'))
        log_init(Var.report)

    def __analytical_testcase_file(self):
        log_info('******************* analytical config *******************')
        for configK, configV in self.config.items():
            log_info('{}:{}'.format(configK, configV))
        log_info('******************* analytical testcase *******************')
        testcase = TestCaseUtils()
        self.testcase = testcase.testcase_path(Var.ROOT, Var.testcase)
        log_info('testcase:{}'.format(self.testcase))

    def __analytical_common_file(self):
        log_info('******************* analytical common *******************')
        Var.common_func = Dict()
        common_dir = os.path.join(Var.ROOT, "Common")
        for rt, dirs, files in os.walk(common_dir):
            if rt == common_dir:
                self.__load_common_func(rt, files)
            elif rt.split(os.sep)[-1].lower() == Var.platformName.lower():
                self.__load_common_func(rt, files)
        log_info('common:{}'.format(Var.common_func.keys()))

    def __load_common_func(self,rt ,files):
        for f in files:
            if not f.endswith('yaml'):
                continue
            for commonK, commonV in analytical_file(os.path.join(rt, f)).items():
                Var.common_func[commonK] = commonV


    def __init_testcase_suite(self):
        self.suite = []
        for case_path in self.testcase:
            testcase = analytical_file(case_path)
            testcase['testcase_path'] = case_path
            Var.testcase = testcase
            subsuite = unittest.TestLoader().loadTestsFromTestCase(RunCase)
            self.suite.append(subsuite)
            Var.testcase = None

    def start(self):

        log_info('The project starts running...')
        server = ServerUtils()
        Var.device_port = server.get_device_port()
        for k, v in Var.desired_caps.items():
            log_info('{}:{}'.format(k, v))
        server.start_server()
        Var.driver = WebDriver(Var.desired_caps, url='http://127.0.0.1:{}/wd/hub'.format(Var.device_port))
        try:
            Var.driver.init()
        except:
            # todo com.macaca.android.testing.test
            server.stop_server()
            raise Exception(traceback.format_exc())

        suite = unittest.TestSuite(tuple(self.suite))
        runner = TestRunner()
        runner.run(suite)
        server.stop_server()
