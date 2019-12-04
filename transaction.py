from aeternity.node import NodeClient, Config
from aeternity.compiler import CompilerClient
from aeternity.contract_native import ContractNative
from aeternity.signing import Account
from flask import Flask
from flask_restful import Api, Resource, reqparse
import os

server_account = Account.from_secret_key_string("b7bec661327b7b2b9f6804000d104730402b8b3e7c5e3b4cd6ccd62942a073b46f01309c2c1f3ea4a9338b481038c11a6327a1d76f4677bf09047c756dc31bcf")
with open(CONTRACT_FILE, 'r') as file:
    signature_checker_contract = file.read()

signature_checker_instance = ContractNative(client=node_cli, 
                                compiler=COMPILER_URL, 
                                account=server_account, 
                                source=signature_checker_contract)

signature_checker_instance.at("ct_8n7ZdPSuhgp4hdcU49fy6d8UThqCv68C1cVQCVWw7biqrWcag")


class getAddress(Resource):
	def get(self):
		return ae_address, 200

	def post(self, ae_address, signature):
		parser = reqparse.RequestParser()
		parser.add_argument("ae_address")
		parser.add_argument("signature")
		
		tx_validate_info, tx_validate_result = signature_checker_instance.get_eth_address_string(args["ae_address"], args["signature"])
		return tx_validate_result, 200


api.add_resource(getAddress, "/getAddress")
app.run(debug=True)