import hashlib
import json
from time import time

class BabyChain:
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        # The Genesis block (first block)
        self.new_block()
        
    def new_block(self, proof=None, previous_hash=None):
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
    
    @staticmethod
    def hash(block):
        # Order is important so that the correct hash is created
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

# Initialise chain    
myChain = BabyChain()

# Add transactions
myChain.pending_transactions.append({"sender": "Satoshi Nakamoto", "recipient": "Hal Finney", "amount": 50})
myChain.pending_transactions.append({"sender": "Adam Back", "recipient": "Satoshi Nakamoto", "amount": 10})

# Fake block (TODO: adding a proof of work algorithm for block validation)
myChain.new_block(proof=12345)

# Print the chain to see our work
print(json.dumps(myChain.chain, indent=4))
