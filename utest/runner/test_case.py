#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import unittest
import traceback
from utest.common import *


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
        setattr(self, 'driver', Var.driver)
        setattr(self, 'testcase_path', Var.testcase_path)
        setattr(self, 'module', Var.module)
        setattr(self, 'description', Var.description)
        setattr(self, 'skip', Var.skip)
        setattr(self, 'steps', Var.steps)
        self.SnapshotDir = os.path.join(Var.Report, self.module, self.testcase_path.split(os.sep)[-1].split(".")[0])

    def run(self, result=None):

        try:
            Var.CaseMessage = ""
            Var.CaseStepIndex = 0
            Var.SnapshotIndex = 0
            Var.SnapshotDir = self.SnapshotDir
            if not os.path.exists(Var.SnapshotDir):
                os.makedirs(Var.SnapshotDir)
            log_info("******************* TestCase {} Start *******************".format(self.description))
            unittest.TestCase.run(self, result)
            log_info("******************* Total: {}, Pass: {}, Failed: {}, Error: {}, Skipped: {} ********************"
                    .format(result.testsRun, len(result.successes), len(result.failures), len(result.errors), len(result.skipped)))
        except:
            traceback.print_exc()