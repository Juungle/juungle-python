# from unittest import TestCase

# from mock import MagicMock, patch

# from juungle.auth import URL_API, Auth
# from juungle.nft import NFT
# from juungle.user import User


# class AuthGetTest(TestCase):
#     @patch("juungle.auth.Auth.__init__")
#     def setUp(self, auth_mock):
#         auth_mock.return_value = None
#         self.auth = Auth()
#         self.auth.login_user = 'username'
#         self.auth.login_pass = 'pass'


#     def test_call_post(self):
#         with patch('requests.get') as mock_post:
#             response = MagicMock()
#             response.status_code = 200
#             response.content = {'success': True}
#             mock_post.return_value = response

#             assert self.auth.call_post(
#                 'endpoint', {},
#                 headers={'Content-Type': 'application/json'}).content == \
#                 {'success': True}

#             mock_post.assert_called_once()
#             mock_post.assert_called_with(
#                 URL_API + '/endpoint', json={},
#                 headers={'Content-Type': 'application/json'})
