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
}
"""

class BlockChain:
    data = {}
    children = []
    parent = None

    def __init__(self, data, parent):
        self.data = data
        self.children = []
        self.parent = parent

    def add_block(self, block):
        prev_blocks = block["prev_transaction_ids"]
        i = 0
        root = self
        if(root.data["transaction_id"]!=prev_blocks[i]):
            print("Block cannot be added")
            return -1
        while(i<len(prev_blocks)):
            i+=1
            flag=False
            for block in root.children:
                if (block.data["transaction_id"]==prev_blocks[i]):
                    flag=True
                    root=block
            if(flag == False):
                print("Block cannot be added")
                return -1
            if(block.data["transaction_id"] == prev_blocks[-1]):
                root.children.append(BlockChain(block, root))
                print("Block Added")
                return 0

    def verify_blockchain(self, root):
        if(root.children == []):
            return 1;
        for block in root.children:
            if root != block.parent:
                print("Verification Failed!!!")
                print("BlockChain has been tampared!!!")
                return -1;

        for block in root.children:
            exit_code = self.verify_blockchain(self, block)
            if(exit_code == -1):
                return -1;
        return 1;

    def lastest_block(self):
        root = self
        while(True):
            if(root.children==[]):
                return root;
            root = root.children[0]

    def block_list(self):
        root = self
        list_of_block = []
        while(True):
            list_of_block.append(root.data)
            if(root.children==[]):
                break
            root = root.children[0]
        return list_of_block

class Network:
    def __init__(self):
        data = { "transaction_id": str(uuid.uuid4()),
                  "prev_transaction_ids" : [],
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
        self.nodes.append(node)

    def verify_blockchain(self):
        if(self.blockchain.verify_blockchain(self.blockchain) == 1):
            print("Blockchain Valid")
        else:
            print("Blockchain invalid")

    def print_blockchain(self):
        #DFS/BFS needs to be inplemented
        pass

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
        lastest_block = network.blockchain.lastest_block()
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
        lastest_block = self.blockchain.lastest_block();
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
