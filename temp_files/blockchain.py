import datetime
import hashlib
import json
import random


# building blockchain

class BlockChain:
    def __init__(self):
        self.chain = []
        self.create_block(proof=1, previous_hash='0')

    def create_block(self, proof, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': str(datetime.datetime.now()),
            'proof': proof,
            'previous_hash': previous_hash,
            'payload': ''.join([chr(random.randint(ord('A'), ord('Z'))) for x in range(64)])
        }
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        new_proof = 1
        flag = False
        while flag is False:
            hash_op = hashlib.sha256(str(new_proof ** 2 - previous_proof ** 2).encode()).hexdigest()
            if hash_op[:6] == '000000':
                flag = True
            else:
                new_proof += 1
        return new_proof

    def hash(self, block):
        encstr = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encstr).hexdigest()

    def is_chain_valid(self):
        previous_block = self.chain[0]
        block_index = 1
        while block_index < len(self.chain):
            block = self.chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                print("-->", block_index + 1)
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_op = hashlib.sha256(str(proof ** 2 - previous_proof ** 2).encode()).hexdigest()
            if hash_op[:6] != '000000':
                print(":: ", block_index)
                return False
            previous_block = block
            block_index += 1
        return True

    def change_payload(self, block_index):
        self.chain[block_index - 1]['payload'] = ''.join([chr(random.randint(ord('A'), ord('Z'))) for x in range(64)])

    def print_blockchain(self):
        for i in self.chain:
            print("--------------------------------")
            for j in i.keys():
                print(j, ":", i[j])
            print("--------------------------------")

    def insert_block(self):
        previous_block = self.get_previous_block()
        proof = self.proof_of_work(previous_block['proof'])
        block = self.create_block(proof, self.hash(previous_block))

    def pow(self, indx):
        previous_block = self.chain[indx - 2]
        previous_proof = previous_block['proof']
        proof = self.proof_of_work(previous_proof)
        self.chain[indx - 1]['proof'] = proof
        self.chain[indx - 1]['previous_hash'] = self.hash(previous_block)


# MAIN

print("1. CREATE BLOCKCHAIN\n"
      "2. INSERT NODE\n"
      "3. CHECK FOR VALIDITY\n"
      "4. MODIFY PAYLOAD->BLOCK-INDEX\n"
      "5. POW->BLOCK-INDEX\n"
      "6. PRINT BLOCKCHAIN\n"
      "0. QUIT\n")
i = int(input("Enter Queries"))
bc = None
while i > 0:
    if i == 1:
        bc = BlockChain()
        bc.print_blockchain()
    elif i == 2:
        bc.insert_block()
        bc.print_blockchain()
    elif i == 3:
        if bc.is_chain_valid():
            print("BLOCKCHAIN IS VALID")
        else:
            print("BLOCKCHAIN IS NOT VALID")
    elif i == 4:
        i2 = int(input("Enter block:"))
        bc.change_payload(i2)
        bc.print_blockchain()
    elif i == 5:
        i2 = int(input("Enter block:"))
        bc.pow(i2)
        print("Done!")
    elif i == 6:
        bc.print_blockchain()
    print('_' * 80)
    print("1. CREATE BLOCKCHAIN\n"
          "2. INSERT NODE\n"
          "3. CHECK FOR VALIDITY\n"
          "4. MODIFY PAYLOAD->BLOCK-INDEX\n"
          "5. POW->BLOCK-INDEX\n"
          "6. PRINT BLOCKCHAIN\n"
          "0. QUIT\n")
    i = int(input("Enter Queries"))
