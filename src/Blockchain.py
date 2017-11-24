import hashlib
import json
from time import time

class Blockchain(object):

	def __init__(self):
		self.chain = []
		self.current_transactions = []

	def new_block(self, proof, previous_hash=None):
		"""
		Create a new block and append it to the Blockchain

		:param proof: <int> The proof given by the Proof of Work algorithm
		:param previous_hash: (Optional) <str> Hash of previous block
		:return: <dict> New block
		"""

		block = {
			'index': len(self.chain) + 1,
			'timestamp': time(),
			'transactions': self.current_transactions,
			'proof': proof,
			'previous_hash': previous_hash or self.hash(self.chain[-1]),
		}
		
		#current transactions processed on new block, reset list of transactions
		self.current_transactions = []

		#append the new block to the chain
		self.chain.append(block)

		return block

	def new_transaction(self, sender, recipient, amount):
		"""
        Creates a new transaction to go into the next mined Block
        :param sender: <str> Address of the Sender
        :param recipient: <str> Address of the Recipient
        :param amount: <int> Amount
        :return: <int> The index of the Block that will hold this transaction
        """

		self.current_transactions.append({
			'sender' : sender,
			'recipient' : recipient,
			'amount' : amount,
			})
		
		return self.last_block['index'] + 1

	@staticmethod
	def hash(block):
		"""
        Creates a SHA-256 hash of a Block
        :param block: <dict> Block
        :return: <str>
        """

        #IMPORTANT: Block dict must be ordered, else possible inconsistencies
		block_string = json.dumps(block, sort_keys=True).encode()
		return hashlib.sha256(block_string).hexdigest()        


	@property
	def last_block(self):
		"""
		getter for last block on the chain
		"""
		return self.chain[-1]