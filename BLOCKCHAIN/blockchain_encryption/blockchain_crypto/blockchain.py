import hashlib
import json
from datetime import datetime
from typing import List, Dict, Any

class Block:
    """Represents a single block in the blockchain"""
    
    def __init__(self, index: int, transaction: Dict[str, Any], previous_hash: str):
        self.index = index
        self.timestamp = datetime.now().isoformat()
        self.transaction = transaction
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()
    
    def calculate_hash(self) -> str:
        """Calculate SHA-256 hash of the block"""
        block_data = {
            'index': self.index,
            'timestamp': self.timestamp,
            'transaction': self.transaction,
            'previous_hash': self.previous_hash,
            'nonce': self.nonce
        }
        block_string = json.dumps(block_data, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def mine_block(self, difficulty: int = 2):
        """Simple Proof of Work - find hash starting with difficulty zeros"""
        target = '0' * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert block to dictionary"""
        return {
            'index': self.index,
            'timestamp': self.timestamp,
            'transaction': self.transaction,
            'previous_hash': self.previous_hash,
            'nonce': self.nonce,
            'hash': self.hash
        }


class Blockchain:
    """Blockchain for recording encryption operations"""
    
    def __init__(self, difficulty: int = 2):
        self.chain: List[Block] = []
        self.difficulty = difficulty
        self.pending_transactions: List[Dict[str, Any]] = []
        
        # Create genesis block
        genesis_block = Block(0, {'type': 'GENESIS'}, '0')
        genesis_block.mine_block(self.difficulty)
        self.chain.append(genesis_block)
    
    def get_latest_block(self) -> Block:
        """Get the last block in the chain"""
        return self.chain[-1]
    
    def add_transaction(self, transaction: Dict[str, Any]) -> bool:
        """Add a transaction and create a new block"""
        try:
            # Create new block with the transaction
            new_block = Block(
                index=len(self.chain),
                transaction=transaction,
                previous_hash=self.get_latest_block().hash
            )
            
            # Mine the block (Proof of Work)
            new_block.mine_block(self.difficulty)
            
            # Add to chain
            self.chain.append(new_block)
            
            return True
        except Exception as e:
            print(f"Error adding transaction: {e}")
            return False
    
    def is_valid(self) -> bool:
        """Verify the entire blockchain"""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            # Verify current block's hash
            if current_block.hash != current_block.calculate_hash():
                return False
            
            # Verify link to previous block
            if current_block.previous_hash != previous_block.hash:
                return False
            
            # Verify Proof of Work
            if current_block.hash[:self.difficulty] != '0' * self.difficulty:
                return False
        
        return True
    
    def get_chain(self) -> List[Dict[str, Any]]:
        """Get entire blockchain as list of dictionaries"""
        return [block.to_dict() for block in self.chain]
    
    def get_block(self, index: int) -> Dict[str, Any]:
        """Get specific block by index"""
        if 0 <= index < len(self.chain):
            return self.chain[index].to_dict()
        return None
    
    def get_blocks_by_filename(self, filename: str) -> List[Dict[str, Any]]:
        """Get all blocks related to a specific file"""
        blocks = []
        for block in self.chain:
            if 'transaction' in block.transaction:
                if block.transaction.get('original_filename') == filename:
                    blocks.append(block.to_dict())
        return blocks
    
    def get_transaction_count(self) -> int:
        """Get total number of transactions (excluding genesis block)"""
        return len(self.chain) - 1
    
    def get_summary(self) -> Dict[str, Any]:
        """Get blockchain summary"""
        total_transactions = self.get_transaction_count()
        
        encrypt_count = 0
        decrypt_count = 0
        total_data_processed = 0
        
        for block in self.chain[1:]:  # Skip genesis block
            trans = block.transaction
            if trans.get('operation') == 'ENCRYPT':
                encrypt_count += 1
                total_data_processed += trans.get('file_size', 0)
            elif trans.get('operation') == 'DECRYPT':
                decrypt_count += 1
        
        return {
            'total_blocks': len(self.chain),
            'total_transactions': total_transactions,
            'encrypted_operations': encrypt_count,
            'decrypted_operations': decrypt_count,
            'total_data_processed_bytes': total_data_processed,
            'total_data_processed_mb': round(total_data_processed / (1024*1024), 2),
            'blockchain_valid': self.is_valid()
        }
