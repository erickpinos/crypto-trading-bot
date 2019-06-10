from pycoingecko import CoinGeckoAPI
import datetime

cg = CoinGeckoAPI()


#bitcoin = cg.get_price(ids='bitcoin', vs_currencies='usd')
def get_prices(coin,start_date,end_date):
    coin = 'bitcoin'
    date = '01-06-2019'

    day = 1
    num_of_days = 10

    datetime_start_date = datetime.datetime.strptime(start_date, '%d-%m-%Y')
    datetime_end_date = datetime.datetime.strptime(end_date, '%d-%m-%Y') 

    datetime_1 = datetime_start_date
    
    #coin_info = cg.get_coin_history_by_id(coin, start_date)

    while datetime_1 != datetime_end_date + datetime.timedelta(days=1):
        print(datetime_1.strftime("%d-%m-%Y"))
        print("- Day", day)
        print("- Portfolio value is", balance)
        datetime_string = datetime_1.strftime("%d-%m-%Y")

        coin_info = cg.get_coin_history_by_id(coin, datetime_string)
        print(coin, " price on ", datetime_1, " was ", coin_info.get('market_data').get('current_price').get('usd'))

        datetime_1 = datetime_1 + datetime.timedelta(days=1)
        day += 1

        # bitcoin_value = bitcoin_price * bitcoin_held
    # Iterate & print the dict
    #for key in coin_info:
    #    print(key, " = ", bitcoin.get(key))



balance = 1000
start_date = '01-06-2019'
end_date = '09-06-2019'

print("Starting balance is", balance, "USD")

day = 1
num_of_days = 10

bitcoin_price = { '01-06-2019': 8575.646353354166,
                  '02-06-2019': 8554.261728092017,
                  '03-06-2019': 8743.705469134235,
                  '04-06-2019': 8173.632761796738,
                  '05-06-2019': 7683.636261419786,
                  '06-06-2019': 7812.448854732150,
                  '07-06-2019': 7821.123897094859,
                  '08-06-2019': 8036.108159122215,
                  '09-06-2019': 7705.539284064289
                }

x = datetime.datetime.now()
x = datetime.datetime(2020, 5, 17)

date_1 = datetime.datetime(2019, 6, 1)

#bitcoin_held = balance / bitcoin_price
#print(bitcoin_held)
def run(coin_1,percentage_1,coin_2,percentage_2,start_date,end_date, strategy):

    day = 1
    datetime_start_date = datetime.datetime.strptime(start_date, '%d-%m-%Y')
    datetime_end_date = datetime.datetime.strptime(end_date, '%d-%m-%Y') 

    datetime_1 = datetime_start_date

    balance = 1000

    portfolio_percentage = .5
        
    bitcoin_held = balance*percentage_2 / bitcoin_price.get(datetime_1.strftime("%d-%m-%Y"))

    usd_held = balance*percentage_1
#    print(bitcoin_held)
    
    print("Bought", bitcoin_held, "bitcoin at", bitcoin_price.get(datetime_1.strftime("%d-%m-%Y")), "USD")

    #coin_info = cg.get_coin_history_by_id(coin, start_date)

    if strategy == 'bnh':
        while datetime_1 != datetime_end_date + datetime.timedelta(days=1):
            print(datetime_1.strftime("%d-%m-%Y"))
            balance = usd_held + bitcoin_held * bitcoin_price.get(datetime_1.strftime("%d-%m-%Y"))
            print("- Day", day)
            print("- Bitcoin price is :", bitcoin_price.get(datetime_1.strftime("%d-%m-%Y")))
            print("- Portfolio value is", balance, "USD")
            datetime_1 = datetime_1 + datetime.timedelta(days=1)
            day += 1
         #   bitcoin_value = bitcoin_price * bitcoin_held

    if strategy == 'rebalance_daily':
        while datetime_1 != datetime_end_date + datetime.timedelta(days=1):
            # Before rebalance
            print(datetime_1.strftime("%d-%m-%Y"))
            usd_value = usd_held
            bitcoin_value = bitcoin_held * bitcoin_price.get(datetime_1.strftime("%d-%m-%Y"))
            balance = usd_value + bitcoin_value
            print("- Day", day)
            print("- Bitcoin price is :", bitcoin_price.get(datetime_1.strftime("%d-%m-%Y")))
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
                purchase_bitcoin = bitcoin_difference / bitcoin_price.get(datetime_1.strftime("%d-%m-%Y"))
                print("bought ", purchase_bitcoin, "bitcoin for", bitcoin_difference, "USD")
                bitcoin_held += purchase_bitcoin
                usd_held -= bitcoin_difference

            if bitcoin_value > usd_value:
                bitcoin_sold = bitcoin_difference / bitcoin_price.get(datetime_1.strftime("%d-%m-%Y"))
                print("sold ", bitcoin_sold, "bitcoin for", bitcoin_difference, "USD")
                bitcoin_held += bitcoin_sold
                usd_held -= bitcoin_difference
                
            # After rebalance
            print("After rebalance")
            usd_value = usd_held
            bitcoin_value = bitcoin_held * bitcoin_price.get(datetime_1.strftime("%d-%m-%Y"))
            balance = usd_value + bitcoin_value
            print("- Bitcoin value is :", bitcoin_value)
            print("- USD value is is :", usd_value)
            print("- Portfolio value is", balance, "USD")
            datetime_1 = datetime_1 + datetime.timedelta(days=1)
            day += 1
         #   bitcoin_value = bitcoin_price * bitcoin_held

    return balance

x = 'bitcoin'
y = '01-06-2019'
z = '09-06-2019'
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
