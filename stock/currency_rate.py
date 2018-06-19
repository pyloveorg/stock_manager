import requests
from datetime import datetime, timedelta


def currency(cur):
    date = (datetime.today() - timedelta(1)).strftime("%Y-%m-%d")
    if cur == "pln":
        return 1
    else:
        try:
            resp = requests.get("http://api.nbp.pl/api/exchangerates/rates/a/{}/today/?format=json".format(cur))
            resp_json = resp.json()
            return resp_json["rates"][0]["mid"]
        except Exception:
            resp = requests.get("http://api.nbp.pl/api/exchangerates/rates/a/{}/{}/?format=json".format(cur, date))
            resp_json = resp.json()
            return resp_json["rates"][0]["mid"]
    