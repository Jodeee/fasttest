#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import sys
import traceback
from fasttest.common import Var
from fasttest.runner.action_analysis import ActionAnalysis

class CaseAnalysis(object):

    def __init__(self):
        self.action_nalysis = ActionAnalysis()
        self.testcase_steps = []
        self.is_run = None
        self.timeout = 10

    def iteration(self, steps, style='', common={}, iterating_var=None):
        '''

        @param steps:
        @param style: 控制结果报告中每句case的缩进
        @param common: call 调用时需要的参数
        @param iterating_var: for 迭代对象
        @return:
        '''
        if isinstance(steps, list):
            for step in steps:
                if isinstance(step, str):
                    self.case_executor(step, style, common, iterating_var)
                    if step.startswith('break'):
                        return 'break'
                elif isinstance(step, dict):
                    result = self.iteration(step, style, common, iterating_var)
                    if result == 'break':
                        return 'break'
        elif isinstance(steps, dict):
            for key, values in steps.items():
                if key.startswith('while'):
                    while self.case_executor(key, style, common, iterating_var):
                        result = self.iteration(values, f'{style}  ', common, iterating_var)
                        if result == 'break':
                            break
                elif key.startswith('if') or key.startswith('elif') or key.startswith('else'):
                    if self.case_executor(key, style, common, iterating_var):
                        result = self.iteration(values, f'{style}  ', common, iterating_var)
                        if result == 'break':
                            return 'break'
                        break # 判断下执行完毕，跳出循环
                elif re.match('for\s+(\$\{\w+\})\s+in\s+(\S+)', key):
                    parms = self.case_executor(key, style, common, iterating_var)
                    for f in parms['value']:
                        iterating_var = {parms['key']: f}
                        result = self.iteration(values, f'{style}  ', common, iterating_var)
                        if result == 'break':
                            break
                else:
                    raise SyntaxError('- {}:'.format(key))

    def case_executor(self, step, style, common, iterating_var):

        # call 需要全局变量判断是否是debug模式
        if step.strip().endswith('--Debug') or step.strip().endswith('--debug') or Var.is_debug:
            Var.is_debug = True
            while True:
                try:
                    if self.is_run is False:
                        print(step)
                        out = input('>')
                    elif not (step.strip().endswith('--Debug') or step.strip().endswith('--debug')):
                        self.is_run = True
                        result = self.action_nalysis.action_analysis(self.rstrip_step(step), style, common, iterating_var)
                        return result
                    else:
                        print(step)
                        out = input('>')

                    if not len(out):
                        self.is_run = False
                        continue
                    elif out.lower() == 'r':
                        # run
                        self.is_run = True
                        result = self.action_nalysis.action_analysis(self.rstrip_step(step), style, common, iterating_var)
                        return result
                    elif out.lower() == 'c':
                        # continue
                        self.is_run = False
                        break
                    elif out.lower() == 'n':
                        # next
                        self.is_run = False
                        result = self.action_nalysis.action_analysis(self.rstrip_step(step), style, common, iterating_var)
                        return result
                    elif out.lower() == 'q':
                        # quit
                        sys.exit()
                    else:
                        # runtime
                        self.is_run = False
                        self.timeout = Var.time_out
                        Var.time_out = 0.5
                        self.action_nalysis.action_analysis(out, style, common, iterating_var)
                        Var.time_out = self.timeout
                        continue
                except Exception as e:
                    Var.time_out = self.timeout
                    self.is_run = False
                    traceback.print_exc()
                    continue
        else:
            result = self.action_nalysis.action_analysis(step, style, common, iterating_var)
            return result


    def rstrip_step(self, step):
        if step.strip().endswith('--Debug') or step.strip().endswith('--debug'):
            return step.strip()[:-7].strip()
        return step