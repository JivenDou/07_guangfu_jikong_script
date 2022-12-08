import logging
from abc import ABC, abstractmethod

log = logging.getLogger("connector")


class Connector(ABC):

    @abstractmethod
    def open(self):
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def get_name(self):
        pass

    @abstractmethod
    def is_connected(self):
        pass

    @abstractmethod
    def send_command(self, content):
        pass

    @abstractmethod
    def command_polling(self, content):
        pass
