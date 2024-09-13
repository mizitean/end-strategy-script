import json
from decimal import Decimal
from typing import Any, Dict, Optional



class Order:

    def __init__(self, symbol: str, side: str, order_type: str, status: str, order_id: str,
                 fee: Optional[Decimal],feeUnit: str, quantity: Decimal, price: Decimal, spent: Decimal,
                 original_type: Optional[str] = None) -> None:
        self.side: str = side
        self.symbol: str = symbol
        self.type: str = order_type
        self.status: str = status
        self.order_id: str = order_id
        self.fee: Decimal = fee
        self.feeUnit: str = feeUnit
        self.quantity: Decimal = quantity
        self.price: Decimal = price
        self.spent: Decimal = spent
        self.original_type: Optional[str] = original_type

    def to_string(self) -> str:
        """
        Returns a string representation of the object's key-value pairs.
        """
        return json.dumps(self.__dict__, indent=4, default=str)

    def print_attributes(self):
        print(f"Side: {self.side}")
        print(f"Symbol: {self.symbol}")
        print(f"Type: {self.type}")
        print(f"Status: {self.status}")
        print(f"Order ID: {self.order_id}")
        print(f"Fee: {self.fee}")
        print(f"Quantity: {self.quantity}")
        print(f"Price: {self.price}")
        print(f"Spent: {self.spent}")
        print(f"Original Type: {self.original_type}")

    @staticmethod
    def binance_from_dict_limit(values: Dict[str, Any], quantity_key: str, price_key: str = 'price',
                                price: Decimal = None) -> 'Order':
        # if price is None:
            # price = parse_decimal(values[price_key])

        # quantity = parse_decimal(values[quantity_key])
        order_list_id = values['orderListId'] if values.get('orderListId', -1) != -1 else None

        return Order(values['symbol'], values['side'], values['type'], values['status'], values['orderId'],
                     order_list_id, 0, price, values['"cummulativeQuoteQty"'])
    @staticmethod
    def from_data(order_id: str,price: Decimal, quantity: Decimal, spent:Decimal) -> 'Order':
        return Order(symbol="", side="", order_type="", status="", order_id=order_id,
                     fee=None, quantity=quantity, price=price, spent=spent)
