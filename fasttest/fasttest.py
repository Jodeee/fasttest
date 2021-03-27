#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import getopt
from fasttest.version import VERSION

def usage():
    print('')
    print('  usage: fasttest [-h|-v|] [arg] ...')
    print('')
    print('  options:')
    print('')
    print('    -h, --help      show help screen and exit.')
    print('    -V, --Version   show version.')
    print('    -i, --init      create a project, specify a project name.')
    print('    -r, --run       running the current project.')
    print('')
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
                     "    - platformName: 'Android'\n" \
                     "      udid: 'device_id'\n" \
                     "      appPackage: 'com.android.mobile'\n" \
                     "      appActivity: 'com.android.mobile.Launcher'\n" \
                     "      automationName: 'Appium'\n" \
                     "      deviceName: 'HUWWEI P40 Pro'\n" \
                     "      noReset: True\n" \
                     "testcase:\n" \
                     "    - TestCase/case.yaml"
            f.write(config)

        data_path = os.path.join(dir, 'data.yaml')
        with open(data_path, 'w') as f:
            print('create file: {}'.format(data_path))
            config = "variable:\n" \
                     "  - userid: 'admin'\n" \
                     "  - password: '13456'\n" \
                     "resource:\n" \
                     "  - logo: 'Resource/logo.png'\n" \
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
        print(e)

def main():
    '''
    :return:
    '''
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hVi:r:', ['help','Version', 'init=', 'run='])
        for o, a in opts:
            if o in ('-h', '--help'):
                usage()
            elif o in ('-V', '--Version'):
                print(VERSION)
            elif o in ('-i', '--init'):
                init_project(a)
            elif o in ('-r', '--run'):
                print('等我开发完[狗头]...')
            else:
                raise
    except Exception as e:
        print('usage: fasttest ... [-i init | -r [run]] [arg] ...')
        print("try 'fasttest -h' for more information.")
        sys.exit()

if __name__ == '__main__':
    main()