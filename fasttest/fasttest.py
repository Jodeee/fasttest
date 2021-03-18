#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import json
import getopt

def usage():
    print('usage: fasttest ... [-i init | -r [run]] [arg] ...')
    print('-i --init      :')
    print('-r --run       :')
    sys.exit()

def init_project(dir):
    '''
    create project
    :param path:
    :return:
    '''
    try:
        if not dir:
            print('Please enter a project name...')
            sys.exit()

        dirs = ['Common/Android', 'Common/iOS', 'Common/Selenium', 'Resource', 'Scripts', 'TestCase']
        for dir_ in dirs:
            path = os.path.join(dir, dir_)
            print('create {}...'.format(path))
            os.makedirs(path)

        config_path = os.path.join(dir, 'config.yaml')
        config = "driver: 'appium'\n" \
                 "browser: 'chrome'\n" \
                 "reStart: True\n" \
                 "clear: True\n" \
                 "saveScreenshot: False\n" \
                 "timeOut: 10\n" \
                 "desiredCapabilities:\n" \
                 "    - platformName: 'Android'\n" \
                 "      udid: 'device_id'\n" \
                 "      appPackage: 'com.android.mobile'\n" \
                 "      appActivity: 'com.android.mobile.Launcher'\n" \
                 "      automationName: 'Appium'\n" \
                 "      deviceName: 'HUWWEI P40 Pro'\n" \
                 "      noReset: True\n" \
                 "testcase:\n" \
                 "    - TestCase/case.yaml"
        with open(config_path, "w") as f:
            f.write(config)

        data_path = os.path.join(dir, 'data.json')
        data = {
            'variable':{},
            'resource':{},
            'keywords':['ScriptsTest']
        }
        with open(data_path, 'w') as f:
            json.dump(data, fp=f)

        common_path = os.path.join(dir, 'Common', 'common.yaml')
        common = "CommonTest:\n" \
                 " description: 'common test'\n" \
                 " input: [value]\n" \
                 " output: []\n" \
                 " steps:\n" \
                 "    - for ${i} in ${value}:\n" \
                 "        - if ${i} == 3:\n" \
                 "            - break"
        with open(common_path, "w") as f:
            f.write(common)

        case_path = os.path.join(dir, 'TestCase', 'case.yaml')
        case = "module: test_module\n" \
               "skip: False\n" \
               "description: 'this is a test case'\n" \
               "steps:\n" \
               "    - ${t1} = $.id(1+2*3)\n\n" \
               "    - ${t2} = 6\n\n" \
               "    - assert ${t1} > ${t2}\n\n" \
               "    - ${ls} = ScriptsTest(${t2})\n\n" \
               "    - call CommonTest(${ls})"

        with open(case_path, "w") as f:
            f.write(case)

        scripts_path = os.path.join(dir, 'Scripts', 'case.py')
        scripts = '#!/usr/bin/env python3\n' \
                  '# -*- coding: utf-8 -*-\n\n' \
                  'def ScriptsTest(value):\n\n' \
                  '    return [1,2,3,4,5,value]'
        with open(scripts_path, "w") as f:
            f.write(scripts)

    except Exception as e:
        print(e)

def main():
    '''
    :return:
    '''
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hi:r:', ['help', 'init=', 'run='])
        for o, a in opts:
            if o in ('-h', 'help'):
                usage()
            elif o in ('-i', '--init'):
                init_project(a)
            elif o in ('-r', '--run'):
                print('等我开发[狗头]...')

    except Exception as e:
        print('usage: fasttest ... [-i init | -r [run]] [arg] ...')
        print("Try `fasttest -h' for more information.")
        sys.exit()

if __name__ == '__main__':
    main()