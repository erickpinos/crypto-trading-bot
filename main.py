from pycoingecko import CoinGeckoAPI
import datetime
import time
from prices import *

cg = CoinGeckoAPI()



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
    print(coin + '_prices = {')

    while date != end_date + datetime.timedelta(days=1):
        date_str = date.strftime("%d-%m-%Y")

        coin_info = cg.get_coin_history_by_id(coin, date_str)
        current_price = coin_info.get('market_data').get('current_price').get('usd')
        print("    '" + date_str + "': " + format(current_price) + ',')

        date += datetime.timedelta(days=1)
        time.sleep(1)
 
    print("   }")

# Iterate & print the dict
def print_dict(coin, date_str):
    coin_info = cg.get_coin_history_by_id(coin, date_str)

    for key in coin_info:
        print(key, " = ", bitcoin.get(key))

# Buy and hold strategy
def run_strategy_bnh(portfolio,start_date_str,end_date_str):
    day = 1
    start_date = datetime.datetime.strptime(start_date_str, '%d-%m-%Y')
    end_date = datetime.datetime.strptime(end_date_str, '%d-%m-%Y') 
    date = start_date
    

    portfolio = rebalance(portfolio, date)

    while date != end_date + datetime.timedelta(days=1):
        portfolio_value = 0
        date_str = date.strftime("%d-%m-%Y")
        #print("Day " + format(day) + ": " + date_str)

        for key in portfolio:
            balance = portfolio.get(key).get('balance')
            prices = portfolio.get(key).get('prices')
            price = prices.get(date.strftime("%d-%m-%Y"))
            value = balance * price
#            print("- " + format(key) + " balance: " + format(balance))
#            print("- " + format(key) + " price: " + format(price))
#            print("- " + format(key) + " value: " + format(value))
            portfolio_value += value

        #print("- Total portfolio value: ", portfolio_value, "USD")
        #print("\n")
        date = date + datetime.timedelta(days=1)
        day += 1
    return portfolio_value

def get_portfolio_value(portfolio, date):
    portfolio_value = 0

    for key in portfolio:
        balance = portfolio.get(key).get('balance')
        prices = portfolio.get(key).get('prices')
        price = prices.get(date.strftime("%d-%m-%Y"))
        value = balance * price

        portfolio[key]['value'] = value
        portfolio_value += value

    return portfolio_value

def rebalance(portfolio, date):

    portfolio_value = 0
    
    # Get total value of portfolio
    portfolio_value = get_portfolio_value(portfolio, date)
    print("- Total portfolio value is " + format(portfolio_value))

    for key in portfolio:

        #Before rebalance
        percentage = portfolio.get(key).get('percentage')
        balance = portfolio.get(key).get('balance')
        prices = portfolio.get(key).get('prices')
        value = portfolio.get(key).get('value')
        price = prices.get(date.strftime("%d-%m-%Y"))
#        print("- " + format(key) + " balance: " + format(balance))
#        print("- " + format(key) + " price: " + format(price))
#        print("- " + format(key) + " value: " + format(value))

        target_value = portfolio_value * percentage
        print("- Target value is", target_value)

        #Rebalance
        difference = target_value - value
        portfolio[key]['difference'] = difference
        #print("- " + format(key) + " difference: " + format(difference))

        change = difference / price
        portfolio[key]['balance'] += change
        #print("-* rebalanced " + format(change) + " " + format(key) + " for " + format(difference) + " USD")

        balance = portfolio.get(key).get('balance')
        portfolio[key]['value'] = balance * price
        value = portfolio.get(key).get('value')
        portfolio[key]['difference'] = 0
        #print("- " + key + " value: " + format(value))

    print("- Total portfolio value: ", portfolio_value, "USD")
    print("\n")

    return portfolio

# Rebalance strategy
def run_strategy_rebalance(portfolio,start_date_str,end_date_str):
    day = 1
    start_date = datetime.datetime.strptime(start_date_str, '%d-%m-%Y')
    end_date = datetime.datetime.strptime(end_date_str, '%d-%m-%Y') 
    date = start_date

    balance = 1000
    portfolio_value = balance

    print("Starting portfolio value: " + format(portfolio_value))
    
    while date != end_date + datetime.timedelta(days=1):

        date_str = date.strftime("%d-%m-%Y")
        print("Day " + format(day) + ": " + date_str)

        portfolio = rebalance(portfolio, date)

        date = date + datetime.timedelta(days=1)
        day += 1

    portfolio_value = get_portfolio_value(portfolio, date)
    return portfolio_value

