from abc import ABC, abstractmethod


class StrategyBase(ABC):

    def __init__(self, params):
        self.params = params

    @abstractmethod
    def generate_signals(self, df):
        pass
