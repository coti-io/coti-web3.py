from eth_account.signers.local import LocalAccount
from coti.crypto_utils import generate_rsa_keypair, recover_user_key, sign
from web3 import Web3
from web3.middleware import ExtraDataToPOAMiddleware
from .constants import CotiNetwork, ACCOUNT_ONBOARD_CONTRACT_ABI, ACCOUNT_ONBOARD_CONTRACT_ADDRESS

def init_web3(coti_network: CotiNetwork):
    web3 = Web3(Web3.HTTPProvider(coti_network.value))
    web3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)

    return web3

def onboard(web3: Web3, account: LocalAccount, onboard_contract_address: str):
    onboard_contract = web3.eth.contract(address=onboard_contract_address, abi=ACCOUNT_ONBOARD_CONTRACT_ABI)

    [rsa_private_key, rsa_public_key] = generate_rsa_keypair()

    signature = sign(rsa_public_key, account.key)

    tx = onboard_contract.functions.onboardAccount(rsa_public_key, signature).build_transaction({
        'from': account.address,
        'chainId': web3.eth.chain_id,
        'nonce': web3.eth.get_transaction_count(account.address),
        'gas': 15000000,
        'gasPrice': web3.to_wei(30, 'gwei')
    })

    signed_tx = web3.eth.account.sign_transaction(tx, account.key)

    tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)

    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

    user_key_events = onboard_contract.events.AccountOnboarded().process_receipt(tx_receipt)
    key_0_share = user_key_events[0].args.userKey1
    key_1_share = user_key_events[0].args.userKey2

    aes_key = recover_user_key(rsa_private_key, key_0_share, key_1_share).hex()

    account.set_user_onboard_info({
        "rsa_key_pair": (rsa_private_key.hex(), rsa_public_key.hex()),
        "tx_hash": tx_hash.hex(),
        "aes_key": aes_key
    })

def recover_aes_from_tx(web3: Web3, account: LocalAccount, onboard_contract_address: str):
    tx_receipt = web3.eth.get_transaction_receipt(bytes.fromhex(account.onboard_tx_hash))

    onboard_contract = web3.eth.contract(address=onboard_contract_address, abi=ACCOUNT_ONBOARD_CONTRACT_ABI)

    user_key_events = onboard_contract.events.AccountOnboarded().process_receipt(tx_receipt)

    key_0_share = user_key_events[0].args.userKey1
    key_1_share = user_key_events[0].args.userKey2

    aes_key = recover_user_key(bytes.fromhex(account.rsa_key_pair[0]), key_0_share, key_1_share).hex()

    account.set_aes_key(aes_key)


def generate_or_recover_aes(web3: Web3, account: LocalAccount, onboard_contract_address: str = ACCOUNT_ONBOARD_CONTRACT_ADDRESS):
    if account.user_onboard_info and account.aes_key:
        return
    
    if account.user_onboard_info and account.rsa_key_pair and account.onboard_tx_hash:
        recover_aes_from_tx(web3, account, onboard_contract_address)
        return

    account_balance = web3.eth.get_balance(account.address)

    if account_balance == 0:
        raise RuntimeError("Account balance is 0 so user cannot be onboarded.")
    
    onboard(web3, account, onboard_contract_address)