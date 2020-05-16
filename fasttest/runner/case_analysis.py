#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fasttest.runner.action_analysis import ActionAnalysis

class CaseAnalysis(object):

    def __init__(self):
        self.action_nalysis = ActionAnalysis()
        self.testcase_steps = []

    def iteration(self, steps):

        if not self.testcase_steps:
            self.getstep(steps)

        if isinstance(steps, list):
            for step in steps:
                if isinstance(step, str):
                    self.case_executor(step)
                    if step == 'break':
                        return True
                elif isinstance(step, dict):
                    result = self.iteration(step)
                    if result:
                        return True
        elif isinstance(steps, dict):
            for key, values in steps.items():
                if key.startswith('while'):
                    while self.case_executor(key):
                        result = self.iteration(values)
                        if result:
                            break
                elif key.startswith('if') or key.startswith('elif') or key.startswith('else'):
                    if self.case_executor(key):
                        result = self.iteration(values)
                        if result:
                            return True
                        break
                else:
                    raise SyntaxError('- {}:'.format(key))

    def getstep(self,steps):
        for step in steps:
            if isinstance(step, dict):
                for key, value in step.items():
                    self.testcase_steps.append(key)
                    self.getstep(value)
            elif isinstance(step, list):
                self.getstep(step)
            elif isinstance(step, str):
                self.testcase_steps.append(step)

    def case_executor(self, step):
        result = self.action_nalysis.action_analysis(step)
        return result