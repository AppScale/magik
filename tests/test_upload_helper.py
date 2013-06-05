#!/usr/bin/env python
# Programmer: Chris Bunch (chris@appscale.com)
""" Tests for lib/upload.py. """


# General-purpose Python library imports
import os
import sys
import unittest


# Third-party testing libraries
from flexmock import flexmock


# Upload Helper import, the library that we're testing here
lib = os.path.dirname(__file__) + os.sep + ".." + os.sep + "storage"
sys.path.append(lib)


class TestUploadHelper(unittest.TestCase):


  def test_nothing_yet(self):
    pass
