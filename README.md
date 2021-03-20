## juungle-python
Python package to access Juungle.net API

## Requirements

`$ python -m pip -r requirements.txt`

## User credentials for Juungle.net
Create a file `user-config.ini`:
```
LOGIN_USERNAME="username"
LOGIN_PASSWORD="password"
```

## Usage
List all WAIFUs nfts that are being sale for 0.01 BCH or less
```python
from juungle.nfts import NFTs

nfts = NFTs()

nfts.available_to_buy = True
nfts.purchased = False
nfts.token_group = 'WAIFU'

nfts.get_nfts()

for nft in nfts.list_nfts:
    if nft.price_bch <= 0.01:
        print(nft.token_name)
```

## Tokens Group IDs
Because tokens/group name are not unique we have to use the HEX id that can be
found at the [simpleledger.info](https://simpleledger.info).

Juungle-python package provides a list of IDs just to make easier of the most
common toekns:

Token Name | Token ID
---------- | --------
WAIFU | [a2987562a405648a6c5622ed6c205fca6169faa8afeb96a994b48010bd186a66](https://simpleledger.info/token/a2987562a405648a6c5622ed6c205fca6169faa8afeb96a994b48010bd186a66)
