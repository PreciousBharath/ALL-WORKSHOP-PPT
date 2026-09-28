

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

    def faucet(self, name, amount=10):
        self.balances[name] = self.balances.get(name, 0) + amount
        print(f"🚰 Faucet sent {amount} test coins to {name}")
        print(f"   New balance: {self.balances[name]}")

    def send(self, sender, receiver, amount):
        if sender not in self.balances:
            print(f"❌ '{sender}' has no wallet yet. Use the faucet first.")
            return
        if receiver not in self.balances:
            self.balances[receiver] = 0
        if self.balances[sender] < amount:
            print(f"❌ Transaction failed: {sender} only has {self.balances[sender]} coins.")
            return

        print(f"📤 Sending {amount} coins from {sender} to {receiver}...")
        print("   Mining block to confirm transaction...")

        tx = f"{sender} -> {receiver} : {amount} coins"
        new_block = Block(len(self.chain), [tx], self.chain[-1].hash)
        self.chain.append(new_block)

        self.balances[sender] -= amount
        self.balances[receiver] += amount

        print(f"✅ Confirmed in Block #{new_block.index}")
        print(f"   Block Hash: {new_block.hash}")

    def explorer(self):
        print("\n" + "=" * 60)
        print(" MINI BLOCK EXPLORER ")
        print("=" * 60)
        for block in self.chain:
            print(f"Block #{block.index}")
            print(f"   Transactions : {block.transactions}")
            print(f"   Hash         : {block.hash}")
            print(f"   Previous Hash: {block.previous_hash}\n")
        print("Current Balances:")
        if not self.balances:
            print("   (no wallets yet)")
        for name, bal in self.balances.items():
            print(f"   {name:10s} -> {bal} coins")
        print("=" * 60)


def main():
    chain = Blockchain()

    print("=" * 60)
    print(" TESTNET SIMULATOR — TRY IT YOURSELF ")
    print("=" * 60)
    print("This mimics: faucet -> send transaction -> block explorer")

    while True:
        print("\nWhat would you like to do?")
        print("  1. Claim free coins from faucet")
        print("  2. Send coins to someone")
        print("  3. View block explorer")
        print("  4. Quit")
        choice = input("Enter choice (1-4): ").strip()

        if choice == "1":
            name = input("Your name: ").strip() or "student"
            chain.faucet(name)

        elif choice == "2":
            sender = input("Your name (sender): ").strip() or "student"
            receiver = input("Receiver's name: ").strip() or "friend"
            amount_str = input("Amount to send: ").strip()
            if not amount_str.isdigit():
                print("Please enter a whole number amount.")
                continue
            chain.send(sender, receiver, int(amount_str))

        elif choice == "3":
            chain.explorer()

        elif choice == "4":
            print("Session ended. That's exactly what happens for real on Sepolia! 👋")
            break

        else:
            print("Please enter a number between 1 and 4.")


if __name__ == "__main__":
    main()
