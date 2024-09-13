from decimal import Decimal
from dummy_spot_api import DummySpotApi
import os
import sys
from dotenv import load_dotenv
import time
import concurrent.futures
import requests
import json
from typing import List, Optional
from models import ExchangeStrategyResponse, StrategyStateUpdate, ResponseWrapper, StrategyState


load_dotenv()

API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')
DB_API_URL = os.getenv('DB_API_URL')

instance_setting_object = {
  "id": 1,
  "date_created": "2024-09-09T22:08:20.352000Z",
  "api_id": "d8690572-01ef-4edf-8d07-a7e9a7bbf8bb",
  "ticker": "BTCUSDT",
  "average_buy": 30,
  "amount_to_sell": 10,
  "price_unit": 40,
  "start_sell_at": 57960,
  "frequency": 30,
  "frequency_unit": "SECONDS",
  "state_id": "9bc0cecb-38d4-4218-b9fe-cc755421bb01",
}

api_object = {
      "id": "d8690572-01ef-4edf-8d07-a7e9a7bbf8bb",
      "user_created": "8adf17ca-3fef-453a-b578-d91b34400fb4",
      "date_created": "2024-09-07T21:46:26.336000Z",
      "user_updated": "8adf17ca-3fef-453a-b578-d91b34400fb4",
      "date_updated": "2024-09-08T20:37:53.954000Z",
      "name": "jano",
      "key": "ddd",
      "secret": "ddd",
      "client_id": "1111111",
      "user_id": "8adf17ca-3fef-453a-b578-d91b34400fb4",
      "exchange": "PHEMEX"
  }

state_object = {
    "id": "9bc0cecb-38d4-4218-b9fe-cc755421bb01",
    "date_created": "2024-09-08T20:41:04.703000Z",
    "current_amount": "4100",
    "current_fiat": "2500"
  }

instance_setting = ExchangeStrategyResponse(api_object=api_object,
                                                state_object=state_object,
                                                **instance_setting_object)

# Instead of creating threads one by one manually, 
# you can submit multiple tasks to a pool of threads, 
# and the pool handles the execution and scheduling 
# of threads automatically.


def get_multiple_instance_setting_directus() -> List[ExchangeStrategyResponse]:
    mutliple_instace_settings = requests.get(f"{DB_API_URL}/instances")
    return mutliple_instace_settings

def update_strategy_state(id: str, data: StrategyStateUpdate) -> Optional[StrategyStateUpdate]:
    url = f"{DB_API_URL}/update_strategy_state/{id}"
    json_data = {
      "current_amount": int(data.current_amount),
      "current_fiat": int(data.current_fiat)
    }

    try:
        response = requests.post(url, json=json_data) 
        response.raise_for_status()

        response_data = ResponseWrapper[StrategyState](data=response.json()['data'], error=response.json()['error'])

        if response_data.error:
            print(f"Error occurred: {response_data.error.code} - {response_data.error.message}")
            raise ValueError(f"API Error {response_data.error.code}: {response_data.error.message}")
        
        return response_data

    except requests.exceptions.RequestException as e:
        print(f"HTTP Request failed: {str(e)}")
        raise RuntimeError(f"HTTP Request failed: {str(e)}") 

 

def monitor_tickers_for_instance_settings(instance_settings: List[ExchangeStrategyResponse]):
    """
    Executes in parallel mode function monitor_tickers_for_users
    
    parallel lib "concurrent.futures"
    :param: List of Directus Exchange Settings
    """
    pass

def monitor_ticker_for_instance_setting(setting: ExchangeStrategyResponse ) -> None:
    """
    Gets current market_price of ticker from exchange.
    
    Sell condition: start_sell_at > market_price

    If sell condition is meet call market_sell
    If not do nothing

    Put thread to sleep for frequency (frequency_unit)
    Repeat
    """
    client =  DummySpotApi(API_KEY, API_SECRET)
    
    while True:
        if setting.amount_to_sell == 0:
          print(f"Nothing to sell")
          return
        try:
            price = client.get_single_price(setting.ticker, False)
            print(f"Current price of {setting.ticker} for {setting.api_object.name}: {price}")
            
            if price >= setting.start_sell_at:
                print(f"{setting.api_object.name} sold {setting.ticker} for {price}")

                new_amount = setting.state_object.current_amount - setting.amount_to_sell
                new_fiat = setting.state_object.current_fiat + Decimal((setting.amount_to_sell * price))
                
                data = StrategyStateUpdate(current_amount=new_amount, current_fiat=new_fiat)
                update_strategy_state(setting.state_object.id, data)

                setting.amount_to_sell -= 1  

            else:
                print(f"{setting.api_object.name} did not sold {setting.ticker} for {price}")

            time.sleep(10)

        except Exception as e:
            print(f"Error fetching price for {setting.api_object.name}: {e}")



def init_binance_client(instance_setting: ExchangeStrategyResponse) -> DummySpotApi:
    """
    Initializes and returns the Binance client.

    :param api_key: Your Binance API key
    :param api_secret: Your Binance API secret
    :return: Initialized Binance client
    """

    client =  DummySpotApi(instance_setting.api_id, instance_setting.api_object.secret)
    print(client.get_single_price("BTCUSDT", True))
    print(client.__dict__)


if __name__ == "__main__":
    # update_data = StrategyStateUpdate(current_amount=410, current_fiat=2500)

    # # Call the update_user function with the given ID and data
    # update_user("9bc0cecb-38d4-4218-b9fe-cc755421bb01", update_data)

    # print(instance_setting)

    monitor_ticker_for_instance_setting(instance_setting)

