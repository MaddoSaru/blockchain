from typing import Dict
from datetime import datetime
import hashlib
import json


class blockchain:
    def __init__(self) -> None:
        self.chain = list()
        genesis_block = self.create_block(
            index=0, data="genesis_block", proof=0, previous_hash="0"
        )
        self.chain.append(genesis_block)

    def create_block(
        self,
        index: int,
        data: str,
        proof: int,
        previous_hash: str,
    ) -> Dict:
        block = {
            "index": index,
            "timestamp": datetime.now().timestamp()*1e3,
            "data": data,
            "proof": proof,
            "previous_hash": previous_hash,
        }

        return block

    def get_previous_block(self) -> Dict:
        return self.chain[-1]

    def to_process(
        self,
        previous_index: int,
        previous_data: str,
        new_proof: int,
        previous_proof: int,
    ) -> bytes:
        to_process = (
            str(new_proof**4 + previous_proof**4 + previous_index) + previous_data
        )

        return to_process.encode()

    def hash_validation(
        self,
        previous_index: int,
        previous_data: str,
        new_proof: int,
        previous_proof: str,
    ) -> bool:
        to_process = self.to_process(
            previous_index=previous_index,
            previous_data=previous_data,
            new_proof=new_proof,
            previous_proof=previous_proof,
        )
        hash_operation = hashlib.sha256(to_process).hexdigest()

        return hash_operation[:4] == "0123"

    def proof_of_work(
        self,
        previous_index: int,
        previous_data: str,
        previous_proof: int,
    ) -> int:
        new_proof = 1
        check_proof = False

        while not check_proof:
            if (
                self.hash_validation(
                    previous_index=previous_index,
                    previous_data=previous_data,
                    new_proof=new_proof,
                    previous_proof=previous_proof,
                )
                == True
            ):
                check_proof = True
            else:
                new_proof += 1

        return new_proof

    def hash(
        self,
        block: Dict,
    ) -> str:
        encoded_block = json.dumps(block, sort_keys=True).encode()

        return hashlib.sha256(encoded_block).hexdigest()

    def mine_block(self, data: str) -> Dict:
        previous_block = self.get_previous_block()
        previous_index = previous_block.get("index")
        previous_data = previous_block.get("data")
        previous_proof = previous_block.get("proof")
        previous_hash = self.hash(block=previous_block)

        index = previous_index + 1

        proof = self.proof_of_work(
            previous_index=previous_index,
            previous_data=previous_data,
            previous_proof=previous_proof,
        )

        block = self.create_block(
            index=index, data=data, proof=proof, previous_hash=previous_hash
        )

        self.chain.append(block)

        return block

    def chain_validation(self) -> bool:
        current_block = self.chain[0]
        block_index = current_block.get("index") + 1

        while block_index < len(self.chain):
            next_block = self.chain[block_index]

            if next_block.get("previous_hash") != self.hash(current_block):
                return False

            current_index, current_data, current_proof = (
                current_block.get("index"),
                current_block.get("data"),
                current_block.get("proof"),
            )
            next_proof = next_block.get("proof")

            if (
                self.hash_validation(
                    previous_index=current_index,
                    previous_data=current_data,
                    new_proof=next_proof,
                    previous_proof=current_proof,
                )
                == False
            ):
                return False

            current_block = next_block
            block_index += 1

        return True
