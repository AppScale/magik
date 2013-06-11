#!/usr/bin/env pyhton
# Programmer: Chris Bunch (chris@appscale.com)
""" storage_factory.py defines a single class, StorageFactory, that can be used
to create connections to each type of cloud storage that magik supports. """


# magik-specific imports
from custom_exceptions import BadConfigurationException
from azure_storage import AzureStorage
from gc_storage import GCStorage
from s3_storage import S3Storage
from walrus_storage import WalrusStorage


class StorageFactory():
  """ StorageFactory provides callers with a simple, unified interface that can
  be used to get a *Storage object. """

  
  # A tuple containing the cloud storage platforms that magik supports.
  SUPPORTED_STORAGE_PLATFORMS = ('azure', 'gcs', 's3', 'walrus')


  @classmethod
  def get_storage(cls, parameters):
    """ Instantiates a new *Storage object, based on the name of the cloud
    storage platform the user wants to connect to, and with the given
    credentials.

    Args:
      parameters: A dict that contains information about which cloud storage
        we should interact with, and the storage-specific credentials needed
        to use this storage service.
    Raises:
      BadConfigurationException: If the caller fails to specify a cloud storage
        platform to instantiate.
      NotImplementedError: If the cloud storage platform named is not one that
        magik supports.
    """
    if 'name' not in parameters:
      raise BadConfigurationException('Need to specify a cloud storage name.')

    storage_name = parameters['name']
    if storage_name == 'azure':
      return AzureStorage(parameters)
    elif storage_name == 'gcs':
      return GCStorage(parameters)
    elif storage_name == 's3':
      return S3Storage(parameters)
    elif storage_name == 'walrus':
      return WalrusStorage(parameters)
    else:
      raise NotImplementedError('{0} is not a supported cloud storage' \
        .format(storage_name))
