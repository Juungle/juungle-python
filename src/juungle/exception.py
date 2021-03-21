class NoLoginProvided(Exception):
    pass


class NoPasswordProvided(Exception):
    pass


class LoginFailed(Exception):
    pass


class CommandFailed(Exception):
    pass


class FailedRequest(Exception):
    pass


class TooManyRequests(Exception):
    pass
