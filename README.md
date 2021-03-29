[![Python application](https://github.com/Juungle/juungle-python/actions/workflows/run_tests.yml/badge.svg)](https://github.com/Juungle/juungle-python/actions/workflows/run_tests.yml)
## NOTE: ALTHOUGH THIS PROJECT WORKS, IT IS STILL UNDER HEAVY DEVELOPMENT AND THINGS WILL CHANGE BEFORE v1.0


## juungle-python
Python package to access Juungle.net API

## Installation
`$ python -m pip install juungle`

## Running from source
```
$ git clone https://github.com/Juungle/juungle-python.git juungle
$ cd juungle
$ python -m pip -r requirements.txt
```
## User credentials for Juungle.net
### Using a config file
Create a file `user-config.ini` with juungle.net credentials
in the same directory of your code:
```
LOGIN_USERNAME="username@email"
LOGIN_PASSWORD="password"
```
### OR While creaing the object
Inside the code

```python
from juungle.nfts import NFTs

nfts = NFTs('username@email', 'password')
```
## Usage
### List all WAIFUs nfts that are being sale for 0.01 BCH or less
```python
from juungle.nft import NFTs

nfts = NFTs()

nfts.available_to_buy = True
nfts.purchased = False
nfts.token_group = 'WAIFU'

nfts.get_nfts()

for nft in nfts.list_nfts:
    if nft.price_bch <= 0.01:
        print(nft.token_name)
```

### List all my NFTs

```python
from juungle.nft import NFTS

nfts = NFTs()
nfts.get_my_nfts()

for nft in nfts.list_nfts:
    print(nft.token_name)
```

### List all my NFTs prices in USD and EUR
**To query prices we going to use coingecko api**

`pip install pycoingecko`

```python
from juungle.nft import NFTS
from pycoingecko import CoinGeckoAPI

nfts = NFTs()
nfts.get_my_nfts()

# Query price
cg = CoinGeckoAPI()

bch_price = cg.get_price(ids='bitcoin-cash',
            vs_currencies=['usd', 'eur'])['bitcoin-cash']

msg = "NFT: {} with price {} USD or {} EUR"

for nft in nfts.list_nfts:
    print(msg.format(nft.token_name, bch_price['usd'], bch_price['eur'])
```

## Tokens Group IDs
Because tokens/group name are not unique we have to use the HEX id that can be
found at the [simpleledger.info](https://simpleledger.info).

Juungle-python package provides a list of IDs just to make easier of the most
common toekns:

Token Name | Token ID
---------- | --------
WAIFU | [a2987562a405648a6c5622ed6c205fca6169faa8afeb96a994b48010bd186a66](https://simpleledger.info/token/a2987562a405648a6c5622ed6c205fca6169faa8afeb96a994b48010bd186a66)
