#!/usr/bin/env python
# Programmer: Chris Bunch (chris@appscale.com)
""" Tests for lib/rest_server.py. """


# General-purpose Python library imports
import os
import sys
import unittest
import uuid


# Third-party libraries
from flexmock import flexmock


# RESTServer import, the library that we're testing here
lib = os.path.dirname(__file__) + os.sep + ".." + os.sep + "magik"
sys.path.append(lib)
from rest_server import RESTServer
from storage_factory import StorageFactory


class TestRESTServer(unittest.TestCase):


  def test_put_route_without_body(self):
    # If the user fails to pass in a request body, it should fail.
    server = RESTServer()
    server.request = flexmock(body='')
    server.response = flexmock()
    server.response.should_receive('write').and_return()
    self.assertEquals(RESTServer.FAILURE, server.put('baz/gbaz.txt'))


  def test_put_route_with_s3_credentials(self):
    # Allow the user to store data in Amazon S3 if they specify all the
    # correct credentials.
    server = RESTServer()
    server.request = flexmock(body='file contents')

    # Presume that the user has only specified S3 credentials.
    server.request.should_receive('get').with_args('name').and_return('s3')
    server.request.should_receive('get').with_args('AWS_ACCESS_KEY').and_return(
      'access')
    server.request.should_receive('get').with_args('AWS_SECRET_KEY').and_return(
      'secret')
    server.request.should_receive('get').with_args('GCS_ACCESS_KEY').and_return(
      '')
    server.request.should_receive('get').with_args('GCS_SECRET_KEY').and_return(
      '')
    server.request.should_receive('get').with_args('S3_URL').and_return('')
    server.request.should_receive('get').with_args('AZURE_ACCOUNT_NAME') \
      .and_return('')
    server.request.should_receive('get').with_args('AZURE_ACCOUNT_KEY') \
      .and_return('')

    # Mock out writing the file contents that were sent over.
    flexmock(uuid)
    uuid.should_receive('uuid4').and_return('123')

    fake_file = flexmock(name='fake_file')
    fake_file.should_receive('write').with_args('file contents')

    fake_builtins = flexmock(sys.modules['__builtin__'])
    fake_builtins.should_call('open')
    fake_builtins.should_receive('open').with_args('/tmp/magik-temp-123', 'w') \
      .and_return(fake_file)

    # Mock out interacting with S3.
    fake_storage = flexmock(name='fake_storage')
    fake_storage.should_receive('upload_files').with_args([{
      'source' : '/tmp/magik-temp-123',
      'destination' : '/baz/gbaz.txt'
    }])

    flexmock(StorageFactory)
    StorageFactory.should_receive('get_storage').with_args(dict).and_return(
      fake_storage)

    # Mock out writing the response.
    server.response = flexmock()
    server.response.should_receive('write').and_return()

    # Finally, mock out removing the tempfile we created.
    flexmock(os)
    os.should_receive('remove').with_args('/tmp/magik-temp-123')

    self.assertEquals(RESTServer.SUCCESS, server.put('baz/gbaz.txt'))
