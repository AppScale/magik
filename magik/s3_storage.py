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


  def does_bucket_exist(self, bucket_name):
    """ Queries Amazon S3 to see if the specified bucket exists or not.

    Args:
      bucket_name: A str containing the name of the bucket we wish to query for
        existence.
    Returns:
      True if the bucket does exist, and False otherwise.
    """
    bucket = self.connection.lookup(bucket_name)
    if bucket:
      return True
    else:
      return False


  def create_bucket(self, bucket_name):
    """ Creates the named bucket in Amazon S3.

    Args:
      bucket_name: A str containing the name of the bucket we wish to create.
    """
    self.connection.create_bucket(bucket_name)


  def upload_file(self, source, bucket_name, key_name):
    """ Uploads a file from the local filesystem to Amazon S3.

    Args:
      source: A str containing the name of the file on the local filesystem that
        should be uploaded to Amazon S3.
      bucket_name: A str containing the name of the bucket that the file should
        be placed in.
      key_name: A str containing the name of the key that the file should be
        placed in.
    """
    bucket = self.connection.lookup(bucket_name)
    key = boto.s3.key.Key(bucket)
    key.key = key_name
    key.set_contents_from_filename(source)


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
