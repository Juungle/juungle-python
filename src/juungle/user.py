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
        response = self.call_get_json("/user/details", {}, True)
        j_response = response.json()
        self.user_id = j_response['id']
        self.email = j_response['email']
        self.deposit_address = j_response['depositAddress']
        self.bch_balance = j_response['bchBalance']

    def withdraw_bch(self, to_address):
        data = {
            "toAddress": to_address,
            "password": self.login_pass
        }
        response = self.call_post('user/withdraw_bch', data, True)
        print(response.json()['txid'])
