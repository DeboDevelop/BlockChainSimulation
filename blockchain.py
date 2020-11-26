import uuid
import random
import datetime

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
                { "transaction_id": str(uuid.uuid4()),
                  "prev_transaction_ids" : [],
                  "sender_id" : "",
                  "receiver_id" : "",
                  "created_by" : "Network",
                  "created_at" : datetime.datetime.now(),
                  "coins" : 0,
                  "transaction_fee" : 0,
                  "incentive" : 0,
                  "payment_received" : True,
                },
            ],
        ]
        self.nodes = []

    def add_block(self, block):
        # Checking if the block exist in the blockchain or not.
        for block_list in self.blockchain:
            for existing_block in block_list:
                if existing_block["transaction_id"] == block["transaction_id"]:
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
                        self.blockchain[j+1].append(block)

        for i in range(self.nodes):
            if self.nodes[i]["miner_id"] == block["created_by"]:
                self.nodes[i].receive_incentive(block, self)
                break

    def add_node(self, node):
        self.nodes.append(node)

    def verify_blockchain(self):
        current = 1
        while(current < len(self.blockchain)):
            prev = self.blockchain[current-1]
            curr = self.blockchain[current]
            l = len(prev) if len(prev) < len(curr) else len(curr)
            i = 0
            while (i<l):
                if(prev[i]["transaction_id"] != curr[i]["prev_transaction_ids"][-1]):
                    print("Blockchain not valid")
                    return
                i+=1
            current+=1
        print("Blockchain Valid")

    def print_blockchain(self):
        for block in self.blockchain:
            print(" ")
            print(block)
            print(" ")

"""
block_schema = {
    "transaction_id" : some_id,
    "prev_transaction_ids" : [ some_id, some_id, some_id ],
    "sender_id" : sender_id,
    "receiver_id" : receiver_id,
    "coins" : amount_contained, #Will be give to receiver
    "transaction_fee" : transaction_fee, #Will be given to miner
    "incentive" : coins_generated_by_network, #Will be given to miner
    "work_needed" : amount_of_word # proof of concept
}
"""

class Miner:
    miner_id = ""
    blockchain = []
    nodes = []
    mempool = []
    wallet = 0

    def __init__(self, network):
        self.miner_id = str(uuid.uuid4())
        self.blockchain = network.blockchain
        self.nodes = network.nodes
        self.mempool = []
        self.wallet = 0

    def add_node(self, node):
        self.nodes.append(node)

    def create_transaction(self, coins, receiver, transaction_fee):
        prev_transaction_ids = self.blockchain[-1][0]["prev_transaction_ids"]
        prev_transaction_ids.append(self.blockchain[-1][0]["transaction_id"])
        random.seed(coins)
        block = {
            "transaction_id" : str(uuid.uuid4()),
            "prev_transaction_ids" : prev_transaction_ids,
            "sender_id" : self.miner_id,
            "receiver_id" : receiver,
            "coins" : coins,
            "transaction_fee" : transaction_fee,
            "incentive" : random.random()*100, 
            "work_needed" : random.random()*100 
        }
        self.mempool.append(block)
        self.request_block(block)

    def request_block(self, block):
        for i in range(self.nodes):
            self.nodes[i].receive_transaction(block)

    def receive_transaction(self, block):
        self.mempool.append(block)

    def add_block_to_network(self, block, network):
        new_block =  {
            "transaction_id" : block["transaction_id"],
            "prev_transaction_ids" : block["prev_transaction_ids"],
            "sender_id" : block["sender_id"],
            "receiver_id" : block["receiver_id"],
            "created_by" : self.miner_id,
            "created_at" : datetime.datetime.now(),
            "coins" : block["coins"], 
            "transaction_fee" : block["transaction_fee"], 
            "incentive" : block["incentive"],
            "payment_received" : False, 
        }
        network.add_block(new_block)

    def receive_incentive(self, block):
        wallet += block["transaction_fee"] + block["incentive"]
        broadcast(block)
        
    def broadcast(self, block):
        for i in range(self.nodes):
            self.nodes[i].receive_block(block)

    def receive_block(self, block):
        pass
        #Complicated Stuff

    def request_blockchain(self):
        pass

    def receive_coins(self):
        for block_list in self.blockchain:
            if block_list[0]["receiver_id"] == self.miner_id:
                if block_list[0]["payment_received"] == False:
                    wallet += block_list[0]["coins"]
                    block_list[0]["payment_received"] == True

    def work(self):
        pass