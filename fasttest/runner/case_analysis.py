#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fasttest.common import log_info
from fasttest.runner.case_executor import CaseExecutor

class CaseAnalysis(object):

    def __init__(self):
        self.CaseExecutor = CaseExecutor()

    def iteration(self, steps):

        if isinstance(steps, list):
            for step in steps:
                if isinstance(step, str):
                    self.CaseExecutor.case_executor(step)
                    if step == 'break':
                        return True
                elif isinstance(step, dict):
                    result = self.iteration(step)
                    if result:
                        return True
        elif isinstance(steps, dict):
            for key, values in steps.items():
                if key.startswith('while'):
                    while self.CaseExecutor.case_executor(key):
                        result = self.iteration(values)
                        if result:
                            break
                elif key.startswith('if') or key.startswith('elif') or key.startswith('else'):
                    if self.CaseExecutor.case_executor(key):
                        result = self.iteration(values)
                        if result:
                            return True