"""
LAB 1 (INTERACTIVE): PROOF-OF-WORK MINING
--------------------------------------------
Students type their own message and pick a difficulty level,
then watch the program "mine" it live.
"""

import hashlib
import time


def calculate_hash(data, nonce):
    text = f"{data}{nonce}"
    return hashlib.sha256(text.encode()).hexdigest()


def mine_block(data, difficulty):
    target = "0" * difficulty
    nonce = 0
    start_time = time.time()

    while True:
        hash_result = calculate_hash(data, nonce)
        if hash_result.startswith(target):
            end_time = time.time()
            print(f"\n✅ Block mined!")
            print(f"   Data       : {data}")
            print(f"   Nonce found: {nonce}")
            print(f"   Hash       : {hash_result}")
            print(f"   Attempts   : {nonce + 1}")
            print(f"   Time taken : {end_time - start_time:.4f} seconds")
            return
        nonce += 1
        # Show progress every 200,000 tries so it doesn't feel frozen
        if nonce % 200000 == 0:
            print(f"   ...still trying, {nonce} attempts so far")


def main():
    print("=" * 60)
    print(" PROOF OF WORK MINING — TRY IT YOURSELF ")
    print("=" * 60)
    print("Type 'quit' anytime to exit.\n")

    while True:
        data = input("Enter a message to put in your block (e.g. your name + amount): ").strip()
        if data.lower() == "quit":
            break
        if data == "":
            data = "default block data"

        while True:
            level = input("Choose difficulty (1-6 recommended, higher = slower): ").strip()
            if level.lower() == "quit":
                return
            if level.isdigit() and 1 <= int(level) <= 8:
                difficulty = int(level)
                break
            print("Please enter a number between 1 and 8.")

        print(f"\nMining your block with difficulty {difficulty} "
              f"(hash must start with '{'0' * difficulty}')...")
        mine_block(data, difficulty)

        again = input("\nMine another block? (y/n): ").strip().lower()
        print()
        if again != "y":
            break

    print("Session ended. Great job mining! 👋")


if __name__ == "__main__":
    main()
