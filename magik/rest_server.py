#!/usr/bin/env python
# Programmer: Chris Bunch (chris@appscale.com)
""" rest_server.py defines two classes: RESTServer and MagikUI.

RESTServer defines RESTful routes to store and retrieve data, and MagikUI
provides a web client that talks to these routes

See bin/magik-server for how this server is started and controlled. """


# General-purpose Python library imports
import json
import sys


# Third-party library imports
import webapp2


class RESTServer(webapp2.RequestHandler):


  SUCCESS = 'success'


  FAILURE = 'failure'

 
  def get(self, path):
    pass


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
    source_to_dest_list = [{
      'source' : something,
      'destination' : path
    }]
    self.response.write(storage.upload_files(source_to_dest_list))
    return self.SUCCESS


class MagikUI(webapp2.RequestHandler):


  def get(self):
    pass


  def post(self):
    pass
