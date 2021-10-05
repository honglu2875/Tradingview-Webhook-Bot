import requests
import json

class AlpacaHandler():
    def __init__(self, key, secret, paper=False):
        self._key = key
        self._secret = secret

        if paper:
            self._BASE_URL = "https://paper-api.alpaca.markets"
        else:
            self._BASE_URL = "https://api.alpaca.markets"

        self._HEADERS = {'APCA-API-KEY-ID': self._key, 'APCA-API-SECRET-KEY': self._secret}


    def placeOrder(self, data):
        ORDERS_URL = "{}/v2/orders".format(self._BASE_URL)

        order = requests.post(ORDERS_URL, json=data, headers=self._HEADERS)
        return json.loads(order.content)

    def flatten_alpaca(self, symbol):
        POSITIONS_URL = "{}/v2/positions".format(self._BASE_URL)
        ORDERS_URL = "{}/v2/orders".format(self._BASE_URL)

        pos_byte = requests.get(POSITIONS_URL+"/"+symbol, headers=self._HEADERS)
        pos = json.loads(pos_byte.content)

        if "qty" not in pos: return {}

        if pos["side"] == "long":
            SIDE = "short"
        elif pos["side"] == "short":
            SIDE = "long"
        else:
            return {}

        order = request.post(ORDERS_URL, json={"symbol":symbol, "qty": pos["qty"], "side": SIDE, "type": "market", "time_in_force": "gtc"}, headers=self._HEADERS)

        return json.loads(order.content)


    def order_parse(self, data):
        out = dict()
        out["symbol"] = data["symbol"]
        out["qty"] = data["qty"]
        out["side"] = data["side"]
        out["type"] = data["type"]
        out["time_in_force"] = data["time_in_force"]
        return out

    def log(self, data, logger):
        #logger.info('Alert:' + str(data))
        logger.info('Sending order: Symbol ' + data["symbol"] + ' Quantity: ' + data["qty"] + ' Buy/Sell: ' + data["side"] + ' Type: ' + data["type"] + ' Time in force: ' + data["time_in_force"])
        logger.info(' ---- Order Sent\n')
