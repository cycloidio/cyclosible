import abc
import six
import logging
logger = logging.getLogger(__name__)


@six.add_metaclass(abc.ABCMeta)
class VaultBase(object):
    """Base class for Cyclosible vault plugin
    """

    def __init__(self):
        self.vault_password = None

    @abc.abstractmethod
    def get_password(self):
        """Get the ansible vault password.
        :returns: String
        """
