from pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()

coins_dict = cg.get_coins_list()
holder = next(coin for coin in coins_dict if coin['name'].lower() == 'bitcoin')
print(holder)
coin_id = holder['id']
print(coin_id)
actual_price = cg.get_price(ids = coin_id, vs_currencies='usd')[coin_id]
print(type(actual_price['usd']))
