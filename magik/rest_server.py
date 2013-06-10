#!/usr/bin/env python
# Programmer: Chris Bunch (chris@appscale.com)
""" rest_server.py defines two classes: RESTServer and MagikUI.

RESTServer defines RESTful routes to store and retrieve data, and MagikUI
provides a web client that talks to these routes

See bin/magik-server for how this server is started and controlled. """


# General-purpose Python library imports
import json
import os
import sys
import uuid


# Third-party library imports
import webapp2


# Magik library imports
from storage_factory import StorageFactory


class RESTServer(webapp2.RequestHandler):


  SUCCESS = 'success'


  FAILURE = 'failure'

 
  def get(self, path):
    args = self.get_args_from_request_params(self.request)
    storage = StorageFactory.get_storage(args)

    random_suffix = str(uuid.uuid4()).replace('-', '')[:10]
    destination = '/tmp/magik-temp-{0}'.format(random_suffix)
    source_to_dest_list = [{
      'source' : path,
      'destination' : destination
    }]
    storage.download_files(source_to_dest_list)
    with open(destination, 'r') as file_handle:
      self.response.write(file_handle.read())
    os.remove(destination)
    return self.SUCCESS


  def put(self, path):
    file_contents = self.request.body
    if file_contents == '':
      self.response.write(json.dumps([{
        'success' : False,
        'failure_reason' : 'no request body specified'
      }]))
      return self.FAILURE

    args = self.get_args_from_request_params(self.request)
    storage = StorageFactory.get_storage(args)

    source = self.write_temporary_file(file_contents)
    source_to_dest_list = [{
      'source' : source,
      'destination' : path
    }]
    self.response.write(storage.upload_files(source_to_dest_list))
    os.remove(source)
    return self.SUCCESS


  def get_args_from_request_params(self, request):
    args = {}

    for item in ['name', 'AWS_ACCESS_KEY', 'AWS_SECRET_KEY', 'GCS_ACCESS_KEY',
      'GCS_SECRET_KEY', 'S3_URL', 'AZURE_ACCOUNT_NAME', 'AZURE_ACCOUNT_KEY']:
      args[item] = request.get(item)

    return args


  def write_temporary_file(self, contents):
    key = str(uuid.uuid4()).replace('-', '')[:10]
    tempfile = '/tmp/magik-temp-{0}'.format(key)
    with open(tempfile, 'w') as file_handle:
      file_handle.write(contents)
    return tempfile


class MagikUI(webapp2.RequestHandler):


  def get(self):
    pass


  def post(self):
    pass
