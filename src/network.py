import uuid
import random
import datetime
from blockchain import BlockChain

"""
block_schema = {
    "transaction_id" : some_id,
    "prev_transaction_ids" : [ some_id, some_id, some_id ],
    "sender_id" : sender_id,
    "receiver_id" : receiver_id,
    "created_by" : block_miner_id,
    "created_at" : date_and_time,
    "coins" : amount_contained, #Will be give to receiver
    "transaction_fee" : transaction_fee, #Will be given to miner
    "incentive" : coins_generated_by_network, #Will be given to miner
}
"""

class Network:
    def __init__(self):
        data = { "transaction_id": str(uuid.uuid4()),
                  "prev_transaction_ids" : (),
                  "sender_id" : "",
                  "receiver_id" : "",
                  "created_by" : "Network",
                  "created_at" : datetime.datetime.now(),
                  "coins" : 0,
                  "transaction_fee" : 0,
                  "incentive" : 0,
                }
        self.blockchain = BlockChain(data, None)
        self.nodes = []

    def add_block(self, block):
        return self.blockchain.add_block(block)

    def add_node(self, node):
        if(str(type(node))=="<class 'miner.Miner'>"):
            self.nodes.append(node)

    def verify_blockchain(self):
        if(self.blockchain.verify_blockchain(self.blockchain) == 1):
            print("Blockchain Valid")
        else:
            print("Blockchain invalid")