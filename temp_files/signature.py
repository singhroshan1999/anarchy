from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature
def gen_keys():
    private = rsa.generate_private_key(
        public_exponent= 65537,
        key_size=1024,
        backend=default_backend()
    )
    public = private.public_key()
    return private, public

def sign(message,private):
    sig = private.sign(
        message.encode(),
        padding.PSS(mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                    ),
        hashes.SHA256()
    )
    return sig

def verify(message,sig,public):
    try:
        public.verify(
            sig,
            message.encode(),
            padding.PSS(mgf=padding.MGF1(hashes.SHA256()),
                        salt_length=padding.PSS.MAX_LENGTH
                        ),
            hashes.SHA256()
        )
    except InvalidSignature:
        return False
    return True

if __name__ == "__main__":
    pv,pu = gen_keys()
    message = "fdfgdfgfg"
    sig = sign(message,pv)
    ver = verify(message,sig,pu)
    print(sig.hex())
    if ver:
        print("Verified")
    else:
        print("Not verified")
