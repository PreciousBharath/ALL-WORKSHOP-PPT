"""
================================================================
 DAY 2: CONSENSUS, NETWORKS & WALLETS — COMPLETE INTERACTIVE GUIDE
================================================================
This single program walks through the entire Day 2 topic:

  1. The Consensus Problem        (why agreement is hard)
  2. Consensus Mechanisms Compared (PoW vs PoS vs PBFT vs DPoS)
  3. Wallets & Platforms Explained (hot/cold, custodial, seed phrase)
  4. Hands-on Lab A: Mine a block  (Proof-of-Work)
  5. Hands-on Lab B: Create a wallet (keys & addresses)
  6. Hands-on Lab C: Send a transaction + explorer
  7. Quick Recap Quiz

Run it, pick a number from the menu, and follow along.
Every explanation is written in plain language — no prior
blockchain or coding knowledge required.
================================================================
"""

import hashlib
import secrets
import time


def pause():
    input("\n(Press Enter to continue) ")


def header(title):
    print("\n" + "=" * 65)
    print(f" {title} ")
    print("=" * 65)


# ----------------------------------------------------------------
# SECTION 1: THE CONSENSUS PROBLEM
# ----------------------------------------------------------------
def section_consensus_problem():
    header("1. THE CONSENSUS PROBLEM")
    print("""
Imagine 5 generals surrounding a city, ready to attack. They will
only WIN if they ALL attack at the SAME time. If even one general
attacks alone, they lose.

The problem: they can only send messengers, and some messengers
might be spies (traitors) who change the message or lie.

  Question: How do all HONEST generals agree on the same plan,
  even if some generals are traitors and some messages are lost
  or faked?

This is called the "Byzantine Generals Problem" — and it's
exactly the problem a cryptocurrency network faces:

  - The "generals" = computers (nodes) in the network
  - The "attack plan" = the next block of transactions
  - The "traitors" = malicious or faulty nodes trying to cheat
  - "Winning" = everyone agrees on ONE single, true history

Why does this matter for money? Because if the network can't
agree, someone could spend the same coin twice (double-spending),
or the transaction history could fork into two different
versions ("forks") that disagree with each other.
""")
    print("Real example: 'Orphan blocks' happen when two miners find")
    print("a valid block at almost the same time — the network has")
    print("to pick one and discard ('orphan') the other.")
    pause()


# ----------------------------------------------------------------
# SECTION 2: CONSENSUS MECHANISMS COMPARED
# ----------------------------------------------------------------
MECHANISMS = {
    "1": {
        "name": "Proof of Work (PoW)",
        "used_by": "Bitcoin",
        "how": "Miners compete to solve a hard math puzzle (find a\n"
               "     special number). First to solve it gets to add the\n"
               "     next block and is rewarded with coins.",
        "pros": "Very secure, battle-tested since 2009.",
        "cons": "Uses huge amounts of electricity; slower confirmations.",
    },
    "2": {
        "name": "Proof of Stake (PoS)",
        "used_by": "Ethereum (since 2022)",
        "how": "Instead of solving puzzles, validators 'lock up' (stake)\n"
               "     their own coins as a deposit. The network randomly\n"
               "     picks a validator to add the next block, weighted\n"
               "     by how much they've staked.",
        "pros": "Much less energy use; faster than PoW.",
        "cons": "Rich validators (more coins staked) have more influence.",
    },
    "3": {
        "name": "PBFT (Practical Byzantine Fault Tolerance)",
        "used_by": "Permissioned/enterprise blockchains (e.g. Hyperledger)",
        "how": "A known, fixed set of validators exchange messages and\n"
               "     vote directly. If more than 2/3 agree, the block is\n"
               "     final immediately — no waiting for confirmations.",
        "pros": "Instant finality, very fast for small validator sets.",
        "cons": "Doesn't scale well to thousands of validators.",
    },
    "4": {
        "name": "Delegated Proof of Stake (DPoS)",
        "used_by": "EOS, TRON",
        "how": "Coin holders VOTE for a small number of 'delegates' who\n"
               "     take turns producing blocks on everyone's behalf.",
        "pros": "Very fast and cheap transactions.",
        "cons": "More centralized — power sits with a small group of\n"
                "     elected delegates.",
    },
}


