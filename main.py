from pycoingecko import CoinGeckoAPI
import datetime
import time

cg = CoinGeckoAPI()

# Cryptocurrency prices
bitcoin_price = {
    '01-05-2019': 5292.803974562054,
    '02-05-2019': 5354.5868001739655,
    '03-05-2019': 5450.706620486424,
    '04-05-2019': 5731.493099606555,
    '05-05-2019': 5803.943309048437,
    '06-05-2019': 5749.323780460327,
    '07-05-2019': 5715.7571359661015,
    '08-05-2019': 5841.053771273751,
    '09-05-2019': 5957.856732858399,
    '10-05-2019': 6168.268996398258,
    '11-05-2019': 6370.233758607852,
    '12-05-2019': 7258.261280655222,
    '13-05-2019': 6953.75138858638,
    '14-05-2019': 7805.98164948938,
    '15-05-2019': 7990.055553534356,
    '16-05-2019': 8192.223138952013,
    '17-05-2019': 7875.913199526066,
    '18-05-2019': 7343.371457162994,
    '19-05-2019': 7300.655158341227,
    '20-05-2019': 8168.730689783752,
    '21-05-2019': 7976.851712899625,
    '22-05-2019': 7958.365526075088,
    '23-05-2019': 7665.79685383355,
    '24-05-2019': 7861.812792465447,
    '25-05-2019': 7977.244882467973,
    '26-05-2019': 8037.627431860584,
    '27-05-2019': 8631.080577844017,
    '28-05-2019': 8816.03391493351,
    '29-05-2019': 8726.978110456395,
    '30-05-2019': 8650.677405968292,
    '31-05-2019': 8310.891063057417,
    '01-06-2019': 8575.646353354166,
    '02-06-2019': 8554.261728092017,
    '03-06-2019': 8743.705469134235,
    '04-06-2019': 8173.632761796738,
    '05-06-2019': 7683.636261419786,
    '06-06-2019': 7812.448854732150,
    '07-06-2019': 7821.123897094859,
    '08-06-2019': 8036.108159122215,
    '09-06-2019': 7705.539284064289,
   }


# Useful functions
#   bitcoin = cg.get_price(ids='bitcoin', vs_currencies='usd')
#   datetime.datetime.now()
#   datetime.datetime(2020, 5, 17)

# Pull prices for a cryptocurrency from CoinGecko
def get_prices(coin,start_date_str,end_date_str):

    start_date = datetime.datetime.strptime(start_date_str, '%d-%m-%Y')
    end_date = datetime.datetime.strptime(end_date_str, '%d-%m-%Y') 
    date = start_date
    
    # Construct the dictionary
    print(coin + '_price = {')

    while date != end_date + datetime.timedelta(days=1):
        date_str = date.strftime("%d-%m-%Y")

        coin_info = cg.get_coin_history_by_id(coin, date_str)
        current_price = coin_info.get('market_data').get('current_price').get('usd')
        print("    '" + date_str + "': " + format(current_price) + ',')

        date += datetime.timedelta(days=1)
        time.sleep(1)
 
    print("   }")

# Iterate & print the dict
def print_dict(coin, date_str)
    coin_info = cg.get_coin_history_by_id(coin, date_str)

    for key in coin_info:
        print(key, " = ", bitcoin.get(key))

# Run the simulation
def run(coin_1,percentage_1,coin_2,percentage_2,start_date_str,end_date_str, strategy):

    day = 1
    start_date = datetime.datetime.strptime(start_date_str, '%d-%m-%Y')
    end_date = datetime.datetime.strptime(end_date_str, '%d-%m-%Y') 
    date = start_date

    balance = 1000

    portfolio_percentage = .5
        
    bitcoin_held = balance*percentage_2 / bitcoin_price.get(date.strftime("%d-%m-%Y"))

    usd_held = balance*percentage_1
