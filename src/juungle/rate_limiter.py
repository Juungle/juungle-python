
class Limiter:
    def __init__(self, headers):
        self.rate_limit_remaining = int(headers['RateLimit-Remaining'])
        self.rate_limit_reset = int(headers['RateLimit-Reset'])

    def update(self, headers):
        self.rate_limit_remaining = int(headers['RateLimit-Remaining'])
        self.rate_limit_reset = int(headers['RateLimit-Reset'])
