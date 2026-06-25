from dotenv import load_dotenv
import os
import requests
from urllib3 import response

load_dotenv()
token = os.getenv('STALZONE_TOKEN')

BASE_URL = 'https://dapi.stalzone.com'
DEMO_TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwibmJmIjoxNjczNzk3ODM4LCJleHAiOjQ4MjczOTc4MzgsImlhdCI6MTY3Mzc5NzgzOCwianRpIjoiYXhwbzAzenJwZWxkMHY5dDgzdzc1N2x6ajl1MmdyeHVodXVlb2xsZ3M2dml1YjVva3NwZTJ3eGFrdjJ1eWZxaDU5ZDE2ZTNlN2FqdW16Z3gifQ.ZNSsvwAX72xT5BzLqqYABuH2FGbOlfiXMK5aYO1H5llG51ZjcPvOYBDRR4HUoPZVLFY8jyFUsEXNM7SYz8qL9ePmLjJl6pib8FEtqVPmf9ldXvKkbaaaSp4KkJzsIEMY_Z5PejB2Vr-q-cL13KPgnLGUaSW-2X_sHPN7VZJNMjRgjw4mPiRZTe4CEpQq0BEcPrG6OLtU5qlZ6mLDJBjN2xtK0DI6xgmYriw_5qW1mj1nqF_ewtUiQ1KTVhDgXnaNUdkGsggAGqyicTei0td6DTKtnl3noD5VkipWn_CwSqb2Mhm16I9BPfX_d5ARzWrnrwPRUf6PA_7LipNU6KkkW0mhZfmwEPTm_sXPus0mHPENoVZArdFT3L5sOYBcpqwvVIEtxRUTdcsKp-y-gSzao5muoyPVoCc2LEeHEWx0cIi9spsZ46SPRQpN4baVFp7y5rp5pjRsBKHQYUJ0lTmh1_vyfzOzbtNN2v6W_5w9JTLrN1U6fhmifvKHppFSEqD6DameL1TC59kpIdufRkEU9HE4O-ErEf1GuJFRx-Dew6XDvb_ExhvEqcw31yNvKzpVqLYJfLazqn6tUbVuAiPwpy6rP9tYO2taT1vj5TGn_vxwDu9zoLWe796tFMPS-kmbCglxB5C9L4EbpfWNbWxYjUkTvjT2Ml9OnrB0UbYo1jI'

HEADERS = {'Authorization': f'Bearer {DEMO_TOKEN}'}

def get_price_history(item: str, region: str = 'ru', limit: int = 200, offset: int = 0):
    url = f'{BASE_URL}/{region}/auction/{item}/history'
    params = {'limit': limit, 'offset': offset}
    response = requests.get(url, headers=HEADERS, params=params)

    if response.status_code != 200:
        print(f'Ошибка: {response.status_code}')
        return None

    return response.json()

get_price_history('0n9q')


def get_active_lots(item: str, region: str = 'ru', limit: int = 200, offset: int = 0):
    url = f'{BASE_URL}/{region}/auction/{item}/lots'
    params = {'limit': limit, 'offset': offset}
    response = requests.get(url, headers=HEADERS, params=params)

    if response.status_code != 200:
        print(f'Ошибка: {response.status_code}')
        return None

    data = response.json()
    print(f'Кол-во активных лотов: {data["total"]}')
    print(data)

# print()
# get_active_lots('0n9q')