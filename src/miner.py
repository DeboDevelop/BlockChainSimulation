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
        lastest_block = self.blockchain.latest_block();
        prev_transaction_ids = lastest_block.data["prev_transaction_ids"]
        prev_transaction_ids.append(lastest_block.data["transaction_id"])
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
        }
        network.add_block(new_block)
        self.blockchain.add_block(new_block)
        self.receive_incentive(new_block)

    def receive_incentive(self, block):
        wallet += block["transaction_fee"] + block["incentive"]
        broadcast(block)
        
    def broadcast(self, block):
        for i in range(self.nodes):
            self.nodes[i].receive_block(block)

    def receive_block(self, block):
        self.blockchain.add_block(block)
        self.receive_coins(block)

    def request_blockchain(self):
        #Requesting all other peers for their blockchain
        # Needs to be rewritten
        pass

    def receive_coins(self, block):
        #Unloading coins from the newly created block.
        if block["receiver_id"] == self.miner_id:
            wallet += block["coins"]

    def work(self, network):
        random.seed(10)
        select = (random.random()*100)%(len(self.mempool))
        if(mempool[select][work_needed] < self.computation_power):
            mempool[select][work_needed] = 0
            block = mempool.pop(select)
            self.add_block_to_network(block, network)
        else:
            mempool[select][work_needed] -= self.computation_power
