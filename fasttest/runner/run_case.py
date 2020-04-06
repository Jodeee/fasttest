from fasttest.common import Var
from fasttest.runner.test_case import TestCase
from fasttest.drivers.driver_base import DriverBase
from fasttest.runner.case_analysis import CaseAnalysis


class RunCase(TestCase):

    def setUp(self):
        if Var.restart and not self.skip:
            DriverBase.launch_app(None)

    def testCase(self):
        if self.skip:
            self.skipTest('skip')
        case = CaseAnalysis()
        case.iteration(self.steps)

    def tearDown(self):
        if Var.restart and not self.skip:
            DriverBase.close_app(None)
