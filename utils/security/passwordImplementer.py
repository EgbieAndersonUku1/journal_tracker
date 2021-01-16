from flask_bcrypt import check_password_hash, generate_password_hash


class PasswordImplementer(object):

    @classmethod
    def hash_password(cls, password: str) -> str:
        """hash_password(str: password) -> str:

           Takes a plain text password and turns that password
           into a hash string that cannot be decrypted.

           :parameter
                :password: A plain text password that will turned into a hash
           :usage:
                PasswordImplementer.hash_password(password)
        """
        return generate_password_hash(password)

    @classmethod
    def is_password_valid(cls, hash_password: str, password: str) -> bool:
        """is_password_valid(str hash_password, str password) -> bool

           Takes a hash password and plaintext password and confirms
           if the password is a match. Returns true if it is valid or False
           otherwise

           :parameter
                :hash_password: A hash string
                :password: A plaintext string

            :usage:
                PasswordImplementer.is_password_valid(hash_password. password)
        """
        return check_password_hash(hash_password, password)
