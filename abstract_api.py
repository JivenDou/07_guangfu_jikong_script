from abc import ABC, abstractmethod

class AbstractApi(ABC):

    @abstractmethod
    def operation(self, request):
        pass