# Run the strategy
def run_strategy(portfolio,start_date_str,end_date_str, strategy):
    
    if strategy == 'bnh':
        portfolio_value = run_strategy_bnh(portfolio,start_date_str,end_date_str)

    if strategy == 'rebalance_daily':
        portfolio_value = run_strategy_rebalance(portfolio,start_date_str,end_date_str)

    return portfolio_value

start_date = '01-05-2019'
end_date = '08-06-2019'

portfolio_1 = { 
    'usd': {'percentage': .25, 'prices': usd_prices, 'balance': 1000, 'value': 1000, 'difference': 0},
    'bitcoin': {'percentage': .25, 'prices': bitcoin_prices, 'balance': 0, 'value': 0, 'difference': 0},
    'ethereum': {'percentage': .25, 'prices': ethereum_prices, 'balance': 0, 'value': 0, 'difference': 0},
    'binance': {'percentage': .25, 'prices': binancecoin_prices, 'balance': 0, 'value': 0, 'difference': 0},
    'neo': {'percentage': .25, 'prices': neo_prices, 'balance': 0, 'value': 0, 'difference': 0},
    'litecoin': {'percentage': .25, 'prices': litecoin_prices, 'balance': 0, 'value': 0, 'difference': 0},
    'ontology': {'percentage': .25, 'prices': ontology_prices, 'balance': 0, 'value': 0, 'difference': 0},
    'eos': {'percentage': .25, 'prices': eos_prices, 'balance': 0, 'value': 0, 'difference': 0},
    'pundi-x': {'percentage': .25, 'prices': pundi_x_prices, 'balance': 0, 'value': 0, 'difference': 0},
    'bitcoin-cash': {'percentage': .25, 'prices': bitcoin_cash_prices, 'balance': 0, 'value': 0, 'difference': 0},
    'cardano': {'percentage': .25, 'prices': cardano_prices, 'balance': 0, 'value': 0, 'difference': 0},
    'tron': {'percentage': .25, 'prices': tron_prices, 'balance': 0, 'value': 0, 'difference': 0},
    'cosmos': {'percentage': .25, 'prices': cosmos_prices, 'balance': 0, 'value': 0, 'difference': 0},
    'nem': {'percentage': .25, 'prices': nem_prices, 'balance': 0, 'value': 0, 'difference': 0},
    'ravencoin': {'percentage': .25, 'prices': ravencoin_prices, 'balance': 0, 'value': 0, 'difference': 0},
    'gxchain': {'percentage': .25, 'prices': gxchain_prices, 'balance': 0, 'value': 0, 'difference': 0},
    'bittorrent-2': {'percentage': .25, 'prices': bittorrent_2_prices, 'balance': 0, 'value': 0, 'difference': 0},
    'matic-network': {'percentage': .25, 'prices': matic_network_prices, 'balance': 0, 'value': 0, 'difference': 0},
    'celer-network': {'percentage': .25, 'prices': celer_network_prices, 'balance': 0, 'value': 0, 'difference': 0},
    'fetch-ai': {'percentage': .25, 'prices': fetch_ai_prices, 'balance': 0, 'value': 0, 'difference': 0},
    }

portfolio_2 = { 
    'usd': {'percentage': .5, 'prices': usd_prices, 'balance': 1000, 'value': 1000, 'difference': 0},
    'bitcoin': {'percentage': .5, 'prices': bitcoin_prices, 'balance': 0, 'value': 0, 'difference': 0},
    }

portfolio_3 = { 
    'usd': {'percentage': 0, 'prices': usd_prices, 'balance': 1000, 'value': 1000, 'difference': 0},
    'bitcoin': {'percentage': 1, 'prices': bitcoin_prices, 'balance': 0, 'value': 0, 'difference': 0},
    }

portfolio_4 = { 
    'usd': {'percentage': .5, 'prices': usd_prices, 'balance': 1000, 'value': 1000, 'difference': 0},
    'ontology': {'percentage': .5, 'prices': ontology_prices, 'balance': 0, 'value': 0, 'difference': 0},
    }

portfolio_5 = { 
    'usd': {'percentage': 0, 'prices': usd_prices, 'balance': 1000, 'value': 1000, 'difference': 0},
    'ontology': {'percentage': 1, 'prices': ontology_prices, 'balance': 0, 'value': 0, 'difference': 0},
    }

