import uuid
import json
from backend.config import STARTING_BALANCE
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes,serialization
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.utils import decode_dss_signature, encode_dss_signature



class Wallet:
    """
    Individual wallet for a miner
    Keeps track of miner's balance
    Allows miner to authorize transactions
    """

    def __init__(self,blockchain=None):
        self.blockchain=blockchain
        self.address=str(uuid.uuid4())[0:8]
        self.private_key=ec.generate_private_key(ec.SECP256K1(),
                                                 default_backend()
                                                 )

        self.public_key=self.private_key.public_key()
        self.serialized_public_key()

    @property
    def balance(self):
        return Wallet.calculate_balance(self.blockchain,self.address)

    def sign(self,data):
        """
        Generate signature based on data using the local private key
        """
        return decode_dss_signature(self.private_key.sign(json.dumps(data).encode(),
                                     ec.ECDSA(hashes.SHA256())
                                     ))
    



    def serialized_public_key(self):
        """
        Reset public key to serialized version
        """
        self.public_key=self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode('utf-8')

        
    
    @staticmethod
    def verify(public_key,data,signature):
        """
        Verify signature based on public key and data
        """
        deserialize_public_key=serialization.load_pem_public_key(
            public_key.encode('utf-8'),
            default_backend()
        )

        (r,s)=signature

        try:
            deserialize_public_key.verify(encode_dss_signature(r,s),
                          json.dumps(data).encode(),
                          ec.ECDSA(hashes.SHA256())
                          )
            return True
        except InvalidSignature:
            return False
        
    
    @staticmethod
    def calculate_balance(blockchain,address):
        """
        Calculates balance of given address using the following

        Balance is found by adding o/p values of that address since most recent transaction
        """
        balance=STARTING_BALANCE

        if not blockchain:
            return balance
        
        for block in blockchain.chain:
            for transaction in block.data:
                if transaction['input']['address']==address:
                    balance=transaction['output'][address]
                
                elif address in transaction['output']:
                    balance+=transaction['output'][address]

        return balance



def main():
    wallet=Wallet()
    print(f'wallet.dict: {wallet.__dict__}')
    data={'foo':'bar'}
    signature=wallet.sign(data)
    print(f'signature: {signature}')


    should_be_valid=Wallet.verify(wallet.public_key,data, signature)
    print(f'should_be_valid: {should_be_valid}')

    should_be_invalid=Wallet.verify(Wallet().public_key,data, signature)
    print(f'should_be_invalid: {should_be_invalid}')

if __name__=='__main__':
    main()

