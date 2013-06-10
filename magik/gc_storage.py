#!/usr/bin/env python
# Programmer: Chris Bunch (chris@appscale.com)
""" gc_storage.py provides a single class, GCStorage, that callers can use to
interact with Google Cloud Storage (GCS). """


# General-purpose Python library imports
import os.path
import re


# Third-party libraries
import boto.gs.connection
#import boto.s3.key


# GCStorage-specific imports
from s3_storage import S3Storage
from custom_exceptions import BadConfigurationException


class GCStorage(S3Storage):
  """ GCStorage provides callers with an interface to Google Cloud Storage. """


  def __init__(self, parameters):
    """ Creates a new GCStorage object, with the GCS_ACCESS_KEY and
    GCS_SECRET_KEY that the user has specified.

    Args:
      parameters: A dict that contains the credentials necessary to authenticate
        with GCS.
    Raises:
      BadConfigurationException: If GCS_ACCESS_KEY or GCS_SECRET_KEY is not
        specified.
    """
    if 'GCS_ACCESS_KEY' not in parameters:
      raise BadConfigurationException("GCS_ACCESS_KEY needs to be specified")

    if 'GCS_SECRET_KEY' not in parameters:
      raise BadConfigurationException("GCS_SECRET_KEY needs to be specified")

    self.gcs_access_key = parameters['GCS_ACCESS_KEY']
    self.gcs_secret_key = parameters['GCS_SECRET_KEY']
    self.connection = self.create_gcs_connection()
    # TODO(cgb): Consider validating the user's credentials here, and throw
    # a BadConfigurationException if they aren't valid.


  def create_gcs_connection(self):
    """ Uses boto to connect to Google Cloud Storage.

    Returns:
      A boto.gs.connection.GSConnection, which represents a connection to Google
        Cloud Storage.
    """
    return boto.gs.connection.GSConnection(gs_access_key_id=self.gcs_access_key,
      gs_secret_access_key=self.gcs_secret_key)
