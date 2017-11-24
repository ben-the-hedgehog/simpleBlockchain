class Blockchain(object):

	def __init__(self):
		self.chain = []
		self.current_transactions = []

	def new_block(self):
		#create a new block and add to the chain

		pass

	def new_transaction(self):
		#Adds a new transaction to list of transactions

		pass

	@staticmethod
	def hash(block):
		#Hashes a block

		pass

	@property
	def last_block(self):
		#returns the last block in the chain

		pass