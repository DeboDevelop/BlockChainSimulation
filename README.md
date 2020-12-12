# BlockChainSimulation
A Blockchain Simulator created after taking inspiration from Satoshi Nakamoto's white paper on bitcoin. It can be read [here](https://bitcoin.org/bitcoin.pdf).

It provides 3 classes Blockchain, Network and Miner. You can instanciates these classes and simulate a blockchain.

[![Build Status](https://travis-ci.com/DeboDevelop/BlockChainSimulation.svg?branch=main)](https://travis-ci.com/DeboDevelop/BlockChainSimulation)

## Warning - Do not deploy in production. It's not stable yet.

### Features
- Minimum use of third party library.

### Requirement

Python 3.6 or above.

### To Run Locally

1. Create an environment variable

    `python3 -m venv env`
    
2. Activate the virtual env

   `source env/bin/activate`

3. Install the Dependencies

    `pip install -r requirements.txt`

    or

    `pip3 install -r requirements.txt`

    If it doesn't work then,

    `pip install nose2, schedule`

    or

    `pip3 install nose2, schedule`

4. Run the test

    `nose2`

4. Create your own simulation.py and run

    `python simulation.py`

    Look at the Quick Start on how to create it.

### Quick Start

Read about Schedule package [Here](https://pypi.org/project/schedule/).

```
from blockchain import BlockChain
from network import Network
from miner import Miner
import threading
import time
import schedule

# Refer to schedule's documentation to understand this snippet of code.
def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()

#Create a object of Network class.
#It will contain the main blockchain or actual blockchain an each miner will maintain
#his own copy of blockchain.
network = Network()

#Create some miners
# It takes 3 parameters
# 1st -> Network, the network it belongs too.
# 2nd -> The money of money/coins/points it will start with.
# 3rd -> It's computation power.
miner1 = Miner(network, 1000, 12)
miner2 = Miner(network, 1000, 24)

# Add the Miner's in each other's node list(aka the nodes present in the network.)
miner1.add_node(miner2)
miner2.add_node(miner1)

# Create some transactions
# The create transaction function takes 3 parameters.
# 1st -> The amount it is sending.
# 2nd -> The receivers' id.
# 3rd -> The transaction fee.
miner1.create_transaction(100, miner2.miner_id, 10)
miner2.create_transaction(200, miner1.miner_id, 40)

# Schedule the miner's work function to run every x seconds.
# I am using schedule here, you don't have too.
# The Miner's work function takes 1 parameter.
# 1st -> The network which it belongs to.
schedule.every(5).seconds.do(run_threaded, miner1.work(network))
schedule.every(5).seconds.do(run_threaded, miner2.work(network))

# Run the schuduler according to your own condition.
# I want to stop the simulation after 2 blocks has been added.
while 1:
    schedule.run_pending()
    time.sleep(1)
    if network.blockchain.size >= 2:
        network.verify_blockchain()
        network.blockchain.print_blockchain()
        sys.exit("Simulation Complete!!!")
```

## License

This project is licensed under the GPLv3 License - see the [LICENSE](LICENSE) file for details

## Author

[Debajyoti Dutta](https://github.com/DeboDevelop)
