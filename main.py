from pycoingecko import CoinGeckoAPI
import datetime
import time

cg = CoinGeckoAPI()

# Cryptocurrency prices
usd_price = {
    '01-05-2019': 1,
    '02-05-2019': 1,
    '03-05-2019': 1,
    '04-05-2019': 1,
    '05-05-2019': 1,
    '06-05-2019': 1,
    '07-05-2019': 1,
    '08-05-2019': 1,
    '09-05-2019': 1,
    '10-05-2019': 1,
    '11-05-2019': 1,
    '12-05-2019': 1,
    '13-05-2019': 1,
    '14-05-2019': 1,
    '15-05-2019': 1,
    '16-05-2019': 1,
    '17-05-2019': 1,
    '18-05-2019': 1,
    '19-05-2019': 1,
    '20-05-2019': 1,
    '21-05-2019': 1,
    '22-05-2019': 1,
    '23-05-2019': 1,
    '24-05-2019': 1,
    '25-05-2019': 1,
    '26-05-2019': 1,
    '27-05-2019': 1,
    '28-05-2019': 1,
    '29-05-2019': 1,
    '30-05-2019': 1,
    '31-05-2019': 1,
    '01-06-2019': 1,
    '02-06-2019': 1,
    '03-06-2019': 1,
    '04-06-2019': 1,
    '05-06-2019': 1,
    '06-06-2019': 1,
    '07-06-2019': 1,
    '08-06-2019': 1,
    '09-06-2019': 1,
    }

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

