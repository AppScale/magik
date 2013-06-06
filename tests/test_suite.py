#!/usr/bin/env python
# Programmer: Chris Bunch

import sys
import unittest


# imports for upload helper tests
from test_upload_helper import TestUploadHelper

test_cases = [TestUploadHelper]

test_case_names = []
for cls in test_cases:
  test_case_names.append(str(cls.__name__))

appscale_test_suite = unittest.TestSuite()
run_test_cases = test_case_names

for test_class, test_name in zip(test_cases,test_case_names):
  if test_name in run_test_cases:
    tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
    appscale_test_suite.addTests(tests)

all_tests = unittest.TestSuite([appscale_test_suite])
unittest.TextTestRunner(verbosity=2).run(all_tests)