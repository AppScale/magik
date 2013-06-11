#!/usr/bin/env python
# Programmer: Chris Bunch (chris@appscale.com)
""" base_storage.py defines a single class, BaseStorage, that defines an
interface that details all of the operations that *Storage classes need
to define to be magik-compatible. """


import os.path


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
    # TODO(cgb): Parallelize the upload process.
    upload_result = source_to_dest_list[:]

    for item_to_upload in upload_result:
      # First, make sure the file to upload actually exists.
      source = item_to_upload['source']
      if not os.path.exists(source):
        item_to_upload['success'] = False
        item_to_upload['failure_reason'] = 'file not found'
        continue

      # Next, make sure the user specified a bucket in the destination.
      destination = item_to_upload['destination']
      bucket_name = destination.split('/')[1]
      key_name = "/".join(destination.split('/')[2:])

      # Make sure the bucket actually exists, and create it if it doesn't.
      if not self.does_bucket_exist(bucket_name):
        self.create_bucket(bucket_name)

      # Finally, upload the file.
      self.upload_file(source, bucket_name, key_name)
      item_to_upload['success'] = True

    return upload_result


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
    # TODO(cgb): Parallelize the download process.
    download_result = source_to_dest_list[:]

    for item_to_download in download_result:
      # First, make sure the item to download actually exists.
      source = item_to_download['source']
      bucket_name = source.split('/')[1]
      key_name = "/".join(source.split('/')[2:])

      # It definitely doesn't exist if the bucket doesn't exist.
      if not self.does_bucket_exist(bucket_name):
        item_to_download['success'] = False
        item_to_download['failure_reason'] = 'bucket not found'
        continue

      if not self.does_key_exist(bucket_name, key_name):
        item_to_download['success'] = False
        item_to_download['failure_reason'] = 'source not found'
        continue

      # Finally, download the file.
      destination = item_to_download['destination']
      self.download_file(destination, bucket_name, key_name)
      item_to_download['success'] = True

    return download_result


  def delete_files(self, files_to_delete):
    """ Deletes one or more files from the storage platform.

    Args:
      files_to_delete: A list of dicts, where each dict has a key named
        'source' that points to the file on the storage platform to delete.
        Note that we intentionally use a dict here, even though it only has
        one key/value pair at the time, in case we need to expand it in the
        future to include other information (e.g., what region the file is in).
    Returns:
      A copy of the same list of dicts that was passed in as an argument,
        with an extra field in each dict named 'success', that indicates if
        the deletion was successful, and in case of failures, a field called
        'failure_reason' that explains why the file could not be deleted.
    """
    # TODO(cgb): Parallelize the deletion process.
    delete_result = files_to_delete[:]

    for item_to_delete in files_to_delete:
      # First, make sure the item to delete actually exists.
      source = item_to_delete['source']
      bucket_name = source.split('/')[1]
      key_name = "/".join(source.split('/')[2:])

      # It definitely doesn't exist if the bucket doesn't exist.
      if not self.does_bucket_exist(bucket_name):
        item_to_delete['success'] = False
        item_to_delete['failure_reason'] = 'bucket not found'
        continue

      if not self.does_key_exist(bucket_name, key_name):
        item_to_delete['success'] = False
        item_to_delete['failure_reason'] = 'source not found'
        continue

      # Finally, download the file.
      self.delete_file(bucket_name, key_name)
      item_to_delete['success'] = True

    return delete_result
