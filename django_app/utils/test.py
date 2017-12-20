from pprint import pprint
from time import sleep, time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver


class CoinChatAPI:

    def upbit(self):
        url = 'https://crix-api-endpoint.upbit.com/v1/crix/recent?codes=CRIX.UPBIT.KRW-SNT,CRIX.UPBIT.KRW-XRP,CRIX.UPBIT.KRW-ADA,CRIX.UPBIT.KRW-XLM,CRIX.UPBIT.KRW-BTC,CRIX.UPBIT.KRW-XEM,CRIX.UPBIT.KRW-STEEM,CRIX.UPBIT.KRW-QTUM,CRIX.UPBIT.KRW-POWR,CRIX.UPBIT.KRW-MER,CRIX.UPBIT.KRW-BCC,CRIX.UPBIT.KRW-EMC2,CRIX.UPBIT.KRW-ETH,CRIX.UPBIT.KRW-SBD,CRIX.UPBIT.KRW-TIX,CRIX.UPBIT.KRW-KMD,CRIX.UPBIT.KRW-GRS,CRIX.UPBIT.KRW-NEO,CRIX.UPBIT.KRW-STRAT,CRIX.UPBIT.KRW-OMG,CRIX.UPBIT.KRW-ETC,CRIX.UPBIT.KRW-STORJ,CRIX.UPBIT.KRW-BTG,CRIX.UPBIT.KRW-MTL,CRIX.UPBIT.KRW-XMR,CRIX.UPBIT.KRW-WAVES,CRIX.UPBIT.KRW-ARK,CRIX.UPBIT.KRW-VTC,CRIX.UPBIT.KRW-LSK,CRIX.UPBIT.KRW-LTC,CRIX.UPBIT.KRW-REP,CRIX.UPBIT.KRW-PIVX,CRIX.UPBIT.KRW-DASH,CRIX.UPBIT.KRW-ZEC,CRIX.UPBIT.KRW-ARDR'
        upbit_dict = {}
        for i in range(0,10):
            try:
                result = requests.get(url).json()
                if result:
                    for i in result:
                        upbit_dict[i['code'].split('-')[1]] = i['tradePrice']
                    return upbit_dict
            except:
                raise ConnectionError("업비트")

    # 빗썸
    def lasttrading(self, coin):
        url = 'https://api.bithumb.com/public/ticker/' + coin
        result = requests.get(url)
        result = result.json()
        if not result['status'] == '0000':
            raise ConnectionError("빗썸")
        if coin == 'ALL':
            result = result['data']
        else:
            result = result['data']['buy_price']

        return result

    # 폴로닉스
    def poloniex(self, coin):
        url = 'https://poloniex.com/public?command=returnTicker'
        result = requests.get(url)
        if not result.ok:
            raise ConnectionError("폴로닉스")
        result = result.json()
        if coin == 'ALL':
            new_result_poloniex = {}
            for i, y in result.items():
                if 'USDT_' in i:
                    new_result_poloniex[i.split('_')[1]] = y['last']
            return new_result_poloniex
        else:
            result = result['USDT_{}'.format(coin.upper())]['last']
        return result

    # 비트파이넥스
    def bitfinex(self, coin):
        coin_select = {
            'iota': 'iot',
            'dash': 'dsh',
            'qtum': 'qtm',
        }
        if coin in coin_select:
            coin = coin_select[coin]
        url = 'https://api.bitfinex.com/v1/pubticker/' + coin + 'USD'
        result = requests.get(url)
        if not result.ok:
            raise ConnectionError("비트파이넥스")
        result = result.json()
        result = result['last_price']
        return result

    # 환율
    def exchange_rate(self):
        url = 'https://api.manana.kr/exchange/rate/KRW/USD.json'
        result = requests.get(url)
        result = result.json()[0]['rate']

        return result

    # 코인원
    def coinone(self, coin):
        # all 하면 전체
        url = 'https://api.coinone.co.kr/ticker/?currency=' + coin
        result = requests.get(url)
        if not result.ok:
            raise ConnectionError("코인원")
        if coin == 'ALL':
            result = result.json()
            del result['errorCode']
            del result['result']
            del result['timestamp']
        else:
            result = result.json()['last']
        return result

    # 코빗
    def korbit(self, coin):
        # 코빗은 비트코인,비트코인캐시,이더리움,이더리움 클래식,리플,비트코인골드 외 다른코인은 지원안함
        coin = coin.lower()
        if not (coin == 'btc' or coin == 'bch' or coin == 'eth' or coin == 'etc' or coin == 'xrp' or coin == 'btg'):
            return '미지원 코인'
        url = 'https://api.korbit.co.kr/v1/ticker?currency_pair=' + coin + '_krw'
        result = requests.get(url)
        if not result.ok:
            raise ConnectionError("코빗")
        result = result.json()['last']
        return result

    # 한강
    def hanriver(self):
        url = 'http://koreawqi.go.kr/index_web.jsp'

        # 로컬용
        # driver = webdriver.PhantomJS('/Users/hongdonghyun/projects/coin_chat/phantomjs')
        # 서버용
        driver = webdriver.PhantomJS('/usr/bin/phantomjs')
        driver.get(url)
        driver.switch_to.frame('MainFrame')
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        suon = soup.find('td', class_='start', text='구리').find_next_sibling("td").text
        return suon
