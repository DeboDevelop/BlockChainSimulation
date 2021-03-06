import uuid
import random
import datetime
from blockchain import BlockChain
from network import Network

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
    def __init__(self, network, coins, comp_power):
        self.miner_id = str(uuid.uuid4())
        lastest_block = network.blockchain.latest_block()
        self.blockchain = BlockChain(lastest_block.data, None)
        self.nodes = network.nodes
        self.mempool = ()
        self.wallet = coins
        self.computation_power = comp_power

    def add_node(self, node):
        if(str(type(node))=="<class 'miner.Miner'>"):
            self.nodes = self.nodes + (node,)
            print("Node Added by Miner: ",self.miner_id)

    def create_transaction(self, coins, receiver, transaction_fee):
        #Creating a new Transactions
        if(self.wallet < coins):
            print("Not enough money in the wallet")
            return -1
        self.wallet-=(coins+transaction_fee)
        lastest_block = self.blockchain.latest_block();
        prev_transaction_ids = lastest_block.data["prev_transaction_ids"]
        prev_transaction_ids += (lastest_block.data["transaction_id"],)
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
        print("Added new block to mempool of Miner: ", self.miner_id)
        self.mempool+=(block,)
        self.request_block(block)
        return 1

    def request_block(self, block):
        #Request all other nodes to create this block
        print(self.miner_id, " is request all nodes to create his block")
        for i in range(len(self.nodes)):
            self.nodes[i].receive_transaction(block)

    def receive_transaction(self, block):
        #All other nodes receiving this block and added it in their mempool
        self.mempool+=(block,)
        print("Added new block to mempool of Miner: ", self.miner_id)

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
        }
        network.add_block(new_block)
        print("New Block added to Network by Miner: ", self.miner_id)
        self.blockchain.add_block(new_block)
        print("New Block added to Own BlockChain by Miner: ", self.miner_id)
        self.receive_incentive(new_block)

    def receive_incentive(self, block):
        self.wallet += block["transaction_fee"] + block["incentive"]
        print(self.miner_id, " received transaction fee and incentive")
        self.broadcast(block)
        
    def broadcast(self, block):
        print(self.miner_id, " is broadcasting the block to all miners")
        for i in range(len(self.nodes)):
            self.nodes[i].receive_block(block)

    def receive_block(self, block):
        x = self.blockchain.add_block(block)
        if x==0:
            self.receive_coins(block)
            print(self.miner_id," added the block sucessfully.")
        else:
            print(self.miner_id," failed to add block")

    def receive_coins(self, block):
        #Unloading coins from the newly created block.
        if block["receiver_id"] == self.miner_id:
            self.wallet += block["coins"]
            print(self.miner_id, " received the money sucessfully")

    def work(self, network):
        if self.mempool == ():
            return
        random.seed(10)
        select = (int(random.random()*100))%(len(self.mempool))
        print(self.miner_id, " is working on block ", self.mempool[select]["transaction_id"])
        if(self.mempool[select]["work_needed"] < self.computation_power):
            self.mempool[select]["work_needed"] = 0
            mid_list = list(self.mempool)
            block = mid_list.pop(select)
            self.mempool = tuple(mid_list)
            self.add_block_to_network(block, network)
        else:
            self.mempool[select]["work_needed"] -= self.computation_power

    def request_blockchain(self):
        #Requesting all other peers for their blockchain
        print(self.miner_id, " is requesting his peers for their copy of blockchain")
        max_size = self.blockchain.size
        max_blockchain = self.blockchain
        for i in range(len(self.nodes)):
            blck = self.nodes[i].sent_blockchain()
            if(blck.size > max_size):
                max_size = blck.size
                max_blockchain = blck
        self.blockchain = max_blockchain

    def sent_blockchain(self):
        return self.blockchain