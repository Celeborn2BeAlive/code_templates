# Examples of authentication to coinbasepro api
# With requests and aiohttp

import asyncio
import json

import aiohttp
from aiohttp import ClientSession

import hmac
import hashlib
import time
import requests
import base64
from requests.auth import AuthBase


def cbpro_auth_headers(secret_key, api_key, passphrase, method, path_url, body):
    timestamp = str(time.time())
    print(method, path_url, body)
    message = timestamp + method + \
        path_url + (body or '')
    message = message.encode('ascii')
    hmac_key = base64.b64decode(secret_key)
    signature = hmac.new(hmac_key, message, hashlib.sha256)
    signature_b64 = base64.b64encode(signature.digest()).decode('utf-8')
    return {
        'CB-ACCESS-SIGN': signature_b64,
        'CB-ACCESS-TIMESTAMP': timestamp,
        'CB-ACCESS-KEY': api_key,
        'CB-ACCESS-PASSPHRASE': passphrase,
        'Content-Type': 'application/json'
    }


class CoinbaseExchangeAuth(AuthBase):
    api_key: str
    secret_key: str
    passphrase: str

    def __init__(self, api_key: str, secret_key: str, passphrase: str):
        self.api_key = api_key
        self.secret_key = secret_key
        self.pass_phrase = passphrase

    def __call__(self, request):
        headers = cbpro_auth_headers(
            self.secret_key, self.api_key, self.pass_phrase,
            request.method, request.path_url, request.body)
        print(headers)
        request.headers.update(headers)
        return request


CBPRO_API_URL = 'https://api.pro.coinbase.com/'


async def main():
    # fill this
    creds = {
        'apiKey': '',
        'apiSecret': '',
        'passPhrase': ''
    }

    cbpro_auth = CoinbaseExchangeAuth(
        creds['apiKey'], creds['apiSecret'], creds['passPhrase'])

    async def products_async():
        endpoint = 'products'
        headers = cbpro_auth_headers(
            cbpro_auth.secret_key, cbpro_auth.api_key, cbpro_auth.pass_phrase,
            'GET', '/' + endpoint, '')
        async with aiohttp.ClientSession() as client:
            async with client.get(CBPRO_API_URL + endpoint, headers=headers) as resp:
                print(await resp.json())

    async def accounts_async():
        endpoint = 'accounts'
        headers = cbpro_auth_headers(
            cbpro_auth.secret_key, cbpro_auth.api_key, cbpro_auth.pass_phrase,
            'GET', '/' + endpoint, '')
        async with aiohttp.ClientSession() as client:
            async with client.get(CBPRO_API_URL + endpoint, headers=headers) as resp:
                print(await resp.json())

    async def order_async():
        endpoint = 'orders'
        params = {
            'size': '0.001',
            'price': '100000',
            'side': 'sell',
            'product_id': 'BTC-EUR'
        }
        data = json.dumps(params)
        headers = cbpro_auth_headers(
            cbpro_auth.secret_key, cbpro_auth.api_key, cbpro_auth.pass_phrase,
            'POST', '/' + endpoint, data)
        async with aiohttp.ClientSession() as client:
            async with client.post(CBPRO_API_URL + endpoint, headers=headers, data=data) as resp:
                print(await resp.json())

    def products_sync():
        endpoint = 'products'
        r = requests.get(CBPRO_API_URL + endpoint,
                         auth=cbpro_auth)
        print(r.json())

    def accounts_sync():
        endpoint = 'accounts'
        r = requests.get(CBPRO_API_URL + endpoint,
                         auth=cbpro_auth)
        print(r.json())

    def order_sync():
        endpoint = 'orders'
        params = {
            'size': '0.001',
            'price': '100000',
            'side': 'sell',
            'product_id': 'BTC-EUR'
        }
        r = requests.post(CBPRO_API_URL + endpoint,
                          auth=cbpro_auth, data=json.dumps(params))
        print(r.json())

    products_sync()
    accounts_sync()
    order_sync()
    await products_async()
    await accounts_async()
    await order_async()

if __name__ == "__main__":
    asyncio.run(main())