#    print(bitcoin_held)
    
    print("Bought", bitcoin_held, "bitcoin at", bitcoin_price.get(date.strftime("%d-%m-%Y")), "USD")

    #coin_info = cg.get_coin_history_by_id(coin, start_date)

    if strategy == 'bnh':
        while date != end_date + datetime.timedelta(days=1):
            date_str = date.strftime("%d-%m-%Y")
            print(date.strftime("%d-%m-%Y"))
            balance = usd_held + bitcoin_held * bitcoin_price.get(date_str)
            print("- Day", day)
            print("- Bitcoin price is :", bitcoin_price.get(date_str))
            print("- Portfolio value is", balance, "USD")
            date = date + datetime.timedelta(days=1)
            day += 1
         #   bitcoin_value = bitcoin_price * bitcoin_held

    if strategy == 'rebalance_daily':
        while date != end_date + datetime.timedelta(days=1):
            # Before rebalance
            date_str = date.strftime("%d-%m-%Y")
            print(date.strftime("%d-%m-%Y"))
            usd_value = usd_held
            bitcoin_value = bitcoin_held * bitcoin_price.get(date_str)
            balance = usd_value + bitcoin_value
            print("- Day", day)
            print("- Bitcoin price is :", bitcoin_price.get(date_str))
            print("- Bitcoin value is :", bitcoin_value)
            print("- USD value is is :", usd_value)
            print("- Portfolio value is", balance, "USD")

            # Rebalance
            dif = usd_value - bitcoin_value
            target_value = balance / 2
            print("- Target value is", target_value)
            bitcoin_difference = target_value - bitcoin_value
            usd_difference = target_value - usd_value
            print("- Bitcoin difference", bitcoin_difference)
            print("- USD difference", usd_difference)

            if bitcoin_value < usd_value:
                purchase_bitcoin = bitcoin_difference / bitcoin_price.get(date_str)
                print("bought ", purchase_bitcoin, "bitcoin for", bitcoin_difference, "USD")
                bitcoin_held += purchase_bitcoin
                usd_held -= bitcoin_difference

            if bitcoin_value > usd_value:
                bitcoin_sold = bitcoin_difference / bitcoin_price.get(date_str)
                print("sold ", bitcoin_sold, "bitcoin for", bitcoin_difference, "USD")
                bitcoin_held += bitcoin_sold
                usd_held -= bitcoin_difference
                
            # After rebalance
            print("After rebalance")
            usd_value = usd_held
            bitcoin_value = bitcoin_held * bitcoin_price.get(date_str)
            balance = usd_value + bitcoin_value
            print("- Bitcoin value is :", bitcoin_value)
            print("- USD value is is :", usd_value)
            print("- Portfolio value is", balance, "USD")
            date = date + datetime.timedelta(days=1)
            day += 1
         #   bitcoin_value = bitcoin_price * bitcoin_held

    return balance

balance = 1000
start_date = '01-06-2019'
end_date = '09-06-2019'

day = 1

x = 'bitcoin'
y = '01-5-2019'
z = '01-06-2019'
#get_prices(x,y,z)

strategy_1 = run('usd',1,'bitcoin',0,y,z, 'bnh')
strategy_2 = run('usd',0,'bitcoin',1,y,z, 'bnh')
strategy_3 = run('usd',.5,'bitcoin',.5,y,z, 'bnh')
strategy_4 = run('usd',.5,'bitcoin',.5,y,z, 'rebalance_daily')

print('buy and hold usd', strategy_1)
print('buy and hold btc', strategy_2)
print('buy and hold 50% usd and 50% btc', strategy_3)
print('rebalance 50% usd and 50% btc', strategy_4)


#Buy and hold strategy
#def buy_and_hold(coin_1,percentage_1,coin_2,percentage_2):
    
#Rebalance daily to equal weights

#buy_and_hold('usd',1,'bitcoin',0)
#buy_and_hold('usd',.5,'bitcoin',.5)
#buy_and_hold('usd',0,'bitcoin',1)
