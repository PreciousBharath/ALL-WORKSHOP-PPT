import hashlib
from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass
class Block:
    index: int
    data: str
    previous_hash: str
    timestamp: str = ""
    nonce: int = 0
    hash: str = ""

    def calculate_hash(self):
        text = f"{self.index}{self.timestamp}{self.data}{self.previous_hash}{self.nonce}"
        return hashlib.sha256(text.encode()).hexdigest()

    def mine(self):
        while not self.hash.startswith("0000"):
            self.nonce += 1
            self.hash = self.calculate_hash()


def new_block(index, data, previous_hash):
    block = Block(index, data, previous_hash, datetime.now(timezone.utc).isoformat())
    block.mine()
    return block


def valid(chain):
    return all(
        block.hash == block.calculate_hash()
        and block.hash.startswith("0000")
        and (i == 0 or block.previous_hash == chain[i - 1].hash)
        for i, block in enumerate(chain)
    )


def show(chain):
    print("\n" + "=" * 72 + "\nBLOCKCHAIN\n" + "=" * 72)
    for block in chain:
        print(f"\nBlock #{block.index}\n  Data:          {block.data}"
              f"\n  Previous hash: {block.previous_hash}\n  Hash:          {block.hash}"
              f"\n  Calculated hash: {block.calculate_hash()}"
              f"\n  Nonce:         {block.nonce:,}")
    print(f"\nChain valid: {'YES' if valid(chain) else 'NO'}")


def explain():
    print("""HOW BLOCKCHAIN WORKS

1. A block stores data, a timestamp, its own hash, and the previous block's hash.
2. A hash is a one-way digital fingerprint. Changing even one character changes it.
3. Mining changes the nonce until the hash starts with four zeroes (proof-of-work).
4. Because every block points to the previous hash, changing an old block breaks the chain.
5. A real blockchain adds many computers, consensus rules, networking, and digital signatures.

This demo focuses on the linked blocks and proof-of-work parts.
""")


def main():
    explain()
    chain = [new_block(0, "Genesis block: the chain begins here.", "0")]
    while True:
        choice = input("\n[A] Add a block  [V] View chain  [T] Tamper with a block  [E] Explain again  [Q] Quit\nSelect an option: ").lower()
        if choice == "a":
            data = input("Enter data for the new block: ").strip()
            if data:
                print("\nMining block...", end="", flush=True)
                block = new_block(len(chain), data, chain[-1].hash)
                chain.append(block)
                print(f" done ({block.nonce:,} attempts).")
            else:
                print("A block needs some data.")
        elif choice == "v":
            show(chain)
        elif choice == "t":
            try:
                index = int(input(f"Choose a block (0-{len(chain) - 1}): "))
                chain[index].data = input("Replace its data with: ")
                print("Data changed without re-mining. View the chain to see validation fail.")
            except (ValueError, IndexError):
                print("Please enter a valid block number.")
        elif choice == "e":
            explain()
        elif choice == "q":
            print("Goodbye!")
            break
        else:
            print("Choose A, V, T, E, or Q.")


if __name__ == "__main__":
    main()
