#!/usr/bin/env python
# Programmer: Chris Bunch (chris@appscale.com)
""" walrus_storage.py provides a single class, WalrusStorage, that callers can
use to interact with Walrus. """


# General-purpose Python library imports
import re


# Third-party libraries
import boto.s3.connection
import boto.s3.key


# WalrusStorage-specific imports
from s3_storage import S3Storage
from custom_exceptions import BadConfigurationException


class WalrusStorage(S3Storage):
  """ WalrusStorage provides callers with an interface to Eucalyptus Walrus. """


  def __init__(self, parameters):
    """ Creates a new WalrusStorage object, with the AWS_ACCESS_KEY,
    AWS_SECRET_KEY, and S3_URL that the user has specified.

    Args:
      parameters: A dict that contains the credentials necessary to authenticate
        with Walrus.
    Raises:
      BadConfigurationException: If AWS_ACCESS_KEY or AWS_SECRET_KEY is not
        specified, or if S3_URL is not a URL (e.g., of the form
        http://1.2.3.4:8773/services/Walrus).
    """
    if 'AWS_ACCESS_KEY' not in parameters:
      raise BadConfigurationException("AWS_ACCESS_KEY needs to be specified")

    if 'AWS_SECRET_KEY' not in parameters:
      raise BadConfigurationException("AWS_SECRET_KEY needs to be specified")

    self.aws_access_key = parameters['AWS_ACCESS_KEY']
    self.aws_secret_key = parameters['AWS_SECRET_KEY']

    if 'S3_URL' not in parameters:
      raise BadConfigurationException("S3_URL needs to be specified")

    # Make sure it's a URL before we assign it.
    s3_host_matchdata = re.match('http://(.*):8773/services/Walrus',
      parameters['S3_URL'])
    if s3_host_matchdata:
      self.s3_url = parameters['S3_URL']
      self.s3_host = s3_host_matchdata.group(1)
    else:
      raise BadConfigurationException('{0} is not a valid S3 URL. Must be ' +
        'of the form http://1.2.3.4:8773/services/Walrus.')

    self.connection = self.create_walrus_connection()
    # TODO(cgb): Consider validating the user's credentials here, and throw
    # a BadConfigurationException if they aren't valid.


  def create_walrus_connection(self):
    """ Uses boto to connect to Walrus.

    Returns:
      A boto.s3.Connection, which represents a connection to Walrus.
    """
    return boto.s3.connection.S3Connection(
      aws_access_key_id=self.aws_access_key,
      aws_secret_access_key=self.aws_secret_key,
      is_secure=False,
      host=self.s3_host,
      port=8773,
      calling_format=boto.s3.connection.OrdinaryCallingFormat(),
      path="/services/Walrus")
