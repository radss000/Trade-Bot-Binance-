import requests
import sqlite3
import base64
import hashlib
import hmac


def getDepth(direction='ask', pair='BTCUSD'):
    # Set the endpoint for the API call
    endpoint = f"https://api.binance.com/api/v3/ticker/price?symbol={pair}"
    
    # Make the GET request
    response = requests.get(endpoint)
    
    # Check the status code of the response
    if response.status_code == 200:
        # If the request was successful, parse the JSON data
        data = response.json()
        
        # Check the direction parameter to determine which price to return
        if direction == 'ask':
            return data['askPrice']
        elif direction == 'bid':
            return data['bidPrice']
    else:
        return None
def getOrderBook(pair='BTCUSD'):
    # Set the endpoint for the API call
    endpoint = f"https://api.binance.com/api/v3/depth?symbol={pair}"
    response = requests.get(endpoint)
    
    # Check the status code of the response
    if response.status_code == 200:
        # If the request was successful, parse the JSON data
        return response.json()
    else:
        return None
def refreshDataCandle(pair='BTCUSD', duration='5m'):
    # Set the endpoint for the API call
    endpoint = f"https://api.binance.com/api/v1/klines?symbol={pair}&interval={duration}"
    response = requests.get(endpoint)
    if response.status_code == 200:
        return response.json()
    else:
        return None
def createCandleTable():
    # Connect to the database
    conn = sqlite3.connect("trading.db")
    c = conn.cursor()

    # Create the table
    c.execute("CREATE TABLE IF NOT EXISTS candles (timestamp INTEGER, open REAL, high REAL, low REAL, close REAL, volume REAL)")
    conn.commit()
    conn.close()     
def refreshDataCandle(pair='BTCUSD', duration='5m'):
    # Set the endpoint for the API call
    endpoint = f"https://api.binance.com/api/v1/klines?symbol={pair}&interval={duration}"
    
    # Make the GET request
    response = requests.get(endpoint)
    if response.status_code == 200:
        data = response.json()
        conn = sqlite3.connect("trading.db")
        c = conn.cursor()
        
        # Check if the latest candle in the database is the same as the latest candle in the data
        c.execute("SELECT * FROM candles ORDER BY timestamp DESC LIMIT 1")
        latest_candle_db = c.fetchone()
        latest_candle_api = data[-1]
        if latest_candle_db[0] != latest_candle_api[0]:
            # If the latest candle is not the same, update the database with the new candle data
            for candle in data:
                c.execute("INSERT INTO candles VALUES (?, ?, ?, ?, ?, ?)", candle)
        
        conn.commit()
        conn.close()
        
        return True
    else:
        return False
def refreshData(pair='BTCUSD'):
    endpoint = f"https://api.binance.com/api/v1/trades?symbol={pair}"
  
    response = requests.get(endpoint)
    
    
    if response.status_code == 200:
        # If succesfull parson json 
        data = response.json()
        
        # Connect to the db
        conn = sqlite3.connect("trading.db")
        c = conn.cursor()
        
        # Iterate through the data and insert it into the table
        for trade in data:
            c.execute("INSERT INTO trades VALUES (?, ?, ?, ?)", (trade['id'], trade['price'], trade['quantity'], trade['timestamp']))
        conn.commit()
        conn.close()
        return True
    else:
        return False       
def createOrder(api_key, secret_key, direction, price, amount, pair='BTCUSD_d', orderType='LimitOrder'):
    # Set the endpoint for the API call
    endpoint = "https://api.binance.com/api/v3/order"
    params = {
        "symbol": pair,
        "side": direction,
        "type": orderType,
        "timeInForce": "GTC",
        "price": price,
        "quantity": amount
    }
    
    # Encode the parameters as a query string
    query_string = "&".join([f"{key}={value}" for key, value in params.items()])
    
    # Generate the signature for the request
    signature = hmac.new(secret_key.encode(), query_string.encode(), hashlib.sha256).hexdigest()
    
    # Set the headers for the request
    headers = {
        "X-MBX-APIKEY": api_key,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    # Make the POST request
    response = requests.post(endpoint, data=query_string, headers=headers)
    
    # Check the status code of the response
    if response.status_code == 200:
        return response.json()
    else:
        return None
        
