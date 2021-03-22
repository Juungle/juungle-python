
from unittest import TestCase

import pytest
from mock import MagicMock, patch

from juungle.auth import URL_API, Auth
from juungle.exception import CommandFailed, FailedRequest, TooManyRequests
from juungle.nft import NFT
from juungle.user import User


class AuthPostTest(TestCase):
    def setUp(self):
        self.auth = Auth('username', 'pass')

    def test_login_fail(self):
        with patch('requests.post') as mock_post:
            response = MagicMock()
            response.status_code = 200
            response.json.return_value = {'success': False}
            mock_post.return_value = response
            with pytest.raises(CommandFailed):
                self.auth.call_post('url', {})

    def test_fail_request(self):
        with patch('requests.post') as mock_post:
            response = MagicMock()
            response.status_code = 201
            with pytest.raises(FailedRequest):
                self.auth.call_post('url', {})

    def test_too_many_request(self):
        with patch('requests.post') as mock_post:
            response = MagicMock()
            response.status_code = 429
            mock_post.return_value = response
            with pytest.raises(TooManyRequests):
                self.auth.call_post('url', {})

    def test_call_post(self):
        with patch('requests.post') as mock_post:
            response = MagicMock()
            response.status_code = 200
            response.content = {'success': True}
            mock_post.return_value = response

            assert self.auth.call_post(
                'endpoint', {},
                headers={'Content-Type': 'application/json'}).content == \
                {'success': True}

            mock_post.assert_called_once()
            mock_post.assert_called_with(
                URL_API + '/endpoint', json={},
                headers={'Content-Type': 'application/json'})

    def test_call_post_token(self):
        with patch('requests.post') as mock_post:
            response = MagicMock()
            response.status_code = 200
            response.content = {'success': True}
            mock_post.return_value = response

            self.auth._get_token()
            mock_post.assert_called_with(URL_API + '/user/login',
                                         json={'email': 'username',
                                               'password': 'pass'},
                                         headers={'Content-Type':
                                                  'application/json'})


class NFTPostTest(TestCase):
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

        self.nft = NFT(nft_info, 'username', 'pass')

    def test_buy_nft(self):
        """test_by_nft"""
        with patch('requests.post') as mock_post:
            response = MagicMock()
            response.status_code = 200
            response.json.side_effect = [
                {'success': True, 'jwtToken': 'Token123'},
                {'success': True, 'jwtToken': 'Token123'},
                {
                    "success": True,
                    "address": "bitcoincash:qqgw27en0rtv2a56",
                    "priceSatoshis": 4400000
                }
            ]
            mock_post.return_value = response

            self.nft.buy('bchaddress')

            url = URL_API + '/nfts/create_purchase_hold'
            mock_post.assert_called_with(url,
                                         json={
                                             'nftId': 3,
                                             'address': 'bchaddress'
                                         },
                                         headers={'Content-Type':
                                                  'application/json',
                                                  'X-Access-Token':
                                                  'Token123'})
            assert self.nft.buy_price == 4400000
            assert self.nft.buy_address == 'bitcoincash:qqgw27en0rtv2a56'

    def test_set_price(self):
        """test_set_price"""
        with patch('requests.post') as mock_post:
            response = MagicMock()
            response.status_code = 200
            response.json.side_effect = [
                {'success': True, 'jwtToken': 'Token123'},
                {'success': True, 'jwtToken': 'Token123'},
            ]
            mock_post.return_value = response

            self.nft.set_price(bch=0.01)

            url = URL_API + '/user/nfts/set_price'
            mock_post.assert_called_with(url,
                                         json={
                                             'nftId': 3,
                                             'priceSatoshis': 1000000
                                         },
                                         headers={'Content-Type':
                                                  'application/json',
                                                  'X-Access-Token':
                                                  'Token123'})

    def test_cancel_sale(self):
        with patch('requests.post') as mock_post:
            response = MagicMock()
            response.status_code = 200
            response.json.side_effect = [
                {'success': True, 'jwtToken': 'Token123'},
                {'success': True, 'jwtToken': 'Token123'},
                {
                    "success": True,
                    "address": "bitcoincash:qqgw27en0rtv2a56n2swz8j5yhmv36sme55xsyekpm",
                    "priceSatoshis": 4400000}
            ]
            mock_post.return_value = response

            self.nft.cancel_sale()

            url = URL_API + '/user/nfts/cancel_sale'
            mock_post.assert_called_with(url,
                                         json={'nftId': 3},
                                         headers={'Content-Type':
                                                  'application/json',
                                                  'X-Access-Token':
                                                  'Token123'})


class UserPostTest(TestCase):
    @patch("juungle.auth.Auth.__init__")
    @patch("juungle.user.User.__init__")
    def setUp(self, user_mock, auth_mock):
        auth_mock.return_value = None
        user_mock.return_value = None

        self.user = User()
        self.user.login_user = 'username'
        self.user.login_pass = 'pass'
        self.user._get_token = MagicMock(return_value="Token123")
        self.user._limiter = None

    def test_withdraw_bch(self):
        with patch('requests.post') as mock_post:
            response = MagicMock()
            response.status_code = 200
            response.content = {'success': True}
            response.json.return_value = {
                "success": True,
                "txid": "66a2987562a405648a6c5622ed6c205fca6169faa8afeb96a994b48010bd186a"}

            mock_post.return_value = response

            self.user.withdraw_bch('bchaddress')

            url = URL_API + '/user/withdraw_bch'
            mock_post.assert_called_with(
                url,
                json={'toAddress': 'bchaddress', 'password': 'pass'},
                headers={'Content-Type':
                         'application/json',
                         'X-Access-Token':
                         'Token123'})
