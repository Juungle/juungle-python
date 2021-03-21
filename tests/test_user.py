
from unittest import TestCase

import pytest

from juungle.exception import NoLoginProvided, NoPasswordProvided
from juungle.user import User


class UserTest(TestCase):
    """Tests for User"""

    def setUp(self):
        self.user = None

    def test_local_user_missing(self):
        with pytest.raises(NoLoginProvided):
            self.user = User()

    def test_local_password(self):
        with pytest.raises(NoPasswordProvided):
            self.user = User('login')
