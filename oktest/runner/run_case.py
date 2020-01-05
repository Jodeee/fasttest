from oktest.common import Var
from oktest.runner.test_case import TestCase
from oktest.drivers.driver_base import DriverBase
from oktest.runner.case_analysis import CaseAnalysis


class RunCase(TestCase):

    def setUp(self):
        if Var.restart and not self.skip:
            DriverBase.startApp(Var.activity)

    def testCase(self):
        if self.skip:
            self.skipTest('skip')
        case = CaseAnalysis()
        case.iteration(self.steps)

    def tearDown(self):
        if Var.restart and not self.skip:
            DriverBase.stopApp(Var.package)
