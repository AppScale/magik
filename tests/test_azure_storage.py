#!/usr/bin/env python
# Programmer: Chris Bunch (chris@appscale.com)
""" Tests for lib/azure_storage.py. """


# General-purpose Python library imports
import os
import sys
import unittest


# Third-party libraries
import azure.storage
from flexmock import flexmock


# S3 storage import, the library that we're testing here
lib = os.path.dirname(__file__) + os.sep + ".." + os.sep + "magik"
sys.path.append(lib)
from custom_exceptions import BadConfigurationException
from storage_factory import StorageFactory


class TestAzureStorage(unittest.TestCase):


  def setUp(self):
    # Set up a mock for when we interact with S3
    self.fake_azure = flexmock(name='fake_azure')
    #flexmock(boto.s3.connection)
    #boto.s3.connection.should_receive('S3Connection').with_args(
    #  aws_access_key_id='access', aws_secret_access_key='secret') \
    #  .and_return(self.fake_azure)

    self.azure = StorageFactory.get_storage({
      "name" : "azure",
      "AZURE_ACCOUNT_NAME" : "access",
      "AZURE_ACCOUNT_KEY" : "secret"
    })


  def test_azure_storage_creation_without_necessary_parameters(self):
    # Trying to create an AzureStorage without the account name should fail.
    self.assertRaises(BadConfigurationException, StorageFactory.get_storage, {
      "name" : "azure"
    })

    # Similarly, creating a AzureStorage object without the account key
    # should fail.
    self.assertRaises(BadConfigurationException, StorageFactory.get_storage, {
      "name" : "azure",
      "AZURE_ACCOUNT_NAME" : "access"
    })

    # Specifying both should result in the AzureStorage object being created,
    # and instance variables set with those values.
    azure = StorageFactory.get_storage({
      "name" : "azure",
      "AZURE_ACCOUNT_NAME" : "access",
      "AZURE_ACCOUNT_KEY" : "secret"
    })
    self.assertEquals("access", azure.azure_account_name)
    self.assertEquals("secret", azure.azure_account_key)


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
    #self.fake_azure.should_receive('lookup').with_args('mybucket').and_return(None)

    # We thus need to be able to create the bucket.
    #fake_bucket = flexmock(name='name_bucket')
    #self.fake_azure.should_receive('create_bucket').with_args('mybucket') \
    #  .and_return(fake_bucket)

    # Also, presume that we can upload the file fine.
    #fake_key = flexmock(name='fake_key')
    #flexmock(boto.s3.key)
    #boto.s3.key.should_receive('Key').with_args(fake_bucket).and_return(
    #  fake_key)
    #fake_key.should_receive('key').with_args('files/fbar1.tgz')
    #fake_key.should_receive('set_contents_from_filename') \
    #  .with_args('/baz/boo/fbar1.tgz')

    # Finally, make sure we can upload our file successfully.
    upload_info = [file_one_info]
    actual = self.azure.upload_files(upload_info)
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
    #fake_bucket = flexmock(name='name_bucket')
    #self.fake_azure.should_receive('lookup').with_args('mybucket').and_return(
    #  fake_bucket)

    # Also, presume that we can upload the file fine.
    #fake_key = flexmock(name='fake_key')
    #flexmock(boto.s3.key)
    #boto.s3.key.should_receive('Key').with_args(fake_bucket).and_return(
    #  fake_key)
    #fake_key.should_receive('key').with_args('files/fbar1.tgz')
    #fake_key.should_receive('set_contents_from_filename') \
    #  .with_args('/baz/boo/fbar1.tgz')

    # Set up mocks for the second file.
    file_two_info = {
      'source' : '/baz/boo/fbar2.tgz',
      'destination' : '/mybucket/files/fbar2.tgz'
    }

    # Presume that the local file does exist.
    os.path.should_receive('exists').with_args('/baz/boo/fbar2.tgz') \
      .and_return(True)

    # Also, presume that we can upload the file fine.
    #fake_key.should_receive('key').with_args('files/fbar2.tgz')
    #fake_key.should_receive('set_contents_from_filename') \
    #  .with_args('/baz/boo/fbar2.tgz')

    # Finally, make sure we can upload our files successfully.
    upload_info = [file_one_info, file_two_info]
    actual = self.azure.upload_files(upload_info)
    for upload_result in actual:
      self.assertEquals(True, upload_result['success'])


  def test_download_one_file_that_doesnt_exist(self):
    # Set up mocks for the first file.
    file_one_info = {
      'source' : '/mybucket/files/fbar1.tgz',
      'destination' : '/baz/boo/fbar1.tgz'
    }

    # And presume that our bucket does not exist.
    #fake_bucket = flexmock(name='name_bucket')
    #self.fake_azure.should_receive('lookup').with_args('mybucket').and_return(None)

    # Finally, make sure we can't download our file.
    download_info = [file_one_info]
    actual = self.azure.download_files(download_info)
    for download_result in actual:
      self.assertEquals(False, download_result['success'])
      self.assertEquals('bucket not found', download_result['failure_reason'])


  def test_download_two_files_that_exist(self):
    # Set up mocks for the first file.
    file_one_info = {
      'source' : '/mybucket/files/fbar1.tgz',
      'destination' : '/baz/boo/fbar1.tgz'
    }

    # And presume that our bucket exists.
    #fake_bucket = flexmock(name='name_bucket')
    #self.fake_azure.should_receive('lookup').with_args('mybucket').and_return(
    #  fake_bucket)

    # Presume that our first file does exist.
    #fake_key = flexmock(name='fake_key')
    #flexmock(boto.s3.key)
    #boto.s3.key.should_receive('Key').with_args(fake_bucket).and_return(
    #  fake_key)
    #fake_key.should_receive('key').with_args('boo/fbar1.tgz')
    #fake_key.should_receive('exists').and_return(True)

    # And presume that we can write to the local filesystem.
    #fake_key.should_receive('get_contents_to_filename').with_args(
    #  '/baz/boo/fbar1.tgz')

    # Set up mocks for the second file.
    file_two_info = {
      'source' : '/mybucket/files/fbar2.tgz',
      'destination' : '/baz/boo/fbar2.tgz'
    }

    # Presume that our second file does exist.
    #fake_key.should_receive('key').with_args('boo/fbar2.tgz')
    #fake_key.should_receive('exists').and_return(True)

    # And presume that we can write to the local filesystem.
    #fake_key.should_receive('get_contents_to_filename').with_args(
    #  '/baz/boo/fbar2.tgz')

    # Finally, make sure we can download our files successfully.
    download_info = [file_one_info, file_two_info]
    actual = self.azure.download_files(download_info)
    for download_result in actual:
      self.assertEquals(True, download_result['success'])
