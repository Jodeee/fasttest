#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
import random
import platform
import traceback
import subprocess
from fasttest.common import *


class ServerUtils(object):

    def __exec_command(self,cmd):
        pipe = subprocess.Popen("%s" % cmd, stdout=subprocess.PIPE, shell=True)
        return pipe.stdout.readlines()

    def __check_port_is_used(self,port):
        p = platform.system()
        if p == 'Windows':
            sys_command = " netstat -ano|findstr %s" % port
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

    def get_device_port(self):
        '''
        :return:
        '''
        for i in range(10):
            port = random.randint(3456, 9999)
            result, pid = self.__check_port_is_used(port)
            if result:
                continue
            else:
                log_info('get port return {}'.format(port))
                return port
        return 3456

    def start_server(self):
        try:
            self.stop_server()
            webdriver_server = WebDriverServer(Var.device_port)
            webdriver_server.start_server()
        except:
            traceback.print_exc()

    def stop_server(self):
        try:
            if Var.platformName in "Android":
                os.system('adb -s {} shell am force-stop {}'.format(Var.udid, Var.package))
            elif Var.platformName in "iOS":
                pass
            if Var.driver:
                Var.driver.quit()
            if Var.device_port is not None:
                result, pid = self.__check_port_is_used(Var.device_port)
                if result:
                    p = platform.system()
                    if p == "Windows":
                        sys_command = "taskkill /pid %s -t -f" % pid
                        info = subprocess.check_output(sys_command)
                        log_info(str(info, encoding='GB2312'))
                    elif p == "Darwin" or p == "Linux":
                        sys_command = "kill -9 %s" % pid
                        os.system(sys_command)
        except:
            traceback.print_exc()


class WebDriverServer(object):
    def __init__(self,port=3456):
        self.__port = port
        self.__thread = None

    def print_server_log(self,out):
        for out_ in out:
            out_  = str(out_,encoding='utf-8')
            log_info(out_)
            if 'Macaca server started' in out_:break

    def start_server(self):
        ob = subprocess.Popen('macaca server -p {}'.format(self.__port),stdout=subprocess.PIPE,shell=True)
        self.print_server_log(ob.stdout)
        return True


