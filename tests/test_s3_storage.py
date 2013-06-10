#!/usr/bin/env python
# Programmer: Chris Bunch (chris@appscale.com)
""" Tests for lib/s3_storage.py. """


# General-purpose Python library imports
import os
import sys
import unittest


# Third-party libraries
import boto.s3.connection
import boto.s3.key
from flexmock import flexmock


# S3 storage import, the library that we're testing here
lib = os.path.dirname(__file__) + os.sep + ".." + os.sep + "magik"
sys.path.append(lib)
from custom_exceptions import BadConfigurationException
from storage_factory import StorageFactory


class TestS3Storage(unittest.TestCase):


  def setUp(self):
    # Set up a mock for when we interact with S3
    self.fake_s3 = flexmock(name='fake_s3')
    flexmock(boto.s3.connection)
    boto.s3.connection.should_receive('S3Connection').with_args(
      aws_access_key_id='access', aws_secret_access_key='secret') \
      .and_return(self.fake_s3)

    self.s3 = StorageFactory.get_storage({
      "name" : "s3",
      "AWS_ACCESS_KEY" : "access",
      "AWS_SECRET_KEY" : "secret"
    })


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
    flexmock(boto.s3.connection)
    boto.s3.connection.should_receive('S3Connection')
    another_s3 = StorageFactory.get_storage({
      "name" : "s3",
      "AWS_ACCESS_KEY" : "access",
      "AWS_SECRET_KEY" : "secret",
      "S3_URL" : "http://1.2.3.4:8773/services/Walrus"
    })
    self.assertEquals("access", another_s3.aws_access_key)
    self.assertEquals("secret", another_s3.aws_secret_key)
    self.assertEquals("http://1.2.3.4:8773/services/Walrus", another_s3.s3_url)


  def test_upload_one_file_and_create_bucket(self):
    file_one_info = {
      'source' : '/baz/boo/fbar1.tgz',
      'destination' : '/mybucket/files/fbar1.tgz'
    }

    # Presume that the local file does exist.
    flexmock(os.path)
    os.path.should_call('exists')
    os.path.should_receive('exists').with_args('/baz/boo/fbar1.tgz') \
      .and_return(True)

    # And presume that our bucket does not exist.
    self.fake_s3.should_receive('lookup').with_args('mybucket').and_return(None)

    # We thus need to be able to create the bucket.
    fake_bucket = flexmock(name='name_bucket')
    self.fake_s3.should_receive('create_bucket').with_args('mybucket') \
      .and_return(fake_bucket)

    # Also, presume that we can upload the file fine.
    fake_key = flexmock(name='fake_key')
    flexmock(boto.s3.key)
    boto.s3.key.should_receive('Key').with_args(fake_bucket).and_return(
      fake_key)
    fake_key.should_receive('key').with_args('files/fbar1.tgz')
    fake_key.should_receive('set_contents_from_filename') \
      .with_args('/baz/boo/fbar1.tgz')

    # Finally, make sure we can upload our file successfully.
    upload_info = [file_one_info]
    actual = self.s3.upload_files(upload_info)
    for upload_result in actual:
      self.assertEquals(True, upload_result['success'])


  def test_upload_two_files_that_exist(self):
    # Set up mocks for the first file.
    file_one_info = {
      'source' : '/baz/boo/fbar1.tgz',
      'destination' : '/mybucket/files/fbar1.tgz'
    }

    # Presume that the local file does exist.
    flexmock(os.path)
    os.path.should_call('exists')
    os.path.should_receive('exists').with_args('/baz/boo/fbar1.tgz') \
      .and_return(True)

    # And presume that our bucket exists.
    fake_bucket = flexmock(name='name_bucket')
    self.fake_s3.should_receive('lookup').with_args('mybucket').and_return(
      fake_bucket)

    # Also, presume that we can upload the file fine.
    fake_key = flexmock(name='fake_key')
    flexmock(boto.s3.key)
    boto.s3.key.should_receive('Key').with_args(fake_bucket).and_return(
      fake_key)
    fake_key.should_receive('key').with_args('files/fbar1.tgz')
    fake_key.should_receive('set_contents_from_filename') \
      .with_args('/baz/boo/fbar1.tgz')

    # Set up mocks for the second file.
    file_two_info = {
      'source' : '/baz/boo/fbar2.tgz',
      'destination' : '/mybucket/files/fbar2.tgz'
    }

    # Presume that the local file does exist.
    os.path.should_receive('exists').with_args('/baz/boo/fbar2.tgz') \
      .and_return(True)

    # Also, presume that we can upload the file fine.
    fake_key.should_receive('key').with_args('files/fbar2.tgz')
    fake_key.should_receive('set_contents_from_filename') \
      .with_args('/baz/boo/fbar2.tgz')

    # Finally, make sure we can upload our files successfully.
    upload_info = [file_one_info, file_two_info]
    actual = self.s3.upload_files(upload_info)
    for upload_result in actual:
      self.assertEquals(True, upload_result['success'])


  def test_download_two_files_that_exist(self):
    # Set up mocks for the first file.
    file_one_info = {
      'source' : '/mybucket/files/fbar1.tgz',
      'destination' : '/baz/boo/fbar1.tgz'
    }

    # And presume that our bucket exists.
    fake_bucket = flexmock(name='name_bucket')
    self.fake_s3.should_receive('lookup').with_args('mybucket').and_return(
      fake_bucket)

    # Presume that our first file does exist.
    fake_key = flexmock(name='fake_key')
    flexmock(boto.s3.key)
    boto.s3.key.should_receive('Key').with_args(fake_bucket).and_return(
      fake_key)
    fake_key.should_receive('key').with_args('boo/fbar1.tgz')
    fake_key.should_receive('exists').and_return(True)

    # And presume that we can write to the local filesystem.
    fake_key.should_receive('get_contents_to_filename').with_args(
      '/baz/boo/fbar1.tgz')

    # Set up mocks for the second file.
    file_two_info = {
      'source' : '/mybucket/files/fbar2.tgz',
      'destination' : '/baz/boo/fbar2.tgz'
    }

    # Presume that our second file does exist.
    fake_key.should_receive('key').with_args('boo/fbar2.tgz')
    fake_key.should_receive('exists').and_return(True)

    # And presume that we can write to the local filesystem.
    fake_key.should_receive('get_contents_to_filename').with_args(
      '/baz/boo/fbar2.tgz')

    # Finally, make sure we can download our files successfully.
    download_info = [file_one_info, file_two_info]
    actual = self.s3.download_files(download_info)
    for download_result in actual:
      self.assertEquals(True, download_result['success'])
