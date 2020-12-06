import unittest
import uuid
import random
import datetime
from blockchain import BlockChain
from network import Network
from miner import Miner

data = { "transaction_id": 1,
         "prev_transaction_ids" : (),
         "sender_id" : "",
         "receiver_id" : "",
         "created_by" : "Network",
         "created_at" : datetime.datetime.now(),
         "coins" : 10,
         "transaction_fee" : 0,
         "incentive" : 0,
       }

bc = BlockChain(data, None)

class MyBlockChainTest(unittest.TestCase):

    def test_1_latest_block(self):
        self.assertEqual(bc.latest_block().data, data)

    def test_2_add_block_success(self):
        lastest_block = bc.latest_block()
        prev_transaction_ids = lastest_block.data["prev_transaction_ids"]
        prev_transaction_ids += (lastest_block.data["transaction_id"],)
        newData = { "transaction_id": 2,
                    "prev_transaction_ids" : prev_transaction_ids,
                    "sender_id" : "",
                    "receiver_id" : "",
                    "created_by" : "Network",
                    "created_at" : datetime.datetime.now(),
                    "coins" : 20,
                    "transaction_fee" : 0,
                    "incentive" : 0,
                  }
        self.assertEqual(bc.add_block(newData), 0)

    def test_3_add_block_success(self):
        prev_transaction_ids = data["prev_transaction_ids"]
        prev_transaction_ids += (data["transaction_id"],)
        newData = { "transaction_id": 3,
                    "prev_transaction_ids" : prev_transaction_ids,
                    "sender_id" : "",
                    "receiver_id" : "",
                    "created_by" : "Network",
                    "created_at" : datetime.datetime.now(),
                    "coins" : 30,
                    "transaction_fee" : 0,
                    "incentive" : 0,
                  }
        self.assertEqual(bc.add_block(newData), 0)

    def test_4_add_block_success(self):
        lastest_block = bc.latest_block()
        prev_transaction_ids = lastest_block.data["prev_transaction_ids"]
        prev_transaction_ids += (lastest_block.data["transaction_id"],)
        newData = { "transaction_id": 4,
                    "prev_transaction_ids" : prev_transaction_ids,
                    "sender_id" : "",
                    "receiver_id" : "",
                    "created_by" : "Network",
                    "created_at" : datetime.datetime.now(),
                    "coins" : 50,
                    "transaction_fee" : 0,
                    "incentive" : 0,
                  }
        self.assertEqual(bc.add_block(newData), 0)

    def test_5_add_block_failed(self):
        newData = { "transaction_id": 7,
                    "prev_transaction_ids" : (),
                    "sender_id" : "",
                    "receiver_id" : "",
                    "created_by" : "Network",
                    "created_at" : datetime.datetime.now(),
                    "coins" : 0,
                    "transaction_fee" : 0,
                    "incentive" : 0,
                  }
        self.assertEqual(bc.add_block(newData), -1)

    def test_6_block_list(self):
        lastest_block = bc.latest_block()
        self.assertEqual(bc.block_list()[-1], lastest_block.data)

    def test_7_verify_blockchain(self):
        self.assertEqual(bc.verify_blockchain(bc), 1)

    def test_8_print_block(self):
        bc.print_block(data)

    def test_9_print_blockchain(self):
        bc.print_blockchain()

nn = Network()
m1 = Miner(nn, 100, 12)

class MyNetworkTest(unittest.TestCase):

    def test_1_add_block_success(self):
        lastest_block = nn.blockchain.latest_block()
        prev_transaction_ids = lastest_block.data["prev_transaction_ids"]
        prev_transaction_ids += (lastest_block.data["transaction_id"],)
        newData = { "transaction_id": str(uuid.uuid4()),
                    "prev_transaction_ids" : prev_transaction_ids,
                    "sender_id" : "",
                    "receiver_id" : "",
                    "created_by" : "Network",
                    "created_at" : datetime.datetime.now(),
                    "coins" : 20,
                    "transaction_fee" : 0,
                    "incentive" : 0,
                  }
        self.assertEqual(nn.add_block(newData), 0)

    def test_2_add_block_failed(self):
        newData = { "transaction_id": 7,
                    "prev_transaction_ids" : (),
                    "sender_id" : "",
                    "receiver_id" : "",
                    "created_by" : "Network",
                    "created_at" : datetime.datetime.now(),
                    "coins" : 0,
                    "transaction_fee" : 0,
                    "incentive" : 0,
                  }
        self.assertEqual(bc.add_block(newData), -1)

    def test_3_verify_blockchain(self):
        nn.verify_blockchain()
        pass

    def test_4_add_node_success(self):
        length = len(nn.nodes)
        nn.add_node(m1)
        self.assertEqual(len(nn.nodes), length+1)

    def test_5_add_node_failure(self):
        length = len(nn.nodes)
        nn.add_node(125)
        self.assertEqual(len(nn.nodes), length)