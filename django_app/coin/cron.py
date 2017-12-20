import os

import django

# 로컬용
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.debug")
# 서버용
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.deploy")
django.setup()
from utils.test import CoinChatAPI
from coin.models import HanriverTemperature, ExchangeRate, BithumbDB, CoinoneDB, PoloniexDB, KorbitDB, BitfinexDB
import kronos
import requests


@kronos.register('*/10 * * * *')
# @kronos.register('*/1 * * * *')
def my_scheduled_job():
    print('run crontab!')
    url_bithumb = 'https://api.bithumb.com/public/ticker/ALL'
    url_poloniex = 'https://poloniex.com/public?command=returnTicker'
    url_coinone = 'https://api.coinone.co.kr/ticker/?currency=all'
    result_bithumb = requests.get(url_bithumb).json()
    result_poloniex = requests.get(url_poloniex).json()
    result_coincone = requests.get(url_coinone).json()
    # 폴로닉스 디비생성 부분
    new_result_poloniex = {}
    for i, y in result_poloniex.items():
        if 'USDT_' in i:
            new_result_poloniex[i.split('_')[1]] = y['last']
    for key, value in new_result_poloniex.items():
        PoloniexDB.objects.create(
            coin_name=key,
            coin_price=value,

        )
    # 빗썸 디비생성 부분
    del result_bithumb['data']['date']
    for key, value in result_bithumb['data'].items():
        BithumbDB.objects.create(
            coin_name=key,
            coin_price=value['buy_price']
        )
    # 코인원 디비생성 부분
    del result_coincone['result']
    del result_coincone['timestamp']
    del result_coincone['errorCode']
    for key, value in result_coincone.items():
        CoinoneDB.objects.create(
            coin_name=key,
            coin_price=value['last']
        )

    return print('success!!')


@kronos.register('*/10 * * * *')
def get_korbit():
    print('run crontab!')
    coin = ['btc', 'bch', 'etc', 'eth', 'xrp', 'btg']
    for i in coin:
        url = 'https://api.korbit.co.kr/v1/ticker?currency_pair=' + i + '_krw'
        result = requests.get(url).json()
        KorbitDB.objects.create(
            coin_name=i,
            coin_price=result['last']
        )
    return print('success!!')

@kronos.register('*/10 * * * *')
def get_bitfienx():
    coin_sel = {
        'btc': 'btc',
        'eth': 'eth',
        'bch': 'bch',
        'xrp': 'xrp',
        'ltc': 'ltc',
        'xmr': 'xmr',
        'zec': 'zec',
        'etc': 'etc',
        'btg': 'btg',
        'eos': 'eos',
        'iot': 'iota',
        'qtm': 'qtum',
        'dsh': 'dash'
    }

    for i in coin_sel:
        url = 'https://api.bitfinex.com/v1/pubticker/' + i + 'USD'

        result = requests.get(url).json()
        BitfinexDB.objects.create(
            coin_name=coin_sel[i],
            coin_price=result['last_price']
        )
    return print('success!')


@kronos.register('0 */2 * * *')
# @kronos.register('*/1 * * * *')
def get_hanriver():
    coinchat = CoinChatAPI()

    temp = coinchat.hanriver()

    HanriverTemperature.objects.create(
        temperature=temp
    )
    return print('success crawl!')


@kronos.register('0 */1 * * *')
# @kronos.register('*/1 * * * *')
def get_exchange_rate():
    coinchat = CoinChatAPI()
    rate = coinchat.exchange_rate()
    ExchangeRate.objects.create(
        rate=rate
    )
    return print('exchange_rate get success!')
