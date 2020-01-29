#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fasttest.runner.action_analysis import ActionAnalysis
from fasttest.runner.action_executor import ActionExecutor

class CaseExecutor(object):

    def __init__(self):
        self.ActionExecutor = ActionExecutor()
        self.ActionAnalysis = ActionAnalysis()

    def case_executor(self, step):
        action = self.ActionAnalysis.action_analysis(step)
        result = self.ActionExecutor.action_executor(action)
        return result