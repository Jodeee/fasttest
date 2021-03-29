from fasttest.common import Var
from fasttest.runner.test_case import TestCase
from fasttest.drivers.driver_base_app import DriverBaseApp
from fasttest.drivers.driver_base_web import DriverBaseWeb
from fasttest.runner.case_analysis import CaseAnalysis


class RunCase(TestCase):

    def setUp(self):
        if self.skip:
            self.skipTest('skip')
        if Var.re_start:
            if Var.driver != 'selenium':
                DriverBaseApp.launch_app(None)
            else:
                DriverBaseWeb.createSession()

    def testCase(self):
        case = CaseAnalysis()
        case.iteration(self.steps)

    def tearDown(self):
        if Var.re_start:
            try:
                if Var.driver != 'selenium':
                    DriverBaseApp.close_app(None)
                else:
                    DriverBaseWeb.quit()
            except:
                pass
