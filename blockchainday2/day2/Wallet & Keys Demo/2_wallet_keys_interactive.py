"""
LAB 2 (INTERACTIVE): WALLET & KEYS
-------------------------------------
Students type a name and get their own private key + public
address generated on the spot. They can create multiple wallets
and see that every one is unique and random.
"""

import hashlib
import secrets

wallets = {}  # store created wallets in memory for this session


def generate_private_key():
    return secrets.token_hex(32)


def derive_public_address(private_key):
    hash1 = hashlib.sha256(private_key.encode()).hexdigest()
    hash2 = hashlib.sha256(hash1.encode()).hexdigest()
    return "0x" + hash2[-40:]


def create_wallet(name):
    private_key = generate_private_key()
    address = derive_public_address(private_key)
    wallets[name] = {"private_key": private_key, "address": address}
    print(f"\n👛 Wallet created for '{name}'")
    print(f"   Private Key (SECRET, never share) : {private_key}")
    print(f"   Public Address (safe to share)     : {address}")


def list_wallets():
    if not wallets:
        print("\nNo wallets created yet.")
        return
    print("\n--- All wallets created this session ---")
    for name, w in wallets.items():
        print(f"  {name:10s} -> {w['address']}")


def check_uniqueness():
    addresses = [w["address"] for w in wallets.values()]
    if len(addresses) != len(set(addresses)):
        print("\n⚠️ Duplicate addresses found (this should never happen)!")
    else:
        print("\n✅ Every wallet address generated is unique, "
              "just like in real crypto wallets.")


def find_wallet_by_address():
    address = input("\nEnter a public address to look up: ").strip().lower()
    for name, wallet in wallets.items():
        if wallet["address"].lower() == address:
            print(f"✅ This address belongs to the wallet named '{name}'.")
            return

    print("❌ No wallet with that address was found in this session.")


def main():
    print("=" * 60)
    print(" WALLET & KEY GENERATION — TRY IT YOURSELF ")
    print("=" * 60)

    while True:
        print("\nWhat would you like to do?")
        print("  1. Create a new wallet")
        print("  2. List all wallets created so far")
        print("  3. Check that all addresses are unique")
        print("  4. Find a wallet by address")
        print("  5. Quit")1
        choice = input("Enter choice (1-5): ").strip()

        if choice == "1":
            name = input("Enter a name for this wallet (e.g. your own name): ").strip()
            if not name:
                name = f"wallet{len(wallets) + 1}"
            if name in wallets:
                print(f"'{name}' already exists — pick a different name.")
                continue
            create_wallet(name)

        elif choice == "2":
            list_wallets()

        elif choice == "3":
            check_uniqueness()

        elif choice == "4":
            find_wallet_by_address()

        elif choice == "5":
            print("Session ended. Remember: never share your private key! 👋")
            break

        else:
            print("Please enter a number between 1 and 5.")


if __name__ == "__main__":
    main()