def section_consensus_mechanisms():
    header("2. CONSENSUS MECHANISMS COMPARED")
    print("Different blockchains solve the consensus problem differently.")
    print("Pick a number to learn about each one (or 'all' to see all,")
    print("or 'back' to return to the main menu):\n")
    for key, m in MECHANISMS.items():
        print(f"  {key}. {m['name']}  (used by {m['used_by']})")

    while True:
        choice = input("\nYour choice: ").strip().lower()
        if choice == "back":
            return
        elif choice == "all":
            for m in MECHANISMS.values():
                print(f"\n--- {m['name']} ---")
                print(f"Used by : {m['used_by']}")
                print(f"How it works: {m['how']}")
                print(f"Pros    : {m['pros']}")
                print(f"Cons    : {m['cons']}")
            pause()
            return
        elif choice in MECHANISMS:
            m = MECHANISMS[choice]
            print(f"\n--- {m['name']} ---")
            print(f"Used by : {m['used_by']}")
            print(f"How it works: {m['how']}")
            print(f"Pros    : {m['pros']}")
            print(f"Cons    : {m['cons']}")
            again = input("\nLook at another one? (y/n): ").strip().lower()
            if again != "y":
                return
        else:
            print("Please enter 1-4, 'all', or 'back'.")


# ----------------------------------------------------------------
# SECTION 3: WALLETS & PLATFORMS EXPLAINED
# ----------------------------------------------------------------
def section_wallets_explained():
    header("3. WALLETS & PLATFORMS EXPLAINED")
    print("""
A crypto wallet does NOT actually "store" your coins — the coins
live on the blockchain itself. A wallet just stores the KEYS that
prove you own them, and lets you sign transactions.

  Private Key  = your secret password. Whoever has it can spend
                 your coins. NEVER share it.
  Public Address = derived from your private key. Safe to share —
                 like your bank account number.
  Seed Phrase   = a human-readable backup of your private key,
                 usually 12-24 words (e.g. "apple tiger river...").
                 Anyone with your seed phrase can recreate your
                 wallet and steal your coins.

Two important spectrums to understand:

  HOT WALLET  <-------------------->  COLD WALLET
  (connected to internet,             (offline, e.g. a USB device
   e.g. MetaMask browser extension)    or paper) - much safer for
                                        long-term storage

  CUSTODIAL   <-------------------->  NON-CUSTODIAL
  (a company holds your keys for       (YOU hold your own keys,
   you, e.g. an exchange like            e.g. MetaMask)
   Coinbase - convenient but you
   must trust them)                   "Not your keys, not your coins"
""")
    print("Platform note: Bitcoin, Ethereum, and Solana are different")
    print("blockchains with their own wallets/rules — a Bitcoin wallet")
    print("cannot directly hold Ethereum or Solana coins.")
    pause()


# ----------------------------------------------------------------
# SECTION 4: HANDS-ON LAB A — PROOF OF WORK MINING
# ----------------------------------------------------------------
def calculate_hash(data, nonce):
    return hashlib.sha256(f"{data}{nonce}".encode()).hexdigest()


def mine_block(data, difficulty):
    target = "0" * difficulty
    nonce = 0
    start_time = time.time()
    while True:
        h = calculate_hash(data, nonce)
        if h.startswith(target):
            elapsed = time.time() - start_time
            print(f"\n✅ Block mined!")
            print(f"   Data       : {data}")
            print(f"   Nonce found: {nonce}")
            print(f"   Hash       : {h}")
            print(f"   Attempts   : {nonce + 1}")
            print(f"   Time taken : {elapsed:.4f} seconds")
            return
        nonce += 1
        if nonce % 300000 == 0:
            print(f"   ...still trying, {nonce} attempts so far")


