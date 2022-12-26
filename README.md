
# Cryptocurrency Trading API
This script provides a set of functions to interact with the Binance API to retrieve and store data on cryptocurrency prices and trades.

# Dependencies

This script requires the following Python modules:

requests: used to make HTTP requests to the Binance API

sqlite3: used to store data in a SQLite database

base64: used to encode and decode data for authentication

hashlib: used to generate hashes for authentication

hmac: used to generate hashes for authentication

You can install these dependencies by running pip install requests sqlite3 base64 hashlib hmac.

# Functions

getDepth(direction='ask', pair='BTCUSD'): retrieves the 'ask' or 'bid' price for a given cryptocurrency pair.

getOrderBook(pair='BTCUSD'): retrieves the order book for a given cryptocurrency pair.

refreshDataCandle(pair='BTCUSD', duration='5m'): retrieves and stores aggregated trading data (candles) for a given cryptocurrency pair and duration.

createCandleTable(): creates a table in the SQLite database to store candle data.

refreshData(pair='BTCUSD'): retrieves and stores all available trade data for a given cryptocurrency pair.

createTradeTable(): creates a table in the SQLite database to store trade data.

createOrder(api_key, secret_key, direction, price, amount, pair='BTCUSD_d', orderType='LimitOrder'): creates an order using the Binance API.

cancelOrder(api_key, secret_key, uuid): cancels an order using the Binance API.

# Disclaimer

This script is provided for educational purposes only. It is not intended for use in real-world trading. I'm not responsible for any losses or damages resulting from the use of this script.
