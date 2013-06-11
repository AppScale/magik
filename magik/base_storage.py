#!/usr/bin/env python
# Programmer: Chris Bunch (chris@appscale.com)
""" base_storage.py defines a single class, BaseStorage, that defines an
interface that details all of the operations that *Storage classes need
to define to be magik-compatible. """


class BaseStorage():
  """ BaseStorage defines a class that all *Storage classes inherit from,
  detailing to implementers of new *Storage classes what the method signatures
  should look like in their new class. """


  def __init__(self, parameters):
    """ Creates a new *Storage object.

    Implementers are advised to validate the parameters that are given here,
    and create a connection to the storage system, to avoid having to create
    one per request.

    Args:
      parameters: A dict that includes fields for each credential needed to
        connect to the storage system.
    """
    raise NotImplementedError


  def upload_files(self, source_to_dest_list):
    """ Uploads one or more files to the storage platform.

    Args:
      source_to_dest_list: A list of dicts, where each dict has a key named
        'source' that points to the file on the local filesystem to upload,
        and a key named 'destination' that points to where it should be
        uploaded on the remote storage service.
    Returns:
      A copy of the same list of dicts that was passed in as an argument,
        with an extra field in each dict named 'success', that indicates if
        the upload was successful, and in case of failures, a field called
        'failure_reason' that explains why the file could not be uploaded.
    """
    raise NotImplementedError


  def download_files(self, source_to_dest_list):
    """ Downloads one or more files from the storage platform.

    Args:
      source_to_dest_list: A list of dicts, where each dict has a key named
        'source' that points to the file on the storage platform to download,
        and a key named 'destination' that points to where it should be
        downloaded on the local filesystem.
    Returns:
      A copy of the same list of dicts that was passed in as an argument,
        with an extra field in each dict named 'success', that indicates if
        the download was successful, and in case of failures, a field called
        'failure_reason' that explains why the file could not be downloaded.
    """
    raise NotImplementedError
