#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import getopt
import traceback
from concurrent import futures
from fasttest.version import VERSION
from fasttest.project import *

def _usage():
    print('')
    print('  usage: fasttest [-h|-v|] [arg] ...')
    print('')
    print('  options:')
    print('')
    print('    -h, --help      show help screen and exit.')
    print('    -V, --Version   show version.')
    print('    -i, --init      specify a project name and create the project.')
    print('    -r, --run       specify the project path and run the project.')
    print('    -w, --workers   specify number of threads.')
    print('')
    sys.exit()

def _init_project(dir):

    try:
        if not dir:
            print('Please enter a project name...')
            sys.exit()

        dirs = ['Common/Android', 'Common/iOS', 'Common/Selenium', 'Resource', 'Scripts', 'TestCase']
        for dir_ in dirs:
            path = os.path.join(dir, dir_)
            print('create directory: {}'.format(path))
            os.makedirs(path)

        config_path = os.path.join(dir, 'config.yaml')
        with open(config_path, "w") as f:
            print('create file: {}'.format(config_path))
            config = "driver: 'appium'\n" \
                     "reStart: True\n" \
                     "saveScreenshot: False\n" \
                     "timeOut: 10\n" \
                     "desiredCapabilities:\n" \
                     "    platformName: 'Android'\n" \
                     "    udid: 'device_id'\n" \
                     "    appPackage: 'com.android.mobile'\n" \
                     "    appActivity: 'com.android.mobile.Launcher'\n" \
                     "    automationName: 'Appium'\n" \
                     "    deviceName: 'HUWWEI P40 Pro'\n" \
                     "    noReset: True\n" \
                     "testcase:\n" \
                     "    - TestCase/case.yaml"
            f.write(config)

        data_path = os.path.join(dir, 'data.yaml')
        with open(data_path, 'w') as f:
            print('create file: {}'.format(data_path))
            config = "variable:\n" \
                     "    userid: 'admin'\n" \
                     "    password: '13456'\n" \
                     "resource:\n" \
                     "    logo: 'Resource/logo.png'\n" \
                     "keywords:\n" \
                     "  - 'ScriptsTest'\n"
            f.write(config)

        common_path = os.path.join(dir, 'Common', 'common.yaml')
        with open(common_path, "w") as f:
            print('create file: {}'.format(common_path))
            common = "CommonTest:\n" \
                     " description: 'common test'\n" \
                     " input: [value]\n" \
                     " output: []\n" \
                     " steps:\n" \
                     "    - for ${i} in ${value}:\n" \
                     "        - if ${i} == 3:\n" \
                     "            - break"
            f.write(common)

        case_path = os.path.join(dir, 'TestCase', 'case.yaml')
        with open(case_path, "w") as f:
            print('create file: {}'.format(case_path))
            case = "module: test_module\n" \
                   "skip: False\n" \
                   "description: 'this is a test case'\n" \
                   "steps:\n" \
                   "    - ${t1} = $.id(1+2*3)\n\n" \
                   "    - ${t2} = 6\n\n" \
                   "    - assert ${t1} > ${t2}\n\n" \
                   "    - ${ls} = ScriptsTest(${t2})\n\n" \
                   "    - call CommonTest(${ls})"
            f.write(case)

        scripts_path = os.path.join(dir, 'Scripts', 'case.py')
        with open(scripts_path, "w") as f:
            print('create file: {}'.format(scripts_path))
            scripts = '#!/usr/bin/env python3\n' \
                      '# -*- coding: utf-8 -*-\n\n' \
                      'def ScriptsTest(value):\n\n' \
                      '    return [1,2,3,4,5,value]'
            f.write(scripts)
        print('create project successfully.')

    except Exception as e:
        raise e

def _start_project(workers, path):

    if workers <= 1:
        project = Project(path=path)
        result = project.start()
        return result
    else:
        result_list = []
        with futures.ThreadPoolExecutor() as t:
            worker_list = []
            for index in range(workers):
                run_info = {
                    'index': index,
                    'workers': workers,
                    'path': path
                }
                worker_list.append(t.submit(_run_project, run_info))

            for f in futures.as_completed(worker_list):
                if f.result() is not None:
                    result = f.result()
                    result_list.append(result)
                if f.exception():
                    print(f.exception())
        return result_list

def _run_project(run_info):

    try:
        index = run_info['index']
        workers = run_info['workers']
        path = run_info['path']
        project = Project(index=index, workers=workers, path=path)
        result = project.start()
        return result
    except Exception as e:
        traceback.print_exc()
        return None

def main():
    '''
    :return:
    '''
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hVi:r:w:', ['help', 'Version', 'init=', 'run=', 'workers='])
    except:
        _usage()
    project_path = '.'
    workers = 1
    for o, a in opts:
        if o in ('-h', '--help'):
            _usage()
        elif o in ('-V', '--Version'):
            print(VERSION)
            sys.exit()
        elif o in ('-i', '--init'):
            _init_project(a)
            sys.exit()
        elif o in ('-r', '--run'):
            project_path = a
        elif o in ('-w', '--workers'):
            workers = int(a)
        else:
            _usage()
    if not os.path.isdir(project_path):
        print('No such directory: {}'.format(project_path))
        _usage()
    start_time = time.time()
    result = _start_project(workers, project_path)
    end_time = time.time()
    print('run time: {}s'.format(int(end_time-start_time)))
    if isinstance(result, list):
        for r in result:
            print('\n')
            for k, v in r.items():
                if k == 'result':
                    continue
                print('{}: {}'.format(k, v))
    else:
        for k, v in result.items():
            if k == 'result':
                continue
            print('{}: {}'.format(k, v))

if __name__ == '__main__':
    main()