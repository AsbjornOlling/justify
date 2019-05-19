""" Maintains a connection to mopidy
Encpasulates the mopidy object.
"""

# deps
from mopidyapi import MopidyAPI


# mopidy connection object
# provides functions and event listeners
# defaults to connecting to localhost
# TODO: make mopidy url configurable
mp = MopidyAPI()

