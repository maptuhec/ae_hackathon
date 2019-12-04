from aeternity.node import NodeClient, Config
from aeternity.compiler import CompilerClient
from aeternity.contract_native import ContractNative
from aeternity.signing import Account
from flask import Flask
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS
import os

app = Flask(__name__)
api = Api(app)

NODE_URL = os.environ.get('TEST_URL', 'https://testnet.aeternity.io')
NODE_INTERNAL_URL = os.environ.get('TEST_DEBUG_URL', 'https://testnet.aeternity.io')
COMPILER_URL = os.environ.get('TEST_COMPILER__URL', 'https://compiler.aepps.com')
CONTRACT_FILE = os.path.join(os.path.dirname(__file__), "./SignatureChecker.aes")

ae_address = "ak_TgaLnCYN1wtXP9KKQz3apMNzXMuUJa9gXbv4o5uW73tRW8Gue"
eth_address = "0XBBAAABE6F5ABEE05380413420DAD35F32C1D683F"
signature = "1ba4c21946723260fd0a09a09008e9011ea1e3f19d7e2704ef49627f5c7259cde514e561d5c363a4b7ba7e8cf14277dee6ba3aab3bdcaa5529329265bc867e3e18"

node_cli = NodeClient(Config(
    external_url=NODE_URL,
    internal_url=NODE_INTERNAL_URL,
    blocking_mode=True,
))

# generate server account 
server_account = Account.from_secret_key_string("b7bec661327b7b2b9f6804000d104730402b8b3e7c5e3b4cd6ccd62942a073b46f01309c2c1f3ea4a9338b481038c11a6327a1d76f4677bf09047c756dc31bcf")
with open(CONTRACT_FILE, 'r') as file:
    signature_checker_contract = file.read()

signature_checker_instance = ContractNative(client=node_cli, 
                                compiler=COMPILER_URL, 
                                account=server_account, 
                                source=signature_checker_contract,
								address="ct_8n7ZdPSuhgp4hdcU49fy6d8UThqCv68C1cVQCVWw7biqrWcag")
# MEthods to deploy and interact with the smart contract
# deployTx = signature_checker_instance.deploy()
# signature_checker_instance.at("ct_8n7ZdPSuhgp4hdcU49fy6d8UThqCv68C1cVQCVWw7biqrWcag")
# tx_info, tx_result = signature_checker_instance.get_eth_address_string("ak_TgaLnCYN1wtXP9KKQz3apMNzXMuUJa9gXbv4o5uW73tRW8Gue", "1ba4c21946723260fd0a09a09008e9011ea1e3f19d7e2704ef49627f5c7259cde514e561d5c363a4b7ba7e8cf14277dee6ba3aab3bdcaa5529329265bc867e3e18")
# tx_validate_info, tx_validate_result = signature_checker_instance.validate_addresses(ae_address, signature,eth_address.upper())

class getAddress(Resource):
	# def get(self):
	# 	return ae_address, 200

	def post(self):
		parser = reqparse.RequestParser()
		parser.add_argument("ae_address")
		parser.add_argument("signature")
		parser.add_argument("eth_address")
		args = parser.parse_args()
		print(f"patamsss {args}")
		print(f"params {args['ae_address']}")
		print(f"params {args['signature']}")
		print(f"params {args['eth_address']}")
		signature_checker_instance.at("ct_8n7ZdPSuhgp4hdcU49fy6d8UThqCv68C1cVQCVWw7biqrWcag")
		tx_validate_info, tx_validate_result = signature_checker_instance.validate_addresses(args['ae_address'], args['signature'],args['eth_address'].upper())
		# tx_validate_info, tx_validate_result = signature_checker_instance.validate_addresses(ae_address, signature,eth_address.upper())
		print(f"REsult {tx_validate_result}")
		return tx_validate_result, 200


api.add_resource(getAddress, "/verifySignature")
# CORS(app)
# app.run(ssl_context=('./openssl/openssl/cert.pem', './openssl/openssl/key.pem'))
app.run()