portfolio_6 = { 
    'usd': {'percentage': 0, 'prices': usd_prices, 'balance': 1000, 'value': 1000, 'difference': 0},
    'bitcoin': {'percentage': 0.5, 'prices': bitcoin_prices, 'balance': 0, 'value': 0, 'difference': 0},
    'ontology': {'percentage': 0.5, 'prices': ontology_prices, 'balance': 0, 'value': 0, 'difference': 0},
    }

portfolio_7 = { 
    'usd': {'percentage': 0.25, 'prices': usd_prices, 'balance': 1000, 'value': 1000, 'difference': 0},
    'bitcoin': {'percentage': 0.25, 'prices': bitcoin_prices, 'balance': 0, 'value': 0, 'difference': 0},
    'ontology': {'percentage': 0.25, 'prices': ontology_prices, 'balance': 0, 'value': 0, 'difference': 0},
    'binancecoin': {'percentage': 0.25, 'prices': binancecoin_prices, 'balance': 0, 'value': 0, 'difference': 0},
    }

portfolio_8 = { 
    'usd': {'percentage': 0, 'prices': usd_prices, 'balance': 1000, 'value': 1000, 'difference': 0},
    'ontology': {'percentage': 0.5, 'prices': ontology_prices, 'balance': 0, 'value': 0, 'difference': 0},
    'binancecoin': {'percentage': 0.5, 'prices': binancecoin_prices, 'balance': 0, 'value': 0, 'difference': 0},
    }

def construct_portfolios():
    portfolios = []
    portfolio = {}

    print("Coin permutations")

    coins = ['usd',
             'bitcoin',
             'ethereum',
             'binance',
             ]

    len(coins)

    for coin in coins:
        
        portfolio[coin]['current_prices']

    portfolios.append(portfolio)
    print("x portfolios constructed")
    
def display_portfolio(portfolio):
    print("Portfolio:")
    for key in portfolio:
        print(key)
        for field in portfolio.get(key):
            if field != 'prices':
                print("- " + format(field) + ": " + format(portfolio.get(key).get(field)))

# Run the simulation
def run():
    strategy_1 = run_strategy(portfolio_1, start_date, end_date, 'bnh')
    strategy_2 = run_strategy(portfolio_1, start_date, end_date, 'rebalance_daily')
    strategy_3 = run_strategy(portfolio_2, start_date, end_date, 'bnh')
    strategy_4 = run_strategy(portfolio_2, start_date, end_date, 'rebalance_daily')
    strategy_5 = run_strategy(portfolio_3, start_date, end_date, 'bnh')
    strategy_6 = run_strategy(portfolio_3, start_date, end_date, 'rebalance_daily')
    strategy_7 = run_strategy(portfolio_4, start_date, end_date, 'bnh')
    strategy_8 = run_strategy(portfolio_4, start_date, end_date, 'rebalance_daily')
    strategy_9 = run_strategy(portfolio_5, start_date, end_date, 'bnh')
    strategy_10 = run_strategy(portfolio_5, start_date, end_date, 'rebalance_daily')
    strategy_11 = run_strategy(portfolio_6, start_date, end_date, 'bnh')
    strategy_12 = run_strategy(portfolio_6, start_date, end_date, 'rebalance_daily')
    strategy_13 = run_strategy(portfolio_7, start_date, end_date, 'bnh')
    strategy_14 = run_strategy(portfolio_7, start_date, end_date, 'rebalance_daily')
    strategy_15 = run_strategy(portfolio_8, start_date, end_date, 'bnh')
    strategy_16 = run_strategy(portfolio_8, start_date, end_date, 'rebalance_daily')

    print('buy and hold usd', strategy_1)
    print('rebalance', strategy_2)
    print('buy and hold usd', strategy_3)
    print('rebalance', strategy_4)
    print('buy and hold usd', strategy_5)
    print('rebalance', strategy_6)
    print('buy and hold usd', strategy_7)
    print('rebalance', strategy_8)
    print('buy and hold usd', strategy_9)
    print('rebalance', strategy_10)
    print('buy and hold usd', strategy_11)
    print('rebalance', strategy_12)
    print('buy and hold usd', strategy_13)
    print('rebalance', strategy_14)
    print('buy and hold usd', strategy_15)
    print('rebalance', strategy_16)


def get_lots_of_prices():
    start_date = '01-05-2019'
    end_date = '09-06-2019'
    coins = [
        'ravencoin',
        'gxchain',
        'bittorrent-2',
        'matic-network',
        'celer-network',
        'fetch-ai',
        'harmony'
        ]

    for coin in coins:
        get_prices(coin, start_date, end_date)
