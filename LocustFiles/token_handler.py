class TokenHandler:
    access_token = None
    refresh_token = None
    userId = None

    @classmethod
    def set_tokens(cls, access_token, refresh_token, userId=None):
        cls.access_token = access_token
        cls.refresh_token = refresh_token
        cls.userId = userId

    @classmethod
    def get_access_token(cls):
        return cls.access_token

    @classmethod
    def get_refresh_token(cls):
        return cls.refresh_token

    @classmethod
    def get_user_id(cls):
        return cls.userId
