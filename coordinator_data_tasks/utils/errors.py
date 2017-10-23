#!/usr/bin/env python
"""Provide error classes for coordinator_data_tasks."""
from coordinator_data_tasks import __author__, __email__


class DataTasksError(Exception):
    """Base error class for data_tasks."""


class NotImplementedYet(NotImplementedError, DataTasksError):
    """Raise when a section of code that has been left for another time is asked to execute."""

    def __init__(self, msg=None):
        """Set up the Exception."""
        if msg is None:
            msg = "That bonehead {author} should really hear your rage about this disgraceful result! Feel free to tell them at {email}".format(
                author=__author__, email=__email__)

        self.args = (msg, *self.args)


class NoResult(DataTasksError):
    """Raise when an iteration has nothing to return, but normally would."""


class ValidationError(DataTasksError):
    """Raise when a validation/sanity check comes back with unexpected value."""
