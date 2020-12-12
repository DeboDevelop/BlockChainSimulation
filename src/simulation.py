from blockchain import BlockChain
from network import Network
from miner import Miner
import threading
import time
import schedule
import sys

def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()

network = Network()

miner1 = Miner(network, 1000, 12)
miner2 = Miner(network, 1000, 24)
# miner3 = Miner(network, 1000, 30)
# miner4 = Miner(network, 1000, 16)

miner1.add_node(miner2)
# miner1.add_node(miner3)
# miner1.add_node(miner4)

miner2.add_node(miner1)
# miner2.add_node(miner3)
# miner2.add_node(miner4)

# miner3.add_node(miner1)
# miner3.add_node(miner2)
# miner3.add_node(miner4)

# miner4.add_node(miner1)
# miner4.add_node(miner2)
# miner4.add_node(miner3)

miner1.create_transaction(100, miner2.miner_id, 10)
miner2.create_transaction(200, miner1.miner_id, 40)
# miner3.create_transaction(50, miner2.miner_id, 1)
# miner4.create_transaction(100, miner3.miner_id, 10)

schedule.every(5).seconds.do(run_threaded, miner1.work(network))
schedule.every(5).seconds.do(run_threaded, miner2.work(network))
# schedule.every(5).seconds.do(run_threaded, miner3.work(network))
# schedule.every(5).seconds.do(run_threaded, miner4.work(network))

while 1:
    schedule.run_pending()
    time.sleep(1)
    if network.blockchain.size >= 2:
        network.verify_blockchain()
        network.blockchain.print_blockchain()
        sys.exit("Simulation Complete!!!")