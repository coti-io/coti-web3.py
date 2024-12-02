from enum import Enum

class CotiNetwork(Enum):
    TESTNET = "https://testnet.coti.io/rpc"

ACCOUNT_ONBOARD_CONTRACT_ADDRESS = "0x24D6c44eaB7aA09A085dDB8cD25c28FFc9917EC9"

ACCOUNT_ONBOARD_CONTRACT_ABI = [
    {
        "anonymous": False,
        "inputs": [
        {
            "indexed": True,
            "internalType": "address",
            "name": "_from",
            "type": "address"
        },
        {
            "indexed": False,
            "internalType": "bytes",
            "name": "userKey1",
            "type": "bytes"
        },
        {
            "indexed": False,
            "internalType": "bytes",
            "name": "userKey2",
            "type": "bytes"
        }
        ],
        "name": "AccountOnboarded",
        "type": "event"
    },
    {
        "inputs": [
        {
            "internalType": "bytes",
            "name": "publicKey",
            "type": "bytes"
        },
        {
            "internalType": "bytes",
            "name": "signedEK",
            "type": "bytes"
        }
        ],
        "name": "onboardAccount",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]