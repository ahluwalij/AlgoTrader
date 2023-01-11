from coinbase.wallet.client import Client

coinbase_API_key = "g02YDVyhB0m7NnBZ"
coinbase_API_secret = "hR8iyuszSetfJkrbIaxzViN7DVaZGMUe"
client = Client(coinbase_API_key, coinbase_API_secret)

currency_code = "USD"
active = True
price = 0
count = 0

while active:
    price = client.get_spot_price(currency_pair= 'BTC-USD')
    print (count,' Current bitcoin price in %s: %s' % (currency_code, price.amount))
    count += 1
    if count == 100:
        active = False
