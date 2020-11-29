import uuid
import random
import datetime
import copy

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
        if block["prev_transaction_ids"] == []:
            print("Block Rejected")
            return -1;
        i = 1
        root = copy.copy(self)
        while True:
            if ((root.children == []) or (root.data["transaction_id"] == block["prev_transaction_ids"][-1])):
                root.children.append(BlockChain(block, root))
                print("Block Added")
                return 0
            for child in root.children:
                if(child.data["transaction_id"]==block["prev_transaction_ids"][i]):
                    i+=1
                    root = copy.copy(child)
                    break
                    
    def verify_blockchain(self, root):
        if(root.children == []):
            return 1;
        for block in root.children:
            if (root.data != block.parent.data):
                print("Verification Failed!!!")
                print("BlockChain has been tampared!!!")
                return -1;

        for block in root.children:
            exit_code = self.verify_blockchain(block)
            if(exit_code == -1):
                return -1;
        return 1;

    def latest_block(self):
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

    def print_block(self, block):
        print("______________________________________")
        for key in block:
            print(key," --> ",block[key])
        print("______________________________________")

    def print_blockchain(self):
        root = self
        if(root == None):
            return
        print("--------------------------------------")
        queue = [root]
        while (len(queue)>0):
            n = len(queue)
            while n>0:
                p = queue.pop(0)
                self.print_block(p.data)
                for child in p.children:
                    queue.append(child)
                n-=1
            print("--------------------------------------")
