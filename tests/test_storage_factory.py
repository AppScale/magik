#!/usr/bin/env python
# Programmer: Chris Bunch (chris@appscale.com)
""" Tests for lib/storage_factory.py. """


# General-purpose Python library imports
import os
import sys
import unittest


# Third-party testing libraries
from flexmock import flexmock


# Storage factory import, the library that we're testing here
lib = os.path.dirname(__file__) + os.sep + ".."
sys.path.append(lib)
from magik.custom_exceptions import BadConfigurationException
from magik.storage_factory import StorageFactory


class TestStorageFactory(unittest.TestCase):


  def test_no_storage_specified(self):
    self.assertRaises(BadConfigurationException, StorageFactory.get_storage, {})


  def test_unsupported_storage_specified(self):
    self.assertRaises(NotImplementedError, StorageFactory.get_storage, {
      "name" : "not a supported storage system"
    })
