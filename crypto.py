import requests
import pandas as pd

def getTradeRate(symbol):
    # contact the iexcloud api servers and get the price of the selected crypto
    api_url = f'https://cloud.iexapis.com/stable/crypto/{symbol}/price?token=pk_a967ee1668a54594b661afc25dfcc3b9'
    raw = requests.get(api_url).json()
    price = raw['price']
    return float(price)

# returns the price of the cryptocurrency as a float

def getPriceGraph(from_currency, to_currency, start_date = None):
    # contact the alphavantage api servers and ask it for a table of the prices of the certain crypto over the past week
    api_url = f'https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol={from_currency}&market={to_currency}&apikey=QZXD767Z4YO825A9'
    raw_df = requests.get(api_url).json()
    # use pandas to properly align the dataframe
    df = pd.DataFrame(raw_df['Time Series (Digital Currency Daily)']).T
    df = df.rename(columns = {'1a. open (USD)': 'open', '2a. high (USD)': 'high', '3a. low (USD)': 'low', '4a. close (USD)': 'close', '5. volume': 'volume'})
    # convert the price values into floats, because they start out as strings for some reason
    for i in df.columns:
        df[i] = df[i].astype(float)
    # format the date index properly
    df.index = pd.to_datetime(df.index)
    df = df.iloc[::-1].drop(['1b. open (USD)', '2b. high (USD)', '3b. low (USD)', '4b. close (USD)', '6. market cap (USD)'], axis = 1)
    # remove any values before the start date
    if start_date:
        df = df[df.index >= start_date]
    # get all the date indexes and put them in a list
    dates = []
    for date in df.index:
        dates.append(date)
    # add the list of dates into a seperate column (matplotlib doesnt like it when the dates are indexes)
    df['date'] = dates
    return df

# returns a table like this:

#      index      open      high       low     close        volume        date
# 2021-11-01  61299.81  62437.74  59405.00  60911.11  44687.666720  2021-11-01
# 2021-11-02  60911.12  64270.00  60624.68  63219.99  46368.284100  2021-11-02
# 2021-11-03  63220.57  63500.00  60382.76  62896.48  43336.090490  2021-11-03
# 2021-11-04  62896.49  63086.31  60677.01  61395.01  35930.933140  2021-11-04
# 2021-11-05  61395.01  62595.72  60721.00  60937.12  31604.487490  2021-11-05

# i had to use 2 different APIs because alphavantage has a limit of 5 requests per minute, and iexCloud doesn't let you
# pull historical data for free, but has a nearly unlimited amount of requests

def combineGraphs(graphs):
    new_graphs = []
    # get the date column and save it
    dates = graphs[0]['date']
    # drop the date column from each graph (you cant add dates)
    for graph in graphs:
        temp_graph = graph
        temp_graph = temp_graph.drop(['date'], axis = 1)
        new_graphs.append(temp_graph)
    # add all the graphs together
    combined_df = new_graphs[0]
    for i in range(len(new_graphs) - 1):
        combined_df = combined_df.add(new_graphs[i + 1])
    # put the date column back in
    combined_df['date'] = dates
    return combined_df
