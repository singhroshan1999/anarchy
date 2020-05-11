from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes,serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.exceptions import InvalidSignature
from base64 import b64encode,b64decode

class host:
    @staticmethod
    def gen_pk(path = None,store=False,password = None):
        pk = ec.generate_private_key(
            ec.SECP256R1(),
            default_backend()
        )
        if store:
            serial = pk.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=(serialization.BestAvailableEncryption(password) if password is not None else serialization.NoEncryption())
            )
            out = open(path,'wb+')
            out.write(serial)
            out.flush()
            out.close()
        return pk
    @staticmethod
    def gen_key_str(key):
        serial = key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        return serial
    @staticmethod
    def gen_key(pk,path = None,store=False):
        key = pk.public_key()
        if store:
            serial = host.gen_key_str(key)
            out = open(path,'wb+')
            out.write(serial)
            out.flush()
            out.close()
        return key
    @staticmethod
    def load_pk(path,password = None):
        inp = open(path,'rb')
        serial = inp.read()
        pk = serialization.load_pem_private_key(
            serial,
            password=password,
            backend=default_backend()
        )
        return pk
    @staticmethod
    def load_key_str(serial):
        return serialization.load_pem_public_key(
            serial,
            backend=default_backend()
        )
    @staticmethod
    def load_key(path):
        inp = open(path,'rb')
        serial = inp.read()
        key = host.load_key_str(serial)
        return key
    @staticmethod
    def sign_str(pk,bstr,hash_function = hashes.SHA3_256()):
        sign = pk.sign(
            bstr,
            ec.ECDSA(hash_function)
        )
        return sign
    @staticmethod
    def verify_str(key,bstr,sign,hash_function = hashes.SHA3_256()):
        try:
            key.verify(
                sign,
                bstr,
                ec.ECDSA(hash_function)
            )
        except InvalidSignature:
            return False
        return True
    @staticmethod
    def b64_str(bstr,encoding = "utf-8"):
        return str(b64encode(bstr),encoding=encoding)


