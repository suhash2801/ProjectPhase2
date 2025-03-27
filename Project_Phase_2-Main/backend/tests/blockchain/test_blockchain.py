from backend.blockchain.blockchain import Blockchain
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
        blockchain.add_block(i)
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
        