def lab_a_mining():
    header("LAB A: MINE YOUR OWN BLOCK (Proof of Work)")
    print("Type a message, choose a difficulty (1-8), and watch the")
    print("computer brute-force a valid hash. Type 'back' to return.\n")

    while True:
        data = input("Message for your block: ").strip()
        if data.lower() == "back":
            return
        if data == "":
            data = "default block data"

        while True:
            level = input("Difficulty (1-8): ").strip()
            if level.lower() == "back":
                return
            if level.isdigit() and 1 <= int(level) <= 8:
                difficulty = int(level)
                break
            print("Enter a number between 1 and 8.")

        print(f"\nMining with difficulty {difficulty} "
              f"(hash must start with '{'0' * difficulty}')...")
        mine_block(data, difficulty)

        again = input("\nMine another block? (y/n): ").strip().lower()
        if again != "y":
            return


# ----------------------------------------------------------------
# SECTION 5: HANDS-ON LAB B — WALLET CREATION
# ----------------------------------------------------------------
wallets = {}


def derive_public_address(private_key):
    h1 = hashlib.sha256(private_key.encode()).hexdigest()
    h2 = hashlib.sha256(h1.encode()).hexdigest()
    return "0x" + h2[-40:]


def lab_b_wallets():
    header("LAB B: CREATE YOUR OWN WALLET")
    print("Create wallets by typing names. Each gets a unique private")
    print("key and derived public address. Type 'back' to return.\n")

    while True:
        print("1. Create a new wallet")
        print("2. List all wallets created")
        print("3. Back to main menu")
        choice = input("Choice: ").strip()

        if choice == "1":
            name = input("Wallet name (e.g. your own name): ").strip() or f"wallet{len(wallets)+1}"
            if name in wallets:
                print(f"'{name}' already exists — pick another name.")
                continue
            private_key = secrets.token_hex(32)
            address = derive_public_address(private_key)
            wallets[name] = {"private_key": private_key, "address": address}
            print(f"\n👛 Wallet '{name}' created")
            print(f"   Private Key (SECRET) : {private_key}")
            print(f"   Public Address       : {address}")

        elif choice == "2":
            if not wallets:
                print("\nNo wallets yet.")
            else:
                print("\n--- Wallets so far ---")
                for n, w in wallets.items():
                    print(f"  {n:10s} -> {w['address']}")

        elif choice == "3" or choice.lower() == "back":
            return
        else:
            print("Please enter 1, 2, or 3.")


# ----------------------------------------------------------------
# SECTION 6: HANDS-ON LAB C — TRANSACTION + EXPLORER
# ----------------------------------------------------------------
class Block:
    def __init__(self, index, transactions, previous_hash):
        self.index = index
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self._mine()

    def _calc_hash(self):
        content = f"{self.index}{self.transactions}{self.previous_hash}{self.nonce}"
        return hashlib.sha256(content.encode()).hexdigest()

    def _mine(self, difficulty=3):
        target = "0" * difficulty
        while True:
            h = self._calc_hash()
            if h.startswith(target):
                return h
            self.nonce += 1


class Blockchain:
    def __init__(self):
        self.chain = [Block(0, ["Genesis Block"], "0")]
        self.balances = {}

    def faucet(self, name, amount=10):
        self.balances[name] = self.balances.get(name, 0) + amount
        print(f"🚰 Faucet sent {amount} coins to {name}. "
              f"New balance: {self.balances[name]}")

    def send(self, sender, receiver, amount):
        if self.balances.get(sender, 0) < amount:
            print(f"❌ '{sender}' doesn't have enough coins "
                  f"(has {self.balances.get(sender, 0)}).")
            return
        self.balances.setdefault(receiver, 0)
        tx = f"{sender} -> {receiver} : {amount} coins"
        block = Block(len(self.chain), [tx], self.chain[-1].hash)
        self.chain.append(block)
        self.balances[sender] -= amount
        self.balances[receiver] += amount
        print(f"✅ Confirmed in Block #{block.index}, hash {block.hash[:16]}...")

    def explorer(self):
        print("\n--- Block Explorer ---")
        for b in self.chain:
            print(f"Block #{b.index} | Tx: {b.transactions} | Hash: {b.hash[:16]}...")
        print("\nBalances:")
        for n, bal in self.balances.items():
            print(f"  {n:10s} -> {bal} coins")


