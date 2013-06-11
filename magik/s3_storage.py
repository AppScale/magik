#!/usr/bin/env python
# Programmer: Chris Bunch (chris@appscale.com)
""" s3_storage.py provides a single class, S3Storage, that callers can use to
interact with Amazon's Simple Storage Service (S3). """


# General-purpose Python library imports
import os.path
import re


# Third-party libraries
import boto.s3.connection
import boto.s3.key


# S3Storage-specific imports
from base_storage import BaseStorage
from custom_exceptions import BadConfigurationException


class S3Storage(BaseStorage):
  """ S3Storage provides callers with an interface to Amazon S3. """


  def __init__(self, parameters):
    """ Creates a new S3Storage object, with the AWS_ACCESS_KEY and
    AWS_SECRET_KEY that the user has specified.

    Args:
      parameters: A dict that contains the credentials necessary to authenticate
        with S3.
    Raises:
      BadConfigurationException: If AWS_ACCESS_KEY or AWS_SECRET_KEY is not
        specified.
    """
    if 'AWS_ACCESS_KEY' not in parameters:
      raise BadConfigurationException("AWS_ACCESS_KEY needs to be specified")

    if 'AWS_SECRET_KEY' not in parameters:
      raise BadConfigurationException("AWS_SECRET_KEY needs to be specified")

    self.aws_access_key = parameters['AWS_ACCESS_KEY']
    self.aws_secret_key = parameters['AWS_SECRET_KEY']
    self.connection = self.create_s3_connection()
    # TODO(cgb): Consider validating the user's credentials here, and throw
    # a BadConfigurationException if they aren't valid.


  def create_s3_connection(self):
    """ Uses boto to connect to Amazon S3.

    Returns:
      A boto.s3.Connection, which represents a connection to Amazon S3.
    """
    return boto.s3.connection.S3Connection(
      aws_access_key_id=self.aws_access_key,
      aws_secret_access_key=self.aws_secret_key)


  def upload_files(self, source_to_dest_list):
    """ Uploads one or more files to Amazon S3.

    Args:
      source_to_dest_list: A list of dicts, where each dict has a key named
        'source' that points to the file on the local filesystem to upload,
        and a key named 'destination' that points to where it should be
        uploaded in Amazon S3. We presume that the bucket name is prepended to
        the destination path, so a destination of '/mybucket/file.tgz' indicates
        that we should upload this file to '/file.tgz' in the bucket 'mybucket'.
    Returns:
      A copy of source_to_dest_list, with an extra field in each dict that
        indicates if the upload was successful, and if not successful, the
        reason why the upload failed.
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
      bucket = self.connection.lookup(bucket_name)
      if not bucket:
        bucket = self.connection.create_bucket(bucket_name)

      # Finally, upload the file.
      key = boto.s3.key.Key(bucket)
      key.key = key_name
      key.set_contents_from_filename(source)
      item_to_upload['success'] = True

    return upload_result


  def download_files(self, source_to_dest_list):
    """ Downloads one or more files from Amazon S3.

    Args:
      source_to_dest_list: A list of dicts, where each dict has a key named
        'source' that points to the file in Amazon S3 to download, and a key
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
      bucket = self.connection.lookup(bucket_name)
      if not bucket:
        item_to_download['success'] = False
        item_to_download['failure_reason'] = 'bucket not found'
        continue

      key = boto.s3.key.Key(bucket)
      key.key = key_name
      if not key.exists():
        item_to_download['success'] = False
        item_to_download['failure_reason'] = 'source not found'
        continue

      # Finally, download the file.
      destination = item_to_download['destination']
      key.get_contents_to_filename(destination)
      item_to_download['success'] = True

    return download_result
