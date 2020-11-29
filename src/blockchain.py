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

    def print_blockchain(self):
        root = self
        if(root == None):
            return
        queue = [root]
        while (len(queue)>0):
            n = len(queue)
            while n>0:
                p = queue.pop(0)
                print(p.data)
                for child in p.children:
                    queue.append(child)
                n-=1
            print("--------------------------------------")