def lab_c_transactions():
    header("LAB C: SEND A TRANSACTION + BLOCK EXPLORER")
    print("Simulates: faucet -> send -> explorer, just like a real")
    print("testnet + MetaMask + Etherscan flow. Type 'back' to return.\n")

    chain = Blockchain()
    while True:
        print("1. Claim faucet coins")
        print("2. Send coins")
        print("3. View block explorer")
        print("4. Back to main menu")
        choice = input("Choice: ").strip()

        if choice == "1":
            name = input("Your name: ").strip() or "student"
            chain.faucet(name)
        elif choice == "2":
            sender = input("Sender name: ").strip() or "student"
            receiver = input("Receiver name: ").strip() or "friend"
            amt = input("Amount: ").strip()
            if amt.isdigit():
                chain.send(sender, receiver, int(amt))
            else:
                print("Enter a whole number amount.")
        elif choice == "3":
            chain.explorer()
        elif choice == "4" or choice.lower() == "back":
            return
        else:
            print("Please enter 1, 2, 3, or 4.")


# ----------------------------------------------------------------
# SECTION 7: QUICK RECAP QUIZ
# ----------------------------------------------------------------
QUIZ = [
    ("What does a private key let you do?",
     ["Spend the coins in that wallet", "Only view the balance", "Nothing important"],
     "1"),
    ("Which consensus mechanism does Bitcoin use?",
     ["Proof of Stake", "Proof of Work", "PBFT"],
     "2"),
    ("A 'cold wallet' means:",
     ["It's stored offline, away from the internet", "It has a low balance", "It's frozen/locked by a bank"],
     "1"),
    ("What is a 'fork' in blockchain terms?",
     ["A physical hardware wallet", "The network disagreeing and splitting into two histories", "A type of coin"],
     "2"),
    ("'Not your keys, not your coins' refers to:",
     ["Custodial wallets where a company holds your keys", "Losing your phone", "Mining difficulty"],
     "1"),
]


def section_quiz():
    header("7. QUICK RECAP QUIZ")
    score = 0
    for i, (q, options, correct) in enumerate(QUIZ, 1):
        print(f"\nQ{i}. {q}")
        for idx, opt in enumerate(options, 1):
            print(f"   {idx}. {opt}")
        ans = input("Your answer: ").strip()
        if ans == correct:
            print("✅ Correct!")
            score += 1
        else:
            print(f"❌ Not quite. Correct answer: {options[int(correct)-1]}")
    print(f"\nFinal score: {score}/{len(QUIZ)}")
    pause()


# ----------------------------------------------------------------
# MAIN MENU
# ----------------------------------------------------------------
def main():
    while True:
        header("DAY 2: CONSENSUS, NETWORKS & WALLETS")
        print("1. The Consensus Problem (concept)")
        print("2. Consensus Mechanisms Compared (concept)")
        print("3. Wallets & Platforms Explained (concept)")
        print("4. Lab A: Mine a Block (hands-on)")
        print("5. Lab B: Create a Wallet (hands-on)")
        print("6. Lab C: Send a Transaction + Explorer (hands-on)")
        print("7. Quick Recap Quiz")
        print("8. Exit")

        choice = input("\nChoose an option (1-8): ").strip()

        if choice == "1":
            section_consensus_problem()
        elif choice == "2":
            section_consensus_mechanisms()
        elif choice == "3":
            section_wallets_explained()
        elif choice == "4":
            lab_a_mining()
        elif choice == "5":
            lab_b_wallets()
        elif choice == "6":
            lab_c_transactions()
        elif choice == "7":
            section_quiz()
        elif choice == "8":
            print("\nSession complete. Great work today! 👋")
            break
        else:
            print("Please enter a number between 1 and 8.")


if __name__ == "__main__":
    main()
