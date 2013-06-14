#!/usr/bin/env python
# Programmer: Chris Bunch (chris@appscale.com)
""" azure_storage.py provides a single class, AzureStorage, that callers can use
to interact with Microsoft Azure's Blob Storage. """


# Third-party libraries
import azure.storage


# S3Storage-specific imports
from magik.base_storage import BaseStorage
from magik.custom_exceptions import BadConfigurationException


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


  def does_key_exist(self, container_name, key_name):
    """ Queries Azure Blob Storage to see if the named file exists.

    Args:
      container_name: A str containing the name of the container that the file
        exists in.
      key_name: A str containing the name of the key that identifies the file.
    Returns:
      True if a file does exist in the named container with the provided key
        name, and False otherwise.
    """
    try:
      self.connection.get_blob_metadata(container_name, key_name)
      return True
    except azure.WindowsAzureMissingResourceError:
      return False


  def download_file(self, destination, container_name, key_name):
    """ Downloads a file to the local filesystem from Azure Blob Storage.

    Args:
      destination: A str contianing the name of the file on the local filesystem
        that we should download the named file to.
      container_name: A str containing the name of the container that the file
        should be downloaded from.
      key_name: A str containing the name of the key that the file should be
        downloaded from.
    """
    blob = self.connection.get_blob(container_name, key_name)
    with open(destination, 'w') as file_handle:
      file_handle.write(blob)


  def delete_file(self, container_name, key_name):
    """ Deletes a file stored in Azure Blob Storage.

    Args:
      container_name: A str containing the name of the container that the file
        should be deleted from.
      key_name: A str containing the name of the key that the file should be
        deleted from.
    """
    self.connection.delete_blob(container_name, key_name)
