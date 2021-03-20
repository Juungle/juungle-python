from juungle.auth import Auth


class User(Auth):
    def __init__(self):
        Auth.__init__(self)
        self.user_id = None
        self.email = None
        self.deposit_address = None
        self.bch_balance = None

        self._load_user()

    def _load_user(self):

        response = self.call_get_json(
            "/user/details",
            {"X-Access-Token": self.token}
        )
        if response.status_code == 200:
            j_response = response.json()
            self.user_id = j_response['id']
            self.email = j_response['email']
            self.deposit_address = j_response['depositAddress']
            self.bch_balance = j_response['bchBalance']
        else:
            raise BaseException('Login fail!')
