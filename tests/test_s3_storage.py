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
from custom_exceptions import BadConfigurationException
from storage_factory import StorageFactory


class TestS3Storage(unittest.TestCase):


  def test_s3_storage_creation_without_necessary_parameters(self):
    # Trying to create a S3Storage without the AWS_ACCESS_KEY should fail.
    self.assertRaises(BadConfigurationException, StorageFactory.get_storage, {
      "name" : "s3"
    })

    # Similarly, creating a S3Storage object without the AWS_SECRET_KEY
    # should fail.
    self.assertRaises(BadConfigurationException, StorageFactory.get_storage, {
      "name" : "s3",
      "AWS_ACCESS_KEY" : "access"
    })

    # Specifying both should result in the S3Storage object being created,
    # and instance variables set with those values.
    s3 = StorageFactory.get_storage({
      "name" : "s3",
      "AWS_ACCESS_KEY" : "access",
      "AWS_SECRET_KEY" : "secret"
    })
    self.assertEquals("access", s3.aws_access_key)
    self.assertEquals("secret", s3.aws_secret_key)

    # If S3_URL is specified, but it isn't a URL, an Exception should be thrown.
    self.assertRaises(BadConfigurationException, StorageFactory.get_storage, {
      "name" : "s3",
      "AWS_ACCESS_KEY" : "access",
      "AWS_SECRET_KEY" : "secret",
      "S3_URL" : "1.2.3.4:8773/services/Walrus"
    })

    # If S3_URL is specified, and is a URL, that should be fine.
    another_s3 = StorageFactory.get_storage({
      "name" : "s3",
      "AWS_ACCESS_KEY" : "access",
      "AWS_SECRET_KEY" : "secret",
      "S3_URL" : "http://1.2.3.4:8773/services/Walrus"
    })
    self.assertEquals("access", another_s3.aws_access_key)
    self.assertEquals("secret", another_s3.aws_secret_key)
    self.assertEquals("http://1.2.3.4:8773/services/Walrus", another_s3.s3_url)
