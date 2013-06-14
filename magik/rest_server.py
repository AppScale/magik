#!/usr/bin/env python
# Programmer: Chris Bunch (chris@appscale.com)
""" rest_server.py defines two classes: RESTServer and MagikUI.

RESTServer defines RESTful routes to store and retrieve data, and MagikUI
provides a web client that talks to these routes

See bin/magik-server for how this server is started and controlled. """


# General-purpose Python library imports
import json
import mimetypes
import os
import sys
import uuid


# Third-party library imports
import requests
import webapp2


# Magik library imports
from storage_factory import StorageFactory


class RESTServer(webapp2.RequestHandler):


  # A string constant that URL handlers can return to indicate that the
  # operation finished successfully.
  SUCCESS = 'success'


  # A string constant that URL handlers can return to indicate that the
  # operation finished unsuccessfully.
  FAILURE = 'failure'

 
  def get(self, path):
    """ Downloads a file from a cloud storage platform.

    In addition to the arguments below, this method also expects the following
    parameters to be posted to it:
      name: The name of the cloud storage platform to interact with (e.g.,
        's3').
      credentials: Any AWS, GCS, Walrus, or Azure credential, that should be
        used to authenticate this user.

    Args:
      path: A str that represents the name of the file to download in the cloud
        storage platform. The name of the bucket should be the first item, so
        a path of '/mybucket/file/name.txt' indicates that the file
        'file/name.txt' should be downloaded from the bucket 'mybucket'.
    """
    args = self.get_args_from_request_params(self.request)
    if args['name'] == '':
      self.response.write(json.dumps([{
        'success' : False,
        'failure_reason' : 'no storage specified'
      }]))
      return
    storage = StorageFactory.get_storage(args)

    random_suffix = str(uuid.uuid4()).replace('-', '')[:10]
    destination = '/tmp/magik-temp-{0}'.format(random_suffix)
    source_to_dest_list = [{
      'source' : path,
      'destination' : destination
    }]
    result = storage.download_files(source_to_dest_list)
    if result[0]['success'] == True:
      with open(destination, 'r') as file_handle:
        self.response.write(file_handle.read())
      os.remove(destination)
    else:
      self.response.write(json.dumps(result))

    return


  def put(self, path):
    """ Uploads a file to a cloud storage platform.

    In addition to the arguments below, this method also expects the following
    parameters to be posted to it:
      body: The contents of the file to store.
      name: The name of the cloud storage platform to interact with (e.g.,
        's3').
      credentials: Any AWS, GCS, Walrus, or Azure credential, that should be
        used to authenticate this user.

    Args:
      path: A str that represents the name of the file to upload in the cloud
        storage platform. The name of the bucket should be the first item, so
        a path of '/mybucket/file/name.txt' indicates that the file
        'file/name.txt' should be uploaded to the bucket 'mybucket'.
    """
    file_contents = self.request.body
    if file_contents == '':
      self.response.write(json.dumps([{
        'success' : False,
        'failure_reason' : 'no request body specified'
      }]))
      return

    args = self.get_args_from_request_params(self.request)
    storage = StorageFactory.get_storage(args)

    source = self.write_temporary_file(file_contents)
    source_to_dest_list = [{
      'source' : source,
      'destination' : path
    }]
    self.response.write(storage.upload_files(source_to_dest_list))
    os.remove(source)
    return


  def delete(self, path):
    """ Deletes a file from a cloud storage platform.

    In addition to the arguments below, this method also expects the following
    parameters to be posted to it:
      name: The name of the cloud storage platform to interact with (e.g.,
        's3').
      credentials: Any AWS, GCS, Walrus, or Azure credential, that should be
        used to authenticate this user.

    Args:
      path: A str that represents the name of the file to delete from the cloud
        storage platform. The name of the bucket should be the first item, so
        a path of '/mybucket/file/name.txt' indicates that the file
        'file/name.txt' should be uploaded to the bucket 'mybucket'.
    """
    args = self.get_args_from_request_params(self.request)
    storage = StorageFactory.get_storage(args)
    files_to_delete = [{
      'source' : path
    }]
    self.response.write(storage.delete_files(files_to_delete))


  def get_args_from_request_params(self, request):
    """ Creates a dict that can be passed to *Storage classes, to upload and
    download files.

    Args:
      request: A web request that contains the name of the storage platform to
        use as well as credentials needed to authenticate with it. Any missing
        credential has a value of an empty string.
    Returns:
      A dict that maps each credential to the value that should be used for it,
        and an additional key for the name of the cloud storage to use.
    """
    args = {}

    for item in ['name', 'AWS_ACCESS_KEY', 'AWS_SECRET_KEY', 'GCS_ACCESS_KEY',
      'GCS_SECRET_KEY', 'S3_URL', 'AZURE_ACCOUNT_NAME', 'AZURE_ACCOUNT_KEY']:
      args[item] = request.get(item)

    return args


  def write_temporary_file(self, contents):
    """ Writes a file to the filesystem, with a random suffix.

    Args:
      contents: A str containing the contents of the file that should be
        written to the local filesystem.
    Returns:
      A str containing the name of the file that was written.
    """
    key = str(uuid.uuid4()).replace('-', '')[:10]
    tempfile = '/tmp/magik-temp-{0}'.format(key)
    with open(tempfile, 'w') as file_handle:
      file_handle.write(contents)
    return tempfile


