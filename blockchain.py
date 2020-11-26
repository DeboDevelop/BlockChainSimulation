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
        #Need to recheck 
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
#Block in mempool
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
    computation_power = 0

    def __init__(self, network, coins, comp_power):
        self.miner_id = str(uuid.uuid4())
        self.blockchain = network.blockchain
        self.nodes = network.nodes
        self.mempool = []
        self.wallet = coins
        self.computation_power = comp_power

    def add_node(self, node):
        self.nodes.append(node)

    def create_transaction(self, coins, receiver, transaction_fee):
        #Creating a new Transactions
        if(wallet < coins):
            print("Not enough money in the wallet")
            return
        wallet-=coins
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
            "incentive" : int(random.random()*100), 
            "work_needed" : int(random.random()*100) 
        }
        self.mempool.append(block)
        self.request_block(block)

    def request_block(self, block):
        #Request all other nodes to create this block
        for i in range(self.nodes):
            self.nodes[i].receive_transaction(block)

    def receive_transaction(self, block):
        #All other nodes receiving this block and added it in their mempool
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
        self.receive_coins(block)

    def request_blockchain(self):
        #Requesting all other peers for their blockchain
        max = 0
        blockchain_list = 0
        for node in self.nodes:
            if max < len(node.blockchain):
                max = len(node.blockchain)
                blockchain_list = node.blockchain
        self.blockchain = blockchain_list

    def receive_coins(self, block):
        #Unloading coins from the newly created block.
        if block["receiver_id"] == self.miner_id:
            if block["payment_received"] == False:
                wallet += block["coins"]
                block["payment_received"] == True

    def work(self, network):
        random.seed(10)
        select = (random.random()*100)%(len(self.mempool))
        if(mempool[select][work_needed] < self.computation_power):
            mempool[select][work_needed] = 0
            block = mempool.pop(select)
            self.add_block_to_network(block, network)
        else:
            mempool[select][work_needed] -= self.computation_power
