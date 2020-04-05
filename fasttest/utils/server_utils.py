#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
import time
import random
import platform
import threading
import subprocess
from fasttest.common import *


class ServerUtils(object):

    def __getattr__(self, item):
        try:
            return self.__getattribute__(item)
        except:
            return None

    def __init__(self, driver, desired_capabilities):

        if driver.lower() in ['appium', 'macaca']:
            self.driver = driver.lower()
        else:
            self.driver = 'appium'
        desired_capabilities_dict = {}
        for key, value in desired_capabilities.items():
            if self.driver == 'appium':
                if key in ['package', 'appPackage']:
                    key = 'appPackage'
                elif key in ['activity', 'appActivity']:
                    key = 'appActivity'
            else:
                if key in ['package', 'appPackage']:
                    key = 'package'
                elif key in ['activity', 'appActivity']:
                    key = 'activity'
            desired_capabilities_dict[key] = value
            log_info('    {}: {}'.format(key, value))
            object.__setattr__(self, key, value)

        self.url = 'http://127.0.0.1'
        self.instance = None
        self.desired_capabilities = desired_capabilities_dict
        self.port = self.__get_device_port()

    def __exec_command(self,cmd):

        pipe = subprocess.Popen("%s" % cmd, stdout=subprocess.PIPE, shell=True)
        return pipe.stdout.readlines()

    def __check_port_is_used(self,port):

        p = platform.system()
        if p == 'Windows':
            sys_command = "netstat -ano|findstr %s" % port
            pipe = subprocess.Popen(sys_command, stdout=subprocess.PIPE, shell=True)
            out, error = pipe.communicate()
            if str(out, encoding='utf-8') != "" and "LISTENING" in str(out, encoding='utf-8'):
                pid = re.search(r"\s+LISTENING\s+(\d+)\r\n", str(out, encoding='utf-8')).groups()[0]
                return True, pid
            else:
                return False, None
        elif p == 'Darwin' or p == 'Linux':
            sys_command = "lsof -i:%s" % port
            pipe = subprocess.Popen(sys_command, stdout=subprocess.PIPE, shell=True)
            for line in pipe.stdout.readlines():
                if "LISTEN" in str(line, encoding='utf-8'):
                    pid = str(line, encoding='utf-8').split()[1]
                    return True, pid
            return False, None
        else:
            log_error('The platform is {} ,this platform is not support.'.format(p))

    def __get_device_port(self):

        for i in range(10):
            port = random.randint(3456, 9999)
            result, pid = self.__check_port_is_used(port)
            if result:
                continue
            else:
                log_info('get port return {}'.format(port))
                return port
        return 3456

    def __print_appium_log(self):

        log_tag = False
        while True:
            out = self.pipe.stdout.readline()
            out = str(out,encoding='utf-8').strip()
            if 'Appium REST http interface' in out:
                log_tag = True
                log_info(out)
            elif out:
                if not log_tag:
                    log_info(out)
            else:
                break

    def start_server(self):

        try:
            log_info('Start the server')
            self.stop_server()
            if self.driver == 'appium':
                self.pipe = subprocess.Popen('appium -a {} -p {} --session-override --log-level info'.format('127.0.0.1', self.port), stdout=subprocess.PIPE, shell=True)
                thread = threading.Thread(target=self.__print_appium_log)
                thread.start()
                time.sleep(5)
            else:
                ob = subprocess.Popen('macaca server -p {}'.format(self.port), stdout=subprocess.PIPE, shell=True)
                for out_ in ob.stdout:
                    out_ = str(out_, encoding='utf-8')
                    log_info(out_.strip())
                    if 'Macaca server started' in out_: break
        except Exception as e:
            raise e

    def start_connect(self):

        try:
            log_info('Connect to server')
            if self.driver == 'appium':
                from appium import webdriver
                self.instance = webdriver.Remote(command_executor='{}:{}/wd/hub'.format(self.url, self.port),
                                                 desired_capabilities=self.desired_capabilities)

                if self.timeout:
                    self.instance.implicitly_wait(int(self.timeout))
                else:
                    self.instance.implicitly_wait(10)
            else:
                from macaca import WebDriver
                self.instance = WebDriver(url='{}:{}/wd/hub'.format(self.url, self.port),
                                          desired_capabilities=self.desired_capabilities)
                self.instance.init()
            return self.instance

        except Exception as e:
            log_error('Unable to connect to the server, please reconnect!', False)
            if self.driver == 'appium':
                os.system('adb uninstall io.appium.uiautomator2.server')
                os.system('adb uninstall io.appium.uiautomator2.server.test')
            else:
                os.system('adb uninstall com.macaca.android.testing')
                os.system('adb uninstall com.macaca.android.testing.test')
                os.system('adb uninstall xdf.android_unlock')
            self.stop_server()
            raise e

    def stop_server(self):

        try:
            if self.platformName.lower() == "android":
                os.system('adb -s {} shell am force-stop {}'.format(self.udid, self.package if self.package else self.appPackage))
            elif self.platformName.lower() == "ios":
                pass
            if self.instance:
                self.instance.quit()
            if self.port is not None:
                result, pid = self.__check_port_is_used(self.port)
                if result:
                    p = platform.system()
                    if p == "Windows":
                        sys_command = "taskkill /pid %s -t -f" % pid
                        info = subprocess.check_output(sys_command)
                        log_info(str(info, encoding='GB2312'))
                    elif p == "Darwin" or p == "Linux":
                        sys_command = "kill -9 %s" % pid
                        os.system(sys_command)
        except Exception as e:
            raise e

