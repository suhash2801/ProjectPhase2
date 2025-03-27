from backend.blockchain.blockchain import Blockchain
from backend.wallet.wallet import Wallet
from backend.wallet.transaction import Transaction
from backend.blockchain.block import GENESIS_DATA
import pytest

def test_blockchain_instance():
    blockchain=Blockchain()
    assert blockchain.chain[0].hash==GENESIS_DATA['hash']

def test_add_block():
    blockchain=Blockchain()
    data='test-data'
    blockchain.add_block(data)

    assert blockchain.chain[-1].data==data
    
@pytest.fixture
def blochain_three_blocks():
    blockchain=Blockchain()
    for i in range(3):
        blockchain.add_block([Transaction(Wallet(),'recipient',i).to_json()])
    return blockchain

def test_is_valid_chain(blochain_three_blocks):
    

    Blockchain.is_valid_chain(blochain_three_blocks.chain)

def test_is_valid_chain_bad_genesis(blochain_three_blocks):
    blochain_three_blocks.chain[0].hash='evil-hash'
    
    with pytest.raises(Exception,match='Genesis block must be valid'):
        Blockchain.is_valid_chain(blochain_three_blocks.chain)

def test_replace_chain(blochain_three_blocks):
    blockchain=Blockchain()

    blockchain.replace_chain(blochain_three_blocks.chain)

    assert blockchain.chain== blochain_three_blocks.chain

def test_replace_chain_not_longer(blochain_three_blocks):
    blockchain= Blockchain()
    with pytest.raises(Exception,match='Cannot replace. Incoming chain must be longer'):
        blochain_three_blocks.replace_chain(blockchain.chain)

def test_replace_chain_bad_chain(blochain_three_blocks):
    blockchain=Blockchain()
    blochain_three_blocks.chain[1].hash='evil_hash'
    with pytest.raises(Exception,match='Incoming chain is invalid'):
        blockchain.replace_chain(blochain_three_blocks.chain)
        

def test_valid_transaction_chain(blochain_three_blocks):
    Blockchain.is_valid_transaction_chain(blochain_three_blocks.chain)

def test_is_valid_transaction_chain_duplicate_transaction(blochain_three_blocks):
    transaction=Transaction(Wallet(),'recipient',1).to_json()

    blochain_three_blocks.add_block([transaction,transaction])
    with pytest.raises(Exception,match='is not unique'):
        Blockchain.is_valid_transaction_chain(blochain_three_blocks.chain)

def test_is_valid_transaction_chain_multiple_rewards(blochain_three_blocks):
    reward_1=Transaction.reward_transaction(Wallet()).to_json()
    reward_2=Transaction.reward_transaction(Wallet()).to_json()


    blochain_three_blocks.add_block([reward_1,reward_2])
    with pytest.raises(Exception,match='one mining reward per block'):
        Blockchain.is_valid_transaction_chain(blochain_three_blocks.chain)


def test_is_valid_transaction_chain_bad_transaction(blochain_three_blocks):
    bad_transaction=Transaction(Wallet(),'recipient',1)
    bad_transaction.input['signature']=Wallet().sign(bad_transaction.output)
    blochain_three_blocks.add_block([bad_transaction.to_json()])
    
    
    with pytest.raises(Exception):
        Blockchain.is_valid_transaction_chain(blochain_three_blocks.chain)


def test_is_valid_transaction_chain_bad_historic_balance(blochain_three_blocks):
    wallet=Wallet()
    bad_transaction=Transaction(wallet,'recipient',1)
    bad_transaction.output[wallet.address]=9000
    bad_transaction.input['amount']=9001
    bad_transaction.input['signature']=wallet.sign(bad_transaction.output)

    blochain_three_blocks.add_block([bad_transaction.to_json()])
    
    with pytest.raises(Exception,match='has invalid input amount'):
        Blockchain.is_valid_transaction_chain(blochain_three_blocks.chain)

