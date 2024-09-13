import json
import math
from decimal import Decimal

import requests
from binance.client import Client

# from app.bot.AsyncLogger2 import AsyncLogger2
# from app.bot.helpers import parse_decimal
# from app.bot.implementation.helpers import round_decimal
# from app.bot.interface.api import SymbolInfo, Api
# from app.bot.models.order import Order
import json
import math
from datetime import datetime
from decimal import Decimal
from time import time
from api import SymbolInfo

import grpc
import requests
from binance.client import Client

# from app.bot.AsyncLogger2 import AsyncLogger2
# from app.bot.helpers import parse_decimal
# from app.bot.implementation.helpers import round_decimal
# from app.bot.interface.api import Api, SymbolInfo
from order import Order
from api import Api
# from app.bot.models.protos.prices import prices_pb2
# from app.bot.models.protos.prices import prices_pb2_grpc

# logger = AsyncLogger2()

class DummySpotApi(Api):

    def __init__(self, client: Client, ticker: str) -> None:
        self.client = client
        self._symbol_info = self.get_symbol_info(ticker)

    def getSymbolInfo(self) -> SymbolInfo:
        return SymbolInfo(6, 2, 10)

    def market_buy(self, symbol: str, amount: Decimal) -> Order:
        pass

    def market_sell(self, symbol: str, total_quantity: Decimal) -> Order:
        pass

    def isEndOfMockData(self) -> bool:
        return True


    def get_single_price(self, symbol: str, retryable: bool) -> float:
        try:
            response = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=" + symbol)
            print(response)
            res = json.loads(response.text)
            return float(res["price"])
        except Exception as e:
            if retryable == False:
                raise e
            # logger.info("get price exception")
            # logger.info(e)
            raise ValueError("Error while load local Rest price")


    def get_price(self, symbol: str) -> float:
        try:
            # channel = grpc.insecure_channel('localhost:50051')
            # stub = prices_pb2_grpc.PriceServiceStub(channel)
            # feature = stub.GetPrices(prices_pb2.PriceRequest(symbol=symbol))
            # diff = int(time() * 1000) - feature.time
            # if (diff < 400):
            #     return float(feature.price)
            # else:
            return self.get_single_price(symbol=symbol, retryable=True)
        except Exception as e:
            now = datetime.now()
            # logger.error(e)
            date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
            # logger.info(date_time + " USE SINGLE REST PRICE")
            return self.get_single_price(symbol=symbol, retryable=False)

    # def limit_buy(self, symbol: str, price: Decimal, amount: Decimal) -> Order:
    #     return Order(
    #         symbol=symbol,
    #         side="BUY_LIMIT",
    #         order_type="Market",
    #         order_id="ORDER_ID",
    #         status="NEW",
    #         fee=Decimal.from_float(float(0)),
    #         feeUnit="not_filled",
    #         quantity=round_decimal(amount, self._symbol_info.quantity_precision, "UP"),
    #         price=price,
    #         spent=price * amount,
    #     )

    # def limit_sell(self, symbol: str, price: Decimal, amount: Decimal) -> Order:
    #     return Order(
    #         symbol=symbol,
    #         side="SELL_LIMIT",
    #         order_type="Market",
    #         order_id="ORDER_ID",
    #         status="NEW",
    #         fee=Decimal.from_float(float(0)),
    #         feeUnit="not_filled",
    #         quantity=round_decimal(amount, self._symbol_info.quantity_precision, "UP"),
    #         price=price,
    #         spent=price * amount,
    #     )

    # # def cancel_order(self, symbol: str, order_id: int) -> None:
    # #     info = self._client.cancel_order(symbol=symbol, orderId=order_id)
    # #     assert info['listStatusType'] == 'ALL_DONE', f'Got {info["listStatusType"]}'

    def market_sell(self, symbol: str, total_quantity: Decimal) -> Order:
        pass

    def get_symbol_info(self, symbol: str) -> SymbolInfo:
        return self.getSymbolInfo()
