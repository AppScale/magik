""" custom_exceptions.py defines classes that provide Magik-specific Exceptions.
Right now, we only define one class here, BadConfigurationException, if the
user improperly tries to interact with magik."""


class BadConfigurationException(Exception):
  """ BadConfigurationException should be thrown whenever a caller invokes a
  method that sets up a Storage service but either (1) passes in invalid
  arguments that prevent it from being configured correctly, or (2) fails to
  pass in required arguments needed to configure it. """
  pass
