from fasttest.common import Var
from fasttest.runner.test_case import TestCase
from fasttest.drivers.driver_base import DriverBase
from fasttest.runner.case_analysis import CaseAnalysis


class RunCase(TestCase):

    def setUp(self):
        if Var.restart:
            DriverBase.launch_app(None)
        if self.skip:
            self.skipTest('skip')

    def testCase(self):
        case = CaseAnalysis()
        case.iteration(self.steps)

    def tearDown(self):
        if Var.restart:
            DriverBase.close_app(None)
