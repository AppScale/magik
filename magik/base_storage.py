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
