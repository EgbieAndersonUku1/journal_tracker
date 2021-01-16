from dataclasses import dataclass, field
from itsdangerous import URLSafeTimedSerializer


@dataclass
class EmailTokenGenerator(object):
    """EmailTokenGenerator is a class that generates and verifies a token that is
       send along in a confirmation email link in order to verify the user's
       email address.
    """
    email: str
    key: str

    confirm_serializer: "URLSafeTimedSerializer" = field(init=False, default=None)
    salt: str = field(default=None)

    def __post_init__(self):
        EmailTokenGenerator.confirm_serializer = URLSafeTimedSerializer(self.key)

    def gen_confirmation_email_token(self) -> str:
        """Generates a token that will be send along in an email confirmation link. This
           token will be used to verify the user email address
        """
        return EmailTokenGenerator.confirm_serializer.dumps(self.email, salt=self.salt)

    def validate_confirmation_token(self, token: str, max_age: int) -> bool:
        """validate_confirmation_token(token: str, max_age: int) -> confirm_serializer object

            Takes a token (str) and a max_age (int) and uses it to confirm a given token. If the token
            is less or equal to the max age of the token then a True value is returned otherwise False

            :parameter
                max_age: int: The max age for the token.
                token: str: The token to validate

        """
        return EmailTokenGenerator.confirm_serializer.loads(token, salt=self.salt, max_age=max_age)




