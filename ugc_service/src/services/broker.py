from abc import ABC, abstractmethod


class BaseBroker(ABC):

    @abstractmethod
    def produce(self, topic: str, key: str, body: str | dict):
        pass
