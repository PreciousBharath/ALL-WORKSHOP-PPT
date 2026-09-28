"""
LAB 1: PROOF-OF-WORK MINING DEMO
---------------------------------
Goal: Show students WHY mining takes effort, and why higher
"difficulty" = more time/energy.

Concept in one line:
  A miner must find a number (nonce) such that the hash of
  (data + nonce) starts with a certain number of zeros.
  There's no shortcut — you just have to keep guessing (brute force).
"""

import hashlib
import time


def calculate_hash(data, nonce):
    """Combine data + nonce and hash it using SHA-256."""
    text = f"{data}{nonce}"
    return hashlib.sha256(text.encode()).hexdigest()


def mine_block(data, difficulty):
    """
    Try nonce = 0, 1, 2, 3... until we find a hash that starts
    with `difficulty` number of zeros.
    """
    target = "0" * difficulty
    nonce = 0
    start_time = time.time()

    while True:
        hash_result = calculate_hash(data, nonce)

        if hash_result.startswith(target):
            end_time = time.time()
            print(f"✅ Block mined!")
            print(f"   Data       : {data}")
            print(f"   Nonce found: {nonce}")
            print(f"   Hash       : {hash_result}")
            print(f"   Attempts   : {nonce + 1}")
            print(f"   Time taken : {end_time - start_time:.4f} seconds\n")
            return nonce, hash_result

        nonce += 1


if __name__ == "__main__":
    print("=" * 60)
    print(" PROOF OF WORK MINING DEMO ")
    print("=" * 60)

    block_data = "Block #1: Alice pays Bob 5 coins"

    # --- Try increasing difficulty live in front of students ---
    for difficulty in [1, 2, 3, 4, 5]:
        print(f"\n--- Mining with DIFFICULTY = {difficulty} "
              f"(hash must start with {'0' * difficulty}) ---")
        mine_block(block_data, difficulty)

    print("Notice: as difficulty increases, attempts & time increase")
    print("sharply. This is exactly why Bitcoin mining needs huge")
    print("computing power — miners are just guessing numbers really fast!")
