from django.db import models


class UserDB(models.Model):
    user_key = models.CharField(max_length=30)
    exchange_name = models.CharField(max_length=15)
    coin_name = models.CharField(max_length=30)
    coin_price = models.FloatField()
    coin_count = models.FloatField(null=True)

    def __str__(self):
        return '\n[{}] key: {}, exchange_name: {}\n' \
               'coin_name: {}, coin_price: {}\n' \
               'coin_count: {}\n'.format(self.pk,self.user_key, self.exchange_name, self.coin_name, self.coin_price,
                                       self.coin_count)


class BithumbDB(models.Model):
    coin_name = models.CharField(max_length=30)
    coin_price = models.FloatField()
    check_date = models.DateTimeField(auto_now_add=True)


class PoloniexDB(models.Model):
    coin_name = models.CharField(max_length=30)
    coin_price = models.FloatField()
    check_date = models.DateTimeField(auto_now_add=True)


class CoinoneDB(models.Model):
    coin_name = models.CharField(max_length=30)
    coin_price = models.FloatField()
    check_date = models.DateTimeField(auto_now_add=True)


class KorbitDB(models.Model):
    coin_name = models.CharField(max_length=30)
    coin_price = models.FloatField()
    check_date = models.DateTimeField(auto_now_add=True)


class UpbitDB(models.Model):
    coin_name = models.CharField(max_length=30)
    coin_price = models.FloatField()
    check_date = models.DateTimeField(auto_now_add=True)


class BitfinexDB(models.Model):
    coin_name = models.CharField(max_length=30)
    coin_price = models.FloatField()
    check_date = models.DateTimeField(auto_now_add=True)


# 환율
class ExchangeRate(models.Model):
    rate = models.FloatField()


# 한강수온
class HanriverTemperature(models.Model):
    temperature = models.FloatField()
