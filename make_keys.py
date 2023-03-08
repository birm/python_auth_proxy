from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization


def make_keys(privateFn, publicFn):
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    unencrypted_pem_private_key = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )
    pem_public_key = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    private_key_file = open(privateFn, "w")
    private_key_file.write(unencrypted_pem_private_key.decode())
    private_key_file.close()
    public_key_file = open(publicFn, "w")
    public_key_file.write(pem_public_key.decode())
    public_key_file.close()
