#!/usr/bin/python
import optparse
import sys
# Install the Python unittest package before you run this script.
import unittest

USAGE = """%prog SDK_PATH TEST_PATH
Run unit tests for App Engine apps.

SDK_PATH    Path to the SDK installation
TEST_PATH   Path to package containing test modules"""


def main(sdk_path, test_path):
    sys.path.insert(0, sdk_path)
    import dev_appserver
    dev_appserver.fix_sys_path()

    from google.appengine.dist import use_library
    use_library('django', '1.2')

    suite = unittest.loader.TestLoader().discover(test_path)
    unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == '__main__':
    parser = optparse.OptionParser(USAGE)
    options, args = parser.parse_args()
    SDK_PATH = '/usr/local/google_appengine'
    TEST_PATH = '.'
        
    if len(args) == 1:
        TEST_PATH = args[0]
    #    print 'Error: Exactly 2 arguments required.'
    #    parser.print_help()
    #    sys.exit(1)
    #SDK_PATH = args[0]
    #TEST_PATH = args[1]
    
    main(SDK_PATH, TEST_PATH)