class MagikUI(webapp2.RequestHandler):


  def get(self):
    index_file = os.path.dirname(__file__) + "/../templates/index.html"
    self.response.out.write(file(index_file).read())


  def post(self):
    cloud_name = self.request.get('cloud')
    params = {"name" : cloud_name}

    # get cloudy credentials
    if cloud_name == "s3":
      params["AWS_ACCESS_KEY"] = self.request.get('AWS_ACCESS_KEY')
      params["AWS_SECRET_KEY"] = self.request.get('AWS_SECRET_KEY')
    elif cloud_name == "gcs":
      params["GCS_ACCESS_KEY"] = self.request.get('GCS_ACCESS_KEY')
      params["GCS_SECRET_KEY"] = self.request.get('GCS_SECRET_KEY')
    elif cloud_name == "walrus":
      params["AWS_ACCESS_KEY"] = self.request.get('WALRUS_ACCESS_KEY')
      params["AWS_SECRET_KEY"] = self.request.get('WALRUS_SECRET_KEY')
    elif cloud_name == "azure":
      params["AZURE_ACCOUNT_NAME"] = self.request.get('AZURE_ACCOUNT_NAME')
      params["AZURE_ACCOUNT_KEY"] = self.request.get('AZURE_ACCOUNT_KEY')
    else:
      self.response.out.write(json.dumps({
        "success" : False,
        "failure_reason" : "need to specify a cloud"
      }))
      return

    # get directive
    directive = self.request.get('directive')
    if directive == "upload":
      method = "PUT"
      url = "{0}/{1}".format(self.request.get("upload_bucket"),
        self.request.get("upload_key"))
      file_to_upload = self.request.get('upload_file')
      request = requests.put("http://127.0.0.1:8080/{0}".format(url),
        params=params, data=file_to_upload)
    elif directive == "download":
      method = "GET"
      url = "{0}/{1}".format(self.request.get("download_bucket"),
        self.request.get("download_key"))
      request = requests.get("http://127.0.0.1:8080/{0}".format(url),
        params=params)
    elif directive == "delete":
      method = "DELETE"
      url = "{0}/{1}".format(self.request.get("delete_bucket"),
        self.request.get("delete_key"))
      request = requests.delete("http://127.0.0.1:8080/{0}".format(url),
        params=params)
    else:
      self.response.out.write(json.dumps({
        "success" : False,
        "failure_reason" : "need to specify a directive"
      }))
      return

    # print the response
    self.response.out.write(request.text)


class StaticFileHandler(webapp2.RequestHandler):


  def get(self, path):
    abs_path = os.path.dirname(__file__) + "/../static/" + path
    if os.path.isdir(abs_path): #or abs_path.find(os.getcwd()) != 0:
      self.response.set_status(403)
      return

    try:
      with open(abs_path, 'r') as file_handle:
        self.response.headers['Content-Type'] = mimetypes.guess_type(abs_path)[0]
        self.response.out.write(file_handle.read())
    except:
      self.response.set_status(404)
