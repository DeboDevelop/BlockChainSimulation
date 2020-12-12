import unittest
import uuid
import random
import datetime
from io import StringIO 
from unittest.mock import patch 
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

def mock_print_blockchain(root):
        expected_output = ""
        if(root == None):
            return
        expected_output+="--------------------------------------\n"
        queue = [root]
        while (len(queue)>0):
            n = len(queue)
            while n>0:
                p = queue.pop(0)
                expected_output = mock_print_block(expected_output, p.data)
                for child in p.children:
                    queue.append(child)
                n-=1
            expected_output+="--------------------------------------\n"

        return expected_output

def mock_print_block(expected_output, block):
        expected_output+="______________________________________\n"
        for key in block:
            expected_output+= str(key)+"  -->  "+str(block[key])+"\n"
        expected_output+="______________________________________\n"
        return expected_output

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
        self.maxDiff = None
        expected_output = ""
        expected_output = mock_print_block(expected_output, data)
        with patch('sys.stdout', new = StringIO()) as fake_out: 
            bc.print_block(data)
            self.assertEqual(fake_out.getvalue(), expected_output) 

    def test_9_print_blockchain(self):
        expected_output = mock_print_blockchain(bc)
        with patch('sys.stdout', new = StringIO()) as fake_out: 
            bc.print_blockchain()
            self.assertEqual(fake_out.getvalue(), expected_output) 

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
        expected_output = "Blockchain Valid\n"
        nn.verify_blockchain()
        with patch('sys.stdout', new = StringIO()) as fake_out: 
            nn.verify_blockchain()
            self.assertEqual(fake_out.getvalue(), expected_output) 

    def test_4_add_node_success(self):
        length = len(nn.nodes)
        nn.add_node(m1)
        self.assertEqual(len(nn.nodes), length+1)

    def test_5_add_node_failure(self):
        length = len(nn.nodes)
        nn.add_node(125)
        self.assertEqual(len(nn.nodes), length)

netwrk = Network()
miner1 = Miner(netwrk, 1000, 24)
miner2 = Miner(netwrk, 1200, 12)

