from utest.common import Var
from utest.runner.test_case import TestCase
from utest.drivers.driver_base import DriverBase
from utest.runner.case_analysis import CaseAnalysis


class RunCase(TestCase):

    def setUp(self):
        if Var.restart:
            DriverBase.startApp(Var.activity)

    def testCase(self):
        case = CaseAnalysis()
        case.iteration(self.steps)

    def tearDown(self):
        if Var.restart:
            DriverBase.stopApp(Var.package)
