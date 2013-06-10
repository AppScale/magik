#!/usr/bin/env python
# Programmer: Chris Bunch (chris@appscale.com)
""" Tests for lib/rest_server.py. """


# General-purpose Python library imports
import os
import sys
import unittest


# Third-party libraries
from flexmock import flexmock


# RESTServer import, the library that we're testing here
lib = os.path.dirname(__file__) + os.sep + ".." + os.sep + "magik"
sys.path.append(lib)
from rest_server import RESTServer


class TestRESTServer(unittest.TestCase):


  def test_nothing_yet(self):
    pass
