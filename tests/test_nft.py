
from unittest import TestCase

import pytest

from juungle.exception import NoLoginProvided, NoPasswordProvided
from juungle.nft import NFTs


class NFTTest(TestCase):
    """Tests for NFT"""

    def setUp(self):
        self.nft = None

    def test_local_user_missing(self):
        with pytest.raises(NoLoginProvided):
            self.nft = NFTs()

    def test_local_password(self):
        with pytest.raises(NoPasswordProvided):
            self.nft = NFTs('login')
