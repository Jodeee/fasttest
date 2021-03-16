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
        config = '''driver: 'appium'
browser: 'chrome'
reStart: True
saveScreenshot: False
timeOut: 10
desiredCapabilities:
    - appium:
        - platformName: 'Android'
          udid: 'device_id'
          clear: True
          package: 'com.android.mobile'
          activity: 'com.android.mobile.Launcher'
          automationName: 'Appium'
          deviceName: 'HUWWEI P40 Pro'
          noReset: True
      macaca:
        - platformName: 'iOS'
          udid: 'device_id'
          clear: True
          bundleId: 'com.apple.mobilesafari'
          reuse: 3
      selenium:
        - maxWindow: True
          chrome:
              - driver: 'chromedriver_path'
                options: 
                    - '--headless'
                    - '--dissble-gpu'
                    - '--window-size=1920,1050'
          firefox:
              - driver: 'geckodriver_path'
                options: 
testcase:
    - TestCase/case.yaml
        '''
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
        common = '''CommonTest:
 description: 'common test'
 input: [value]
 output: []
 steps:
    - for ${i} in ${value}:
      - if ${i} == 3:
          - break
'''
        with open(common_path, "w") as f:
            f.write(common)

        case_path = os.path.join(dir, 'TestCase', 'case.yaml')
        case = '''module: test_module
skip: False
description: 'this is a test case'
steps:
    - ${t1} = $.id(1+2*3)
    
    - ${t2} = 6
    
    - assert ${t1} > ${t2}
    
    - ${ls} = ScriptsTest(${t2})
    
    - call CommonTest(${ls})
'''
        with open(case_path, "w") as f:
            f.write(case)

        scripts_path = os.path.join(dir, 'Scripts', 'case.py')
        scripts = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def ScriptsTest(value):
    l = range(value)
    return l
'''
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
                pass

    except Exception as e:
        print('usage: fasttest ... [-i init | -r [run]] [arg] ...')
        print("Try `fasttest -h' for more information.")
        sys.exit()

if __name__ == '__main__':
    main()