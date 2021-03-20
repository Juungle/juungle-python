from juungle.auth import Auth
from juungle.tokens import TOKENS_IDS
from juungle.user import User


class NFTs(Auth):
    def __init__(self):
        Auth.__init__(self)
        self.clear()

    def add_nft(self, nft_info):
        self.list_nfts.append(NFT(nft_info))

    def get_nfts(self):
        response = self.call_get_query('/nfts', self._search_options)
        l_nfts = response.json()
        for nft in l_nfts['nfts']:
            self.add_nft(nft)

    def clear(self):
        self.list_nfts = list()
        self._search_options = {
            'offset': 0,
            'limit': 10000
        }

    @property
    def token_group(self):
        return self._search_options['groupTokenId']

    @token_group.setter
    def token_group(self, value):
        self._search_options['groupTokenId'] = TOKENS_IDS[value] \
            if value in TOKENS_IDS else value

    @property
    def offset(self):
        return self._search_options['offset']

    @offset.setter
    def offset(self, value):
        self._search_options['offsite'] = value

    @property
    def limit(self):
        return self._search_options['limit']

    @limit.setter
    def limit(self, value):
        # limit has to be less than 10 000
        if value < 10000:
            self._search_options['limit'] = value

    @property
    def purchased(self):
        if 'purchaseTxidSet' in self._search_options:
            return self._search_options['purchaseTxidSet']

    @purchased.setter
    def purchased(self, value):
        if isinstance(value, bool):
            self._search_options['purchaseTxidSet'] = str(value).lower()
        else:
            raise ValueError('Purchased must be True or False')

    @property
    def deposited(self):
        if 'depositTxidSet' in self._search_options:
            return self._search_options['depositTxidSet']

    @deposited.setter
    def deposited(self, value):
        if isinstance(value, bool):
            self._search_options['depositTxidSet'] = str(value).lower()
        else:
            raise ValueError('Deposited must be True or False')

    @property
    def available_to_buy(self):
        if 'priceSatoshisSet' in self._search_options:
            return self._search_options['priceSatoshisSet']

    @available_to_buy.setter
    def available_to_buy(self, value):
        if isinstance(value, bool):
            self._search_options['priceSatoshisSet'] = str(value).lower()
            self._search_options['depositTxidSet'] = str(value).lower()
            self._search_options['withdrawTxid'] = str(not value).lower()
            self._search_options['purchaseTxid'] = str(not value).lower()
        else:
            raise ValueError('Available to buy must be True or False')

    def get_my_nfts(self):
        self.clear()
        user = User()
        self._search_options['userId'] = user.user_id
        # Wait a little bit before trying to query again
        self.get_nfts()


class NFT(Auth):
    def __init__(self, nft_info):
        self.nft_id = nft_info["id"]
        self.user_d = nft_info["userId"]
        self.deposit_txid = nft_info["depositTxid"]
        self.withdraw_txid = nft_info["withdrawTxid"]
        self.purchase_txid = nft_info["purchaseTxid"]
        self.token_id = nft_info["tokenId"]
        self.token_name = nft_info["tokenName"]
        self.token_symbol = nft_info["tokenSymbol"]
        self.group_tokenid = nft_info["groupTokenId"]
        self.price_satoshis = nft_info["priceSatoshis"]
        if nft_info["priceSatoshis"]:
            self.price_bch = nft_info["priceSatoshis"] / 100000000
        self.ts = nft_info["ts"]
        self.purchase_hold = nft_info["purchaseHold"]
        self.buy_price = None
        self.buy_address = None
        Auth.__init__(self)

    @property
    def name(self):
        return self.token_name

    @property
    def is_purchased(self):
        return bool(self.purchase_txid)

    def _convert_bch_to_sats(self, bch):
        return bch * 100000000

    @property
    def is_for_sale(self):
        if self.price_satoshis and self.deposit_txid and \
                not self.withdraw_txid and not self.purchase_txid:
            return True
        else:
            False

    def buy(self, to_address):
        if not to_address:
            raise ValueError('BCH Address must be inform!')

        data = {
            "nftId": self.nft_id,
            "address": to_address
        }

        response = self.call_post('nfts/create_purchase_hold', data,
                                  True).json()

        self.buy_price = response['priceSatoshis']
        self.buy_address = response['address']

    def set_price(self, sats=None, bch=None):

        if not sats and not bch:
            raise ValueError('Value must be set as satoshis or BCH')

        price = sats
        if bch:
            price = self._convert_bch_to_sats(bch)

        data = {
            "nftId": self.nft_id,
            "priceSatoshis": price
        }

        self.call_post('user/nfts/set_price', data, True)

    def cancel_sale(self):
        data = {
            "nftId": self.nft_id,
        }

        self.call_post('user/nfts/cancel_sale', data, True)
