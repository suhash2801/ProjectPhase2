from backend.blockchain.block import Block
class Blockchain:
    
    def __init__(self):
        self.chain=[Block.genesis()]

    def add_block(self,data):
        self.chain.append(Block.mine_block(self.chain[-1],data))#self.chain[-1] references the last block in the chain
    

    def __repr__(self):
        return f'Blockchain: {self.chain}'
    
    def replace_chain(self,chain):
        """
        Replace the local chain with incoming chain if:
        1. Incoming chain is longer than local
        2. Incoming chain is formatted properly
        """
        if len(chain)<=len(self.chain):
            raise Exception('Cannot replace. Incoming chain must be longer')
        
        try:
            Blockchain.is_valid_chain(chain)

        except Exception as e:
            raise Exception (F'Cannot replace. Incoming chain is invalid: {e}')
        
        self.chain=chain
        
    def to_json(self):
        """Serialize blockchain to list of blocks
        """
        return list(map(lambda block: block.to_json(),self.chain))
    @staticmethod
    def from_json(chain_json):

        """
        Deserialize a list into a blockchain instance.
        Result contains chain list of Block instances
        """
        blockchain=Blockchain()
        blockchain.chain=list(map(lambda block_json: Block.from_json(block_json),chain_json))

        return blockchain

    

    @staticmethod
    def is_valid_chain(chain):
        """
        Validate the incoming chain
        Enforce following rules:
        1. Starts with genesis block
        2. Blocks format must be crct
        """
        if chain[0]!=Block.genesis():
            raise Exception('Genesis block must be valid')

        for i in range(1,len(chain)):
            block=chain[i]
            last_block=chain[i-1]
            Block.is_valid_block(last_block,block)

    
def main():

    blockchain=Blockchain()

    blockchain.add_block('one')
    blockchain.add_block('two')

    print(blockchain)


    print(f'block.py __name__:{__name__}')
if __name__=='__main__':
    main()