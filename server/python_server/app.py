from flask import Flask, request, json, make_response, jsonify
from flask_cors import CORS, cross_origin
import yfinance as yf

app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

def make_custom_error(message, status_code):
    return make_response(jsonify(message), status_code)

#home page
@app.route("/")
def home():
    return "Hello, World! The Python Server is running"


# plot request, contains query params: ticker, start, end, interval
@app.route("/request/plot", methods=["POST"])
@cross_origin()
def retrieve_plot():
    data = request.get_json()
    ticker = data["ticker"]
    start = data["start"]
    end = data["end"]
    interval = data["interval"]

    if(ticker == "null" or ticker == "undefined"):
        ticker = None
    if(start == "null" or start == "undefined"):
        start = None
    if(end == "null" or end == "undefined"):
        end = None
    if(interval == "null" or interval == "undefined"):
        interval = None

    try:
        df = yf.download(ticker, start=start, end=end, interval=interval)
        return make_response(df.to_json(orient="table"), 201)
    except Exception:
        return make_custom_error("Invalid input value, check 1. If the ticker name is valid. 2.If there's any valid dataset between the given time range (i.e. not holidays). Contact zhengpei.pz@gmail.com for more support.", 404)



# ticker info request
# accepts a json object of the type {"ticker" : "ticker_name"}
# return a json object that contains query params: 
# ticker, name, currentPrice, previousClose, type, percentageChange
@app.route("/request/ticker_info", methods=["POST"])
@cross_origin()
def get_ticker_info():
    data = request.get_json()
    ticker = yf.Ticker(data["ticker"])

    # test if the ticker symbol is valid
    try: 
        info = ticker.info

        # find the current price
        currentData = ticker.history(interval="1m", period = "1d").iloc[-1]
        currentPrice = currentData["Open"]

        # calculate the percentage change in price from closing to current price
        percentageChange = currentPrice/info["previousClose"] - 1
        
        res = {
            "ticker" : info["symbol"],
            "name" : info["shortName"],
            "currentPrice" : "{:.2f}".format(currentPrice),
            "previousClose" : info["previousClose"],
            "type": info["quoteType"],
            "percentageChange" : "{:.4f}".format(percentageChange),
        }

        return make_response(jsonify(res), 201)
    except Exception:
        return make_custom_error("Invalid input value, check if the ticker name is valid and if there's any valid dataset between the given time range (i.e. not holidays). Contact zhengpei.pz@gmail.com for more support.", 404)

# multiple ticker info request
# accepts a json object of the type {"ticker" : "[ticker_name, ticker_name, ...]"}
# return a json object that contains multiple single ticker info
@app.route("/request/multiple_ticker_info", methods=["POST"])
@cross_origin()
def get_multiple_ticker_info():
    data = request.get_json()
    value = data["ticker"];
    res = {}

    for key in value:
        try: 
            ticker = yf.Ticker(key)
            info = ticker.info

            # find the current price
            currentData = ticker.history(interval="1m", period = "1d").iloc[-1]
            currentPrice = currentData["Open"]

            # calculate the percentage change in price from closing to current price
            percentageChange = currentPrice/info["previousClose"] - 1
            
            infoOrganized = {
                "ticker" : info["symbol"],
                "name" : info["shortName"],
                "currentPrice" : "{:.2f}".format(currentPrice),
                "previousClose" : info["previousClose"],
                "type": info["quoteType"],
                "percentageChange" : "{:.4f}".format(percentageChange),
            }

            res[key] = infoOrganized
        except Exception:
            return make_custom_error("Invalid input value, check if the ticker name is valid and if there's any valid dataset between the given time range (i.e. not holidays). Contact zhengpei.pz@gmail.com for more support.", 404)

    return  make_response(jsonify(res), 201)


# market value request
# accepts a json object of the type {"ticker" : "holding_num", ...}
# return a json object that contains a number representing the market value (in USD, two decimal places)
@app.route("/request/get_market_value", methods=["POST"])
@cross_origin()
def get_market_value():
    data = request.get_json()
    market_value = 0;

    for [ticker, share] in data.items():
        try: 
            # find the current price
            currentData = yf.Ticker(ticker).history(interval="1m", period = "1d").iloc[-1]
            currentPrice = currentData["Open"]

            market_value += share * currentPrice

        except Exception:
            return make_custom_error("Failed to calculate the market value.", 404)
    
    return make_response(jsonify("{:.2f}".format(market_value)), 201)


        

