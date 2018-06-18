import requests


def currency(cur):
    if cur == "pln":
        return 1
    else:
        resp = requests.get("http://api.nbp.pl/api/exchangerates/rates/a/{}/today/?format=json".format(cur))
        resp_json = resp.json()
        return resp_json["rates"][0]["mid"]

