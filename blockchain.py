import uuid

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
    "payment_received" : boolean_value, #The receiver received the payment or not
}
"""

class Network:
    blockchain = []
    nodes = []
    def __init__(self):
        self.blockchain = [
            [
                { "transaction_id": str(uuid.uuid4()), },
            ],
        ]
        self.nodes = []

    def add_block(self, block):
        # Checking if the block exist in the blockchain or not.
        for block_list in self.blockchain:
            for existing_block in block_list:
                if existing_block["transaction_id"] == block["transaction_id"]:
                    drop_block(self, block)
                    return

        # Finding the Right place to push the block
        for j in range(len(self.blockchain)):
            for i in range(len(self.blockchain[j])):
                if block_list[i]["transaction_id"] == block["prev_transaction_ids"][-1]:
                    #If it is a new block
                    if(i == (len(block_list)-1)):
                        self.blockchain.append([block])
                    #If it is a new branch coming from old block
                    else:
                        self.blockchain[j].append(block)

        for i in range(self.nodes):
            if self.nodes[i]["id"] == block["created_by"]:
                self.nodes[i].receive_incentive()
                break

    #Maybe removed later
    def drop_block(self, block):
        for i in range(self.nodes):
            self.nodes[i].drop_block(block)

    def add_node(self, node):
        self.nodes.append(node)

    def verify_blockchain(self):
        pass

    def print_blockchain(self):
        pass
