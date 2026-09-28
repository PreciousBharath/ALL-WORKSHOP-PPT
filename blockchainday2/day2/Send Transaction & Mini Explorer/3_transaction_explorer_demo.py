pythin"""
LAB 3: SEND TRANSACTION + MINI BLOCK EXPLORER DEMO
-----------------------------------------------------
Goal: Simulate what happens when you use a real testnet:
  1. A faucet gives you free test coins
  2. You send a transaction to someone
  3. It gets mined into a block
  4. You "inspect" it on an explorer (here: just printed nicely)

This mirrors the real Lab 3 (Sepolia faucet -> MetaMask -> Etherscan)
but runs instantly, offline, so students see the full lifecycle
of a transaction before doing it for real on the testnet.
"""

import hashlib
import time


class Block:
    def __init__(self, index, transactions, previous_hash):
        self.index = index
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.timestamp = time.time()
        self.nonce = 0
        self.hash = self.mine(difficulty=3)

    def calculate_hash(self):
        content = f"{self.index}{self.transactions}{self.previous_hash}{self.nonce}"
        return hashlib.sha256(content.encode()).hexdigest()

    def mine(self, difficulty):
        target = "0" * difficulty
        while True:
            h = self.calculate_hash()
            if h.startswith(target):
                return h
            self.nonce += 1


class Blockchain:
    def __init__(self):
        self.chain = [Block(0, ["Genesis Block"], "0")]
        self.balances = {}

    def faucet(self, address, amount=10):
        """Simulate a testnet faucet giving free coins."""
        self.balances[address] = self.balances.get(address, 0) + amount
        print(f"🚰 Faucet sent {amount} test coins to {address}")
        print(f"   New balance: {self.balances[address]}\n")

    def send(self, sender, receiver, amount):
        """Create + mine a transaction between two wallets."""
        if self.balances.get(sender, 0) < amount:
            print(f"❌ Transaction failed: {sender} has insufficient balance\n")
            return

        print(f"📤 {sender[:10]}... is sending {amount} coins to {receiver[:10]}...")
        print("   Mining block... (this is what 'confirming' means)")

        tx = f"{sender} -> {receiver} : {amount} coins"
        new_block = Block(len(self.chain), [tx], self.chain[-1].hash)
        self.chain.append(new_block)

        self.balances[sender] -= amount
        self.balances[receiver] = self.balances.get(receiver, 0) + amount

        print(f"✅ Transaction confirmed in Block #{new_block.index}")
        print(f"   Block Hash: {new_block.hash}\n")

    def explorer(self):
        """Print the whole chain like a simple block explorer."""
        print("=" * 60)
        print(" MINI BLOCK EXPLORER ")
        print("=" * 60)
        for block in self.chain:
            print(f"Block #{block.index}")
            print(f"   Transactions : {block.transactions}")
            print(f"   Hash         : {block.hash}")
            print(f"   Previous Hash: {block.previous_hash}")
            print()
        print("Current Balances:")
        for addr, bal in self.balances.items():
            print(f"   {addr[:12]}...  ->  {bal} coins")
        print("=" * 60)


if __name__ == "__main__":
    chain = Blockchain()

    alice_address = "0xAliceAddress1234567890"
    bob_address = "0xBobAddress0987654321"

    # Step 1: Faucet gives Alice free testnet coins
    chain.faucet(alice_address, amount=10)

    # Step 2: Alice sends coins to Bob (this gets mined)
    chain.send(alice_address, bob_address, amount=4)

    # Step 3: Inspect everything on the "explorer"
    chain.explorer()

    print("\nTeaching point: this is EXACTLY the flow they'll do live —")
    print("faucet -> MetaMask send -> confirm on Sepolia Etherscan.")
    print("Here it's simplified so they understand each step first.")
