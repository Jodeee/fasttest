#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
import unittest
import traceback
from fasttest.common import *


class TestCase(unittest.TestCase):
    def __getattr__(self, item):
        try:
            return self.__getattribute__(item)
        except:
            attrvalue = None
            self.__setattr__(item, attrvalue)
            return attrvalue

    def __init__(self, methodName="runTest"):
        super(TestCase, self).__init__(methodName)
        for key, value in Var.case_info.items():
            setattr(self, key, value)
        self.snapshot_dir = os.path.join(Var.report,'Steps', self.module, self.test_case_path.split('/')[-1].split(os.sep)[-1].split(".")[0])
        self.report = Var.report

    def run(self, result=None):

        try:
            Var.case_step_index = 0
            Var.case_snapshot_index = 0
            Var.snapshot_dir = self.snapshot_dir
            testcase_steps = []
            if not os.path.exists(Var.snapshot_dir):
                os.makedirs(Var.snapshot_dir)
            with open(self.test_case_path, 'r', encoding='UTF-8') as r:
                s = r.readlines()
                index = s.index('steps:\n')
                for step in s[index+1:]:
                    if not (step.lstrip().startswith('#') or re.match('#', step.lstrip().lstrip('-').lstrip())):
                        if step != '\n':
                            testcase_steps.append(step)
            log_info("******************* TestCase {} Start *******************".format(self.description))
            unittest.TestCase.run(self, result)
            log_info("******************* Total: {}, Success: {}, Failed: {}, Error: {}, Skipped: {} ********************\n"
                    .format(result.testsRun, len(result.successes), len(result.failures), len(result.errors), len(result.skipped)))
        except:
            traceback.print_exc()