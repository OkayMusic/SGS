import cPickle
import threading
import hashlib


class User(object):
    """
    What's wrong, mr User? Do you not like my mouth-words?
    -Andre Lukas
    """

    def __init__(self, ID):
        """
        All users must have a unique ID, which should be a hash of their
        username.
        """
        self.ID = ID
        self.lock_user = threading.RLock()
