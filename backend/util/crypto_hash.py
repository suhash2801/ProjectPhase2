import hashlib
import json

def crypto_hash(*args):
    """
    Returns sha-256 hash of  given arguments
    """
    stringified_args=sorted(map(lambda data:json.dumps(data),args))
    joined_data=''.join(stringified_args)


    return hashlib.sha256(joined_data.encode()).hexdigest()

def main():
    print(f"crypto_hash([]): {crypto_hash(2,'one',[3])}")
    
if __name__=="__main__":
    main()