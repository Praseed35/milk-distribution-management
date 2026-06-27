from app.exceptions.base import BusinessException

class UserAlreadyExistsError(Exception):

    def __init__(self):

        super().__init__(
            "Username already exists."
        )


class InvalidCredentialsError(Exception):

    def __init__(self):

        super().__init__(
            "Invalid username or password."
        )