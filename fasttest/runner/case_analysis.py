#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fasttest.runner.action_analysis import ActionAnalysis
from fasttest.runner.action_executor import ActionExecutor

class CaseAnalysis(object):

    def __init__(self):
        self.action_executor = ActionExecutor()
        self.action_nalysis = ActionAnalysis()

    def iteration(self, steps):

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

    def case_executor(self, step):
        action = self.action_nalysis.action_analysis(step)
        if action:
            result = self.action_executor.action_executor(action)
        else:
            result = None
        return result