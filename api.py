from abc import ABC, abstractmethod
from collections import namedtuple
from decimal import Decimal

from order import Order

SymbolInfo = namedtuple('SymbolInfo', 'quantity_precision, price_precision, min_notional')


class Api(ABC):
    _STOP_PRICE_CORRECTION = Decimal(0.5) / 100  # 0.5%

    @abstractmethod
    def getSymbolInfo(self) -> SymbolInfo:
        pass

    @abstractmethod
    def market_buy(self, symbol: str, amount: Decimal) -> Order:
        pass

    @abstractmethod
    def isEndOfMockData(self) -> int:
        pass

    @abstractmethod
    def get_price(self, symbol: str) -> float:
        pass

    # @abstractmethod
    # def limit_buy(self, symbol: str, price: Decimal, amount: Decimal) -> Order:
    #     pass

    # @abstractmethod
    # def limit_sell(self, symbol: str, price: Decimal, amount: Decimal) -> Order:
    #     pass

    @abstractmethod
    def market_sell(self, symbol: str, total_quantity: Decimal) -> Order:
        pass

    @abstractmethod
    def get_symbol_info(self, symbol: str) -> SymbolInfo:
        pass
