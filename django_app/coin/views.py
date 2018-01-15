import json
from datetime import datetime, timedelta

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

from coin.models import HanriverTemperature, BithumbDB, CoinoneDB, KorbitDB, PoloniexDB, BitfinexDB, UserDB
from utils.test import CoinChatAPI


def data_func(text, buttons):
    data = {
        "message":
            {
                "text": text
            },
        "keyboard":
            {
                "type": "buttons",
                "buttons": buttons
            }

    }
    data = json.dumps(data, ensure_ascii=False)
    return HttpResponse(data, content_type='application/json')


def arrow_func(value1, value2):
    arrow = '등락없음'
    result = value1 - value2
    if result > 0:
        arrow = '상승⬆︎'
    elif result < 0:
        arrow = '하락⬇︎'
    return arrow


@csrf_exempt
@api_view(['POST'])
def callcoin(request):
    coin_select = {
        "비트코인": "btc",
        "이더리움": "eth",
        "비트코인캐시": "bch",
        "리플": "xrp",
        "라이트코인": "ltc",
        "대시": "dash",
        "모네로": "xmr",
        "제트캐시": "zec",
        "이더리움클래식": "etc",
        "아이오타": "iota",
        "비트코인골드": "btg",
        "퀀텀": "qtum",
        "이오스": "eos",
    }

    coinchat = CoinChatAPI()
    message = ((request.body).decode('utf-8'))
    return_json_str = json.loads(message)
    coin = return_json_str['content']
    # coin = request.POST['content']
    bithumb_dict = {
        'BTC': '비트코인',
        'ETH': '이더리움',
        'BCH': '비트코인캐시',
        'XRP': '리플',
        'LTC': '라이트코인',
        'DASH': '대시',
        'XMR': '모네로',
        'EOS': '이오스',
        'BTG': '비트코인골드',
        'QTUM': '퀀텀',
        'ETC': '이더리움클래식',
        'ZEC': '제트캐시',

    }
    coinone_dict = {
        'bch': '비트코인 캐시',
        'qtum': '퀀텀',
        'iota': '아이오타',
        'ltc': '라이트코인',
        'etc': '이더리움클래식',
        'btg': '비트코인골드',
        'btc': '비트코인',
        'eth': '이더리움',
        'xrp': '리플',
    }
    korbit_dict = {
        '비트코인': 'btc',
        '비트코인 캐시': 'bch',
        '이더리움': 'eth',
        '비트코인 골드': 'btg',
        '이더리움 클래식': 'etc',
        '리플': 'xrp'
    }
    if coin == '처음으로':
        return data_func('메뉴를 선택하세요.', ['마이페이지', '코인', '거래소별 시세', '한강수온', '직접입력'])
    if coin == '코인':
        _list = list(coin_select.keys())
        _list.append('처음으로')
        return data_func('코인을 선택하세요.', _list)

    if coin == '거래소별 시세':
        return data_func('거래소를 선택하세요.', ['빗썸', '코인원', '코빗', '업비트', '폴로닉스', '처음으로'])

    if coin == '업비트':
        coin = CoinChatAPI()
        try:
            upbit = coin.upbit()
        except:
            return data_func("API 연동에 실패했습니다.\n 업비트 API가 터진것 같아요.", ['업비트', '빗썸', '코빗', '코인원', '폴로닉스', '처음으로'])
        upbit_coin_dict = {
            'ADA': '에이다',
            'ARDR': '아더',
            'ARK': '아크',
            'BCC': '비트코인캐시',
            'BTC': '비트코인',
            'BTG': '비트코인골드',
            'DASH': '대시',
            'EMC2': '아인스타이늄',
            'ETC': '이더리움클래식',
            'ETH': '이더리움',
            'GRS': '그로스톨코인',
            'KMD': '코모도',
            'LSK': '리스크',
            'LTC': '라이트코인',
            'MER': '머큐리',
            'MTL': '메탈',
            'NEO': '네오',
            'OMG': '오미세고',
            'PIVX': '피벡스',
            'POWR': '파워렛져',
            'QTUM': '퀀텀',
            'REP': '어거',
            'SBD': '스팀달러',
            'SNT': '스테이터스네트워크토큰',
            'STEEM': '스팀',
            'STORJ': '스토리지',
            'STRAT': '스트라티스',
            'TIX': '블록틱스',
            'VTC': '버트코인',
            'WAVES': '웨이브',
            'XEM': '뉴이코노미무브먼트',
            'XLM': '스텔라루멘',
            'XMR': '모네로',
            'XRP': '리플',
            'ZEC': '제트캐시'
        }
        return_text = []
        for key, value in sorted(upbit.items(), key=lambda upbit: upbit[1], reverse=True):
            return_text.append(upbit_coin_dict[key])
            return_text.append(': ')
            return_text.append('{:,}원\n'.format(int(value)))
        return_text = ''.join(return_text)
        return data_func(return_text, ['업비트', '빗썸', '코빗', '코인원', '폴로닉스', '처음으로'])
    if coin == '빗썸':
        coin = CoinChatAPI()
        try:
            bithumb = coin.lasttrading('ALL')
        except:
            return data_func("API 연동에 실패했습니다.\n 빗썸 API가 터진것 같아요.", ['빗썸', '코인원', '코빗', '업비트', '폴로닉스', '처음으로'])
        del bithumb['date']
        for key, value in bithumb.items():
            bithumb[key] = int(value['buy_price'])
        return_text = []
        for key, value in sorted(bithumb.items(), key=lambda bithumb: bithumb[1], reverse=True):
            return_text.append(bithumb_dict[key])
            return_text.append(': ')
            return_text.append('{:,}원\n'.format(value))
        return_text = ''.join(return_text)

        return data_func(return_text, ['빗썸', '코인원', '코빗', '업비트', '폴로닉스', '처음으로'])
    if coin == '코빗':
        coin = CoinChatAPI()
        try:
            coin.korbit('btc')
        except:
            return data_func("API 연동에 실패했습니다.\n 코빗 API가 터진것 같아요.", ['코빗', '빗썸', '코인원', '업비트', '폴로닉스', '처음으로'])
        return_text = []
        for key, value in korbit_dict.items():
            return_text.append(key)
            return_text.append(': ')
            return_text.append('{:,}'.format(int(coin.korbit(value))))
            return_text.append('원\n')
        return_text = ''.join(return_text)

        return data_func(return_text, ['코빗', '빗썸', '코인원', '업비트', '폴로닉스', '처음으로'])
    if coin == '코인원':
        coin = CoinChatAPI()
        try:
            coinone = coin.coinone('ALL')
        except:
            return data_func("API 연동에 실패했습니다.\n 코인원 API가 터진것 같아요.", ['코인원', '빗썸', '코빗', '업비트', '폴로닉스', '처음으로'])
        for key, value in coinone.items():
            coinone[key] = int(value['last'])
        return_text = []
        for key, value in sorted(coinone.items(), key=lambda coinone: coinone[1], reverse=True):
            return_text.append(coinone_dict[key])
            return_text.append(': ')
            return_text.append('{:,}'.format(value))
            return_text.append('원\n')
        return_text = ''.join(return_text)
        return data_func(return_text, ['코인원', '빗썸', '코빗', '업비트', '폴로닉스', '처음으로'])
    if coin == '폴로닉스':
        coin = CoinChatAPI()
        return_text = []
        _rate = coinchat.exchange_rate()

        poloniex_dict = {
            'BTC': '비트코인',
            'DASH': '대시',
            'LTC': '라이트코인',
            'NXT': 'NXT',
            'STR': '스텔라',
            'XMR': '모네로',
            'XRP': '리플',
            'ETH': '이더리움',
            'ETC': '이더리움클래식',
            'REP': '어거',
            'ZEC': '제트캐시',
            'BCH': '비트코인캐시',

        }
        try:
            poloniex = coin.poloniex('ALL')
        except:
            return data_func("API 연동에 실패했습니다.\n 폴로닉스 API가 터진것 같아요.", ['폴로닉스', '코빗', '빗썸', '코인원', '업비트', '처음으로'])
        for key, value in sorted(poloniex.items(), key=lambda poloniex: float(poloniex[1]), reverse=True):
            return_text.append(poloniex_dict[key])
            return_text.append(': ')
            return_text.append('{:,.2f}'.format(float(value) * _rate))
            return_text.append('원\n')
        return_text = ''.join(return_text)

        return data_func(return_text, ['폴로닉스', '코빗', '빗썸', '코인원', '업비트', '처음으로'])
    if coin == '한강수온':
        return data_func(text='현재 한강 수온은 {}도 입니다.'.format(HanriverTemperature.objects.last().temperature),
                         buttons=['한강수온', '마이페이지', '코인', '거래소별 시세', '직접입력'])
    if coin == '마이페이지':
        # 로컬용
        # user = request.POST['user_key']
        # 서버용
        user = return_json_str['user_key']
        coin = CoinChatAPI()
        if not UserDB.objects.filter(user_key=user).exists():
            return data_func('등록된 정보가 없네요.\n 직접입력을 눌러서 입력해주세요.\n', ['직접이력', '처음으로'])
        else:
            user = UserDB.objects.filter(user_key=user).order_by('exchange_name')
            if user.filter(exchange_name='빗썸').exists():
                bithumb = coin.lasttrading('ALL')
                del bithumb['date']
                new_bithumb_dict = {}
                for key, value in bithumb.items():
                    new_bithumb_dict[bithumb_dict[key]] = int(value['buy_price'])
            if user.filter(exchange_name='코인원').exists():
                coinone = coin.coinone('ALL')
                new_coinone_dict = {}
                for key, value in coinone.items():
                    new_coinone_dict[coinone_dict[key]] = int(value['last'])
            if user.filter(exchange_name='코빗').exists():
                korbit_user = user.filter(exchange_name='코빗')
                korbit = {}
                for i in korbit_user:
                    korbit[i.coin_name] = int(coin.korbit(korbit_dict[i.coin_name]))

            text = ["[내 코인 정보]\n"]
            for i in user:
                text.append('[{} {}]\n평균단가: {:,.2f}원 수량: {}개\n총 매수가격 {:,.2f}원\n '.format(
                    i.exchange_name, i.coin_name,
                    i.coin_price, i.coin_count,
                    i.coin_price if i.coin_count < 0.9999 else
                    i.coin_price * i.coin_count))
            text.append('\n[현재 가격 정보]')
            for i in user:
                if i.exchange_name == '빗썸':
                    current_price = new_bithumb_dict[i.coin_name]
                elif i.exchange_name == '코인원':
                    current_price = new_coinone_dict[i.coin_name]
                else:
                    current_price = korbit[i.coin_name]
                text.append('\n[{} {}]\n 현재가격: {:,.2f}원\n'.format(
                    i.exchange_name, i.coin_name, current_price
                ))
                if i.coin_count > 0:
                    text.append('현재시세 대비 가격: {:,.2f}원\n'.format(
                        i.coin_count * current_price))
                    text.append(
                        '{:,.2f}원'.format((i.coin_count * current_price) - (i.coin_price if i.coin_count < 0.9999 else
                                                                            i.coin_price * i.coin_count)))
                    text.append('{}\n'.format(
                        arrow_func(i.coin_count * current_price, i.coin_price if i.coin_count < 0.9999 else
                        i.coin_price * i.coin_count)))
                else:
                    pass
            text = ''.join(text)
            return data_func(text, ['마이페이지', '코인', '거래소별 시세', '직접입력', '처음으로', '한강수온'])
    if coin == '직접입력':
        data = {
            "message":
                {
                    "text": '코인정보 등록 Beta입니다.\n'
                            '국내 거래소(업비트 제외)만 지원합니다.\n'
                            '등록하실 코인 정보를 거래소,코인명,총 구매가격,수량순으로 입력해주세요.\n'
                            '코인명에 띄워쓰기는 안돼요.\n'
                            '예시) 빗썸,비트코인캐시,47000.33,34.8847(띄워쓰기로 구분 가능합니다)\n'
                            '버튼식으로 돌아가시려면 "처음으로"라고 입력하세요.\n'
                }
        }
        data = json.dumps(data, ensure_ascii=False)
        return HttpResponse(data, content_type='application/json')
    if coin in coin_select:
        _list = list(coin_select.keys())
        _list.append('처음으로')
        # 환율
        _rate = coinchat.exchange_rate()
        # 코인
        _coin = coin_select[coin]
        # 시간
        tenminutes = timedelta(minutes=10)
        current_time = datetime.now()
        twenty = timedelta(minutes=20)

        return_text = ''
        # 코빗,코인원,빗썸,폴로닉스,비트파이넥스가 공통으로 지원하는 코인들
        if _coin == 'btc' or _coin == 'bch' or _coin == 'etc' or _coin == 'eth' or _coin == 'xrp':
            # 사이트별 10분전 가격
            tenminutes = timedelta(minutes=10)
            current_time = datetime.now()
            bithumb_ten = BithumbDB.objects.filter(check_date__range=(current_time - tenminutes, current_time),
                                                   coin_name=_coin.upper()).first()

            coinone_ten = CoinoneDB.objects.filter(check_date__range=(current_time - tenminutes, current_time),
                                                   coin_name=_coin.lower()).first()
            korbit_ten = KorbitDB.objects.filter(check_date__range=(current_time - tenminutes, current_time),
                                                 coin_name=_coin.lower()).first()
            poloniex_ten = PoloniexDB.objects.filter(check_date__range=(current_time - tenminutes, current_time),
                                                     coin_name=_coin.upper()).first()
            finex_ten = BitfinexDB.objects.filter(check_date__range=(current_time - tenminutes, current_time),
                                                  coin_name=_coin.lower()).first()
            # 사이트별 20분전 가격
            twenty = timedelta(minutes=20)
            bithumb_twen = BithumbDB.objects.filter(check_date__range=(current_time - twenty, current_time),
                                                    coin_name=_coin.upper()).first()

            coinone_twen = CoinoneDB.objects.filter(check_date__range=(current_time - twenty, current_time),
                                                    coin_name=_coin.lower()).first()
            korbit_twen = KorbitDB.objects.filter(check_date__range=(current_time - twenty, current_time),
                                                  coin_name=_coin.lower()).first()
            poloniex_twen = PoloniexDB.objects.filter(check_date__range=(current_time - twenty, current_time),
                                                      coin_name=_coin.upper()).first()
            finex_twen = BitfinexDB.objects.filter(check_date__range=(current_time - twenty, current_time),
                                                   coin_name=_coin.lower()).first()
            try:
                bithumb_current = float(coinchat.lasttrading(_coin))
            except ConnectionError as e:
                coinone_current = float(coinchat.coinone(_coin))
                korbit_current = float(coinchat.korbit(_coin))
                poloniex_price = float(coinchat.poloniex(_coin))
                finex_price = float(coinchat.bitfinex(_coin))
                # 환율 적용
                poloniex_price_to_krw = float(poloniex_price * _rate)
                finex_price_to_krw = float(finex_price * _rate)
                text1 = '김치 프리미엄 \t(현재 가격대비 등락) \n[국내:코인원, 해외:폴로닉스 기준]\n'
                text2 = '현재 김치 프리미엄{:,.2f}% \n'.format(
                    ((coinone_current - poloniex_price_to_krw) / poloniex_price_to_krw) * 100
                )
                text3 = '{}시 {}분경 김치 프리미엄{:,.2f}% ({:,.2f})%\n'.format(
                    coinone_twen.check_date.hour, coinone_twen.check_date.minute,
                    (coinone_twen.coin_price - (poloniex_twen.coin_price * _rate)) / (
                        poloniex_twen.coin_price * _rate) * 100,
                    ((
                         coinone_current - poloniex_price_to_krw) / poloniex_price_to_krw) * 100 - (
                        coinone_twen.coin_price - (
                            poloniex_twen.coin_price * _rate)) / (
                        poloniex_twen.coin_price * _rate) * 100
                )
                text4 = '{}시 {}분경 김치 프리미엄{:,.2f}% ({:,.2f})%\n\n'.format(coinone_ten.check_date.hour,
                                                                         coinone_ten.check_date.minute, (
                                                                             coinone_ten.coin_price - (
                                                                                 poloniex_ten.coin_price * _rate)) / (
                                                                             poloniex_ten.coin_price * _rate) * 100,
                                                                         ((
                                                                              coinone_current - poloniex_price_to_krw) / poloniex_price_to_krw) * 100 - (
                                                                             coinone_ten.coin_price - (
                                                                                 poloniex_ten.coin_price * _rate)) / (
                                                                             poloniex_ten.coin_price * _rate) * 100
                                                                         )

                text5 = '{}시 {}분경 가격\n'.format(coinone_twen.check_date.hour, coinone_twen.check_date.minute)
                text6 = '코인원: {:,.2f}원\n'.format(coinone_twen.coin_price)
                text7 = '코빗: {:,.2f}원\n'.format(korbit_twen.coin_price)
                text8 = '폴로닉스: {:,.2f}원 {:,.2f}$\n'.format(poloniex_twen.coin_price * _rate, poloniex_twen.coin_price)
                text9 = '비트파이넥스: {:,.2f}원 {:,.2f}$\n\n'.format(finex_twen.coin_price * _rate, finex_twen.coin_price)
                text10 = '{}시 {}분경 가격 \n'.format(coinone_ten.check_date.hour, coinone_ten.check_date.minute)
                text11 = '코인원: {:,.2f}원\n'.format(coinone_ten.coin_price)
                text12 = '코빗: {:,.2f}원\n'.format(korbit_ten.coin_price)
                text13 = '폴로닉스: {:,.2f}원 {:,.2f}$\n'.format(poloniex_ten.coin_price * _rate, poloniex_ten.coin_price)
                text14 = '비트파이넥스: {:,.2f}원 {:,.2f}$\n\n'.format(finex_ten.coin_price * _rate, finex_ten.coin_price)
                text15 = '현재 해외 {}의 가격\n'.format(_coin.upper())
                text16 = '폴로닉스: {:,.2f}원 ({:,.2f}$) \n({}분전에 비해 {:,.2f}원{})\n'.format(poloniex_price_to_krw,
                                                                                      poloniex_price,
                                                                                      current_time.minute - poloniex_ten.check_date.minute,
                                                                                      poloniex_price_to_krw - poloniex_ten.coin_price * _rate,
                                                                                      arrow_func(poloniex_price_to_krw,
                                                                                                 poloniex_ten.coin_price * _rate))
                text17 = '비트파이넥스: {:,.2f}원 ({:,.2f}$) \n({}분전에 비해 {:,.2f}원{})\n\n'.format(finex_price_to_krw,
                                                                                          finex_price,
                                                                                          current_time.minute - finex_ten.check_date.minute,
                                                                                          finex_price_to_krw - finex_ten.coin_price * _rate,
                                                                                          arrow_func(finex_price_to_krw,
                                                                                                     finex_ten.coin_price * _rate))
                text18 = '현재 국내 {}의 가격\n'.format(_coin.upper())
                text19 = '코인원: {:,.2f}원 \n({}분전에 비해 {:,.2f}원{})\n'.format(coinone_current,
                                                                          current_time.minute - coinone_ten.check_date.minute,
                                                                          coinone_current - coinone_ten.coin_price,
                                                                          arrow_func(coinone_current,
                                                                                     coinone_ten.coin_price))
                text20 = '코빗: {:,.2f}원 \n({}분전에 비해 {:,.2f}원{})\n'.format(korbit_current,
                                                                         current_time.minute - korbit_ten.check_date.minute,
                                                                         korbit_current - korbit_ten.coin_price,
                                                                         arrow_func(korbit_current,
                                                                                    korbit_ten.coin_price))

                return_text = text1 + text2 + text3 + text4 + text5 + text6 + text7 + text8 + text9 + text10 + text11 + text12 + text13 + text14 + text15 + text16 + text17 + text18 + text19 + text20 + "**빗썸 API와의 통신이 되지않아 빗썸을 제외한 결과입니다.**"

                return data_func(return_text, buttons=_list)
            try:
                coinone_current = float(coinchat.coinone(_coin))
            except ConnectionError as e:
                bithumb_current = float(coinchat.lasttrading(_coin))
                korbit_current = float(coinchat.korbit(_coin))
                poloniex_price = float(coinchat.poloniex(_coin))
                finex_price = float(coinchat.bitfinex(_coin))
                # 환율 적용
                poloniex_price_to_krw = float(poloniex_price * _rate)
                finex_price_to_krw = float(finex_price * _rate)
                text1 = '김치 프리미엄 \t(현재 가격대비 등락) \n[국내:빗썸, 해외:폴로닉스 기준]\n'
                text2 = '현재 김치 프리미엄{:,.2f}% \n'.format(
                    ((bithumb_current - poloniex_price_to_krw) / poloniex_price_to_krw) * 100
                )
                text3 = '{}시 {}분경 김치 프리미엄{:,.2f}% ({:,.2f})%\n'.format(
                    bithumb_twen.check_date.hour, bithumb_twen.check_date.minute,
                    (bithumb_twen.coin_price - (poloniex_twen.coin_price * _rate)) / (
                        poloniex_twen.coin_price * _rate) * 100,
                    ((
                         bithumb_current - poloniex_price_to_krw) / poloniex_price_to_krw) * 100 - (
                        bithumb_twen.coin_price - (
                            poloniex_twen.coin_price * _rate)) / (
                        poloniex_twen.coin_price * _rate) * 100
                )
                text4 = '{}시 {}분경 김치 프리미엄{:,.2f}% ({:,.2f})%\n\n'.format(bithumb_ten.check_date.hour,
                                                                         bithumb_ten.check_date.minute, (
                                                                             bithumb_ten.coin_price - (
                                                                                 poloniex_ten.coin_price * _rate)) / (
                                                                             poloniex_ten.coin_price * _rate) * 100,
                                                                         ((
                                                                              bithumb_current - poloniex_price_to_krw) / poloniex_price_to_krw) * 100 - (
                                                                             bithumb_ten.coin_price - (
                                                                                 poloniex_ten.coin_price * _rate)) / (
                                                                             poloniex_ten.coin_price * _rate) * 100
                                                                         )

                text5 = '{}시 {}분경 가격\n'.format(bithumb_twen.check_date.hour, bithumb_twen.check_date.minute)
                text6 = '빗썸: {:,.2f}원\n'.format(bithumb_twen.coin_price)
                text7 = '코빗: {:,.2f}원\n'.format(korbit_twen.coin_price)
                text8 = '폴로닉스: {:,.2f}원 {:,.2f}$\n'.format(poloniex_twen.coin_price * _rate, poloniex_twen.coin_price)
                text9 = '비트파이넥스: {:,.2f}원 {:,.2f}$\n\n'.format(finex_twen.coin_price * _rate, finex_twen.coin_price)
                text10 = '{}시 {}분경 가격 \n'.format(bithumb_ten.check_date.hour, bithumb_ten.check_date.minute)
                text11 = '빗썸: {:,.2f}원\n'.format(bithumb_ten.coin_price)
                text12 = '코빗: {:,.2f}원\n'.format(korbit_ten.coin_price)
                text13 = '폴로닉스: {:,.2f}원 {:,.2f}$\n'.format(poloniex_ten.coin_price * _rate, poloniex_ten.coin_price)
                text14 = '비트파이넥스: {:,.2f}원 {:,.2f}$\n\n'.format(finex_ten.coin_price * _rate, finex_ten.coin_price)
                text15 = '현재 해외 {}의 가격\n'.format(_coin.upper())
                text16 = '폴로닉스: {:,.2f}원 ({:,.2f}$) \n({}분전에 비해 {:,.2f}원{})\n'.format(poloniex_price_to_krw,
                                                                                      poloniex_price,
                                                                                      current_time.minute - poloniex_ten.check_date.minute,
                                                                                      poloniex_price_to_krw - poloniex_ten.coin_price * _rate,
                                                                                      arrow_func(poloniex_price_to_krw,
                                                                                                 poloniex_ten.coin_price * _rate))
                text17 = '비트파이넥스: {:,.2f}원 ({:,.2f}$) \n({}분전에 비해 {:,.2f}원{})\n\n'.format(finex_price_to_krw,
                                                                                          finex_price,
                                                                                          current_time.minute - finex_ten.check_date.minute,
                                                                                          finex_price_to_krw - finex_ten.coin_price * _rate,
                                                                                          arrow_func(finex_price_to_krw,
                                                                                                     finex_ten.coin_price * _rate))
                text18 = '현재 국내 {}의 가격\n'.format(_coin.upper())
                text19 = '빗썸: {:,.2f}원 \n({}분전에 비해 {:,.2f}원{})\n'.format(bithumb_current,
                                                                         current_time.minute - bithumb_ten.check_date.minute,
                                                                         bithumb_current - bithumb_ten.coin_price,
                                                                         arrow_func(bithumb_current,
                                                                                    bithumb_ten.coin_price))
                text20 = '코빗: {:,.2f}원 \n({}분전에 비해 {:,.2f}원{})\n\n'.format(korbit_current,
                                                                           current_time.minute - korbit_ten.check_date.minute,
                                                                           korbit_current - korbit_ten.coin_price,
                                                                           arrow_func(korbit_current,
                                                                                      korbit_ten.coin_price))

                return_text = text1 + text2 + text3 + text4 + text5 + text6 + text7 + text8 + text9 + text10 + text11 + text12 + text13 + text14 + text15 + text16 + text17 + text18 + text19 + text20 + "**코인원 API와의 통신이 되지않아 코인원을 제외한 결과입니다.**"
                return data_func(return_text, buttons=_list)
            try:
                korbit_current = float(coinchat.korbit(_coin))
            except ConnectionError as e:
                bithumb_current = float(coinchat.lasttrading(_coin))
                coinone_current = float(coinchat.coinone(_coin))
                poloniex_price = float(coinchat.poloniex(_coin))
                finex_price = float(coinchat.bitfinex(_coin))
                # 환율 적용
                poloniex_price_to_krw = float(poloniex_price * _rate)
                finex_price_to_krw = float(finex_price * _rate)
                text1 = '김치 프리미엄 \t(현재 가격대비 등락) \n[국내:빗썸, 해외:폴로닉스 기준]\n'
                text2 = '현재 김치 프리미엄{:,.2f}% \n'.format(
                    ((bithumb_current - poloniex_price_to_krw) / poloniex_price_to_krw) * 100
                )
                text3 = '{}시 {}분경 김치 프리미엄{:,.2f}% ({:,.2f})%\n'.format(
                    bithumb_twen.check_date.hour, bithumb_twen.check_date.minute,
                    (bithumb_twen.coin_price - (poloniex_twen.coin_price * _rate)) / (
                        poloniex_twen.coin_price * _rate) * 100,
                    ((
                         bithumb_current - poloniex_price_to_krw) / poloniex_price_to_krw) * 100 - (
                        bithumb_twen.coin_price - (
                            poloniex_twen.coin_price * _rate)) / (
                        poloniex_twen.coin_price * _rate) * 100
                )
                text4 = '{}시 {}분경 김치 프리미엄{:,.2f}% ({:,.2f})%\n\n'.format(bithumb_ten.check_date.hour,
                                                                         bithumb_ten.check_date.minute, (
                                                                             bithumb_ten.coin_price - (
                                                                                 poloniex_ten.coin_price * _rate)) / (
                                                                             poloniex_ten.coin_price * _rate) * 100,
                                                                         ((
                                                                              bithumb_current - poloniex_price_to_krw) / poloniex_price_to_krw) * 100 - (
                                                                             bithumb_ten.coin_price - (
                                                                                 poloniex_ten.coin_price * _rate)) / (
                                                                             poloniex_ten.coin_price * _rate) * 100
                                                                         )

                text5 = '{}시 {}분경 가격\n'.format(bithumb_twen.check_date.hour, bithumb_twen.check_date.minute)
                text6 = '빗썸: {:,.2f}원\n'.format(bithumb_twen.coin_price)
                text7 = '코인원: {:,.2f}원\n'.format(coinone_twen.coin_price)
                text8 = '폴로닉스: {:,.2f}원 {:,.2f}$\n'.format(poloniex_twen.coin_price * _rate, poloniex_twen.coin_price)
                text9 = '비트파이넥스: {:,.2f}원 {:,.2f}$\n\n'.format(finex_twen.coin_price * _rate, finex_twen.coin_price)
                text10 = '{}시 {}분경 가격 \n'.format(bithumb_ten.check_date.hour, bithumb_ten.check_date.minute)
                text11 = '빗썸: {:,.2f}원\n'.format(bithumb_ten.coin_price)
                text12 = '코인원: {:,.2f}원\n'.format(coinone_ten.coin_price)
                text13 = '폴로닉스: {:,.2f}원 {:,.2f}$\n'.format(poloniex_ten.coin_price * _rate, poloniex_ten.coin_price)
                text14 = '비트파이넥스: {:,.2f}원 {:,.2f}$\n\n'.format(finex_ten.coin_price * _rate, finex_ten.coin_price)
                text15 = '현재 해외 {}의 가격\n'.format(_coin.upper())
                text16 = '폴로닉스: {:,.2f}원 ({:,.2f}$) \n({}분전에 비해 {:,.2f}원{})\n'.format(poloniex_price_to_krw,
                                                                                      poloniex_price,
                                                                                      current_time.minute - poloniex_ten.check_date.minute,
                                                                                      poloniex_price_to_krw - poloniex_ten.coin_price * _rate,
                                                                                      arrow_func(poloniex_price_to_krw,
                                                                                                 poloniex_ten.coin_price * _rate))
                text17 = '비트파이넥스: {:,.2f}원 ({:,.2f}$) \n({}분전에 비해 {:,.2f}원{})\n\n'.format(finex_price_to_krw,
                                                                                          finex_price,
                                                                                          current_time.minute - finex_ten.check_date.minute,
                                                                                          finex_price_to_krw - finex_ten.coin_price * _rate,
                                                                                          arrow_func(finex_price_to_krw,
                                                                                                     finex_ten.coin_price * _rate))
                text18 = '현재 국내 {}의 가격\n'.format(_coin.upper())
                text19 = '빗썸: {:,.2f}원 \n({}분전에 비해 {:,.2f}원{})\n'.format(bithumb_current,
                                                                         current_time.minute - bithumb_ten.check_date.minute,
                                                                         bithumb_current - bithumb_ten.coin_price,
                                                                         arrow_func(bithumb_current,
                                                                                    bithumb_ten.coin_price))
                text20 = '코인원: {:,.2f}원 \n({}분전에 비해 {:,.2f}원{})\n'.format(coinone_current,
                                                                          current_time.minute - coinone_ten.check_date.minute,
                                                                          coinone_current - coinone_ten.coin_price,
                                                                          arrow_func(coinone_current,
                                                                                     coinone_ten.coin_price))

                return_text = text1 + text2 + text3 + text4 + text5 + text6 + text7 + text8 + text9 + text10 + text11 + text12 + text13 + text14 + text15 + text16 + text17 + text18 + text19 + text20 + "**코빗 API와의 통신이 되지않아 코빗을 제외한 결과입니다.**"
                return data_func(return_text, buttons=_list)
            try:
                poloniex_price = float(coinchat.poloniex(_coin))
            except ConnectionError as e:
                bithumb_current = float(coinchat.lasttrading(_coin))
                coinone_current = float(coinchat.coinone(_coin))
                korbit_current = float(coinchat.korbit(_coin))
                finex_price = float(coinchat.bitfinex(_coin))
                # 환율 적용
                finex_price_to_krw = float(finex_price * _rate)
                text1 = '김치 프리미엄 \t(현재 가격대비 등락) \n[국내:빗썸, 해외:비트파이넥스 기준]\n'
                text2 = '현재 김치 프리미엄{:,.2f}% \n'.format(
                    ((bithumb_current - finex_price_to_krw) / finex_price_to_krw) * 100
                )
                text3 = '{}시 {}분경 김치 프리미엄{:,.2f}% ({:,.2f})%\n'.format(
                    bithumb_twen.check_date.hour, bithumb_twen.check_date.minute,
                    (bithumb_twen.coin_price - (finex_twen.coin_price * _rate)) / (
                        finex_twen.coin_price * _rate) * 100,
                    ((
                         bithumb_current - finex_price_to_krw) / finex_price_to_krw) * 100 - (
                        bithumb_twen.coin_price - (
                            finex_twen.coin_price * _rate)) / (
                        finex_twen.coin_price * _rate) * 100
                )
                text4 = '{}시 {}분경 김치 프리미엄{:,.2f}% ({:,.2f})%\n\n'.format(bithumb_ten.check_date.hour,
                                                                         bithumb_ten.check_date.minute, (
                                                                             bithumb_ten.coin_price - (
                                                                                 finex_ten.coin_price * _rate)) / (
                                                                             finex_ten.coin_price * _rate) * 100,
                                                                         ((
                                                                              bithumb_current - finex_price_to_krw) / finex_price_to_krw) * 100 - (
                                                                             bithumb_ten.coin_price - (
                                                                                 finex_ten.coin_price * _rate)) / (
                                                                             finex_ten.coin_price * _rate) * 100
                                                                         )

                text5 = '{}시 {}분경 가격\n'.format(bithumb_twen.check_date.hour, bithumb_twen.check_date.minute)
                text6 = '빗썸: {:,.2f}원\n'.format(bithumb_twen.coin_price)
                text7 = '코인원: {:,.2f}원\n'.format(coinone_twen.coin_price)
                text8 = '코빗: {:,.2f}원\n'.format(korbit_twen.coin_price)
                text9 = '비트파이넥스: {:,.2f}원 {:,.2f}$\n\n'.format(finex_twen.coin_price * _rate, finex_twen.coin_price)
                text10 = '{}시 {}분경 가격 \n'.format(bithumb_ten.check_date.hour, bithumb_ten.check_date.minute)
                text11 = '빗썸: {:,.2f}원\n'.format(bithumb_ten.coin_price)
                text12 = '코인원: {:,.2f}원\n'.format(coinone_ten.coin_price)
                text13 = '코빗: {:,.2f}원\n'.format(korbit_ten.coin_price)
                text14 = '비트파이넥스: {:,.2f}원 {:,.2f}$\n\n'.format(finex_ten.coin_price * _rate, finex_ten.coin_price)
                text15 = '현재 해외 {}의 가격\n'.format(_coin.upper())
                text16 = '비트파이넥스: {:,.2f}원 ({:,.2f}$) \n({}분전에 비해 {:,.2f}원{})\n\n'.format(finex_price_to_krw,
                                                                                          finex_price,
                                                                                          current_time.minute - finex_ten.check_date.minute,
                                                                                          finex_price_to_krw - finex_ten.coin_price * _rate,
                                                                                          arrow_func(finex_price_to_krw,
                                                                                                     finex_ten.coin_price * _rate))
                text17 = '현재 국내 {}의 가격\n'.format(_coin.upper())
                text18 = '빗썸: {:,.2f}원 \n({}분전에 비해 {:,.2f}원{})\n'.format(bithumb_current,
                                                                         current_time.minute - bithumb_ten.check_date.minute,
                                                                         bithumb_current - bithumb_ten.coin_price,
                                                                         arrow_func(bithumb_current,
                                                                                    bithumb_ten.coin_price))
                text19 = '코인원: {:,.2f}원 \n({}분전에 비해 {:,.2f}원{})\n'.format(coinone_current,
                                                                          current_time.minute - coinone_ten.check_date.minute,
                                                                          coinone_current - coinone_ten.coin_price,
                                                                          arrow_func(coinone_current,
                                                                                     coinone_ten.coin_price))
                text20 = '코빗: {:,.2f}원 \n({}분전에 비해 {:,.2f}원{})\n\n'.format(korbit_current,
                                                                           current_time.minute - korbit_ten.check_date.minute,
                                                                           korbit_current - korbit_ten.coin_price,
                                                                           arrow_func(korbit_current,
                                                                                      korbit_ten.coin_price))

                return_text = text1 + text2 + text3 + text4 + text5 + text6 + text7 + text8 + text9 + text10 + text11 + text12 + text13 + text14 + text15 + text16 + text17 + text18 + text19 + text20 + "**폴로닉스 API와의 통신이 되지않아 폴로닉스를 제외한 결과입니다.**"
                return data_func(return_text, buttons=_list)
            try:
                finex_price = float(coinchat.bitfinex(_coin))
            except ConnectionError as e:
                bithumb_current = float(coinchat.lasttrading(_coin))
                coinone_current = float(coinchat.coinone(_coin))
                korbit_current = float(coinchat.korbit(_coin))
                poloniex_price = float(coinchat.poloniex(_coin))
                # 환율 적용
                poloniex_price_to_krw = float(poloniex_price * _rate)
                text1 = '김치 프리미엄 \t(현재 가격대비 등락) \n[국내:빗썸, 해외:폴로닉스 기준]\n'
                text2 = '현재 김치 프리미엄{:,.2f}% \n'.format(
                    ((bithumb_current - poloniex_price_to_krw) / poloniex_price_to_krw) * 100
                )
                text3 = '{}시 {}분경 김치 프리미엄{:,.2f}% ({:,.2f})%\n'.format(
                    bithumb_twen.check_date.hour, bithumb_twen.check_date.minute,
                    (bithumb_twen.coin_price - (poloniex_twen.coin_price * _rate)) / (
                        poloniex_twen.coin_price * _rate) * 100,
                    ((
                         bithumb_current - poloniex_price_to_krw) / poloniex_price_to_krw) * 100 - (
                        bithumb_twen.coin_price - (
                            poloniex_twen.coin_price * _rate)) / (
                        poloniex_twen.coin_price * _rate) * 100
                )
                text4 = '{}시 {}분경 김치 프리미엄{:,.2f}% ({:,.2f})%\n\n'.format(bithumb_ten.check_date.hour,
                                                                         bithumb_ten.check_date.minute, (
                                                                             bithumb_ten.coin_price - (
                                                                                 poloniex_ten.coin_price * _rate)) / (
                                                                             poloniex_ten.coin_price * _rate) * 100,
                                                                         ((
                                                                              bithumb_current - poloniex_price_to_krw) / poloniex_price_to_krw) * 100 - (
                                                                             bithumb_ten.coin_price - (
                                                                                 poloniex_ten.coin_price * _rate)) / (
                                                                             poloniex_ten.coin_price * _rate) * 100
                                                                         )

                text5 = '{}시 {}분경 가격\n'.format(bithumb_twen.check_date.hour, bithumb_twen.check_date.minute)
                text6 = '빗썸: {:,.2f}원\n'.format(bithumb_twen.coin_price)
                text7 = '코인원: {:,.2f}원\n'.format(coinone_twen.coin_price)
                text8 = '코빗: {:,.2f}원\n'.format(korbit_twen.coin_price)
                text9 = '폴로닉스: {:,.2f}원 {:,.2f}$\n'.format(poloniex_twen.coin_price * _rate, poloniex_twen.coin_price)
                text10 = '{}시 {}분경 가격 \n'.format(bithumb_ten.check_date.hour, bithumb_ten.check_date.minute)
                text11 = '빗썸: {:,.2f}원\n'.format(bithumb_ten.coin_price)
                text12 = '코인원: {:,.2f}원\n'.format(coinone_ten.coin_price)
                text13 = '코빗: {:,.2f}원\n'.format(korbit_ten.coin_price)
                text14 = '폴로닉스: {:,.2f}원 {:,.2f}$\n'.format(poloniex_ten.coin_price * _rate, poloniex_ten.coin_price)
                text15 = '현재 해외 {}의 가격\n'.format(_coin.upper())
                text16 = '폴로닉스: {:,.2f}원 ({:,.2f}$) \n({}분전에 비해 {:,.2f}원{})\n'.format(poloniex_price_to_krw,
                                                                                      poloniex_price,
                                                                                      current_time.minute - poloniex_ten.check_date.minute,
                                                                                      poloniex_price_to_krw - poloniex_ten.coin_price * _rate,
                                                                                      arrow_func(poloniex_price_to_krw,
                                                                                                 poloniex_ten.coin_price * _rate))
                text17 = '현재 국내 {}의 가격\n'.format(_coin.upper())
                text18 = '빗썸: {:,.2f}원 \n({}분전에 비해 {:,.2f}원{})\n'.format(bithumb_current,
                                                                         current_time.minute - bithumb_ten.check_date.minute,
                                                                         bithumb_current - bithumb_ten.coin_price,
                                                                         arrow_func(bithumb_current,
                                                                                    bithumb_ten.coin_price))
                text19 = '코인원: {:,.2f}원 \n({}분전에 비해 {:,.2f}원{})\n'.format(coinone_current,
                                                                          current_time.minute - coinone_ten.check_date.minute,
                                                                          coinone_current - coinone_ten.coin_price,
                                                                          arrow_func(coinone_current,
                                                                                     coinone_ten.coin_price))
                text20 = '코빗: {:,.2f}원 \n({}분전에 비해 {:,.2f}원{})\n\n'.format(korbit_current,
                                                                           current_time.minute - korbit_ten.check_date.minute,
                                                                           korbit_current - korbit_ten.coin_price,
                                                                           arrow_func(korbit_current,
                                                                                      korbit_ten.coin_price))

                return_text = text1 + text2 + text3 + text4 + text5 + text6 + text7 + text8 + text9 + text10 + text11 + text12 + text13 + text14 + text15 + text16 + text17 + text18 + text19 + text20 + "**비트파이넥스 API와의 통신이 되지않아 비트파이넥스를 제외한 결과입니다.**"
                return data_func(return_text, buttons=_list)
            # 환율 적용
            poloniex_price_to_krw = float(poloniex_price * _rate)
            finex_price_to_krw = float(finex_price * _rate)

            text1 = '김치 프리미엄 \t(현재 가격대비 등락) \n[국내:빗썸, 해외:폴로닉스 기준]\n'
            text2 = '현재 김치 프리미엄{:,.2f}% \n'.format(
                ((bithumb_current - poloniex_price_to_krw) / poloniex_price_to_krw) * 100
            )
            text3 = '{}시 {}분경 김치 프리미엄{:,.2f}% ({:,.2f})%\n'.format(
                bithumb_twen.check_date.hour, bithumb_twen.check_date.minute,
                (bithumb_twen.coin_price - (poloniex_twen.coin_price * _rate)) / (
                    poloniex_twen.coin_price * _rate) * 100,
                ((
                     bithumb_current - poloniex_price_to_krw) / poloniex_price_to_krw) * 100 - (
                    bithumb_twen.coin_price - (
                        poloniex_twen.coin_price * _rate)) / (
                    poloniex_twen.coin_price * _rate) * 100
            )
            text4 = '{}시 {}분경 김치 프리미엄{:,.2f}% ({:,.2f})%\n\n'.format(bithumb_ten.check_date.hour,
                                                                     bithumb_ten.check_date.minute, (
                                                                         bithumb_ten.coin_price - (
                                                                             poloniex_ten.coin_price * _rate)) / (
                                                                         poloniex_ten.coin_price * _rate) * 100,
                                                                     ((
                                                                          bithumb_current - poloniex_price_to_krw) / poloniex_price_to_krw) * 100 - (
                                                                         bithumb_ten.coin_price - (
                                                                             poloniex_ten.coin_price * _rate)) / (
                                                                         poloniex_ten.coin_price * _rate) * 100
                                                                     )

            text5 = '{}시 {}분경 가격\n'.format(bithumb_twen.check_date.hour, bithumb_twen.check_date.minute)
            text6 = '빗썸: {:,.2f}원\n'.format(bithumb_twen.coin_price)
            text7 = '코인원: {:,.2f}원\n'.format(coinone_twen.coin_price)
            text8 = '코빗: {:,.2f}원\n'.format(korbit_twen.coin_price)
            text9 = '폴로닉스: {:,.2f}원 {:,.2f}$\n'.format(poloniex_twen.coin_price * _rate, poloniex_twen.coin_price)
            text10 = '비트파이넥스: {:,.2f}원 {:,.2f}$\n\n'.format(finex_twen.coin_price * _rate, finex_twen.coin_price)
            text11 = '{}시 {}분경 가격 \n'.format(bithumb_ten.check_date.hour, bithumb_ten.check_date.minute)
            text12 = '빗썸: {:,.2f}원\n'.format(bithumb_ten.coin_price)
            text13 = '코인원: {:,.2f}원\n'.format(coinone_ten.coin_price)
            text14 = '코빗: {:,.2f}원\n'.format(korbit_ten.coin_price)
            text15 = '폴로닉스: {:,.2f}원 {:,.2f}$\n'.format(poloniex_ten.coin_price * _rate, poloniex_ten.coin_price)
            text16 = '비트파이넥스: {:,.2f}원 {:,.2f}$\n\n'.format(finex_ten.coin_price * _rate, finex_ten.coin_price)
            text17 = '현재 해외 {}의 가격\n'.format(_coin.upper())
            text18 = '폴로닉스: {:,.2f}원 ({:,.2f}$) \n({}분전에 비해 {:,.2f}원{})\n'.format(poloniex_price_to_krw,
                                                                                  poloniex_price,
                                                                                  current_time.minute - poloniex_ten.check_date.minute,
                                                                                  poloniex_price_to_krw - poloniex_ten.coin_price * _rate,
                                                                                  arrow_func(poloniex_price_to_krw,
                                                                                             poloniex_ten.coin_price * _rate))
            text19 = '비트파이넥스: {:,.2f}원 ({:,.2f}$) \n({}분전에 비해 {:,.2f}원{})\n\n'.format(finex_price_to_krw,
                                                                                      finex_price,
                                                                                      current_time.minute - finex_ten.check_date.minute,
                                                                                      finex_price_to_krw - finex_ten.coin_price * _rate,
                                                                                      arrow_func(finex_price_to_krw,
                                                                                                 finex_ten.coin_price * _rate))
            text20 = '현재 국내 {}의 가격\n'.format(_coin.upper())
            text21 = '빗썸: {:,.2f}원 \n({}분전에 비해 {:,.2f}원{})\n'.format(bithumb_current,
                                                                     current_time.minute - bithumb_ten.check_date.minute,
                                                                     bithumb_current - bithumb_ten.coin_price,
                                                                     arrow_func(bithumb_current,
                                                                                bithumb_ten.coin_price))
            text22 = '코인원: {:,.2f}원 \n({}분전에 비해 {:,.2f}원{})\n'.format(coinone_current,
                                                                      current_time.minute - coinone_ten.check_date.minute,
                                                                      coinone_current - coinone_ten.coin_price,
                                                                      arrow_func(coinone_current,
                                                                                 coinone_ten.coin_price))
            text23 = '코빗: {:,.2f}원 \n({}분전에 비해 {:,.2f}원{})\n\n'.format(korbit_current,
                                                                       current_time.minute - korbit_ten.check_date.minute,
                                                                       korbit_current - korbit_ten.coin_price,
                                                                       arrow_func(korbit_current,
                                                                                  korbit_ten.coin_price))

            return_text = text1 + text2 + text3 + text4 + text5 + text6 + text7 + text8 + text9 + text10 + text11 + text12 + text13 + text14 + text15 + text16 + text17 + text18 + text19 + text20 + text21 + text22 + text23

        # 코인원 비트파이넥스만 지원하는 코인
        if _coin == 'iota':
            tenminutes = timedelta(minutes=10)
            current_time = datetime.now()

            coinone_ten = CoinoneDB.objects.filter(check_date__range=(current_time - tenminutes, current_time),
                                                   coin_name=_coin.lower()).first()

            finex_ten = BitfinexDB.objects.filter(check_date__range=(current_time - tenminutes, current_time),
                                                  coin_name=_coin.lower()).first()
            # 사이트별 20분전 가격
            twenty = timedelta(minutes=20)

            coinone_twen = CoinoneDB.objects.filter(check_date__range=(current_time - twenty, current_time),
                                                    coin_name=_coin.lower()).first()

            finex_twen = BitfinexDB.objects.filter(check_date__range=(current_time - twenty, current_time),
                                                   coin_name=_coin.lower()).first()
            # 코인원이 안될 때
            try:
                coinone_current = float(coinchat.coinone(_coin))
            except ConnectionError as e:
                finex_price = float(coinchat.bitfinex(_coin))
                finex_price_to_krw = float(finex_price * _rate)
                text1 = '{}시 {}분경 가격\n'.format(coinone_twen.check_date.hour, coinone_twen.check_date.minute)
                text2 = '비트파이넥스: {:,.2f}원 {:,.2f}$\n\n'.format(finex_twen.coin_price * _rate, finex_twen.coin_price)
                text3 = '{}시 {}분경 가격 \n'.format(coinone_ten.check_date.hour, coinone_ten.check_date.minute)
                text4 = '비트파이넥스: {:,.2f}원 {:,.2f}$\n\n'.format(finex_ten.coin_price * _rate, finex_ten.coin_price)
                text5 = '현재 해외 {}의 가격\n'.format(_coin.upper())
                text6 = '비트파이넥스: {:,.2f}원 ({:,.2f}$) \n({}분전에 비해 {:,.2f}원{})\n'.format(finex_price_to_krw,
                                                                                       finex_price,
                                                                                       current_time.minute - finex_ten.check_date.minute,
                                                                                       finex_price_to_krw - finex_ten.coin_price * _rate,
                                                                                       arrow_func(finex_price_to_krw,
                                                                                                  finex_ten.coin_price * _rate))
                return_text = text1 + text2 + text3 + text4 + text5 + text6 + "**코인원 API와의 통신이 되지않아 코인원을 제외한 결과입니다.**"
                return data_func(return_text, buttons=_list)
            # 비트파이넥스가 안될 때
            try:
                finex_price = float(coinchat.bitfinex(_coin))
            except ConnectionError as e:
                coinone_current = float(coinchat.coinone(_coin))
                text1 = '{}시 {}분경 가격\n'.format(coinone_twen.check_date.hour, coinone_twen.check_date.minute)
                text2 = '코인원: {:,.2f}원\n'.format(coinone_twen.coin_price)
                text3 = '{}시 {}분경 가격 \n'.format(coinone_ten.check_date.hour, coinone_ten.check_date.minute)
                text4 = '코인원: {:,.2f}원\n'.format(coinone_ten.coin_price)
                text5 = '현재 국내 {}의 가격\n'.format(_coin.upper())
                text6 = '코인원: {:,.2f}원 \n({}분전에 비해 {:,.2f}원{})\n'.format(coinone_current,
                                                                         current_time.minute - coinone_ten.check_date.minute,
                                                                         coinone_current - coinone_ten.coin_price,
                                                                         arrow_func(coinone_current,
                                                                                    coinone_ten.coin_price))

                return_text = text1 + text2 + text3 + text4 + text5 + text6 + "**비트파이넥스 API와의 통신이 되지않아 비트파이넥스를 제외한 결과입니다.**"
                return data_func(return_text, buttons=_list)
            # 환율적용
            finex_price_to_krw = float(finex_price * _rate)
            # 사이트별 10분전 가격
            text1 = '김치 프리미엄 (현재 가격대비 등락) [국내:코인원, 해외:비트파이넥스 기준]\n'
            text2 = '현재 김치 프리미엄{:,.2f}% \n'.format(
                ((coinone_current - finex_price_to_krw) / finex_price_to_krw) * 100
            )
            text3 = '{}시 {}분경 김치 프리미엄{:,.2f}% ({:,.2f})%\n'.format(
                coinone_twen.check_date.hour, coinone_twen.check_date.minute,
                (coinone_twen.coin_price - (finex_twen.coin_price * _rate)) / (
                    finex_twen.coin_price * _rate) * 100,
                ((
                     coinone_current - finex_price_to_krw) / finex_price_to_krw) * 100 - (
                    coinone_twen.coin_price - (
                        finex_twen.coin_price * _rate)) / (
                    finex_twen.coin_price * _rate) * 100
            )
            text4 = '{}시 {}분경 김치 프리미엄{:,.2f}% ({:,.2f})%\n'.format(coinone_ten.check_date.hour,
                                                                   coinone_ten.check_date.minute, (
                                                                       coinone_ten.coin_price - (
                                                                           finex_ten.coin_price * _rate)) / (
                                                                       finex_ten.coin_price * _rate) * 100,
                                                                   ((
                                                                        coinone_current - finex_price_to_krw) / finex_price_to_krw) * 100 - (
                                                                       coinone_ten.coin_price - (
                                                                           finex_ten.coin_price * _rate)) / (
                                                                       finex_ten.coin_price * _rate) * 100
                                                                   )
            text5 = '{}시 {}분경 가격\n'.format(coinone_twen.check_date.hour, coinone_twen.check_date.minute)
            text6 = '코인원: {:,.2f}원\n'.format(coinone_twen.coin_price)
            text7 = '비트파이넥스: {:,.2f}원 {:,.2f}$\n\n'.format(finex_twen.coin_price * _rate, finex_twen.coin_price)
            text8 = '{}시 {}분경 가격 \n'.format(coinone_ten.check_date.hour, coinone_ten.check_date.minute)
            text9 = '코인원: {:,.2f}원\n'.format(coinone_ten.coin_price)
            text10 = '비트파이넥스: {:,.2f}원 {:,.2f}$\n\n'.format(finex_ten.coin_price * _rate, finex_ten.coin_price)
            text11 = '현재 해외 {}의 가격\n'.format(_coin.upper())
            text12 = '비트파이넥스: {:,.2f}원 ({:,.2f}$) \n({}분전에 비해 {:,.2f}원{})\n\n'.format(finex_price_to_krw, finex_price,
                                                                                      current_time.minute - finex_ten.check_date.minute,
                                                                                      finex_price_to_krw - finex_ten.coin_price * _rate,
                                                                                      arrow_func(finex_price_to_krw,
                                                                                                 finex_ten.coin_price * _rate))
            text13 = '현재 국내 {}의 가격\n'.format(_coin.upper())
            text14 = '코인원: {:,.2f}원 \n({}분전에 비해 {:,.2f}원{})'.format(coinone_current,
                                                                    current_time.minute - coinone_ten.check_date.minute,
                                                                    coinone_current - coinone_ten.coin_price,
                                                                    arrow_func(coinone_current,
                                                                               coinone_ten.coin_price))

            return_text = text1 + text2 + text3 + text4 + text5 + text6 + text7 + text8 + text9 + text10 + text11 + text12 + text13 + text14

        # 폴로닉스를 제외하고 전부 지원하는 코인
        if _coin == 'btg':
            # 사이트별 10분전 가격
            tenminutes = timedelta(minutes=10)
            current_time = datetime.now()
            bithumb_ten = BithumbDB.objects.filter(check_date__range=(current_time - tenminutes, current_time),
                                                   coin_name=_coin.upper()).first()

            coinone_ten = CoinoneDB.objects.filter(check_date__range=(current_time - tenminutes, current_time),
                                                   coin_name=_coin.lower()).first()
            korbit_ten = KorbitDB.objects.filter(check_date__range=(current_time - tenminutes, current_time),
                                                 coin_name=_coin.lower()).first()

            finex_ten = BitfinexDB.objects.filter(check_date__range=(current_time - tenminutes, current_time),
                                                  coin_name=_coin.lower()).first()
            # 사이트별 20분전 가격
            twenty = timedelta(minutes=20)
            bithumb_twen = BithumbDB.objects.filter(check_date__range=(current_time - twenty, current_time),
                                                    coin_name=_coin.upper()).first()

            coinone_twen = CoinoneDB.objects.filter(check_date__range=(current_time - twenty, current_time),
                                                    coin_name=_coin.lower()).first()
            korbit_twen = KorbitDB.objects.filter(check_date__range=(current_time - twenty, current_time),
                                                  coin_name=_coin.lower()).first()

            finex_twen = BitfinexDB.objects.filter(check_date__range=(current_time - twenty, current_time),
                                                   coin_name=_coin.lower()).first()
            # 빗썸이 안될 때
            try:
                bithumb_current = float(coinchat.lasttrading(_coin))
            except ConnectionError as e:
                coinone_current = float(coinchat.coinone(_coin))
                korbit_current = float(coinchat.korbit(_coin))
                finex_price = float(coinchat.bitfinex(_coin))
                finex_price_to_krw = float(finex_price * _rate)
                text1 = '김치 프리미엄 (현재 가격대비 등락) \n[국내:코인원, 해외:비트파이넥스 기준]\n'
                text2 = '현재 김치 프리미엄{:,.2f}% \n'.format(
                    ((coinone_current - finex_price_to_krw) / finex_price_to_krw) * 100
                )
                text3 = '{}시 {}분경 김치 프리미엄{:,.2f}% ({:,.2f})%\n'.format(
                    coinone_twen.check_date.hour, coinone_twen.check_date.minute,
                    (coinone_twen.coin_price - (finex_twen.coin_price * _rate)) / (
                        finex_twen.coin_price * _rate) * 100,
                    ((
                         coinone_current - finex_price_to_krw) / finex_price_to_krw) * 100 - (
                        coinone_twen.coin_price - (
                            finex_twen.coin_price * _rate)) / (
                        finex_twen.coin_price * _rate) * 100
                )
                text4 = '{}시 {}분경 김치 프리미엄{:,.2f}% ({:,.2f})%\n\n'.format(coinone_ten.check_date.hour,
                                                                         coinone_ten.check_date.minute, (
                                                                             coinone_ten.coin_price - (
                                                                                 finex_ten.coin_price * _rate)) / (
                                                                             finex_ten.coin_price * _rate) * 100,
                                                                         ((
                                                                              coinone_current - finex_price_to_krw) / finex_price_to_krw) * 100 - (
                                                                             coinone_ten.coin_price - (
                                                                                 finex_ten.coin_price * _rate)) / (
                                                                             finex_ten.coin_price * _rate) * 100
                                                                         )
                text5 = '{}시 {}분경 가격\n'.format(coinone_twen.check_date.hour, coinone_twen.check_date.minute)
                text6 = '코인원: {:,.2f}원\n'.format(coinone_twen.coin_price)
                text7 = '코빗: {:,.2f}원\n'.format(korbit_twen.coin_price)
                text8 = '비트파이넥스: {:,.2f}원 {:,.2f}$\n\n'.format(finex_twen.coin_price * _rate, finex_twen.coin_price)
                text9 = '{}시 {}분경 가격 \n'.format(coinone_ten.check_date.hour, coinone_ten.check_date.minute)
                text10 = '코인원: {:,.2f}원\n'.format(coinone_ten.coin_price)
                text11 = '코빗: {:,.2f}원\n'.format(korbit_ten.coin_price)
                text12 = '비트파이넥스: {:,.2f}원 {:,.2f}$\n\n'.format(finex_ten.coin_price * _rate, finex_ten.coin_price)
                text13 = '현재 해외 {}의 가격\n'.format(_coin.upper())
                text14 = '비트파이넥스: {:,.2f}원 ({:,.2f}$) ({}분전에 비해 {:,.2f}원{})\n\n'.format(finex_price_to_krw, finex_price,
                                                                                        current_time.minute - finex_ten.check_date.minute,
                                                                                        finex_price_to_krw - finex_ten.coin_price * _rate,
                                                                                        arrow_func(finex_price_to_krw,
                                                                                                   finex_ten.coin_price * _rate))
                text15 = '현재 국내 {}의 가격\n'.format(_coin.upper())
                text16 = '코인원: {:,.2f}원 \n({}분전에 비해 {:,.2f}원{})\n'.format(coinone_current,
                                                                          current_time.minute - coinone_ten.check_date.minute,
                                                                          coinone_current - coinone_ten.coin_price,
                                                                          arrow_func(coinone_current,
                                                                                     coinone_ten.coin_price))
                text17 = '코빗: {:,.2f}원 \n({}분전에 비해 {:,.2f}원{})\n'.format(korbit_current,
                                                                         current_time.minute - korbit_ten.check_date.minute,
                                                                         korbit_current - korbit_ten.coin_price,
                                                                         arrow_func(korbit_current,
                                                                                    korbit_ten.coin_price))

                return_text = text1 + text2 + text3 + text4 + text5 + text6 + text7 + text8 + text9 + text10 + text11 + text12 + text13 + text14 + text15 + text16 + text17 + "**빗썸 API와의 통신이 되지않아 빗썸을 제외한 결과입니다.**"
                return data_func(return_text, buttons=_list)
            # 코인원이 안될 때
            try:
                coinone_current = float(coinchat.coinone(_coin))
            except ConnectionError as e:
                bithumb_current = float(coinchat.lasttrading(_coin))
                korbit_current = float(coinchat.korbit(_coin))
                finex_price = float(coinchat.bitfinex(_coin))
                finex_price_to_krw = float(finex_price * _rate)
                text1 = '김치 프리미엄 (현재 가격대비 등락) \n[국내:빗썸, 해외:비트파이넥스 기준]\n'
                text2 = '현재 김치 프리미엄{:,.2f}% \n'.format(
                    ((bithumb_current - finex_price_to_krw) / finex_price_to_krw) * 100
                )
                text3 = '{}시 {}분경 김치 프리미엄{:,.2f}% ({:,.2f})%\n'.format(
                    bithumb_twen.check_date.hour, bithumb_twen.check_date.minute,
                    (bithumb_twen.coin_price - (finex_twen.coin_price * _rate)) / (
                        finex_twen.coin_price * _rate) * 100,
                    ((
                         bithumb_current - finex_price_to_krw) / finex_price_to_krw) * 100 - (
                        bithumb_twen.coin_price - (
                            finex_twen.coin_price * _rate)) / (
                        finex_twen.coin_price * _rate) * 100
                )
                text4 = '{}시 {}분경 김치 프리미엄{:,.2f}% ({:,.2f})%\n\n'.format(bithumb_ten.check_date.hour,
                                                                         bithumb_ten.check_date.minute, (
                                                                             bithumb_ten.coin_price - (
                                                                                 finex_ten.coin_price * _rate)) / (
                                                                             finex_ten.coin_price * _rate) * 100,
                                                                         ((
                                                                              bithumb_current - finex_price_to_krw) / finex_price_to_krw) * 100 - (
                                                                             bithumb_ten.coin_price - (
                                                                                 finex_ten.coin_price * _rate)) / (
                                                                             finex_ten.coin_price * _rate) * 100
                                                                         )
                text5 = '{}시 {}분경 가격\n'.format(bithumb_twen.check_date.hour, bithumb_twen.check_date.minute)
                text6 = '빗썸: {:,.2f}원\n'.format(bithumb_twen.coin_price)
                text7 = '코빗: {:,.2f}원\n'.format(korbit_twen.coin_price)
                text8 = '비트파이넥스: {:,.2f}원 {:,.2f}$\n\n'.format(finex_twen.coin_price * _rate, finex_twen.coin_price)
                text9 = '{}시 {}분경 가격 \n'.format(bithumb_ten.check_date.hour, bithumb_ten.check_date.minute)
                text10 = '빗썸: {:,.2f}원\n'.format(bithumb_ten.coin_price)
                text11 = '코빗: {:,.2f}원\n'.format(korbit_ten.coin_price)
                text12 = '비트파이넥스: {:,.2f}원 {:,.2f}$\n\n'.format(finex_ten.coin_price * _rate, finex_ten.coin_price)
                text13 = '현재 해외 {}의 가격\n'.format(_coin.upper())
                text14 = '비트파이넥스: {:,.2f}원 ({:,.2f}$) ({}분전에 비해 {:,.2f}원{})\n\n'.format(finex_price_to_krw, finex_price,
                                                                                        current_time.minute - finex_ten.check_date.minute,
                                                                                        finex_price_to_krw - finex_ten.coin_price * _rate,
                                                                                        arrow_func(finex_price_to_krw,
                                                                                                   finex_ten.coin_price * _rate))
                text15 = '현재 국내 {}의 가격\n'.format(_coin.upper())
                text16 = '빗썸: {:,.2f}원 \n({}분전에 비해 {:,.2f}원{})\n'.format(bithumb_current,
                                                                         current_time.minute - bithumb_ten.check_date.minute,
                                                                         bithumb_current - bithumb_ten.coin_price,
                                                                         arrow_func(bithumb_current,
                                                                                    bithumb_ten.coin_price))
                text17 = '코빗: {:,.2f}원 \n({}분전에 비해 {:,.2f}원{})\n'.format(korbit_current,
                                                                         current_time.minute - korbit_ten.check_date.minute,
                                                                         korbit_current - korbit_ten.coin_price,
                                                                         arrow_func(korbit_current,
                                                                                    korbit_ten.coin_price))

                return_text = text1 + text2 + text3 + text4 + text5 + text6 + text7 + text8 + text9 + text10 + text11 + text12 + text13 + text14 + text15 + text16 + text17 + "**코인원 API와의 통신이 되지않아 코인원을 제외한 결과입니다.**"
                return data_func(return_text, buttons=_list)
            try:
                korbit_current = float(coinchat.korbit(_coin))
            except ConnectionError as e:
                bithumb_current = float(coinchat.lasttrading(_coin))
                coinone_current = float(coinchat.coinone(_coin))
                finex_price = float(coinchat.bitfinex(_coin))
                finex_price_to_krw = float(finex_price * _rate)
                text1 = '김치 프리미엄 (현재 가격대비 등락) \n[국내:빗썸, 해외:비트파이넥스 기준]\n'
                text2 = '현재 김치 프리미엄{:,.2f}% \n'.format(
                    ((bithumb_current - finex_price_to_krw) / finex_price_to_krw) * 100
                )
                text3 = '{}시 {}분경 김치 프리미엄{:,.2f}% ({:,.2f})%\n'.format(
                    bithumb_twen.check_date.hour, bithumb_twen.check_date.minute,
                    (bithumb_twen.coin_price - (finex_twen.coin_price * _rate)) / (
                        finex_twen.coin_price * _rate) * 100,
                    ((
                         bithumb_current - finex_price_to_krw) / finex_price_to_krw) * 100 - (
                        bithumb_twen.coin_price - (
                            finex_twen.coin_price * _rate)) / (
                        finex_twen.coin_price * _rate) * 100
                )
                text4 = '{}시 {}분경 김치 프리미엄{:,.2f}% ({:,.2f})%\n\n'.format(bithumb_ten.check_date.hour,
                                                                         bithumb_ten.check_date.minute, (
                                                                             bithumb_ten.coin_price - (
                                                                                 finex_ten.coin_price * _rate)) / (
                                                                             finex_ten.coin_price * _rate) * 100,
                                                                         ((
                                                                              bithumb_current - finex_price_to_krw) / finex_price_to_krw) * 100 - (
                                                                             bithumb_ten.coin_price - (
                                                                                 finex_ten.coin_price * _rate)) / (
                                                                             finex_ten.coin_price * _rate) * 100
                                                                         )
                text5 = '{}시 {}분경 가격\n'.format(bithumb_twen.check_date.hour, bithumb_twen.check_date.minute)
                text6 = '빗썸: {:,.2f}원\n'.format(bithumb_twen.coin_price)
                text7 = '코인원: {:,.2f}원\n'.format(coinone_twen.coin_price)
                text8 = '비트파이넥스: {:,.2f}원 {:,.2f}$\n\n'.format(finex_twen.coin_price * _rate, finex_twen.coin_price)
                text9 = '{}시 {}분경 가격 \n'.format(bithumb_ten.check_date.hour, bithumb_ten.check_date.minute)
                text10 = '빗썸: {:,.2f}원\n'.format(bithumb_ten.coin_price)
                text11 = '코인원: {:,.2f}원\n'.format(coinone_ten.coin_price)
                text12 = '비트파이넥스: {:,.2f}원 {:,.2f}$\n\n'.format(finex_ten.coin_price * _rate, finex_ten.coin_price)
                text13 = '현재 해외 {}의 가격\n'.format(_coin.upper())
                text14 = '비트파이넥스: {:,.2f}원 ({:,.2f}$) ({}분전에 비해 {:,.2f}원{})\n\n'.format(finex_price_to_krw, finex_price,
                                                                                        current_time.minute - finex_ten.check_date.minute,
                                                                                        finex_price_to_krw - finex_ten.coin_price * _rate,
                                                                                        arrow_func(finex_price_to_krw,
                                                                                                   finex_ten.coin_price * _rate))
                text15 = '현재 국내 {}의 가격\n'.format(_coin.upper())
                text16 = '빗썸: {:,.2f}원 \n({}분전에 비해 {:,.2f}원{})\n'.format(bithumb_current,
                                                                         current_time.minute - bithumb_ten.check_date.minute,
                                                                         bithumb_current - bithumb_ten.coin_price,
                                                                         arrow_func(bithumb_current,
                                                                                    bithumb_ten.coin_price))
                text17 = '코인원: {:,.2f}원 \n({}분전에 비해 {:,.2f}원{})\n'.format(coinone_current,
                                                                          current_time.minute - coinone_ten.check_date.minute,
                                                                          coinone_current - coinone_ten.coin_price,
                                                                          arrow_func(coinone_current,
                                                                                     coinone_ten.coin_price))

                return_text = text1 + text2 + text3 + text4 + text5 + text6 + text7 + text8 + text9 + text10 + text11 + text12 + text13 + text14 + text15 + text16 + text17 + "**코빗 API와의 통신이 되지않아 코빗을 제외한 결과입니다.**"
                return data_func(return_text, buttons=_list)
            # 비트파이넥스가 안될 때
            try:
                finex_price = float(coinchat.bitfinex(_coin))
            except ConnectionError as e:
                bithumb_current = float(coinchat.lasttrading(_coin))
                coinone_current = float(coinchat.coinone(_coin))
                korbit_current = float(coinchat.korbit(_coin))
                text1 = '{}시 {}분경 가격\n'.format(bithumb_twen.check_date.hour, bithumb_twen.check_date.minute)
                text2 = '빗썸: {:,.2f}원\n'.format(bithumb_twen.coin_price)
                text3 = '코인원: {:,.2f}원\n'.format(coinone_twen.coin_price)
                text4 = '코빗: {:,.2f}원\n'.format(korbit_twen.coin_price)
                text5 = '{}시 {}분경 가격 \n'.format(bithumb_ten.check_date.hour, bithumb_ten.check_date.minute)
                text6 = '빗썸: {:,.2f}원\n'.format(bithumb_ten.coin_price)
                text7 = '코인원: {:,.2f}원\n'.format(coinone_ten.coin_price)
                text8 = '코빗: {:,.2f}원\n'.format(korbit_ten.coin_price)
                text9 = '현재 국내 {}의 가격\n'.format(_coin.upper())
                text10 = '빗썸: {:,.2f}원 \n({}분전에 비해 {:,.2f}원{})\n'.format(bithumb_current,
                                                                         current_time.minute - bithumb_ten.check_date.minute,
                                                                         bithumb_current - bithumb_ten.coin_price,
                                                                         arrow_func(bithumb_current,
                                                                                    bithumb_ten.coin_price))
                text11 = '코인원: {:,.2f}원 \n({}분전에 비해 {:,.2f}원{})\n'.format(coinone_current,
                                                                          current_time.minute - coinone_ten.check_date.minute,
                                                                          coinone_current - coinone_ten.coin_price,
                                                                          arrow_func(coinone_current,
                                                                                     coinone_ten.coin_price))
                text12 = '코빗: {:,.2f}원 \n({}분전에 비해 {:,.2f}원{})'.format(korbit_current,
                                                                       current_time.minute - korbit_ten.check_date.minute,
                                                                       korbit_current - korbit_ten.coin_price,
                                                                       arrow_func(korbit_current,
                                                                                  korbit_ten.coin_price))

                return_text = text1 + text2 + text3 + text4 + text5 + text6 + text7 + text8 + text9 + text10 + text11 + text12 + "**비트파이넥스 API와의 통신이 되지않아 비트파이넥스를 제외한 결과입니다.**"
                return data_func(return_text, buttons=_list)

            finex_price_to_krw = float(finex_price * _rate)
            text1 = '김치 프리미엄 (현재 가격대비 등락) \n[국내:빗썸, 해외:비트파이넥스 기준]\n'
            text2 = '현재 김치 프리미엄{:,.2f}% \n'.format(
                ((bithumb_current - finex_price_to_krw) / finex_price_to_krw) * 100
            )
            text3 = '{}시 {}분경 김치 프리미엄{:,.2f}% ({:,.2f})%\n'.format(
                bithumb_twen.check_date.hour, bithumb_twen.check_date.minute,
                (bithumb_twen.coin_price - (finex_twen.coin_price * _rate)) / (
                    finex_twen.coin_price * _rate) * 100,
                ((
                     bithumb_current - finex_price_to_krw) / finex_price_to_krw) * 100 - (
                    bithumb_twen.coin_price - (
                        finex_twen.coin_price * _rate)) / (
                    finex_twen.coin_price * _rate) * 100
            )
            text4 = '{}시 {}분경 김치 프리미엄{:,.2f}% ({:,.2f})%\n\n'.format(bithumb_ten.check_date.hour,
                                                                     bithumb_ten.check_date.minute, (
                                                                         bithumb_ten.coin_price - (
                                                                             finex_ten.coin_price * _rate)) / (
                                                                         finex_ten.coin_price * _rate) * 100,
                                                                     ((
                                                                          bithumb_current - finex_price_to_krw) / finex_price_to_krw) * 100 - (
                                                                         bithumb_ten.coin_price - (
                                                                             finex_ten.coin_price * _rate)) / (
                                                                         finex_ten.coin_price * _rate) * 100
                                                                     )
            text5 = '{}시 {}분경 가격\n'.format(bithumb_twen.check_date.hour, bithumb_twen.check_date.minute)
            text6 = '빗썸: {:,.2f}원\n'.format(bithumb_twen.coin_price)
            text7 = '코인원: {:,.2f}원\n'.format(coinone_twen.coin_price)
            text8 = '코빗: {:,.2f}원\n'.format(korbit_twen.coin_price)
            text9 = '비트파이넥스: {:,.2f}원 {:,.2f}$\n\n'.format(finex_twen.coin_price * _rate, finex_twen.coin_price)
            text10 = '{}시 {}분경 가격 \n'.format(bithumb_ten.check_date.hour, bithumb_ten.check_date.minute)
            text11 = '빗썸: {:,.2f}원\n'.format(bithumb_ten.coin_price)
            text12 = '코인원: {:,.2f}원\n'.format(coinone_ten.coin_price)
            text13 = '코빗: {:,.2f}원\n'.format(korbit_ten.coin_price)
            text14 = '비트파이넥스: {:,.2f}원 {:,.2f}$\n\n'.format(finex_ten.coin_price * _rate, finex_ten.coin_price)
            text15 = '현재 해외 {}의 가격\n'.format(_coin.upper())
            text16 = '비트파이넥스: {:,.2f}원 ({:,.2f}$) ({}분전에 비해 {:,.2f}원{})\n\n'.format(finex_price_to_krw, finex_price,
                                                                                    current_time.minute - finex_ten.check_date.minute,
                                                                                    finex_price_to_krw - finex_ten.coin_price * _rate,
                                                                                    arrow_func(finex_price_to_krw,
                                                                                               finex_ten.coin_price * _rate))
            text17 = '현재 국내 {}의 가격\n'.format(_coin.upper())
            text18 = '빗썸: {:,.2f}원 \n({}분전에 비해 {:,.2f}원{})\n'.format(bithumb_current,
                                                                     current_time.minute - bithumb_ten.check_date.minute,
                                                                     bithumb_current - bithumb_ten.coin_price,
                                                                     arrow_func(bithumb_current,
                                                                                bithumb_ten.coin_price))
            text19 = '코인원: {:,.2f}원 \n({}분전에 비해 {:,.2f}원{})\n'.format(coinone_current,
                                                                      current_time.minute - coinone_ten.check_date.minute,
                                                                      coinone_current - coinone_ten.coin_price,
                                                                      arrow_func(coinone_current,
                                                                                 coinone_ten.coin_price))
            text20 = '코빗: {:,.2f}원 \n({}분전에 비해 {:,.2f}원{})'.format(korbit_current,
                                                                   current_time.minute - korbit_ten.check_date.minute,
                                                                   korbit_current - korbit_ten.coin_price,
                                                                   arrow_func(korbit_current,
                                                                              korbit_ten.coin_price))

            return_text = text1 + text2 + text3 + text4 + text5 + text6 + text7 + text8 + text9 + text10 + text11 + text12 + text13 + text14 + text15 + text16 + text17 + text18 + text19 + text20

        # 코빗을 제외하고 지원하는 코인
        if _coin == 'ltc':
            # 사이트별 10분전 가격
            tenminutes = timedelta(minutes=10)
            current_time = datetime.now()
            bithumb_ten = BithumbDB.objects.filter(check_date__range=(current_time - tenminutes, current_time),
                                                   coin_name=_coin.upper()).first()

            coinone_ten = CoinoneDB.objects.filter(check_date__range=(current_time - tenminutes, current_time),
                                                   coin_name=_coin.lower()).first()
            poloniex_ten = PoloniexDB.objects.filter(check_date__range=(current_time - tenminutes, current_time),
                                                     coin_name=_coin.upper()).first()
            finex_ten = BitfinexDB.objects.filter(check_date__range=(current_time - tenminutes, current_time),
                                                  coin_name=_coin.lower()).first()
            # 사이트별 20분전 가격
            twenty = timedelta(minutes=20)
            bithumb_twen = BithumbDB.objects.filter(check_date__range=(current_time - twenty, current_time),
                                                    coin_name=_coin.upper()).first()

            coinone_twen = CoinoneDB.objects.filter(check_date__range=(current_time - twenty, current_time),
                                                    coin_name=_coin.lower()).first()
            poloniex_twen = PoloniexDB.objects.filter(check_date__range=(current_time - twenty, current_time),
                                                      coin_name=_coin.upper()).first()
            finex_twen = BitfinexDB.objects.filter(check_date__range=(current_time - twenty, current_time),
                                                   coin_name=_coin.lower()).first()
            # 빗썸이 안될 때
            try:
                bithumb_current = float(coinchat.lasttrading(_coin))
            except ConnectionError as e:
                coinone_current = float(coinchat.coinone(_coin))
                poloniex_price = float(coinchat.poloniex(_coin))
                finex_price = float(coinchat.bitfinex(_coin))
                poloniex_price_to_krw = float(poloniex_price * _rate)
                finex_price_to_krw = float(finex_price * _rate)
                text1 = '김치 프리미엄 (현재 가격대비 등락) \n[국내:코인원, 해외:폴로닉스 기준]\n'
                text2 = '현재 김치 프리미엄{:,.2f}% \n'.format(
                    ((coinone_current - poloniex_price_to_krw) / poloniex_price_to_krw) * 100
                )
                text3 = '{}시 {}분경 김치 프리미엄{:,.2f}% ({:,.2f})%\n'.format(
                    coinone_twen.check_date.hour, coinone_twen.check_date.minute,
                    (coinone_twen.coin_price - (poloniex_twen.coin_price * _rate)) / (
                        poloniex_twen.coin_price * _rate) * 100,
                    ((
                         coinone_current - poloniex_price_to_krw) / poloniex_price_to_krw) * 100 - (
                        coinone_twen.coin_price - (
                            poloniex_twen.coin_price * _rate)) / (
                        poloniex_twen.coin_price * _rate) * 100
                )
                text4 = '{}시 {}분경 김치 프리미엄{:,.2f}% ({:,.2f})%\n\n'.format(coinone_ten.check_date.hour,
                                                                         coinone_ten.check_date.minute, (
                                                                             coinone_ten.coin_price - (
                                                                                 poloniex_ten.coin_price * _rate)) / (
                                                                             poloniex_ten.coin_price * _rate) * 100,
                                                                         ((
                                                                              coinone_current - poloniex_price_to_krw) / poloniex_price_to_krw) * 100 - (
                                                                             coinone_ten.coin_price - (
                                                                                 poloniex_ten.coin_price * _rate)) / (
                                                                             poloniex_ten.coin_price * _rate) * 100
                                                                         )

                text5 = '{}시 {}분경 가격\n'.format(coinone_twen.check_date.hour, coinone_twen.check_date.minute)
                text6 = '코인원: {:,.2f}원\n'.format(coinone_twen.coin_price)
                text7 = '폴로닉스: {:,.2f}원 {:,.2f}$\n'.format(poloniex_twen.coin_price * _rate, poloniex_twen.coin_price)
                text8 = '비트파이넥스: {:,.2f}원 {:,.2f}$\n\n'.format(finex_twen.coin_price * _rate, finex_twen.coin_price)
                text9 = '{}시 {}분경 가격 \n'.format(coinone_ten.check_date.hour, coinone_ten.check_date.minute)
                text10 = '코인원: {:,.2f}원\n'.format(coinone_ten.coin_price)
                text11 = '폴로닉스: {:,.2f}원 {:,.2f}$\n'.format(poloniex_ten.coin_price * _rate, poloniex_ten.coin_price)
                text12 = '비트파이넥스: {:,.2f}원 {:,.2f}$\n\n'.format(finex_ten.coin_price * _rate, finex_ten.coin_price)
                text13 = '현재 해외 {}의 가격\n'.format(_coin.upper())
                text14 = '폴로닉스: {:,.2f}원 ({:,.2f}$) \n({}분전에 비해 {:,.2f}원{})\n'.format(poloniex_price_to_krw,
                                                                                      poloniex_price,
                                                                                      current_time.minute - poloniex_ten.check_date.minute,
                                                                                      poloniex_price_to_krw - poloniex_ten.coin_price * _rate,
                                                                                      arrow_func(poloniex_price_to_krw,
                                                                                                 poloniex_ten.coin_price * _rate))
                text15 = '비트파이넥스: {:,.2f}원 ({:,.2f}$) \n({}분전에 비해 {:,.2f}원{})\n\n'.format(finex_price_to_krw,
                                                                                          finex_price,
                                                                                          current_time.minute - finex_ten.check_date.minute,
                                                                                          finex_price_to_krw - finex_ten.coin_price * _rate,
                                                                                          arrow_func(finex_price_to_krw,
                                                                                                     finex_ten.coin_price * _rate))
                text16 = '현재 국내 {}의 가격\n'.format(_coin.upper())
                text17 = '코인원: {:,.2f}원 \n({}분전에 비해 {:,.2f}원{})'.format(coinone_current,
                                                                        current_time.minute - coinone_ten.check_date.minute,
                                                                        coinone_current - coinone_ten.coin_price,
                                                                        arrow_func(coinone_current,
                                                                                   coinone_ten.coin_price))

                return_text = text1 + text2 + text3 + text4 + text5 + text6 + text7 + text8 + text9 + text10 + text11 + text12 + text13 + text14 + text15 + text16 + text17 + "**빗썸 API와의 통신이 되지않아 빗썸을 제외한 결과입니다.**"
                return data_func(return_text, buttons=_list)
            # 코인원이 안될 때
            try:
                coinone_current = float(coinchat.coinone(_coin))
            except ConnectionError as e:
                bithumb_current = float(coinchat.lasttrading(_coin))
                poloniex_price = float(coinchat.poloniex(_coin))
                finex_price = float(coinchat.bitfinex(_coin))
                poloniex_price_to_krw = float(poloniex_price * _rate)
                finex_price_to_krw = float(finex_price * _rate)
                text1 = '김치 프리미엄 (현재 가격대비 등락) \n[국내:빗썸, 해외:폴로닉스 기준]\n'
                text2 = '현재 김치 프리미엄{:,.2f}% \n'.format(
                    ((bithumb_current - poloniex_price_to_krw) / poloniex_price_to_krw) * 100
                )
                text3 = '{}시 {}분경 김치 프리미엄{:,.2f}% ({:,.2f})%\n'.format(
                    bithumb_twen.check_date.hour, bithumb_twen.check_date.minute,
                    (bithumb_twen.coin_price - (poloniex_twen.coin_price * _rate)) / (
                        poloniex_twen.coin_price * _rate) * 100,
                    ((
                         bithumb_current - poloniex_price_to_krw) / poloniex_price_to_krw) * 100 - (
                        bithumb_twen.coin_price - (
                            poloniex_twen.coin_price * _rate)) / (
                        poloniex_twen.coin_price * _rate) * 100
                )
                text4 = '{}시 {}분경 김치 프리미엄{:,.2f}% ({:,.2f})%\n\n'.format(bithumb_ten.check_date.hour,
                                                                         bithumb_ten.check_date.minute, (
                                                                             bithumb_ten.coin_price - (
                                                                                 poloniex_ten.coin_price * _rate)) / (
                                                                             poloniex_ten.coin_price * _rate) * 100,
                                                                         ((
                                                                              bithumb_current - poloniex_price_to_krw) / poloniex_price_to_krw) * 100 - (
                                                                             bithumb_ten.coin_price - (
                                                                                 poloniex_ten.coin_price * _rate)) / (
                                                                             poloniex_ten.coin_price * _rate) * 100
                                                                         )

                text5 = '{}시 {}분경 가격\n'.format(bithumb_twen.check_date.hour, bithumb_twen.check_date.minute)
                text6 = '빗썸: {:,.2f}원\n'.format(bithumb_twen.coin_price)
                text7 = '폴로닉스: {:,.2f}원 {:,.2f}$\n'.format(poloniex_twen.coin_price * _rate, poloniex_twen.coin_price)
                text8 = '비트파이넥스: {:,.2f}원 {:,.2f}$\n\n'.format(finex_twen.coin_price * _rate, finex_twen.coin_price)
                text9 = '{}시 {}분경 가격 \n'.format(bithumb_ten.check_date.hour, bithumb_ten.check_date.minute)
                text10 = '빗썸: {:,.2f}원\n'.format(bithumb_ten.coin_price)
                text11 = '폴로닉스: {:,.2f}원 {:,.2f}$\n'.format(poloniex_ten.coin_price * _rate, poloniex_ten.coin_price)
                text12 = '비트파이넥스: {:,.2f}원 {:,.2f}$\n\n'.format(finex_ten.coin_price * _rate, finex_ten.coin_price)
                text13 = '현재 해외 {}의 가격\n'.format(_coin.upper())
                text14 = '폴로닉스: {:,.2f}원 ({:,.2f}$) \n({}분전에 비해 {:,.2f}원{})\n'.format(poloniex_price_to_krw,
                                                                                      poloniex_price,
                                                                                      current_time.minute - poloniex_ten.check_date.minute,
                                                                                      poloniex_price_to_krw - poloniex_ten.coin_price * _rate,
                                                                                      arrow_func(poloniex_price_to_krw,
                                                                                                 poloniex_ten.coin_price * _rate))
                text15 = '비트파이넥스: {:,.2f}원 ({:,.2f}$) \n({}분전에 비해 {:,.2f}원{})\n\n'.format(finex_price_to_krw,
                                                                                          finex_price,
                                                                                          current_time.minute - finex_ten.check_date.minute,
                                                                                          finex_price_to_krw - finex_ten.coin_price * _rate,
                                                                                          arrow_func(finex_price_to_krw,
                                                                                                     finex_ten.coin_price * _rate))
                text16 = '현재 국내 {}의 가격\n'.format(_coin.upper())
                text17 = '빗썸: {:,.2f}원 \n({}분전에 비해 {:,.2f}원{})\n'.format(bithumb_current,
                                                                         current_time.minute - bithumb_ten.check_date.minute,
                                                                         bithumb_current - bithumb_ten.coin_price,
                                                                         arrow_func(bithumb_current,
                                                                                    bithumb_ten.coin_price))

                return_text = text1 + text2 + text3 + text4 + text5 + text6 + text7 + text8 + text9 + text10 + text11 + text12 + text13 + text14 + text15 + text16 + text17 + "**코인원 API와의 통신이 되지않아 코인원을 제외한 결과입니다.**"
                return data_func(return_text, buttons=_list)
            # 폴로닉스가 안될 때
            try:
                poloniex_price = float(coinchat.poloniex(_coin))
            except ConnectionError as e:
                bithumb_current = float(coinchat.lasttrading(_coin))
                coinone_current = float(coinchat.coinone(_coin))
                finex_price = float(coinchat.bitfinex(_coin))
                finex_price_to_krw = float(finex_price * _rate)
                text1 = '김치 프리미엄 (현재 가격대비 등락) \n[국내:빗썸, 해외:비트파이넥스 기준]\n'
                text2 = '현재 김치 프리미엄{:,.2f}% \n'.format(
                    ((bithumb_current - finex_price_to_krw) / finex_price_to_krw) * 100
                )
                text3 = '{}시 {}분경 김치 프리미엄{:,.2f}% ({:,.2f})%\n'.format(
                    bithumb_twen.check_date.hour, bithumb_twen.check_date.minute,
                    (bithumb_twen.coin_price - (finex_twen.coin_price * _rate)) / (
                        finex_twen.coin_price * _rate) * 100,
                    ((
                         bithumb_current - finex_price_to_krw) / finex_price_to_krw) * 100 - (
                        bithumb_twen.coin_price - (
                            finex_twen.coin_price * _rate)) / (
                        finex_twen.coin_price * _rate) * 100
                )
                text4 = '{}시 {}분경 김치 프리미엄{:,.2f}% ({:,.2f})%\n\n'.format(bithumb_ten.check_date.hour,
                                                                         bithumb_ten.check_date.minute, (
                                                                             bithumb_ten.coin_price - (
                                                                                 finex_ten.coin_price * _rate)) / (
                                                                             finex_ten.coin_price * _rate) * 100,
                                                                         ((
                                                                              bithumb_current - finex_price_to_krw) / finex_price_to_krw) * 100 - (
                                                                             bithumb_ten.coin_price - (
                                                                                 finex_ten.coin_price * _rate)) / (
                                                                             finex_ten.coin_price * _rate) * 100
                                                                         )

                text5 = '{}시 {}분경 가격\n'.format(bithumb_twen.check_date.hour, bithumb_twen.check_date.minute)
                text6 = '빗썸: {:,.2f}원\n'.format(bithumb_twen.coin_price)
                text7 = '코인원: {:,.2f}원\n'.format(coinone_twen.coin_price)
                text8 = '비트파이넥스: {:,.2f}원 {:,.2f}$\n\n'.format(finex_twen.coin_price * _rate, finex_twen.coin_price)
                text9 = '{}시 {}분경 가격 \n'.format(bithumb_ten.check_date.hour, bithumb_ten.check_date.minute)
                text10 = '빗썸: {:,.2f}원\n'.format(bithumb_ten.coin_price)
                text11 = '코인원: {:,.2f}원\n'.format(coinone_ten.coin_price)
                text12 = '비트파이넥스: {:,.2f}원 {:,.2f}$\n\n'.format(finex_ten.coin_price * _rate, finex_ten.coin_price)
                text13 = '현재 해외 {}의 가격\n'.format(_coin.upper())
                text14 = '비트파이넥스: {:,.2f}원 ({:,.2f}$) \n({}분전에 비해 {:,.2f}원{})\n\n'.format(finex_price_to_krw,
                                                                                          finex_price,
                                                                                          current_time.minute - finex_ten.check_date.minute,
                                                                                          finex_price_to_krw - finex_ten.coin_price * _rate,
                                                                                          arrow_func(finex_price_to_krw,
                                                                                                     finex_ten.coin_price * _rate))
                text15 = '현재 국내 {}의 가격\n'.format(_coin.upper())
                text16 = '빗썸: {:,.2f}원 \n({}분전에 비해 {:,.2f}원{})\n'.format(bithumb_current,
                                                                         current_time.minute - bithumb_ten.check_date.minute,
                                                                         bithumb_current - bithumb_ten.coin_price,
                                                                         arrow_func(bithumb_current,
                                                                                    bithumb_ten.coin_price))
                text17 = '코인원: {:,.2f}원 \n({}분전에 비해 {:,.2f}원{})\n'.format(coinone_current,
                                                                          current_time.minute - coinone_ten.check_date.minute,
                                                                          coinone_current - coinone_ten.coin_price,
                                                                          arrow_func(coinone_current,
                                                                                     coinone_ten.coin_price))

                return_text = text1 + text2 + text3 + text4 + text5 + text6 + text7 + text8 + text9 + text10 + text11 + text12 + text13 + text14 + text15 + text16 + text17 + "**폴로닉스 API와의 통신이 되지않아 폴로닉스를 제외한 결과입니다.**"
                return data_func(return_text, buttons=_list)
            # 비트파이넥스가 안될 때
            try:
                finex_price = float(coinchat.bitfinex(_coin))
            except ConnectionError as e:
                bithumb_current = float(coinchat.lasttrading(_coin))
                coinone_current = float(coinchat.coinone(_coin))
                poloniex_price = float(coinchat.poloniex(_coin))
                poloniex_price_to_krw = float(poloniex_price * _rate)
                text1 = '김치 프리미엄 (현재 가격대비 등락) \n[국내:빗썸, 해외:폴로닉스 기준]\n'
                text2 = '현재 김치 프리미엄{:,.2f}% \n'.format(
                    ((bithumb_current - poloniex_price_to_krw) / poloniex_price_to_krw) * 100
                )
                text3 = '{}시 {}분경 김치 프리미엄{:,.2f}% ({:,.2f})%\n'.format(
                    bithumb_twen.check_date.hour, bithumb_twen.check_date.minute,
                    (bithumb_twen.coin_price - (poloniex_twen.coin_price * _rate)) / (
                        poloniex_twen.coin_price * _rate) * 100,
                    ((
                         bithumb_current - poloniex_price_to_krw) / poloniex_price_to_krw) * 100 - (
                        bithumb_twen.coin_price - (
                            poloniex_twen.coin_price * _rate)) / (
                        poloniex_twen.coin_price * _rate) * 100
                )
                text4 = '{}시 {}분경 김치 프리미엄{:,.2f}% ({:,.2f})%\n\n'.format(bithumb_ten.check_date.hour,
                                                                         bithumb_ten.check_date.minute, (
                                                                             bithumb_ten.coin_price - (
                                                                                 poloniex_ten.coin_price * _rate)) / (
                                                                             poloniex_ten.coin_price * _rate) * 100,
                                                                         ((
                                                                              bithumb_current - poloniex_price_to_krw) / poloniex_price_to_krw) * 100 - (
                                                                             bithumb_ten.coin_price - (
                                                                                 poloniex_ten.coin_price * _rate)) / (
                                                                             poloniex_ten.coin_price * _rate) * 100
                                                                         )

                text5 = '{}시 {}분경 가격\n'.format(bithumb_twen.check_date.hour, bithumb_twen.check_date.minute)
                text6 = '빗썸: {:,.2f}원\n'.format(bithumb_twen.coin_price)
                text7 = '코인원: {:,.2f}원\n'.format(coinone_twen.coin_price)
                text8 = '폴로닉스: {:,.2f}원 {:,.2f}$\n'.format(poloniex_twen.coin_price * _rate, poloniex_twen.coin_price)
                text9 = '{}시 {}분경 가격 \n'.format(bithumb_ten.check_date.hour, bithumb_ten.check_date.minute)
                text10 = '빗썸: {:,.2f}원\n'.format(bithumb_ten.coin_price)
                text11 = '코인원: {:,.2f}원\n'.format(coinone_ten.coin_price)
                text12 = '폴로닉스: {:,.2f}원 {:,.2f}$\n'.format(poloniex_ten.coin_price * _rate, poloniex_ten.coin_price)
                text13 = '현재 해외 {}의 가격\n'.format(_coin.upper())
                text14 = '폴로닉스: {:,.2f}원 ({:,.2f}$) \n({}분전에 비해 {:,.2f}원{})\n'.format(poloniex_price_to_krw,
                                                                                      poloniex_price,
                                                                                      current_time.minute - poloniex_ten.check_date.minute,
                                                                                      poloniex_price_to_krw - poloniex_ten.coin_price * _rate,
                                                                                      arrow_func(poloniex_price_to_krw,
                                                                                                 poloniex_ten.coin_price * _rate))
                text15 = '현재 국내 {}의 가격\n'.format(_coin.upper())
                text16 = '빗썸: {:,.2f}원 \n({}분전에 비해 {:,.2f}원{})\n'.format(bithumb_current,
                                                                         current_time.minute - bithumb_ten.check_date.minute,
                                                                         bithumb_current - bithumb_ten.coin_price,
                                                                         arrow_func(bithumb_current,
                                                                                    bithumb_ten.coin_price))
                text17 = '코인원: {:,.2f}원 \n({}분전에 비해 {:,.2f}원{})\n'.format(coinone_current,
                                                                          current_time.minute - coinone_ten.check_date.minute,
                                                                          coinone_current - coinone_ten.coin_price,
                                                                          arrow_func(coinone_current,
                                                                                     coinone_ten.coin_price))

                return_text = text1 + text2 + text3 + text4 + text5 + text6 + text7 + text8 + text9 + text10 + text11 + text12 + text13 + text14 + text15 + text16 + text17 + "**비트파이넥스 API와의 통신이 되지않아 비트파이넥스를 제외한 결과입니다.**"
                return data_func(return_text, buttons=_list)
            # 환율 적용
            poloniex_price_to_krw = float(poloniex_price * _rate)
            finex_price_to_krw = float(finex_price * _rate)
            text1 = '김치 프리미엄 (현재 가격대비 등락) \n[국내:빗썸, 해외:폴로닉스 기준]\n'
            text2 = '현재 김치 프리미엄{:,.2f}% \n'.format(
                ((bithumb_current - poloniex_price_to_krw) / poloniex_price_to_krw) * 100
            )
            text3 = '{}시 {}분경 김치 프리미엄{:,.2f}% ({:,.2f})%\n'.format(
                bithumb_twen.check_date.hour, bithumb_twen.check_date.minute,
                (bithumb_twen.coin_price - (poloniex_twen.coin_price * _rate)) / (
                    poloniex_twen.coin_price * _rate) * 100,
                ((
                     bithumb_current - poloniex_price_to_krw) / poloniex_price_to_krw) * 100 - (
                    bithumb_twen.coin_price - (
                        poloniex_twen.coin_price * _rate)) / (
                    poloniex_twen.coin_price * _rate) * 100
            )
            text4 = '{}시 {}분경 김치 프리미엄{:,.2f}% ({:,.2f})%\n\n'.format(bithumb_ten.check_date.hour,
                                                                     bithumb_ten.check_date.minute, (
                                                                         bithumb_ten.coin_price - (
                                                                             poloniex_ten.coin_price * _rate)) / (
                                                                         poloniex_ten.coin_price * _rate) * 100,
                                                                     ((
                                                                          bithumb_current - poloniex_price_to_krw) / poloniex_price_to_krw) * 100 - (
                                                                         bithumb_ten.coin_price - (
                                                                             poloniex_ten.coin_price * _rate)) / (
                                                                         poloniex_ten.coin_price * _rate) * 100
                                                                     )

            text5 = '{}시 {}분경 가격\n'.format(bithumb_twen.check_date.hour, bithumb_twen.check_date.minute)
            text6 = '빗썸: {:,.2f}원\n'.format(bithumb_twen.coin_price)
            text7 = '코인원: {:,.2f}원\n'.format(coinone_twen.coin_price)
            text8 = '폴로닉스: {:,.2f}원 {:,.2f}$\n'.format(poloniex_twen.coin_price * _rate, poloniex_twen.coin_price)
            text9 = '비트파이넥스: {:,.2f}원 {:,.2f}$\n\n'.format(finex_twen.coin_price * _rate, finex_twen.coin_price)
            text10 = '{}시 {}분경 가격 \n'.format(bithumb_ten.check_date.hour, bithumb_ten.check_date.minute)
            text11 = '빗썸: {:,.2f}원\n'.format(bithumb_ten.coin_price)
            text12 = '코인원: {:,.2f}원\n'.format(coinone_ten.coin_price)
            text13 = '폴로닉스: {:,.2f}원 {:,.2f}$\n'.format(poloniex_ten.coin_price * _rate, poloniex_ten.coin_price)
            text14 = '비트파이넥스: {:,.2f}원 {:,.2f}$\n\n'.format(finex_ten.coin_price * _rate, finex_ten.coin_price)
            text15 = '현재 해외 {}의 가격\n'.format(_coin.upper())
            text16 = '폴로닉스: {:,.2f}원 ({:,.2f}$) \n({}분전에 비해 {:,.2f}원{})\n'.format(poloniex_price_to_krw,
                                                                                  poloniex_price,
                                                                                  current_time.minute - poloniex_ten.check_date.minute,
                                                                                  poloniex_price_to_krw - poloniex_ten.coin_price * _rate,
                                                                                  arrow_func(poloniex_price_to_krw,
                                                                                             poloniex_ten.coin_price * _rate))
            text17 = '비트파이넥스: {:,.2f}원 ({:,.2f}$) \n({}분전에 비해 {:,.2f}원{})\n\n'.format(finex_price_to_krw,
                                                                                      finex_price,
                                                                                      current_time.minute - finex_ten.check_date.minute,
                                                                                      finex_price_to_krw - finex_ten.coin_price * _rate,
                                                                                      arrow_func(finex_price_to_krw,
                                                                                                 finex_ten.coin_price * _rate))
            text18 = '현재 국내 {}의 가격\n'.format(_coin.upper())
            text19 = '빗썸: {:,.2f}원 \n({}분전에 비해 {:,.2f}원{})\n'.format(bithumb_current,
                                                                     current_time.minute - bithumb_ten.check_date.minute,
                                                                     bithumb_current - bithumb_ten.coin_price,
                                                                     arrow_func(bithumb_current,
                                                                                bithumb_ten.coin_price))
            text20 = '코인원: {:,.2f}원 \n({}분전에 비해 {:,.2f}원{})'.format(coinone_current,
                                                                    current_time.minute - coinone_ten.check_date.minute,
                                                                    coinone_current - coinone_ten.coin_price,
                                                                    arrow_func(coinone_current,
                                                                               coinone_ten.coin_price))

            return_text = text1 + text2 + text3 + text5 + text6 + text7 + text8 + text9 + text10 + text11 + text12 + text13 + text14 + text15 + text16 + text17 + text18 + text19 + text20
        # 빗썸 비트파이넥스 폴로닉스 지원하는 코인
        if _coin == 'xmr' or _coin == 'dash' or _coin == 'zec':
            # 사이트별 10분전 가격

            bithumb_ten = BithumbDB.objects.filter(check_date__range=(current_time - tenminutes, current_time),
                                                   coin_name=_coin.upper()).first()
            poloniex_ten = PoloniexDB.objects.filter(check_date__range=(current_time - tenminutes, current_time),
                                                     coin_name=_coin.upper()).first()
            finex_ten = BitfinexDB.objects.filter(check_date__range=(current_time - tenminutes, current_time),
                                                  coin_name=_coin.lower()).first()
            # 사이트별 20분전 가격

            bithumb_twen = BithumbDB.objects.filter(check_date__range=(current_time - twenty, current_time),
                                                    coin_name=_coin.upper()).first()
            poloniex_twen = PoloniexDB.objects.filter(check_date__range=(current_time - twenty, current_time),
                                                      coin_name=_coin.upper()).first()
            finex_twen = BitfinexDB.objects.filter(check_date__range=(current_time - twenty, current_time),
                                                   coin_name=_coin.lower()).first()
            # 빗썸이 안될 때
            try:
                bithumb_current = float(coinchat.lasttrading(_coin))
            except ConnectionError as e:
                poloniex_price = float(coinchat.poloniex(_coin))
                finex_price = float(coinchat.bitfinex(_coin))
                poloniex_price_to_krw = float(poloniex_price * _rate)
                finex_price_to_krw = float(finex_price * _rate)
                text1 = '{}시 {}분경 가격\n'.format(finex_twen.check_date.hour, finex_twen.check_date.minute)
                text2 = '폴로닉스: {:,.2f}원 {:,.2f}$\n'.format(poloniex_twen.coin_price * _rate, poloniex_twen.coin_price)
                text3 = '비트파이넥스: {:,.2f}원 {:,.2f}$\n\n'.format(finex_twen.coin_price * _rate, finex_twen.coin_price)
                text4 = '{}시 {}분경 가격 \n'.format(finex_ten.check_date.hour, finex_twen.check_date.minute)
                text5 = '폴로닉스: {:,.2f}원 {:,.2f}$\n'.format(poloniex_ten.coin_price * _rate, poloniex_ten.coin_price)
                text6 = '비트파이넥스: {:,.2f}원 {:,.2f}$\n\n'.format(finex_ten.coin_price * _rate, finex_ten.coin_price)
                text7 = '현재 해외 {}의 가격\n'.format(_coin.upper())
                text8 = '폴로닉스: {:,.2f}원 ({:,.2f}$) \n({}분전에 비해 {:,.2f}원{})\n'.format(poloniex_price_to_krw,
                                                                                     poloniex_price,
                                                                                     current_time.minute - poloniex_ten.check_date.minute,
                                                                                     poloniex_price_to_krw - poloniex_ten.coin_price * _rate,
                                                                                     arrow_func(poloniex_price_to_krw,
                                                                                                poloniex_ten.coin_price * _rate))
                text9 = '비트파이넥스: {:,.2f}원 ({:,.2f}$) \n({}분전에 비해 {:,.2f}원{})\n\n'.format(finex_price_to_krw,
                                                                                         finex_price,
                                                                                         current_time.minute - finex_ten.check_date.minute,
                                                                                         finex_price_to_krw - finex_ten.coin_price * _rate,
                                                                                         arrow_func(finex_price_to_krw,
                                                                                                    finex_ten.coin_price * _rate))

                return_text = text1 + text2 + text3 + text4 + text5 + text6 + text7 + text8 + text9 + "**빗썸 API와의 통신이 되지않아 빗썸을 제외한 결과입니다.**"
                return data_func(return_text, buttons=_list)
            # 폴로닉스가 안될 때
            try:
                poloniex_price = float(coinchat.poloniex(_coin))
            except ConnectionError as e:
                bithumb_current = float(coinchat.lasttrading(_coin))
                finex_price = float(coinchat.bitfinex(_coin))
                finex_price_to_krw = float(finex_price * _rate)
                text1 = '김치 프리미엄 (현재 가격대비 등락) \n[국내:빗썸, 해외:비트파이넥스 기준]\n'
                text2 = '{}시 {}분경 김치 프리미엄{:,.2f}% ({:,.2f})%\n'.format(
                    bithumb_twen.check_date.hour, bithumb_twen.check_date.minute,
                    (bithumb_twen.coin_price - (finex_twen.coin_price * _rate)) / (
                        finex_twen.coin_price * _rate) * 100,
                    ((
                         bithumb_current - finex_price_to_krw) / finex_price_to_krw) * 100 - (
                        bithumb_twen.coin_price - (
                            finex_twen.coin_price * _rate)) / (
                        finex_twen.coin_price * _rate) * 100
                )
                text3 = '{}시 {}분경 김치 프리미엄{:,.2f}% ({:,.2f})%\n\n'.format(bithumb_ten.check_date.hour,
                                                                         bithumb_ten.check_date.minute, (
                                                                             bithumb_ten.coin_price - (
                                                                                 finex_ten.coin_price * _rate)) / (
                                                                             finex_ten.coin_price * _rate) * 100,
                                                                         ((
                                                                              bithumb_current - finex_price_to_krw) / finex_price_to_krw) * 100 - (
                                                                             bithumb_ten.coin_price - (
                                                                                 finex_ten.coin_price * _rate)) / (
                                                                             finex_ten.coin_price * _rate) * 100
                                                                         )
                text4 = '{}시 {}분경 가격\n'.format(bithumb_twen.check_date.hour, bithumb_twen.check_date.minute)
                text5 = '빗썸: {:,.2f}원\n'.format(bithumb_twen.coin_price)
                text6 = '비트파이넥스: {:,.2f}원 {:,.2f}$\n\n'.format(finex_twen.coin_price * _rate, finex_twen.coin_price)
                text7 = '{}시 {}분경 가격 \n'.format(bithumb_ten.check_date.hour, bithumb_ten.check_date.minute)
                text8 = '빗썸: {:,.2f}원\n'.format(bithumb_ten.coin_price)
                text9 = '비트파이넥스: {:,.2f}원 {:,.2f}$\n\n'.format(finex_ten.coin_price * _rate, finex_ten.coin_price)
                text10 = '현재 해외 {}의 가격\n'.format(_coin.upper())
                text11 = '비트파이넥스: {:,.2f}원 ({:,.2f}$) \n({}분전에 비해 {:,.2f}원{})\n\n'.format(finex_price_to_krw,
                                                                                          finex_price,
                                                                                          current_time.minute - finex_ten.check_date.minute,
                                                                                          finex_price_to_krw - finex_ten.coin_price * _rate,
                                                                                          arrow_func(finex_price_to_krw,
                                                                                                     finex_ten.coin_price * _rate))
                text12 = '현재 국내 {}의 가격\n'.format(_coin.upper())
                text13 = '빗썸: {:,.2f}원 \n({}분전에 비해 {:,.2f}원{})'.format(bithumb_current,
                                                                       current_time.minute - bithumb_ten.check_date.minute,
                                                                       bithumb_current - bithumb_ten.coin_price,
                                                                       arrow_func(bithumb_current,
                                                                                  bithumb_ten.coin_price))

                return_text = text1 + text2 + text3 + text4 + text5 + text6 + text7 + text8 + text9 + text10 + text11 + text12 + text13 + "**폴로닉스 API와의 통신이 되지않아 폴로닉스를 제외한 결과입니다.**"
                return data_func(return_text, buttons=_list)
            # 비트파이넥스가 안될 때
            try:
                finex_price = float(coinchat.bitfinex(_coin))
            except ConnectionError as e:
                poloniex_price = float(coinchat.poloniex(_coin))
                bithumb_current = float(coinchat.lasttrading(_coin))
                poloniex_price_to_krw = float(poloniex_price * _rate)
                text1 = '김치 프리미엄 (현재 가격대비 등락) \n[국내:빗썸, 해외:폴로닉스 기준]\n'
                text2 = '{}시 {}분경 김치 프리미엄{:,.2f}% ({:,.2f})%\n'.format(
                    bithumb_twen.check_date.hour, bithumb_twen.check_date.minute,
                    (bithumb_twen.coin_price - (finex_twen.coin_price * _rate)) / (
                        finex_twen.coin_price * _rate) * 100,
                    ((
                         bithumb_current - poloniex_price_to_krw) / poloniex_price_to_krw) * 100 - (
                        bithumb_twen.coin_price - (
                            poloniex_twen.coin_price * _rate)) / (
                        poloniex_twen.coin_price * _rate) * 100
                )
                text3 = '{}시 {}분경 김치 프리미엄{:,.2f}% ({:,.2f})%\n\n'.format(bithumb_ten.check_date.hour,
                                                                         bithumb_ten.check_date.minute, (
                                                                             bithumb_ten.coin_price - (
                                                                                 poloniex_ten.coin_price * _rate)) / (
                                                                             poloniex_ten.coin_price * _rate) * 100,
                                                                         ((
                                                                              bithumb_current - poloniex_price_to_krw) / poloniex_price_to_krw) * 100 - (
                                                                             bithumb_ten.coin_price - (
                                                                                 poloniex_ten.coin_price * _rate)) / (
                                                                             poloniex_ten.coin_price * _rate) * 100
                                                                         )
                text4 = '{}시 {}분경 가격\n'.format(bithumb_twen.check_date.hour, bithumb_twen.check_date.minute)
                text5 = '빗썸: {:,.2f}원\n'.format(bithumb_twen.coin_price)
                text6 = '폴로닉스: {:,.2f}원 {:,.2f}$\n\n'.format(poloniex_twen.coin_price * _rate, poloniex_twen.coin_price)
                text7 = '{}시 {}분경 가격 \n'.format(bithumb_ten.check_date.hour, bithumb_ten.check_date.minute)
                text8 = '빗썸: {:,.2f}원\n'.format(bithumb_ten.coin_price)
                text9 = '폴로닉스: {:,.2f}원 {:,.2f}$\n\n'.format(poloniex_ten.coin_price * _rate, poloniex_ten.coin_price)
                text10 = '현재 해외 {}의 가격\n'.format(_coin.upper())
                text11 = '폴로닉스: {:,.2f}원 ({:,.2f}$) \n({}분전에 비해 {:,.2f}원{})\n\n'.format(poloniex_price_to_krw,
                                                                                        poloniex_price,
                                                                                        current_time.minute - poloniex_ten.check_date.minute,
                                                                                        poloniex_price_to_krw - poloniex_ten.coin_price * _rate,
                                                                                        arrow_func(
                                                                                            poloniex_price_to_krw,
                                                                                            poloniex_ten.coin_price * _rate))
                text12 = '현재 국내 {}의 가격\n'.format(_coin.upper())
                text13 = '빗썸: {:,.2f}원 \n({}분전에 비해 {:,.2f}원{})'.format(bithumb_current,
                                                                       current_time.minute - bithumb_ten.check_date.minute,
                                                                       bithumb_current - bithumb_ten.coin_price,
                                                                       arrow_func(bithumb_current,
                                                                                  bithumb_ten.coin_price))

                return_text = text1 + text2 + text3 + text4 + text5 + text6 + text7 + text8 + text9 + text10 + text11 + text12 + text13 + "**비트파이넥스 API와의 통신이 되지않아 비트파이넥스를 제외한 결과입니다.**"
                return data_func(return_text, buttons=_list)

            poloniex_price_to_krw = float(poloniex_price * _rate)
            finex_price_to_krw = float(finex_price * _rate)
            text1 = '김치 프리미엄 (현재 가격대비 등락) \n[국내:빗썸, 해외:폴로닉스 기준]\n'
            text2 = '현재 김치 프리미엄{:,.2f}% \n'.format(
                ((bithumb_current - poloniex_price_to_krw) / poloniex_price_to_krw) * 100
            )
            text3 = '{}시 {}분경 김치 프리미엄{:,.2f}% ({:,.2f})%\n'.format(
                bithumb_twen.check_date.hour, bithumb_twen.check_date.minute,
                (bithumb_twen.coin_price - (poloniex_twen.coin_price * _rate)) / (
                    poloniex_twen.coin_price * _rate) * 100,
                ((
                     bithumb_current - poloniex_price_to_krw) / poloniex_price_to_krw) * 100 - (
                    bithumb_twen.coin_price - (
                        poloniex_twen.coin_price * _rate)) / (
                    poloniex_twen.coin_price * _rate) * 100
            )
            text4 = '{}시 {}분경 김치 프리미엄{:,.2f}% ({:,.2f})%\n'.format(bithumb_ten.check_date.hour,
                                                                   bithumb_ten.check_date.minute, (
                                                                       bithumb_ten.coin_price - (
                                                                           poloniex_ten.coin_price * _rate)) / (
                                                                       poloniex_ten.coin_price * _rate) * 100,
                                                                   ((
                                                                        bithumb_current - poloniex_price_to_krw) / poloniex_price_to_krw) * 100 - (
                                                                       bithumb_ten.coin_price - (
                                                                           poloniex_ten.coin_price * _rate)) / (
                                                                       poloniex_ten.coin_price * _rate) * 100
                                                                   )

            text5 = '{}시 {}분경 가격\n'.format(bithumb_twen.check_date.hour, bithumb_twen.check_date.minute)
            text6 = '빗썸: {:,.2f}원\n'.format(bithumb_twen.coin_price)
            text7 = '폴로닉스: {:,.2f}원 {:,.2f}$\n'.format(poloniex_twen.coin_price * _rate, poloniex_twen.coin_price)
            text8 = '비트파이넥스: {:,.2f}원 {:,.2f}$\n\n'.format(finex_twen.coin_price * _rate, finex_twen.coin_price)
            text9 = '{}시 {}분경 가격 \n'.format(bithumb_ten.check_date.hour, bithumb_ten.check_date.minute)
            text10 = '빗썸: {:,.2f}원\n'.format(bithumb_ten.coin_price)

            text11 = '폴로닉스: {:,.2f}원 {:,.2f}$\n'.format(poloniex_ten.coin_price * _rate, poloniex_ten.coin_price)
            text12 = '비트파이넥스: {:,.2f}원 {:,.2f}$\n\n'.format(finex_ten.coin_price * _rate, finex_ten.coin_price)
            text13 = '현재 해외 {}의 가격\n'.format(_coin.upper())
            text14 = '폴로닉스: {:,.2f}원 ({:,.2f}$) \n({}분전에 비해 {:,.2f}원{})\n'.format(poloniex_price_to_krw,
                                                                                  poloniex_price,
                                                                                  current_time.minute - poloniex_ten.check_date.minute,
                                                                                  poloniex_price_to_krw - poloniex_ten.coin_price * _rate,
                                                                                  arrow_func(poloniex_price_to_krw,
                                                                                             poloniex_ten.coin_price * _rate))
            text15 = '비트파이넥스: {:,.2f}원 ({:,.2f}$) \n({}분전에 비해 {:,.2f}원{})\n\n'.format(finex_price_to_krw,
                                                                                      finex_price,
                                                                                      current_time.minute - finex_ten.check_date.minute,
                                                                                      finex_price_to_krw - finex_ten.coin_price * _rate,
                                                                                      arrow_func(finex_price_to_krw,
                                                                                                 finex_ten.coin_price * _rate))
            text16 = '현재 국내 {}의 가격\n'.format(_coin.upper())
            text17 = '빗썸: {:,.2f}원 \n({}분전에 비해 {:,.2f}원{})\n\n'.format(bithumb_current,
                                                                       current_time.minute - bithumb_ten.check_date.minute,
                                                                       bithumb_current - bithumb_ten.coin_price,
                                                                       arrow_func(bithumb_current,
                                                                                  bithumb_ten.coin_price))

            return_text = text1 + text2 + text3 + text4 + text5 + text6 + text7 + text8 + text9 + text10 + text11 + text12 + text13 + text14 + text15 + text16 + text17
        # 빗썸 비트파이넥스 지원하는 코인
        if _coin == 'eos':
            # 환율 적용
            bithumb_ten = BithumbDB.objects.filter(check_date__range=(current_time - tenminutes, current_time),
                                                   coin_name=_coin.upper()).first()

            finex_ten = BitfinexDB.objects.filter(check_date__range=(current_time - tenminutes, current_time),
                                                  coin_name=_coin.lower()).first()

            bithumb_twen = BithumbDB.objects.filter(check_date__range=(current_time - twenty, current_time),
                                                    coin_name=_coin.upper()).first()

            finex_twen = BitfinexDB.objects.filter(check_date__range=(current_time - twenty, current_time),
                                                   coin_name=_coin.lower()).first()
            # 비트파이넥스가 안될 때
            try:
                finex_price = float(coinchat.bitfinex(_coin))
            except ConnectionError as e:
                bithumb_current = float(coinchat.lasttrading(_coin))
                text1 = '{}시 {}분경 가격\n'.format(bithumb_twen.check_date.hour, bithumb_twen.check_date.minute)
                text2 = '빗썸: {:,.2f}원\n'.format(bithumb_twen.coin_price)
                text3 = '{}시 {}분경 가격 \n'.format(bithumb_ten.check_date.hour, bithumb_ten.check_date.minute)
                text4 = '빗썸: {:,.2f}원\n'.format(bithumb_ten.coin_price)
                text5 = '현재 국내 {}의 가격\n'.format(_coin.upper())
                text6 = '빗썸: {:,.2f}원 \n({}분전에 비해 {:,.2f}원{})'.format(bithumb_current,
                                                                      current_time.minute - bithumb_ten.check_date.minute,
                                                                      bithumb_current - bithumb_ten.coin_price,
                                                                      arrow_func(bithumb_current,
                                                                                 bithumb_ten.coin_price))

                return_text = text1 + text2 + text3 + text4 + text5 + text6 + "**비트파이넥스 API와의 통신이 되지않아 비트파이넥스를 제외한 결과입니다.**"

                return data_func(return_text, buttons=_list)
            # 빗썸이 안될 때
            try:
                bithumb_current = float(coinchat.lasttrading(_coin))
            except ConnectionError as e:
                finex_price_to_krw = float(finex_price * _rate)
                text1 = '{}시 {}분경 가격\n'.format(bithumb_twen.check_date.hour, bithumb_twen.check_date.minute)
                text2 = '비트파이넥스: {:,.2f}원 {:,.2f}$\n\n'.format(finex_twen.coin_price * _rate, finex_twen.coin_price)
                text3 = '{}시 {}분경 가격 \n'.format(bithumb_ten.check_date.hour, bithumb_ten.check_date.minute)
                text4 = '비트파이넥스: {:,.2f}원 {:,.2f}$\n\n'.format(finex_ten.coin_price * _rate, finex_ten.coin_price)
                text5 = '현재 해외 {}의 가격\n'.format(_coin.upper())
                text6 = '비트파이넥스: {:,.2f}원 ({:,.2f}$) \n({}분전에 비해 {:,.2f}원{})\n'.format(finex_price_to_krw,
                                                                                       finex_price,
                                                                                       current_time.minute - finex_ten.check_date.minute,
                                                                                       finex_price_to_krw - finex_ten.coin_price * _rate,
                                                                                       arrow_func(finex_price_to_krw,
                                                                                                  finex_ten.coin_price * _rate))
                return_text = text1 + text2 + text3 + text4 + text5 + text6 + "**빗썸 API와의 통신이 되지않아 빗썸을 제외한 결과입니다.**"
                return data_func(return_text, buttons=_list)
            finex_price_to_krw = float(finex_price * _rate)
            text1 = '김치 프리미엄 (현재 가격대비 등락) \n[국내:빗썸, 해외:비트파이넥스 기준]\n'
            text2 = '{}시 {}분경 김치 프리미엄{:,.2f}% ({:,.2f})%\n'.format(
                bithumb_twen.check_date.hour, bithumb_twen.check_date.minute,
                (bithumb_twen.coin_price - (finex_twen.coin_price * _rate)) / (
                    finex_twen.coin_price * _rate) * 100,
                ((
                     bithumb_current - finex_price_to_krw) / finex_price_to_krw) * 100 - (
                    bithumb_twen.coin_price - (
                        finex_twen.coin_price * _rate)) / (
                    finex_twen.coin_price * _rate) * 100
            )
            text3 = '{}시 {}분경 김치 프리미엄{:,.2f}% ({:,.2f})%\n\n'.format(bithumb_ten.check_date.hour,
                                                                     bithumb_ten.check_date.minute, (
                                                                         bithumb_ten.coin_price - (
                                                                             finex_ten.coin_price * _rate)) / (
                                                                         finex_ten.coin_price * _rate) * 100,
                                                                     ((
                                                                          bithumb_current - finex_price_to_krw) / finex_price_to_krw) * 100 - (
                                                                         bithumb_ten.coin_price - (
                                                                             finex_ten.coin_price * _rate)) / (
                                                                         finex_ten.coin_price * _rate) * 100
                                                                     )
            text4 = '{}시 {}분경 가격\n'.format(bithumb_twen.check_date.hour, bithumb_twen.check_date.minute)
            text5 = '빗썸: {:,.2f}원\n'.format(bithumb_twen.coin_price)
            text6 = '비트파이넥스: {:,.2f}원 {:,.2f}$\n\n'.format(finex_twen.coin_price * _rate, finex_twen.coin_price)
            text7 = '{}시 {}분경 가격 \n'.format(bithumb_ten.check_date.hour, bithumb_ten.check_date.minute)
            text8 = '빗썸: {:,.2f}원\n'.format(bithumb_ten.coin_price)
            text9 = '비트파이넥스: {:,.2f}원 {:,.2f}$\n\n'.format(finex_ten.coin_price * _rate, finex_ten.coin_price)
            text10 = '현재 해외 {}의 가격\n'.format(_coin.upper())
            text11 = '비트파이넥스: {:,.2f}원 ({:,.2f}$) \n({}분전에 비해 {:,.2f}원{})\n\n'.format(finex_price_to_krw, finex_price,
                                                                                      current_time.minute - finex_ten.check_date.minute,
                                                                                      finex_price_to_krw - finex_ten.coin_price * _rate,
                                                                                      arrow_func(finex_price_to_krw,
                                                                                                 finex_ten.coin_price * _rate))
            text12 = '현재 국내 {}의 가격\n'.format(_coin.upper())
            text13 = '빗썸: {:,.2f}원 \n({}분전에 비해 {:,.2f}원{})'.format(bithumb_current,
                                                                   current_time.minute - bithumb_ten.check_date.minute,
                                                                   bithumb_current - bithumb_ten.coin_price,
                                                                   arrow_func(bithumb_current,
                                                                              bithumb_ten.coin_price))

            return_text = text1 + text2 + text3 + text4 + text5 + text6 + text7 + text8 + text9 + text10 + text11 + text12 + text13

        # 빗썸 코인원 비트파이넥스 지원 코인
        if _coin == 'qtum':
            # 사이트별 10분전 가격
            tenminutes = timedelta(minutes=10)
            current_time = datetime.now()
            bithumb_ten = BithumbDB.objects.filter(check_date__range=(current_time - tenminutes, current_time),
                                                   coin_name=_coin.upper()).first()

            coinone_ten = CoinoneDB.objects.filter(check_date__range=(current_time - tenminutes, current_time),
                                                   coin_name=_coin.lower()).first()
            finex_ten = BitfinexDB.objects.filter(check_date__range=(current_time - tenminutes, current_time),
                                                  coin_name=_coin.lower()).first()
            # 사이트별 20분전 가격
            twenty = timedelta(minutes=20)
            bithumb_twen = BithumbDB.objects.filter(check_date__range=(current_time - twenty, current_time),
                                                    coin_name=_coin.upper()).first()

            coinone_twen = CoinoneDB.objects.filter(check_date__range=(current_time - twenty, current_time),
                                                    coin_name=_coin.lower()).first()
            finex_twen = BitfinexDB.objects.filter(check_date__range=(current_time - twenty, current_time),
                                                   coin_name=_coin.lower()).first()

            try:
                bithumb_current = float(coinchat.lasttrading(_coin))
            except ConnectionError as e:
                coinone_current = float(coinchat.coinone(_coin))
                finex_price = float(coinchat.bitfinex(_coin))
                finex_price_to_krw = float(finex_price * _rate)
                text1 = '김치 프리미엄 (현재 가격대비 등락) \n[국내:코인원, 해외:비트파이넥스 기준]\n'
                text2 = '현재 김치 프리미엄{:,.2f}% \n'.format(
                    ((coinone_current - finex_price_to_krw) / finex_price_to_krw) * 100
                )
                text3 = '{}시 {}분경 김치 프리미엄{:,.2f}% ({:,.2f})%\n'.format(
                    coinone_twen.check_date.hour, coinone_twen.check_date.minute,
                    (coinone_twen.coin_price - (finex_twen.coin_price * _rate)) / (
                        finex_twen.coin_price * _rate) * 100,
                    ((
                         coinone_current - finex_price_to_krw) / finex_price_to_krw) * 100 - (
                        coinone_twen.coin_price - (
                            finex_twen.coin_price * _rate)) / (
                        finex_twen.coin_price * _rate) * 100
                )
                text4 = '{}시 {}분경 김치 프리미엄{:,.2f}% ({:,.2f})%\n\n'.format(coinone_ten.check_date.hour,
                                                                         coinone_ten.check_date.minute, (
                                                                             coinone_ten.coin_price - (
                                                                                 finex_ten.coin_price * _rate)) / (
                                                                             finex_ten.coin_price * _rate) * 100,
                                                                         ((
                                                                              coinone_current - finex_price_to_krw) / finex_price_to_krw) * 100 - (
                                                                             coinone_ten.coin_price - (
                                                                                 finex_ten.coin_price * _rate)) / (
                                                                             finex_ten.coin_price * _rate) * 100
                                                                         )
                text5 = '{}시 {}분경 가격\n'.format(coinone_twen.check_date.hour, coinone_twen.check_date.minute)
                text7 = '코인원: {:,.2f}원\n'.format(coinone_twen.coin_price)
                text8 = '비트파이넥스: {:,.2f}원 {:,.2f}$\n\n'.format(finex_twen.coin_price * _rate, finex_twen.coin_price)
                text9 = '{}시 {}분경 가격 \n'.format(coinone_ten.check_date.hour, coinone_ten.check_date.minute)
                text11 = '코인원: {:,.2f}원\n'.format(coinone_ten.coin_price)
                text12 = '비트파이넥스: {:,.2f}원 {:,.2f}$\n\n'.format(finex_ten.coin_price * _rate, finex_ten.coin_price)
                text13 = '현재 해외 {}의 가격\n'.format(_coin.upper())
                text14 = '비트파이넥스: {:,.2f}원 ({:,.2f}$) \n({}분전에 비해 {:,.2f}원{})\n\n'.format(finex_price_to_krw,
                                                                                          finex_price,
                                                                                          current_time.minute - finex_ten.check_date.minute,
                                                                                          finex_price_to_krw - finex_ten.coin_price * _rate,
                                                                                          arrow_func(finex_price_to_krw,
                                                                                                     finex_ten.coin_price * _rate))
                text15 = '현재 국내 {}의 가격\n'.format(_coin.upper())
                text17 = '코인원: {:,.2f}원 \n({}분전에 비해 {:,.2f}원{})\n'.format(coinone_current,
                                                                          current_time.minute - coinone_ten.check_date.minute,
                                                                          coinone_current - coinone_ten.coin_price,
                                                                          arrow_func(coinone_current,
                                                                                     coinone_ten.coin_price))

                return_text = text1 + text2 + text3 + text4 + text5 + text7 + text8 + text9 + text11 + text12 + text13 + text14 + text15 + text17 + "**빗썸 API와의 통신이 되지않아 빗썸을 제외한 결과입니다.**"
                return data_func(return_text, buttons=_list)
            try:
                coinone_current = float(coinchat.coinone(_coin))
            except ConnectionError as e:
                bithumb_current = float(coinchat.lasttrading(_coin))
                finex_price = float(coinchat.bitfinex(_coin))
                finex_price_to_krw = float(finex_price * _rate)
                text1 = '김치 프리미엄 (현재 가격대비 등락) \n[국내:빗썸, 해외:비트파이넥스 기준]\n'
                text2 = '현재 김치 프리미엄{:,.2f}% \n'.format(
                    ((bithumb_current - finex_price_to_krw) / finex_price_to_krw) * 100
                )
                text3 = '{}시 {}분경 김치 프리미엄{:,.2f}% ({:,.2f})%\n'.format(
                    bithumb_twen.check_date.hour, bithumb_twen.check_date.minute,
                    (bithumb_twen.coin_price - (finex_twen.coin_price * _rate)) / (
                        finex_twen.coin_price * _rate) * 100,
                    ((
                         bithumb_current - finex_price_to_krw) / finex_price_to_krw) * 100 - (
                        bithumb_twen.coin_price - (
                            finex_twen.coin_price * _rate)) / (
                        finex_twen.coin_price * _rate) * 100
                )
                text4 = '{}시 {}분경 김치 프리미엄{:,.2f}% ({:,.2f})%\n\n'.format(bithumb_ten.check_date.hour,
                                                                         bithumb_ten.check_date.minute, (
                                                                             bithumb_ten.coin_price - (
                                                                                 finex_ten.coin_price * _rate)) / (
                                                                             finex_ten.coin_price * _rate) * 100,
                                                                         ((
                                                                              bithumb_current - finex_price_to_krw) / finex_price_to_krw) * 100 - (
                                                                             bithumb_ten.coin_price - (
                                                                                 finex_ten.coin_price * _rate)) / (
                                                                             finex_ten.coin_price * _rate) * 100
                                                                         )
                text5 = '{}시 {}분경 가격\n'.format(bithumb_twen.check_date.hour, bithumb_twen.check_date.minute)
                text6 = '빗썸: {:,.2f}원\n'.format(bithumb_twen.coin_price)
                text8 = '비트파이넥스: {:,.2f}원 {:,.2f}$\n\n'.format(finex_twen.coin_price * _rate, finex_twen.coin_price)
                text9 = '{}시 {}분경 가격 \n'.format(bithumb_ten.check_date.hour, bithumb_ten.check_date.minute)
                text10 = '빗썸: {:,.2f}원\n'.format(bithumb_ten.coin_price)
                text12 = '비트파이넥스: {:,.2f}원 {:,.2f}$\n\n'.format(finex_ten.coin_price * _rate, finex_ten.coin_price)
                text13 = '현재 해외 {}의 가격\n'.format(_coin.upper())
                text14 = '비트파이넥스: {:,.2f}원 ({:,.2f}$) \n({}분전에 비해 {:,.2f}원{})\n\n'.format(finex_price_to_krw,
                                                                                          finex_price,
                                                                                          current_time.minute - finex_ten.check_date.minute,
                                                                                          finex_price_to_krw - finex_ten.coin_price * _rate,
                                                                                          arrow_func(finex_price_to_krw,
                                                                                                     finex_ten.coin_price * _rate))
                text15 = '현재 국내 {}의 가격\n'.format(_coin.upper())
                text16 = '빗썸: {:,.2f}원 \n({}분전에 비해 {:,.2f}원{})\n'.format(bithumb_current,
                                                                         current_time.minute - bithumb_ten.check_date.minute,
                                                                         bithumb_current - bithumb_ten.coin_price,
                                                                         arrow_func(bithumb_current,
                                                                                    bithumb_ten.coin_price))

                return_text = text1 + text2 + text3 + text4 + text5 + text6 + text8 + text9 + text10 + text12 + text13 + text14 + text15 + text16 + "**코인원 API와의 통신이 되지않아 코인원을 제외한 결과입니다.**"
                return data_func(return_text, buttons=_list)
            try:
                finex_price = float(coinchat.bitfinex(_coin))
            except ConnectionError as e:
                bithumb_current = float(coinchat.lasttrading(_coin))
                text5 = '{}시 {}분경 가격\n'.format(bithumb_twen.check_date.hour, bithumb_twen.check_date.minute)
                text6 = '빗썸: {:,.2f}원\n'.format(bithumb_twen.coin_price)
                text7 = '코인원: {:,.2f}원\n'.format(coinone_twen.coin_price)
                text9 = '{}시 {}분경 가격 \n'.format(bithumb_ten.check_date.hour, bithumb_ten.check_date.minute)
                text10 = '빗썸: {:,.2f}원\n'.format(bithumb_ten.coin_price)
                text11 = '코인원: {:,.2f}원\n'.format(coinone_ten.coin_price)
                text15 = '현재 국내 {}의 가격\n'.format(_coin.upper())
                text16 = '빗썸: {:,.2f}원 \n({}분전에 비해 {:,.2f}원{})\n'.format(bithumb_current,
                                                                         current_time.minute - bithumb_ten.check_date.minute,
                                                                         bithumb_current - bithumb_ten.coin_price,
                                                                         arrow_func(bithumb_current,
                                                                                    bithumb_ten.coin_price))
                text17 = '코인원: {:,.2f}원 \n({}분전에 비해 {:,.2f}원{})\n'.format(coinone_current,
                                                                          current_time.minute - coinone_ten.check_date.minute,
                                                                          coinone_current - coinone_ten.coin_price,
                                                                          arrow_func(coinone_current,
                                                                                     coinone_ten.coin_price))

                return_text = text5 + text6 + text7 + text9 + text10 + text11 + text15 + text16 + text17 + "**비트파이넥스 API와의 통신이 되지않아 비트파이넥스를 제외한 결과입니다.**"
                return data_func(return_text, buttons=_list)
            # 환율 적용
            finex_price_to_krw = float(finex_price * _rate)
            text1 = '김치 프리미엄 (현재 가격대비 등락) \n[국내:빗썸, 해외:비트파이넥스 기준]\n'
            text2 = '현재 김치 프리미엄{:,.2f}% \n'.format(
                ((bithumb_current - finex_price_to_krw) / finex_price_to_krw) * 100
            )
            text3 = '{}시 {}분경 김치 프리미엄{:,.2f}% ({:,.2f})%\n'.format(
                bithumb_twen.check_date.hour, bithumb_twen.check_date.minute,
                (bithumb_twen.coin_price - (finex_twen.coin_price * _rate)) / (
                    finex_twen.coin_price * _rate) * 100,
                ((
                     bithumb_current - finex_price_to_krw) / finex_price_to_krw) * 100 - (
                    bithumb_twen.coin_price - (
                        finex_twen.coin_price * _rate)) / (
                    finex_twen.coin_price * _rate) * 100
            )
            text4 = '{}시 {}분경 김치 프리미엄{:,.2f}% ({:,.2f})%\n\n'.format(bithumb_ten.check_date.hour,
                                                                     bithumb_ten.check_date.minute, (
                                                                         bithumb_ten.coin_price - (
                                                                             finex_ten.coin_price * _rate)) / (
                                                                         finex_ten.coin_price * _rate) * 100,
                                                                     ((
                                                                          bithumb_current - finex_price_to_krw) / finex_price_to_krw) * 100 - (
                                                                         bithumb_ten.coin_price - (
                                                                             finex_ten.coin_price * _rate)) / (
                                                                         finex_ten.coin_price * _rate) * 100
                                                                     )
            text5 = '{}시 {}분경 가격\n'.format(bithumb_twen.check_date.hour, bithumb_twen.check_date.minute)
            text6 = '빗썸: {:,.2f}원\n'.format(bithumb_twen.coin_price)
            text7 = '코인원: {:,.2f}원\n'.format(coinone_twen.coin_price)
            text8 = '비트파이넥스: {:,.2f}원 {:,.2f}$\n\n'.format(finex_twen.coin_price * _rate, finex_twen.coin_price)
            text9 = '{}시 {}분경 가격 \n'.format(bithumb_ten.check_date.hour, bithumb_ten.check_date.minute)
            text10 = '빗썸: {:,.2f}원\n'.format(bithumb_ten.coin_price)
            text11 = '코인원: {:,.2f}원\n'.format(coinone_ten.coin_price)
            text12 = '비트파이넥스: {:,.2f}원 {:,.2f}$\n\n'.format(finex_ten.coin_price * _rate, finex_ten.coin_price)
            text13 = '현재 해외 {}의 가격\n'.format(_coin.upper())
            text14 = '비트파이넥스: {:,.2f}원 ({:,.2f}$) \n({}분전에 비해 {:,.2f}원{})\n\n'.format(finex_price_to_krw,
                                                                                      finex_price,
                                                                                      current_time.minute - finex_ten.check_date.minute,
                                                                                      finex_price_to_krw - finex_ten.coin_price * _rate,
                                                                                      arrow_func(finex_price_to_krw,
                                                                                                 finex_ten.coin_price * _rate))
            text15 = '현재 국내 {}의 가격\n'.format(_coin.upper())
            text16 = '빗썸: {:,.2f}원 \n({}분전에 비해 {:,.2f}원{})\n'.format(bithumb_current,
                                                                     current_time.minute - bithumb_ten.check_date.minute,
                                                                     bithumb_current - bithumb_ten.coin_price,
                                                                     arrow_func(bithumb_current,
                                                                                bithumb_ten.coin_price))
            text17 = '코인원: {:,.2f}원 \n({}분전에 비해 {:,.2f}원{})'.format(coinone_current,
                                                                    current_time.minute - coinone_ten.check_date.minute,
                                                                    coinone_current - coinone_ten.coin_price,
                                                                    arrow_func(coinone_current,
                                                                               coinone_ten.coin_price))

            return_text = text1 + text2 + text3 + text4 + text5 + text6 + text7 + text8 + text9 + text10 + text11 + text12 + text13 + text14 + text15 + text16 + text17

        return data_func(return_text, buttons=_list)
    if len(coin.split(',')) == 3 or len(coin.split(' ')) == 3 or len(coin.split(' ')) == 4 or len(coin.split(',')) == 4:

        try:
            coin_split = coin.split(',')
            print(coin_split[1])
        except:
            coin_split = coin.split(' ')
        coin_dict = {
            '비트코인': 'BTC',
            '이더리움': 'ETH',
            '비트코인캐시': 'BCH',
            '리플': 'XRP',
            '라이트코인': 'LTC',
            '대시': 'DASH',
            '모네로': 'XMR',
            '제트캐시': 'ZEC',
            '이더리움클래식': 'ETC',
            '아이오타': 'IOTA',
            '비트코인골드': 'BTG',
            '퀀텀': 'QTUM',
            '이오스': 'EOS',
        }
        if coin_split[1] in coin_dict.keys():
            # 로컬용
            # user =request.POST['user_key']
            # 서버용
            user = return_json_str['user_key']
            try:
                coin_count = round(float(coin_split[3]), 4)
            except:
                coin_count = 0
            coin_price = round((float(coin_split[2]) / float(coin_count)), 2)

            if coin_split[0] == '코빗':

                if coin_split[1] in korbit_dict.keys():

                    pass
                else:
                    data = {
                        "message":
                            {
                                "text": '코빗에서 지원하는 코인만 등록 가능합니다.\n'
                                        '가능한 코인 목록\n{}\n'
                                        '버튼식으로 돌아가시려면 "처음으로"라고 입력하세요.\n'.format(list(korbit_dict.keys()))
                            }
                    }
                    data = json.dumps(data, ensure_ascii=False)
                    return HttpResponse(data, content_type='application/json')
            elif coin_split[0] == '빗썸':

                if coin_split[1] in bithumb_dict.values():
                    pass
                else:
                    data = {
                        "message":
                            {
                                "text": '빗썸에서 지원하는 코인만 등록 가능합니다.\n'
                                        '가능한 코인 목록\n{}\n'
                                        '버튼식으로 돌아가시려면 "처음으로"라고 입력하세요.\n'.format(list(bithumb_dict.values()))
                            }
                    }
                    data = json.dumps(data, ensure_ascii=False)
                    return HttpResponse(data, content_type='application/json')
            elif coin_split[0] == '코인원':
                if coin_split[1] in coinone_dict.values():
                    pass
                else:
                    data = {
                        "message":
                            {
                                "text": '코인원에서 지원하는 코인만 등록 가능합니다.\n'
                                        '가능한 코인 목록\n{}\n'
                                        '버튼식으로 돌아가시려면 "처음으로"라고 입력하세요.\n'.format(list(coinone_dict.values()))
                            }
                    }
                    data = json.dumps(data, ensure_ascii=False)
                    return HttpResponse(data, content_type='application/json')

            if UserDB.objects.filter(user_key=user, exchange_name=coin_split[0],
                                     coin_name=coin_split[1]).exists():
                userdb = UserDB.objects.get(user_key=user, exchange_name=coin_split[0],
                                            coin_name=coin_split[1])
                userdb.coin_price = coin_price
                userdb.coin_count = coin_count
                userdb.save()
            else:
                userdb = UserDB.objects.create(
                    user_key=user,
                    # user_key=user,
                    exchange_name=coin_split[0],
                    coin_name=coin_split[1],
                    coin_price=coin_price,
                    coin_count=coin_count
                )
            text = '등록이 완료되었습니다.\n등록된 정보는 다음과 같습니다.\n\n거래소: {}\n코인: {}\n가격: {}\n개수: {}'.format(userdb.exchange_name,
                                                                                               userdb.coin_name,
                                                                                               userdb.coin_price,
                                                                                               userdb.coin_count)
            return data_func(text, ['마이페이지', '처음으로', '직접입력'])
        else:
            data = {
                "message":
                    {
                        "text": '빗썸,코인원,코빗에서 지원하는 코인만 등록 가능합니다.\n'
                                '가능한 코인 목록\n{}\n'
                                '버튼식으로 돌아가시려면 "처음으로"라고 입력하세요.\n'.format(list(coin_dict.keys()))
                    }
            }
            data = json.dumps(data, ensure_ascii=False)
            return HttpResponse(data, content_type='application/json')
    else:
        data = {
            "message":
                {
                    "text": '국내 거래소(업비트 제외)만 지원합니다.\n[빗썸,코인원,코빗]\n'
                            '등록하실 코인 정보를\n거래소,코인명,평균단가,수량(옵션)순으로 입력해주세요.\n'
                            '코인명에 띄워쓰기는 안돼요.\n'
                            '예시) 빗썸,비트코인캐시,47000.33(소수점2자리),34.8847(소수점4자리)\n'
                            '버튼식으로 돌아가시려면 "처음으로"라고 입력하세요.\n'
                }
        }
        data = json.dumps(data, ensure_ascii=False)
        return HttpResponse(data, content_type='application/json')


@api_view(['GET'])
def keyboard(request):
    data = {
        "type": "buttons",
        "buttons": ['마이페이지', '코인', '거래소별 시세', '한강수온', '직접입력']
    }
    data = json.dumps(data, ensure_ascii=False)
    return HttpResponse(data, content_type='application/json')


