import hashlib
import uuid

def encrypt_password(password, salt = uuid.uuid4().hex):
    alg = "sha512"

    m = hashlib.new(alg)
    m.update(salt + password)
    password_hash = m.hexdigest()

    encrypted = "$".join([alg, salt, password_hash])

    return encrypted
