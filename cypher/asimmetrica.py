
# creazione environment, per evitare che ubuntu non vi faccia installare la libreria di crittografia
# python -m venv .venv
# e poi:
# . .venv/bin/activate
# e poi fare pip install pycryptodome
#

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64


# # Per importare una chiave pubblica
# keyDER = base64.b64decode(pubkey)
# seq = base64.asn1.DerSequence()
# seq.decode(keyDER)
# keyPub = RSA.construct((seq[0], seq[1]))

# # Per iniziare generiamo una coppia di chiavi e le stampiamo
# # Generating RSA Key Pair
# # Una volta stampate, non serve più
# key_pair = RSA.generate(2048)
# print(key_pair.export_key())
# public_key = key_pair.publickey()
# print(public_key.export_key())
# exit(0)
# sPriv = "-----BEGIN RSA PRIVATE KEY-----\nMIIEowIBAAKCAQEA3AqNkw+4Pnd0fKkYQRKkr8BDrUDVxD75cHizbkfKE4CnWGEW\nfP7Yi25nBp10qCyOdBfr1LD7DGXJpGJA4L1teUOzbT2ztEZGPuur532z/bQdcIte\nIIipO4fGzsCiSkeXVu+W/rLWHGuHgss2ULxeAx8mzbSc1UqdV4z1wmERprqNLLZZ\nIRAewYkdBIhQ57IvxX+DXeQTPkPPO4jZTmWVcf7/JpmDrDiOWbl/fg/UPNxzxvO3\nC2MA3FEr1ZmvUgqKX1M3XZS6FKvJCvnNQdYxPVRe3Ra6KOdA6vdfCOCoGFH8CjwA\nI9Aquz8AM951Sk3tQp8TGXeQOx2H2vemohmAbQIDAQABAoIBABi3zsOQZoAN5zYB\nwMm+kGV10aRqvhi3gknSJUXkJp0ePK4+6cnMzwKKumQR2AL0TmRYM5PG9cykuowO\nxX75iIywwD0rSz6bDlUPIFZ21ntPemckIMTC1U/sprafCRwTArsvWuTtrgOvSJ+2\nuDlFj8IGA9Pj0CJdqWMmYI0fXl4+LT7QleYdoPON0wOMwKRztv7JiLb0zdgAFKhR\n/hpQAL++6FFnH6izSwvd+TDb8jLk2EE3+9XY/SObm+Fftgm2sef11nuTr8GYDycu\nvsfDFxnWmpn7xvMnalGk3+kchoReUHYxoEBo5Ryj5kK5ZETMeWThNxqvqUuHBq3/\nb4x+PLkCgYEA7HoLoF9QWQOOK9IOHWxLl+R7n1ZJwQBqcPm8sNJoQkH1oL3ResPD\nZM12/DDNg5QtgFoe7mDYJnqr8Nc4lm6fgEtM/yGVJ1nAg6TEJEmSp1C5Ksvu8S1H\nKLdZ/OM51lUGuY7nN+rA7h41KnM8Tc6cGBo2X0kUCJsGmf4NSqLAyj8CgYEA7jUk\nQ4wBmH7xvgho8moSQLhP7BR8UahB8Wcw2LQ/tGwRJ9/LZ9hKMQS/hThbCWoOMHwN\ntKSIYnZ7uqWDZ20YJ0PPv967F93oQS7sf6RBoYmm8QEB62A/BrVqj33kCHb5Bu60\nmfktFroS2DwFSvH3lLX77rkiOfhm+EJhKQXAklMCgYACR8sE6OZldVtRoNzx+7Fe\n7Z0jlDlx2wcrv7zKF71ZpjkwK6RxgqHHvxN+qxnQQwWNT1EtC1IKTPSLhgfNq5Nu\nMUu0yiYeEweAPX6Guw7m/ihK+Vx8hutAwUPk5GwSXQ+Lio1ARMtHgJMSrbnPJkbr\nFJWhpZrD2nrd0U1fguJJEQKBgQDl34qbVKTFkNug02TTauEqa7NU04AVHRZl63sL\n5QYFCrSTkjgsgmE2ZKqd2QChWSNQTqa7SHwE6OoF+GuSh4jje2Eke8B5C8ByBuJb\nWxuq07eyo5JCnqKzyqaGyqogMQ+oTPskC34jjHVbDrDc3hxZ+jSg7y/EWZ6kvQoe\nGFr52QKBgDHKMyQ8W2vccZeFJWKThjrM6fatKRgnit2VEUN7qpxyNoFjrHbt4Mzy\nB6JDQ+cMPJ28FhqR4FcjPbqS5osLWIpZe/QXalnFVEDEjePJe2iySZH6rXaOfhb2\nRulv2YiLx0w1W5L44MfJQ4PSsZuTRVC0lQEcWmsdrov6N7hmUUS3\n-----END RSA PRIVATE KEY-----"
sPriv = ""
# sPub = "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA3AqNkw+4Pnd0fKkYQRKk\nr8BDrUDVxD75cHizbkfKE4CnWGEWfP7Yi25nBp10qCyOdBfr1LD7DGXJpGJA4L1t\neUOzbT2ztEZGPuur532z/bQdcIteIIipO4fGzsCiSkeXVu+W/rLWHGuHgss2ULxe\nAx8mzbSc1UqdV4z1wmERprqNLLZZIRAewYkdBIhQ57IvxX+DXeQTPkPPO4jZTmWV\ncf7/JpmDrDiOWbl/fg/UPNxzxvO3C2MA3FEr1ZmvUgqKX1M3XZS6FKvJCvnNQdYx\nPVRe3Ra6KOdA6vdfCOCoGFH8CjwAI9Aquz8AM951Sk3tQp8TGXeQOx2H2vemohmA\nbQIDAQAB\n-----END PUBLIC KEY-----"
sPub = ""
# Ora dobbiamo ricreare le chiavi a partire da queste due stringhe
key_pair = RSA.import_key(sPriv)
public_key = RSA.import_key(sPub)


# Function to encrypt message
def encrypt_message(message, pub_key):
    cipher = PKCS1_OAEP.new(pub_key)
    encrypted_message = cipher.encrypt(message.encode("utf-8"))
    return base64.b64encode(encrypted_message).decode("utf-8")


# Function to decrypt message
def decrypt_message(encrypted_message, priv_key):
    cipher = PKCS1_OAEP.new(priv_key)
    decrypted_message = cipher.decrypt(base64.b64decode(encrypted_message))
    return decrypted_message.decode("utf-8")


# Example usage
message = "This is a secret message"
encrypted_message = encrypt_message(message, public_key)
decrypted_message = decrypt_message(encrypted_message, key_pair)

print("Original Message:", message)
print("Encrypted Message:", encrypted_message)
print("Decrypted Message:", decrypted_message)