class MyMinerTest(unittest.TestCase):
    def test_01_add_node_success(self):
        length = len(miner1.nodes)
        miner1.add_node(miner2)
        self.assertEqual(len(miner1.nodes), length+1)

    def test_02_add_node_success(self):
        length = len(miner2.nodes)
        miner2.add_node(miner1)
        self.assertEqual(len(miner2.nodes), length+1)

    def test_03_add_node_failure(self):
        length = len(miner1.nodes)
        miner1.add_node(125)
        self.assertEqual(len(miner1.nodes), length)

    def test_04_receive_transaction(self):
        data = {
                "transaction_id" : str(uuid.uuid4()),
                "prev_transaction_ids" : (),
                "sender_id" : "",
                "receiver_id" : "",
                "coins" : 100,
                "transaction_fee" : 20,
                "incentive" : int(random.random()*100), 
                "work_needed" : int(random.random()*100) 
               }
        length = len(miner1.mempool)
        miner1.receive_transaction(data)
        self.assertEqual(len(miner1.mempool), length+1)

    def test_05_request_block(self):
        data = {
                "transaction_id" : str(uuid.uuid4()),
                "prev_transaction_ids" : (),
                "sender_id" : "",
                "receiver_id" : "",
                "coins" : 100,
                "transaction_fee" : 20,
                "incentive" : int(random.random()*100), 
                "work_needed" : int(random.random()*100) 
               }
        length = len(miner1.nodes[0].mempool)
        miner1.request_block(data)
        self.assertEqual(len(miner1.nodes[0].mempool), length+1)

    def test_06_create_transaction_failed(self):
        self.assertEqual(miner1.create_transaction(100000, miner2, 100), -1)
    
    def test_07_create_transaction_success(self):
        self.assertEqual(miner1.create_transaction(100, miner2, 10), 1)

    def test_08_receive_coins(self):
        wallet = miner1.wallet
        data = {
                "transaction_id" : str(uuid.uuid4()),
                "prev_transaction_ids" : (),
                "sender_id" : "",
                "receiver_id" : miner1.miner_id,
                "created_by" : miner1.miner_id,
                "created_at" : datetime.datetime.now(),
                "coins" : 100,
                "transaction_fee" : 20,
                "incentive" : 0,
               }
        miner1.receive_coins(data)
        self.assertEqual(miner1.wallet, wallet+data["coins"])

    def test_09_receive_block(self):
        wallet = miner1.wallet
        latest_block = miner1.blockchain.latest_block().data
        prev_transaction_ids = latest_block["prev_transaction_ids"] + (latest_block["transaction_id"],)
        data = {
                "transaction_id" : str(uuid.uuid4()),
                "prev_transaction_ids" : prev_transaction_ids,
                "sender_id" : "",
                "receiver_id" : miner1.miner_id,
                "created_by" : miner1.miner_id,
                "created_at" : datetime.datetime.now(),
                "coins" : 100,
                "transaction_fee" : 20,
                "incentive" : 0,
               }
        miner1.receive_block(data)
        self.assertEqual(miner1.wallet, wallet+data["coins"])

    def test_10_broadcast(self):
        size = miner1.nodes[0].blockchain.size
        latest_block = miner1.nodes[0].blockchain.latest_block().data
        prev_transaction_ids = latest_block["prev_transaction_ids"] + (latest_block["transaction_id"],)
        data = {
                "transaction_id" : str(uuid.uuid4()),
                "prev_transaction_ids" : prev_transaction_ids,
                "sender_id" : "",
                "receiver_id" : miner1.miner_id,
                "created_by" : miner1.miner_id,
                "created_at" : datetime.datetime.now(),
                "coins" : 100,
                "transaction_fee" : 20,
                "incentive" : 0,
               }
        miner1.broadcast(data)
        self.assertEqual(miner1.nodes[0].blockchain.size, size+1)

    def test_11_receive_incentive(self):
        wallet = miner1.wallet
        data = {
                "transaction_id" : str(uuid.uuid4()),
                "prev_transaction_ids" : (),
                "sender_id" : "",
                "receiver_id" : miner1.miner_id,
                "created_by" : miner1.miner_id,
                "created_at" : datetime.datetime.now(),
                "coins" : 0,
                "transaction_fee" : 20,
                "incentive" : 10,
               }
        miner1.receive_incentive(data)
        self.assertEqual(miner1.wallet, wallet+data["transaction_fee"]+data["incentive"])

    def test_12_add_block_to_network(self):
        latest_block = netwrk.blockchain.latest_block().data
        prev_transaction_ids = latest_block["prev_transaction_ids"] + (latest_block["transaction_id"],)
        data = {
                "transaction_id" : str(uuid.uuid4()),
                "prev_transaction_ids" : prev_transaction_ids,
                "sender_id" : "",
                "receiver_id" : miner1.miner_id,
                "created_by" : miner1.miner_id,
                "created_at" : datetime.datetime.now(),
                "coins" : 100,
                "transaction_fee" : 20,
                "incentive" : 0,
               }
        size = netwrk.blockchain.size
        miner1.add_block_to_network(data, netwrk)
        self.assertEqual(netwrk.blockchain.size, size+1)

    def test_13_sent_blockchain(self):
        self.assertEqual(miner1.sent_blockchain(), miner1.blockchain)

    def test_14_request_blockchain(self):
        blch = miner2.blockchain
        miner2.request_blockchain()
        self.assertEqual(miner2.blockchain, blch)

    def test_15_work(self):
        data = {
                "transaction_id" : str(uuid.uuid4()),
                "prev_transaction_ids" : (),
                "sender_id" : "",
                "receiver_id" : "",
                "coins" : 100,
                "transaction_fee" : 20,
                "incentive" : int(random.random()*100), 
                "work_needed" : 50 
               }
        work_needed = data["work_needed"]
        miner2.mempool = (data,)
        miner2.work(netwrk)
        self.assertEqual(miner2.mempool[0]["work_needed"], work_needed - miner2.computation_power)
        