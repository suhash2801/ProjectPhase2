import time
from backend.util.hex_to_binary import hex_to_binary
from backend.util.crypto_hash import crypto_hash
from backend.config import MINE_RATE

GENESIS_DATA = {
    'timestamp': 1,
    'last_hash': 'genesis_last_hash',
    'hash': 'genesis_hash',
    'data': [],
    'difficulty': 3,
    'nonce': 'genesis_nonce',
    'chip_info': {'chip_id': None, 'chip_make': None, 'current_status': None}
}

class Block:
    def __init__(self, timestamp, last_hash, hash, data, difficulty, nonce, chip_info=None):
        self.timestamp = timestamp
        self.data = data
        self.last_hash = last_hash
        self.hash = hash
        self.nonce = nonce
        self.difficulty = difficulty
        self.chip_info = chip_info or {'chip_id': None, 'chip_make': None, 'current_status': None}

    def __repr__(self):
        return (f'Block('
                f'timestamp: {self.timestamp}, '
                f'hash: {self.hash}, '
                f'last_hash: {self.last_hash}, '
                f'data: {self.data}, '
                f'nonce: {self.nonce}, '
                f'difficulty: {self.difficulty}, '
                f'chip_info: {self.chip_info})')
    
    def __eq__(self, other):
        return self.__dict__ == other.__dict__
    
    def to_json(self):
        """Serialize block into dictionary"""
        return self.__dict__

    @staticmethod
    def mine_block(last_block, data, chip_info=None):
        """
        Mines block based on given last block and data
        until block hash meets leading zeroes PoW requirement
        """
        timestamp = time.time_ns()
        last_hash = last_block.hash
        difficulty = last_block.adjust_difficulty(last_block, timestamp)
        nonce = 0
        
        hash = crypto_hash(timestamp, last_hash, data, difficulty, nonce, chip_info)
        while hex_to_binary(hash)[0:difficulty] != '0' * difficulty:
            nonce += 1
            timestamp = time.time_ns()
            difficulty = last_block.adjust_difficulty(last_block, timestamp)
            hash = crypto_hash(timestamp, last_hash, data, difficulty, nonce, chip_info)
        
        return Block(timestamp, last_hash, hash, data, difficulty, nonce, chip_info)
    
    @staticmethod
    def genesis():
        """
        Generates genesis Block
        """
        return Block(**GENESIS_DATA)
    
    @staticmethod
    def from_json(block_json):
        """
        Deserialize a JSON representation into a Block instance
        """
        return Block(**block_json)

    @staticmethod
    def adjust_difficulty(last_block, new_timestamp):
        """
        Calculate adjusted difficulty according to MINE_RATE
        Increase if too easy
        Decrease if too difficult
        """
        if (new_timestamp - last_block.timestamp) < MINE_RATE:
            return last_block.difficulty + 1
        if last_block.difficulty > 1:
            return last_block.difficulty - 1
        return 1
    
    @staticmethod
    def is_valid_block(last_block, block):
        """
        Validate block by enforcing rules:
        1. Block must have correct last_hash reference
        2. Block must satisfy PoW requirement
        3. Difficulty must only be adjusted by 1
        4. Block hash must match
        """
        if block.last_hash != last_block.hash:
            raise Exception('The block last_hash must be correct')
        
        if hex_to_binary(block.hash)[0:block.difficulty] != '0' * block.difficulty:
            raise Exception('PoW requirement was not met')
        
        if abs(last_block.difficulty - block.difficulty) > 1:
            raise Exception('Difficulty difference is more than 1')
        
        reconstructed_hash = crypto_hash(block.timestamp, block.last_hash, block.data, block.nonce, block.difficulty, block.chip_info)
        if block.hash != reconstructed_hash:
            raise Exception('Block hash is not correct')

def main():
    genesis_block = Block.genesis()
    new_block = Block.mine_block(genesis_block, 'foo', {'chip_id': '12345', 'chip_make': 'ChipCorp', 'current_status': 'active'})
    print(new_block)

if __name__ == '__main__':
    main()