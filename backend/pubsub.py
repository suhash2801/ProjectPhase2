from pubnub.pubnub import PubNub
from pubnub.pnconfiguration import PNConfiguration
from pubnub.callbacks import SubscribeCallback
import time
from backend.blockchain.block import Block
from backend.wallet.transaction import Transaction


pnconfig=PNConfiguration()
pnconfig.subscribe_key='sub-c-b4c58c18-1c1a-4126-a572-8b742e73508b'
pnconfig.publish_key='pub-c-a12ece30-0d71-4969-b471-dbdd395da481'


CHANNELS={
    'TEST':'TEST',
    'BLOCK':'BLOCK',
    'TRANSACTION':'TRANSACTION'
          }


class Listener(SubscribeCallback):
    def __init__(self,blockchain,transaction_pool):
        self.blockchain=blockchain
        self.transaction_pool=transaction_pool
        

    def message(self, pubnub, message_object):
        print(f'\n-- Channel: {message_object.channel} | Message: {message_object.message}')
        if message_object.channel==CHANNELS['BLOCK']:
            block=Block.from_json(message_object.message)
            potential_chain=self.blockchain.chain[:]
            potential_chain.append(block)

            try:
                self.blockchain.replace_chain(potential_chain)
                self.transaction_pool.clear_blockchain_transactions(self.blockchain)
                print(f'\n --Successfully replaced local chain')

            except Exception as e:
                print(f'\n --Did not replace chain: {e}')

        elif message_object.channel==CHANNELS['TRANSACTION']:
            transaction=Transaction.from_json(message_object.message)
            self.transaction_pool.set_transaction(transaction)
            print('\n --Set the new transaction in the transaction pool')



class PubSub():
    """
    Handles pub/sub layer of application
    Provides communication between nodes of Blockchain
    """
    def __init__(self,blockchain,transaction_pool):
        self.pubnub=PubNub(pnconfig)
        self.pubnub.subscribe().channels(CHANNELS.values()).execute()
        self.pubnub.add_listener(Listener(blockchain,transaction_pool))

    def publish(self,channel,message):
        """
        Publishes message object to channel
        """
        self.pubnub.unsubscribe().channels([channel]).execute()
        self.pubnub.publish().channel(channel).message(message).sync()
        self.pubnub.subscribe().channels([channel]).execute()

    def broadcast_block(self, block):
        """
        Broadcast block object to all nodes
        """
        self.publish(CHANNELS['BLOCK'],block.to_json())

    def broadcast_transaction(self,transaction):
        """
        Broadcasts transaction to all nodes
        """
        self.publish(CHANNELS['TRANSACTION'],transaction.to_json())






def main():
    pubsub=PubSub()


    time.sleep(1)
    pubsub.publish(CHANNELS['TEST'],{'foo':'bar'})

if __name__=='__main__':
    main()

