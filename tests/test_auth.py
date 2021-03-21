
from unittest import TestCase

import pytest

from juungle.auth import Auth
from juungle.exception import NoLoginProvided, NoPasswordProvided


class AuthTest(TestCase):
    """Tests for Auth"""

    def test_no_login_password_provided(self):
        with pytest.raises(NoLoginProvided):
            Auth(None, None)

    def test_no_login_provided(self):
        with pytest.raises(NoLoginProvided):
            Auth(None, 'Password')

    def test_no_password_provided(self):
        with pytest.raises(NoPasswordProvided):
            Auth('user@email')
