from passlib.context import CryptContext
pwd_cxt = CryptContext(schemes=["bcrypt","scrypt"], deprecated="auto")
import cryptography
from cryptography.fernet import Fernet
# class Hash():
#     def bcrypt(password: str):
#         return pwd_cxt.hash(password)

     # def verify(hashed_password,plain_password):
        # return pwd_cxt.verify(plain_password,hashed_password)import base64



class Hash():

    def encrypt(password):
        key = Fernet.generate_key()
        fernate= Fernet(key)
        encryptor = fernate.encrypt(password.encode())
        # pa= password.encode()
        # encryptor= base64.a85encode(pa)
        return encryptor



