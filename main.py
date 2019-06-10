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
        print("Day " + format(day) + ": " + date_str)

        for key in portfolio:
            balance = portfolio.get(key).get('balance')
            prices = coin_prices.get(key)
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
    return portfolio_value

def get_portfolio_value(portfolio, date):
    portfolio_value = 0

    for key in portfolio:
        balance = portfolio.get(key).get('balance')
        prices = coin_prices.get(key)
        price = prices.get(date.strftime("%d-%m-%Y"))
        value = balance * price

        portfolio[key]['value'] = value
        portfolio_value += value

    return portfolio_value

def rebalance(portfolio, date):

    this_portfolio = portfolio.copy()
    
    portfolio_value = 0
    
    # Get total value of portfolio
    portfolio_value = get_portfolio_value(this_portfolio, date)
#    print("- Total portfolio value is " + format(portfolio_value))

    for key in portfolio:

        #Before rebalance
        percentage = this_portfolio.get(key).get('percentage')
        balance = this_portfolio.get(key).get('balance')
        prices = coin_prices.get(key)
        value = this_portfolio.get(key).get('value')
        price = prices.get(date.strftime("%d-%m-%Y"))
#        print("- " + format(key) + " balance: " + format(balance))
#        print("- " + format(key) + " price: " + format(price))
#        print("- " + format(key) + " value: " + format(value))

        target_value = portfolio_value * percentage
#        print("- Target value is", target_value)

        #Rebalance
        difference = target_value - value
        this_portfolio[key]['difference'] = difference
        #print("- " + format(key) + " difference: " + format(difference))

        change = difference / price
        this_portfolio[key]['balance'] += change
        #print("-* rebalanced " + format(change) + " " + format(key) + " for " + format(difference) + " USD")

        balance = portfolio.get(key).get('balance')
        this_portfolio[key]['value'] = balance * price
        value = this_portfolio.get(key).get('value')
        this_portfolio[key]['difference'] = 0
        #print("- " + key + " value: " + format(value))

#    print("- Total portfolio value: ", portfolio_value, "USD")
#    print("\n")

    return portfolio

# Rebalance strategy
def run_strategy_rebalance(portfolio,start_date_str,end_date_str):

    this_portfolio = portfolio.copy()

    day = 1
    start_date = datetime.datetime.strptime(start_date_str, '%d-%m-%Y')
    end_date = datetime.datetime.strptime(end_date_str, '%d-%m-%Y') 
    date = start_date

    balance = 1000
    portfolio_value = balance

#    print("Starting portfolio value: " + format(portfolio_value))
    
    while date != end_date + datetime.timedelta(days=1):

        date_str = date.strftime("%d-%m-%Y")
#        print("Day " + format(day) + ": " + date_str)

        portfolio = rebalance(this_portfolio, date)

        date = date + datetime.timedelta(days=1)
        day += 1

    portfolio_value = get_portfolio_value(this_portfolio, date)
    return portfolio_value

# Run the strategy
def run_strategy(portfolio,start_date_str,end_date_str, strategy):

    this_portfolio = portfolio.copy()

    if strategy == 'bnh':
        portfolio_value = run_strategy_bnh(this_portfolio,start_date_str,end_date_str)

    if strategy == 'rebalance_daily':
        portfolio_value = run_strategy_rebalance(this_portfolio,start_date_str,end_date_str)

    return portfolio_value

start_date = '01-05-2019'
end_date = '08-06-2019'

portfolio_1 = { 
    'usd': {'percentage': .25, 'balance': 1000, 'value': 1000, 'difference': 0},
    'bitcoin': {'percentage': .25, 'balance': 0, 'value': 0, 'difference': 0},
    'ethereum': {'percentage': .25, 'balance': 0, 'value': 0, 'difference': 0},
    'binance': {'percentage': .25, 'balance': 0, 'value': 0, 'difference': 0},
    'neo': {'percentage': .25, 'balance': 0, 'value': 0, 'difference': 0},
    'litecoin': {'percentage': .25, 'balance': 0, 'value': 0, 'difference': 0},
    'ontology': {'percentage': .25, 'balance': 0, 'value': 0, 'difference': 0},
    'eos': {'percentage': .25, 'balance': 0, 'value': 0, 'difference': 0},
    'pundi-x': {'percentage': .25, 'balance': 0, 'value': 0, 'difference': 0},
    'bitcoin-cash': {'percentage': .25, 'balance': 0, 'value': 0, 'difference': 0},
    'cardano': {'percentage': .25, 'balance': 0, 'value': 0, 'difference': 0},
    'tron': {'percentage': .25, 'balance': 0, 'value': 0, 'difference': 0},
    'cosmos': {'percentage': .25, 'balance': 0, 'value': 0, 'difference': 0},
    'nem': {'percentage': .25, 'balance': 0, 'value': 0, 'difference': 0},
    'ravencoin': {'percentage': .25, 'balance': 0, 'value': 0, 'difference': 0},
    'gxchain': {'percentage': .25, 'balance': 0, 'value': 0, 'difference': 0},
    'bittorrent-2': {'percentage': .25, 'balance': 0, 'value': 0, 'difference': 0},
    'matic-network': {'percentage': .25, 'balance': 0, 'value': 0, 'difference': 0},
    'celer-network': {'percentage': .25, 'balance': 0, 'value': 0, 'difference': 0},
    'fetch-ai': {'percentage': .25, 'balance': 0, 'value': 0, 'difference': 0},
    }

def construct_portfolios():
    portfolios = []

    coins = ['usd',
             'bitcoin',
             'ethereum',
             'binance',
             ]

    percentage = 1 / len(coins)

    # Create one asset portfolios
    for main in coins:
        portfolio = {}

        for coin in coins:
            portfolio[coin] = {}
            portfolio[coin]['percentage'] = percentage
            portfolio[coin]['balance'] = 0
            portfolio[coin]['value'] = 0
            portfolio[coin]['difference'] = 0

        portfolio[main]['balance'] = 100
        
        portfolios.append(portfolio)

    print(format(len(portfolios)) + " portfolios constructed")

    for portfolio in portfolios:
        display_portfolio(portfolio)
        print("\n")

    return portfolios

def display_portfolio(portfolio):
    for key in portfolio:
        print(key)
        for field in portfolio.get(key):
            print("- " + format(field) + ": " + format(portfolio.get(key).get(field)))

# Run the simulation
def run():

    start_date = '01-06-2019'
    end_date = '01-06-2019'

    results = []

    portfolios = construct_portfolios()

    num = 1

    strategies = ['bnh', 'rebalance_daily']
    for strategy in strategies:
        for portfolio in portfolios:
            print("Portfolio #" + format(num))
            print(portfolio)
            display_portfolio(portfolio)
            results.append(run_strategy(portfolio, start_date, end_date, strategy))
            num += 1
            print("\n")
        
    print(results)    

def get_lots_of_prices():
    start_date = '01-05-2019'
    end_date = '01-06-2019'
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
