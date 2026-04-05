import hashlib
import ecdsa
import base58
from Crypto.Hash import RIPEMD

class BabyWallet:
    def __init__(self):
        self.sk = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
        self.vk = self.sk.verifying_key
        self.private_key = self.sk.to_string().hex() # convert to human readable string
        self.public_key = b"\x04" + self.vk.to_string() # raw bytes
        self.address = self.generate_address()
  
    def generate_address(self):
        sha = hashlib.sha256(self.public_key).digest()
        # extra hash for shorter address
        ripemd = RIPEMD.new(sha).digest()
        prefixed = b"\x00" + ripemd
        # to verify and prevent data corruption (that it is a valid address)
        checksum = hashlib.sha256(hashlib.sha256(prefixed).digest()).digest()[:4]
        return base58.b58encode(prefixed + checksum).decode()
  
    def sign_transaction(self, message: str):
        return self.sk.sign(message.encode()).hex()
  
    def verify_transaction(self, message: str, signature: str):
        return self.vk.verify(bytes.fromhex(signature), message.encode())

# wallet = BabyWallet()
# print("Private Key:", wallet.private_key)
# print("Public Key:", wallet.public_key)
# print("Address:", wallet.address)

# msg = "Send 10 coins to Alice"
# sig = wallet.sign_transaction(msg)
# print("Signature:", sig)
# print("Verify:", wallet.verify_transaction(msg, sig))
