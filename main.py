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

        for key in portfolio.get('balances'):
            balance = portfolio.get('balances').get(key)
            prices = coin_prices.get(key)
            price = prices.get(date.strftime("%d-%m-%Y"))
            value = balance * price
#            print("- " + format(key) + " balance: " + format(balance))
#            print("- " + format(key) + " price: " + format(price))
#            print("- " + format(key) + " value: " + format(value))
            portfolio_value += value

#        print("- Total portfolio value: ", portfolio_value, "USD")
#        print("\n")
        date = date + datetime.timedelta(days=1)
        day += 1
    return portfolio_value

def get_portfolio_value(portfolio, date):
    portfolio_value = 0

    for key in portfolio.get('balances'):
        balance = portfolio.get('balances').get(key)
        prices = coin_prices.get(key)
        price = prices.get(date.strftime("%d-%m-%Y"))
        value = balance * price

        portfolio_value += value

    return portfolio_value

def rebalance(portfolio, date):

#    print("Rebalancing...")
        
    # Get total value of portfolio
    portfolio_value = get_portfolio_value(portfolio, date)
#    print("- Total portfolio value: " + format(portfolio_value))

    for key in portfolio.get('balances'):

        #Before rebalance
        allocation = portfolio.get('allocations').get(key)
        balance = portfolio.get('balances').get(key)
        prices = coin_prices.get(key)
        price = prices.get(date.strftime("%d-%m-%Y"))
        value = balance * price
#        print("- " + format(key) + " allocation: " + format(allocation))
#        print("- " + format(key) + " balance: " + format(balance))
#        print("- " + format(key) + " price: " + format(price))
#        print("- " + format(key) + " value: " + format(value))

        target_value = portfolio_value * allocation
#        print("- Target value is", target_value)

        #Rebalance
        difference = target_value - value
#        print("- " + format(key) + " difference: " + format(difference))

        change = difference / price
        portfolio['balances'][key] += change
#        print("-* rebalanced " + format(change) + " " + format(key) + " for " + format(difference) + " USD")

        balance = portfolio.get('balances').get(key)
        value = balance * price
 #       print("- " + key + " value: " + format(value))

 #   print("- Total portfolio value: ", portfolio_value, "USD")
 #   print("\n")

    return portfolio

# Rebalance strategy
def run_strategy_rebalance(portfolio,start_date_str,end_date_str):

    this_portfolio = portfolio.copy()

    day = 1
    start_date = datetime.datetime.strptime(start_date_str, '%d-%m-%Y')
    end_date = datetime.datetime.strptime(end_date_str, '%d-%m-%Y') 
    date = start_date

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
def run_strategy(portfolio,start_date,end_date, strategy):

    if strategy == 'buy and hold':
        portfolio_value = run_strategy_bnh(portfolio,start_date,end_date)

    if strategy == 'rebalance daily':
        portfolio_value = run_strategy_rebalance(portfolio,start_date,end_date)

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
    num = 1

    coins = ['usd',
             'bitcoin',
             'ethereum',
             'binance',
             'neo',
             'litecoin',
             'ontology',
             'eos',
             'pundi-x',
             'bitcoin-cash',
             'cardano',
             'tron',
             'cosmos',
             'nem',
             'ravencoin',
             'gxchain',
             'bittorrent-2',
             'matic-network',
             'celer-network',
             'fetch-ai',
             ]

    # Create one asset portfolios w/ buy and hold strategy
    for main in coins:
        portfolio = {}
        portfolio['allocations'] = {}
        portfolio['balances'] = {}
        portfolio['name'] = "Portfolio #" + format(num)
        portfolio['strategy'] = 'buy and hold'     
        for coin in coins:
            portfolio['allocations'][coin] = 0
            portfolio['balances'][coin] = 0
        portfolio['allocations'][main] = 1
        portfolio['balances'][coins[0]] = 1000

        portfolios.append(portfolio)
        num += 1

    # Create evenly split multi-asset portfolio w/ buy and hold strategy
    portfolio = {}
    portfolio['allocations'] = {}
    portfolio['balances'] = {}
    allocation = 1 / len(coins)
        
    for coin in coins:
        portfolio['name'] = "Portfolio #" + format(num)
        portfolio['strategy'] = 'buy and hold'
        portfolio['allocations'][coin] = allocation
        portfolio['balances'][coin] = 0

    portfolio['balances'][coins[0]] = 1000

    portfolios.append(portfolio)
    num += 1

    # Create evenly split multi-asset portfolio w/ rebalance strategy
    portfolio = {}
    portfolio['allocations'] = {}
    portfolio['balances'] = {}
    allocation = 1 / len(coins)
        
    for coin in coins:
        portfolio['name'] = "Portfolio #" + format(num)
        portfolio['strategy'] = 'rebalance daily'
        portfolio['allocations'][coin] = allocation
        portfolio['balances'][coin] = 0

    portfolio['balances'][coins[0]] = 1000

    portfolios.append(portfolio)
    num += 1

    print(format(len(portfolios)) + " portfolios constructed" + "\n")

    for portfolio in portfolios:
#        print_portfolio(portfolio)
        print("\n")

    return portfolios

def print_portfolio(portfolio):
    print(format(portfolio.get('name')))
    print("- Strategy: " + format(portfolio.get('strategy')))

    print("- Allocations:")
    for coin in portfolio.get('allocations'):
        print("-- " + format(coin) + ": " + format(portfolio.get('allocations').get(coin)))

    print("- Balances:")
    for coin in portfolio.get('balances'):
        print("-- " + format(coin) + ": " + format(portfolio.get('balances').get(coin)))


# Run the simulation
def run():

    start_date = '01-06-2019'
    end_date = '02-06-2019'

    results = []

    portfolios = construct_portfolios()

    for portfolio in portfolios:
        name = portfolio.get('name')
        strategy = portfolio.get('strategy')
        print("Running " + strategy + " simulation on " + name)
        results.append([portfolio, run_strategy(portfolio, start_date, end_date, strategy)])
        print("\n")

    for result in results:
        print_portfolio(result[0])
        print(result[1])
        print("\n")

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
