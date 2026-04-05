import hashlib
import json
import ecdsa
from time import time
from wallet import BabyWallet


class BabyChain:
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        # The Genesis block (first block)
        self.new_block(previous_hash="The Beginning", proof="first proof")
        
    def new_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.pending_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        self.pending_transactions = [] # Reset transactions
        self.chain.append(block)
        return block

    def validate_proof(self, proof):
        block_string = json.dumps(self.hash(self.chain[-1]), sort_keys=True)
        # Append the input to the previous block
        proof_string = f"{block_string}{proof}".encode()
        hash_string = hashlib.sha256(proof_string).hexdigest()
        ### Hashes starting with "000" are accepted (16^3 odds)
        return hash_string[0:3] == "000"
    
    def validate_chain(self):
        # The first block is always valid in this algorithm
        if len(self.chain) < 2:
            return True
        
        # Skip the first block as there is no previous block to append
        for i, block in enumerate(self.chain[1:]):
            # i is actually the previous index (compared to the block) as we skipped the first
            block_string = json.dumps(self.hash(self.chain[i]), sort_keys=True)
            proof_string = f"{block_string}{block['proof']}".encode()
            hash_string = hashlib.sha256(proof_string).hexdigest()
            print(hash_string)
            if hash_string[0:3] != "000":
                return False
            
        return True
    
    # sender and recipient arguments are wallets
    def create_transaction(self, sender, recipient, amount):
        tx = {
            "sender": sender.address,
            "recipient": recipient,
            "amount": amount
        }
        message = json.dumps(tx, sort_keys=True)
        signature = sender.sign_transaction(message)
        
        # Can now complete the other fields of tx
        tx["signature"] = signature
        tx["public_key"] = sender.public_key.hex()
        return tx
    
    # TODO: Implement and test this function
    @staticmethod
    def verify_transaction(tx):
        # convert back to bytes as it was converted to hex in create_transaction()
        public_key = bytes.fromhex(tx["public_key"])
        # Create corresponding verifying key from public key
        vk = ecdsa.VerifyingKey.from_string(public_key[1:], curve=ecdsa.SECP256k1)
        
        message = json.dumps({
            "sender": tx["sender"],
            "recipient": tx["recipient"],
            "amount": tx["amount"]
        }, sort_keys=True)
        
        try:
            return vk.verify(bytes.fromhex(tx["signature"]), message.encode())
        except:
            return False
            
    @staticmethod
    def hash(block):
        # Order is important so that the correct hash is created
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()


# Initialise chain    
myChain = BabyChain()

# Initialise wallets for users
satoshi = BabyWallet()
hal = BabyWallet()
adam = BabyWallet()

for i in range(10000):
    if i % 2000 == 0:
        if i % 4000 == 0:
            myChain.pending_transactions.append(myChain.create_transaction(satoshi, hal.address, 50))
        else:
            myChain.pending_transactions.append(myChain.create_transaction(adam, satoshi.address, 10))
            
    if myChain.validate_proof(proof=i):
        myChain.new_block(proof=i)
        print(myChain.validate_chain())

# Print the chain to see our work
print(json.dumps(myChain.chain, indent=4))
