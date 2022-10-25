from passlib.context import CryptContext

hasher = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hasher():

    @staticmethod
    def hash_password(plain_passwd):
        return hasher.hash(plain_passwd)

    @staticmethod
    def verify_password(plain_passwd, hashed_passwd):
        return hasher.verify(plain_passwd, hashed_passwd)