from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["md5_crypt"], deprecated="auto")

class CryptUtil:

    def hash_password(password):
        return pwd_context.hash(password)

    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)