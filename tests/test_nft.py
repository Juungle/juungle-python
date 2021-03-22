
from unittest import TestCase

import pytest
from mock import MagicMock, patch

from juungle.exception import NoLoginProvided, NoPasswordProvided
from juungle.nft import NFT, NFTs


class NFTTest(TestCase):
    """Tests for NFT"""

    def setUp(self):

        nft_info = {
            "id": 3,
            "userId": 4123,
            "depositTxid": "2ff07c7bb90396c30cbe51c563a9f572906602cbadde16bd137f63bdf4d98c3c",
            "withdrawTxid": None,
            "purchaseTxid": None,
            "tokenId": "2ff07c7bb90396c30cbe51c563a9f572906602cbadde16bd137f63bdf4d98c3c",
            "tokenName": "Aya Royama",
            "tokenSymbol": "WAIFU",
            "groupTokenId": "a2987562a405648a6c5622ed6c205fca6169faa8afeb96a994b48010bd186a66",
            "priceSatoshis": 333000,
            "ts": "2021-01-26T21:53:08.020Z",
            "purchaseHold": False}

        self.nft = NFT(nft_info, 'username', 'password')

    def test_local_user_missing(self):
        with pytest.raises(NoLoginProvided):
            self.nfts = NFTs()

    def test_local_password(self):
        with pytest.raises(NoPasswordProvided):
            self.nfts = NFTs('login')
