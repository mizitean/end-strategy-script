from datetime import datetime
import decimal
from typing import Generic, Literal, List, Optional, TypeVar
from pydantic import ConfigDict, BaseModel, condecimal, model_validator
from py_directus.models import DirectusModel
from typing import Generic, Optional, TypeVar



class StrategyState(DirectusModel):
    id: str
    date_created: datetime
    current_amount: decimal.Decimal
    current_fiat: decimal.Decimal

    model_config = ConfigDict(collection="aa_tge_end_strategy_state")

class StrategyStateUpdate(BaseModel):
    current_amount: condecimal(ge=0)
    current_fiat: condecimal(ge=0)

    @model_validator(mode='before')
    def check_fields(cls, values):
        current_amount = values.get('current_amount')
        current_fiat = values.get('current_fiat')

        # if not isinstance(current_amount, decimal.Decimal):
        #     raise ValueError('current_amount must be of type decimal.Decimal.')
        # if not isinstance(current_fiat, decimal.Decimal):
        #     raise ValueError('current_fiat must be of type decimal.Decimal.')
        try:
          if current_amount <= 0:
              raise ValueError('current_amount cannot be negative number or zero.')
          if current_fiat <= 0:
              raise ValueError('current_fiat cannot be negative number or zero.')

          return values
        except Exception as e:
          return ValueError({str(e)})



class ExchangeStrategy(DirectusModel):
    id: int
    date_created: Optional[datetime]
    api_id: str
    ticker: str
    average_buy: int
    amount_to_sell: int
    price_unit: int
    start_sell_at: int
    frequency: int
    frequency_unit: Literal['SECONDS']
    state_id: str

    model_config = ConfigDict(collection="aa_exchange_end_strategy")


class ExchangeAPI(DirectusModel):
    id: str
    user_created: str
    date_created: datetime
    user_updated: str
    date_updated: datetime
    name: str
    key: str
    secret: str
    client_id: str
    user_id: str
    exchange: Literal['BINANCE', 'PHEMEX', 'COINMATE']

    model_config = ConfigDict(collection="aa_exchange_api")


class StrategyStateResponse(StrategyState):
    pass

class ExchangeStrategyResponse(ExchangeStrategy):
    api_object: Optional[ExchangeAPI]
    state_object: Optional[StrategyState]

class ExchangeAPIResponse(ExchangeAPI):
    pass

T = TypeVar('T')

class ErrorResponse(BaseModel):
    code: int
    message: str

class ResponseWrapper(BaseModel, Generic[T]):
    data: Optional[T]  
    error: Optional[ErrorResponse]