#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import time
import json
import unittest
from fasttest.common import Var, Dict, DictEncoder
from fasttest.result.test_result import TestResult
from fasttest.result.html_result import HTMLTestRunner


class TestRunner(unittest.TextTestRunner):

    def __init__(self,stream=sys.stderr,
                 descriptions=True, verbosity=1,
                 failfast=False, buffer=False,resultclass=None):
        unittest.TextTestRunner.__init__(self, stream, descriptions, verbosity,
                                failfast=failfast, buffer=buffer)
        self.descriptions = descriptions
        self.verbosity = verbosity
        self.failfast = failfast
        self.buffer = buffer
        if resultclass is None:
            self.resultclass = TestResult
        else:
            self.resultclass = resultclass

    def _makeResult(self):
            return  self.resultclass(self.stream,self.descriptions,self.verbosity)

    def run(self, test):
        '''
        :param test:
        :return:
        '''
        result = self._makeResult()
        result.failfast = self.failfast
        result.buffer = self.buffer
        starTime = time.time()
        test(result)
        stopTime = time.time()

        test_result = Dict()
        for modulek, modulev in result.result.items():
            test_list = []
            for info in modulev:
                case_info = Dict({
                    'caseName': info.case_name,
                    'casePath': info.case_path,
                    'dataId': info.data_id,
                    'description': info.description,
                    'moduleName': info.module_name,
                    'report': info.report,
                    'snapshotDir': info.snapshot_dir,
                    'startTime': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(info.start_time)),
                    'duration': str(int(info.stop_time - info.start_time)) + 's',
                    'status': info.status,
                    'err': info.err,
                    'steps': info.test_case_steps
                })
                test_list.append(case_info)
            test_result[modulek] = test_list

        failures_list = []
        for failure in result.failures:
            cast_info = failure[0]
            failures_list.append(cast_info.test_case_path)

        errors_list = []
        for errors in result.errors:
            cast_info = errors[0]
            errors_list.append(cast_info.test_case_path)

        result = Dict({
            'report': result.report,
            'total': result.testsRun,
            'successes': len(result.successes),
            'failures': len(result.failures),
            'errors': len(result.errors),
            'skipped': len(result.skipped),
            'startTime': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(starTime)),
            'duration': str(int(stopTime - starTime)) + 's',
            'result': test_result,
            'errorsList': errors_list,
            'failuresList': failures_list
        })

        properties_path = os.path.join(Var.root, 'result.properties')
        with open(properties_path, "w") as f:
            f.write(f'report={result.report}\n')
            f.write(f'total={result.total}\n')
            f.write(f'successes={result.successes}\n')
            f.write(f'failures={result.failures}\n')
            f.write(f'errors={result.errors}\n')
            f.write(f'skipped={result.skipped}\n')

        json_path = os.path.join(result.report, 'result.json')
        with open(json_path, 'w') as f:
            json.dump(result, fp=f, cls=DictEncoder, indent=4)

        html_file = os.path.join(Var.report,'report.html')
        fp = open(html_file,'wb')
        html_runner = HTMLTestRunner(stream=fp,
                                     title='Test Results',
                                     description='Test')
        html_runner.generate_report(result)
        Var.all_result = result
        fp.close()

        return result




