from django.conf import settings
from redis import Redis, ConnectionPool
import abc
import six
import logging
import tempfile
logger = logging.getLogger(__name__)


def check_plugin_enabled(plugin):
    if plugin.name in settings.STORAGE_ENABLED:
        return True
    else:
        return False


@six.add_metaclass(abc.ABCMeta)
class StorageBase(object):
    """Base class for Cyclosible plugin
    """

    def __init__(self, task_id):
        self.redis_connection = Redis(connection_pool=ConnectionPool(**settings.WS4REDIS_CONNECTION))
        self.tmpfile = tempfile.NamedTemporaryFile(mode='a+')
        for log in self.redis_connection.lrange(':'.join(['tasks', task_id]), 0, -1):
            self.tmpfile.write(log)
        # Rewind the log file
        self.tmpfile.seek(0)
        self.log_url = None

    @abc.abstractmethod
    def write_log(self):
        """Write the log somewhere.
        :returns: Boolean. True if success, False if failure
        """

    def get_url_log(self):
        """Get the url of the log.
        :returns: Url of the log. Can be empty
        """
        return self.log_url
