#!/usr/bin/env pyhton
# Programmer: Chris Bunch (chris@appscale.com)
""" storage_factory.py defines a single class, StorageFactory, that can be used
to create connections to each type of cloud storage that magik supports. """


class StorageFactory():
  """ StorageFactory provides callers with a simple, unified interface that can
  be used to get a *Storage object. """

  
  # A tuple containing the cloud storage platforms that magik supports.
  SUPPORTED_STORAGE_PLATFORMS = ('s3')


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
      NotImplementedError: If the cloud storage platform named is not one that
        magik supports.
    """
    pass
