#!/usr/bin/env python
# Programmer: Chris Bunch (chris@appscale.com)
""" Tests for lib/s3_storage.py. """


# General-purpose Python library imports
import os
import sys
import unittest


# Third-party testing libraries
from flexmock import flexmock


# S3 storage import, the library that we're testing here
lib = os.path.dirname(__file__) + os.sep + ".." + os.sep + "magik"
sys.path.append(lib)
from storage_factory import StorageFactory


class TestS3Storage(unittest.TestCase):


  def test_upload_files(self):
    s3 = StorageFactory.get_storage({})
