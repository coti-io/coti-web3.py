from enum import Enum

class CotiNetwork(Enum):
    TESTNET = "https://testnet.coti.io/rpc"

ACCOUNT_ONBOARD_CONTRACT_ADDRESS = "0x536A67f0cc46513E7d27a370ed1aF9FDcC7A5095"

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