class User:

    def __init__(
        self,
        user_id: int,
        name: str,
        email: str,
        password_hash: str,
    ):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.password_hash = password_hash