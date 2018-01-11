import hashlib
import json

from Blockchain import *
from uuid import uuid4
from flask import Flask, request, jsonify

#Instantiate our node
app = Flask(__name__)

#Generate UUID for this node
node_identifier = str(uuid4()).replace('-', '')

#Instantiate the blockchain
blockchain = Blockchain()

@app.route('/mine', methods=['GET'])
def mine():
	#run proof of work algorithm to get the next proof
	last_block = blockchain.last_block
	last_proof = last_block['proof']
	proof = blockchain.proof_of_work(last_proof)

	#Give the miner the reward for finding the proof
	#Sender is "0" to signify that this node has mined a new coin
	blockchain.new_transaction(
		sender = "0",
		recipient = node_identifier, 
		amount = 1,
	)

	#Add the new block to the chain
	previous_hash = blockchain.hash(last_block)
	block = blockchain.new_block(proof, previous_hash)

	response = {
		'message': "New Block Forged",
		'index': block['index'],
	}

	return jsonify(response), 202

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
	values = request.get_json()

	#Check all the required values are in the POST'ed data
	required = ['sender', 'recipient', 'amount']
	if not all(k in values for k in required):
		return 'Missing Values!', 400

	#Create the new transaction
	index = blockchain.new_transaction(
			values['sender'],
			values['recipient'],
			values['amount']
	)

	response = {'message' : f'Transaction will be added to Block {index}'}

	return jsonify(response), 201

@app.route('/chain', methods=['GET'])
def full_chain():
	response = {
			'chain' : blockchain.chain,
			'length' : len(blockchain.chain)
	}

	return jsonify(response), 200

@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }

    return jsonify(response), 200

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000)