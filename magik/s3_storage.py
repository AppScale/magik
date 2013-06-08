#!/usr/bin/env python
# Programmer: Chris Bunch (chris@appscale.com)
""" s3_storage.py provides a single class, S3Storage, that callers can use to
interact with Amazon's Simple Storage Service (S3). """


# General-purpose Python library imports
import re


# Third-party libraries
import boto.s3.connection


# S3Storage-specific imports
from custom_exceptions import BadConfigurationException


class S3Storage():
  """ S3Storage provides callers with an interface to Amazon S3, and other
  services that are API-compatible with it (e.g., Walrus). """


  def __init__(self, parameters):
    """ Creates a new S3Storage object, with the AWS_ACCESS_KEY, AWS_SECRET_KEY,
    and (optionally) S3_URL that the user has specified.

    Args:
      parameters: A dict that contains the credentials necessary to authenticate
        with S3. S3_URL can optionally be specified, to tell S3Storage where
        S3 is located (useful when pointing at S3-compatible services).
    Raises:
      BadConfigurationException: If AWS_ACCESS_KEY or AWS_SECRET_KEY is not
        specified, or if S3_URL is given but is not a URL (e.g., of the form
        http://1.2.3.4:8773/services/Walrus).
    """
    if 'AWS_ACCESS_KEY' not in parameters:
      raise BadConfigurationException("AWS_ACCESS_KEY needs to be specified")

    if 'AWS_SECRET_KEY' not in parameters:
      raise BadConfigurationException("AWS_SECRET_KEY needs to be specified")

    self.aws_access_key = parameters['AWS_ACCESS_KEY']
    self.aws_secret_key = parameters['AWS_SECRET_KEY']

    if 'S3_URL' in parameters:
      # Make sure it's a URL before we assign it.
      s3_host_matchdata = re.match('http://(.*):8773/services/Walrus',
        parameters['S3_URL'])
      if s3_host_matchdata:
        self.s3_url = parameters['S3_URL']
        self.s3_host = s3_host_matchdata.group(1)
      else:
        raise BadConfigurationException('{0} is not a valid S3 URL. Must be ' +
          'of the form http://1.2.3.4:8773/services/Walrus.')

    self.s3_connection = self.create_s3_connection()
    # TODO(cgb): Consider validating the user's credentials here, and throw
    # a BadConfigurationException if they aren't valid.


  def create_s3_connection(self):
    """ Uses boto to connect to Amazon S3, or a S3-compatible service if S3_URL
    is specified.

    Returns:
      A boto.s3.Connection, which represents a connection to Amazon S3.
    """
    if hasattr(self, 's3_url'):
      calling_format=boto.s3.connection.OrdinaryCallingFormat()
      connection = boto.s3.connection.S3Connection(
        aws_access_key_id=self.aws_access_key,
        aws_secret_access_key=self.aws_secret_key,
        is_secure=False,
        host=self.s3_host,
        port=8773,
        calling_format=calling_format,
        path="/services/Walrus")
    else:
      connection = boto.s3.connection.S3Connection(
        aws_access_key_id=self.aws_access_key,
        aws_secret_access_key=self.aws_secret_key)
    return connection