ethereum_price = {
    '01-05-2019': 160.74469184721738,
    '02-05-2019': 159.48931440238658,
    '03-05-2019': 160.95718796104512,
    '04-05-2019': 166.63211526803485,
    '05-05-2019': 162.83631690744346,
    '06-05-2019': 162.37013497277283,
    '07-05-2019': 172.8283284518378,
    '08-05-2019': 170.09589748059332,
    '09-05-2019': 170.11063311538186,
    '10-05-2019': 170.57549417946805,
    '11-05-2019': 172.68209089135948,
    '12-05-2019': 196.6901677286205,
    '13-05-2019': 187.2720183708742,
    '14-05-2019': 196.0761130134244,
    '15-05-2019': 218.28460968764938,
    '16-05-2019': 248.74500426984366,
    '17-05-2019': 264.90012138907406,
    '18-05-2019': 243.57049917993308,
    '19-05-2019': 235.32720134101993,
    '20-05-2019': 260.59698403060327,
    '21-05-2019': 251.9614994995826,
    '22-05-2019': 256.0830401834705,
    '23-05-2019': 244.54946301361036,
    '24-05-2019': 244.6460957973966,
    '25-05-2019': 248.54526290535333,
    '26-05-2019': 250.82036469745617,
    '27-05-2019': 266.12218207843597,
    '28-05-2019': 273.40508817754096,
    '29-05-2019': 271.227867157993,
    '30-05-2019': 268.7857564563058,
    '31-05-2019': 255.37736314606394,
    '01-06-2019': 268.12603920482644,
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
 
    print("     }")

# Iterate & print the dict
def print_dict(coin, date_str):
    coin_info = cg.get_coin_history_by_id(coin, date_str)

    for key in coin_info:
        print(key, " = ", bitcoin.get(key))

# Run the strategy
def run_strategy(coin_1,percentage_1,coin_2,percentage_2,start_date_str,end_date_str, strategy):

    day = 1
    start_date = datetime.datetime.strptime(start_date_str, '%d-%m-%Y')
    end_date = datetime.datetime.strptime(end_date_str, '%d-%m-%Y') 
    date = start_date

    balance = 1000
    portfolio_value = balance

    print("Starting portfolio value: " + format(portfolio_value))

#    for key in portfolio:
#        percentage = portfolio.get(key).get('percentage')
#        prices = portfolio.get(key).get('prices')
#        price = prices.get(date.strftime("%d-%m-%Y"))
#        amount_bought = balance * percentage / price
#        print("Bought " + format(amount_bought) + " " + key + " at " + format(price))
#        portfolio[key]['balance'] = amount_bought
#        portfolio[key]['value'] = amount_bought * price
    
    if strategy == 'bnh':
        while date != end_date + datetime.timedelta(days=1):
            portfolio_value = 0
            date_str = date.strftime("%d-%m-%Y")
            print("Day " + format(day) + ": " + date_str)

            for key in portfolio:
                balance = portfolio.get(key).get('balance')
                prices = portfolio.get(key).get('prices')
                price = prices.get(date.strftime("%d-%m-%Y"))
                value = balance * price
                print("- " + format(key) + " balance: " + format(balance))
                print("- " + format(key) + " price: " + format(price))
                print("- " + format(key) + " value: " + format(value))
                portfolio_value += value

            print("- Total portfolio value: ", portfolio_value, "USD")
            print("\n")
            date = date + datetime.timedelta(days=1)
            day += 1

    if strategy == 'rebalance_daily':

        while date != end_date + datetime.timedelta(days=1):

            date_str = date.strftime("%d-%m-%Y")
            print("Day " + format(day) + ": " + date_str)

            # Get total value
            portfolio_value = 0
            for key in portfolio:
                balance = portfolio.get(key).get('balance')
                prices = portfolio.get(key).get('prices')
                price = prices.get(date.strftime("%d-%m-%Y"))
                value = balance * price
                print("- " + format(key) + " balance: " + format(balance))
                print("- " + format(key) + " price: " + format(price))
                print("- " + format(key) + " value: " + format(value))

                portfolio[key]['value'] = value
                portfolio_value += value

            print("- Total portfolio value is " + format(portfolio_value))

            for key in portfolio:

                #Before rebalance
                percentage = portfolio.get(key).get('percentage')
                balance = portfolio.get(key).get('balance')
                prices = portfolio.get(key).get('prices')
                value = portfolio.get(key).get('value')
                price = prices.get(date.strftime("%d-%m-%Y"))
                print("- " + format(key) + " balance: " + format(balance))
                print("- " + format(key) + " price: " + format(price))
                print("- " + format(key) + " value: " + format(value))

                target_value = portfolio_value * percentage
                print("- Target value is", target_value)

                #Rebalance
                difference = target_value - value
                portfolio[key]['difference'] = difference
                print("- " + format(key) + " difference: " + format(difference))

                change = difference / price
                portfolio[key]['balance'] += change
                portfolio['usd']['balance'] -= difference
                print("-* rebalanced " + format(change) + " " + format(key) + " for " + format(difference) + " USD")

                balance = portfolio.get(key).get('balance')
                value = portfolio.get(key).get('value')
                portfolio[key][value] = balance * price
                print("- " + key + " value: " + format(portfolio[key]['value']))

            print("- Total portfolio value: ", portfolio_value, "USD")
            print("\n")

            date = date + datetime.timedelta(days=1)
            day += 1

    return balance

balance = 1000
start_date = '01-05-2019'
end_date = '05-05-2019'

day = 1

x = 'bitcoin'
y = '01-05-2019'
z = '04-05-2019'
#get_prices(x,y,z)


portfolio = { 
    'usd': {'percentage': .5, 'prices': usd_price, 'balance': 1000, 'value': 1000, 'difference': 0},
    'bitcoin': {'percentage': .5, 'prices': bitcoin_price, 'balance': 0, 'value': 0, 'difference': 0},
    }

# Run the simulation
def run():
#    strategy_1 = run_strategy('usd',1,'bitcoin',0,y,z, 'bnh')
#    strategy_2 = run_strategy('usd',0,'bitcoin',1,y,z, 'bnh')
#    strategy_3 = run_strategy('usd',.5,'bitcoin',.5,y,z, 'bnh')
    strategy_4 = run_strategy('usd',.5,'bitcoin',.5,y,z, 'rebalance_daily')

#    print('buy and hold usd', strategy_1)
#    print('buy and hold btc', strategy_2)
#    print('buy and hold 50% usd and 50% btc', strategy_3)
    print('rebalance 50% usd and 50% btc', strategy_4)


#Buy and hold strategy
#def buy_and_hold(coin_1,percentage_1,coin_2,percentage_2):
    
#Rebalance daily to equal weights

#buy_and_hold('usd',1,'bitcoin',0)
#buy_and_hold('usd',.5,'bitcoin',.5)
#buy_and_hold('usd',0,'bitcoin',1)
