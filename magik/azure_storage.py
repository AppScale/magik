#!/usr/bin/env python
# Programmer: Chris Bunch (chris@appscale.com)
""" azure_storage.py provides a single class, AzureStorage, that callers can use
to interact with Microsoft Azure's Blob Storage. """


# General-purpose Python library imports
import os.path
import re


# Third-party libraries
import azure.storage


# S3Storage-specific imports
from base_storage import BaseStorage
from custom_exceptions import BadConfigurationException


class AzureStorage(BaseStorage):
  """ AzureStorage provides callers with an interface to Microsoft Azure's Blob
  Storage. """


  def __init__(self, parameters):
    """ Creates a new AzureStorage object, with the account name and account key
    and that the user has specified.

    Args:
      parameters: A dict that contains the credentials necessary to authenticate
        with the Blob Storage.
    Raises:
      BadConfigurationException: If the account name or account key are not
        specified.
    """
    if 'AZURE_ACCOUNT_NAME' not in parameters:
      raise BadConfigurationException("AZURE_ACCOUNT_NAME needs to be " + 
        "specified")

    if 'AZURE_ACCOUNT_KEY' not in parameters:
      raise BadConfigurationException("AZURE_ACCOUNT_KEY needs to be specified")

    self.azure_account_name = parameters['AZURE_ACCOUNT_NAME']
    self.azure_account_key = parameters['AZURE_ACCOUNT_KEY']
    self.connection = self.create_azure_connection()
    # TODO(cgb): Consider validating the user's credentials here, and throw
    # a BadConfigurationException if they aren't valid.


  def create_azure_connection(self):
    """ Uses the Azure SDK for Python to connect to Azure Blob Storage.

    Returns:
      A BlobService object, which represents a connection to Azure Blob Storage.
    """
    return azure.storage.BlobService(self.azure_account_name,
      self.azure_account_key)

  
  def does_bucket_exist(self, container_name):
    """ Queries Microsoft Azure to see if the specified container exists or not.

    Args:
      container_name: A str containing the name of the container we wish to
        query for existence.
    Returns:
      True if the container does exist, and False otherwise.
    """
    try:
      self.connection.get_container_metadata(container_name)
      return True
    except azure.WindowsAzureMissingResourceError:
      return False


  def create_bucket(self, container_name):
    """ Creates the named container in Microsoft Azure Blob Storage.
    
    Args:
      container_name: A str containing the name of the container we wish to
        create.
    """
    self.connection.create_container(container_name)


  def upload_file(self, source, container_name, key_name):
    """ Uploads a file from the local filesystem to Microsoft Azure Blob
    Storage.

    Args:
      source: A str containing the name of the file on the local filesystem that
        should be uploaded to Azure Blob Storage.
      container_name: A str containing the name of the container that the file
        should be placed in.
      key_name: A str containing the name of the key that the file should be
        placed in.
    """
    file_contents = None
    with open(source, 'r') as file_handle:
      file_contents = file_handle.read()
    self.connection.put_blob(container_name, key_name, file_contents,
      'BlockBlob')


  def download_files(self, source_to_dest_list):
    """ Downloads one or more files from Azure Blob Storage.

    Args:
      source_to_dest_list: A list of dicts, where each dict has a key named
        'source' that points to the file in Azure to download, and a key
        named 'destination' that points to where it should be downloaded.
    Returns:
      A copy of the same list of dicts that was passed in as an argument,
        with an extra field in each dict indicating if the download was
        successful, and in case of failures, a field that explains why the
        download failed.
    """
    # TODO(cgb): Parallelize the download process.
    download_result = source_to_dest_list[:]

    for item_to_download in download_result:
      # First, make sure the item to download actually exists.
      source = item_to_download['source']
      bucket_name = source.split('/')[1]
      key_name = "/".join(source.split('/')[2:])

      # It definitely doesn't exist if the bucket doesn't exist.
      try:
        self.connection.get_container_metadata(bucket_name)
      except azure.WindowsAzureMissingResourceError:
        item_to_download['success'] = False
        item_to_download['failure_reason'] = 'bucket not found'
        continue

      try:
        self.connection.get_blob_metadata(bucket_name, key_name)
      except azure.WindowsAzureMissingResourceError:
        item_to_download['success'] = False
        item_to_download['failure_reason'] = 'source not found'
        continue

      # Finally, download the file.
      destination = item_to_download['destination']
      blob = self.connection.get_blob(bucket_name, key_name)
      with open(destination, 'w') as file_handle:
        file_handle.write(blob)
      item_to_download['success'] = True

    return download_result
