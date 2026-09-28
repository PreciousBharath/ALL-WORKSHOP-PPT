"""Educational CLI for hashing, blockchain blocks, and classic cryptography.

Install the dependency first:
    p

Run:
    python crypto_blockchain_demo.py
"""

from __future__ import annotations

import base64
import hashlib
import json
import re
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any

from Crypto.Cipher import AES, DES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad


# ---------- Shared helpers ----------


def encode_bytes(value: bytes) -> str:
    """Make binary ciphertext safe to copy and display as text."""
    return base64.b64encode(value).decode("ascii")


def decode_text(value: str) -> bytes:
    try:
        return base64.b64decode(value.encode("ascii"), validate=True)
    except (ValueError, UnicodeEncodeError) as error:
        raise ValueError("Ciphertext must be valid Base64 text.") from error


def read_required(prompt: str) -> str:
    value = input(prompt).strip()
    if not value:
        raise ValueError("Input cannot be empty.")
    return value


def read_rsa_key(prompt: str) -> str:
    key = read_required(prompt)
    if key in {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9"}:
        raise ValueError(
            "RSA operation still needs the complete key. Paste the key, or press Ctrl+C to cancel."
        )
    return key


# ---------- Blockchain ----------


@dataclass
class Block:
    index: int
    timestamp: str
    data: str
    previous_hash: str
    nonce: int = 0

    def hash(self) -> str:
        block_data = json.dumps(asdict(self), sort_keys=True).encode("utf-8")
        return hashlib.sha256(block_data).hexdigest()


class Blockchain:
    def __init__(self) -> None:
        self.chain = [
            Block(
                index=0,
                timestamp=datetime.now(timezone.utc).isoformat(),
                data="Genesis block",
                previous_hash="0",
            )
        ]

    def add_block(self, data: str) -> Block:
        previous_block = self.chain[-1]
        new_block = Block(
            index=len(self.chain),
            timestamp=datetime.now(timezone.utc).isoformat(),
            data=data,
            previous_hash=previous_block.hash(),
        )
        self.chain.append(new_block)
        return new_block

    def is_valid(self) -> bool:
        for current, previous in zip(self.chain[1:], self.chain):
            if current.previous_hash != previous.hash():
                return False
        return True

    def show(self) -> None:
        for block in self.chain:
            print(json.dumps({**asdict(block), "hash": block.hash()}, indent=2))


# ---------- AES ----------


def aes_encrypt(message: str, password: str) -> str:
    key = hashlib.sha256(password.encode("utf-8")).digest()
    cipher = AES.new(key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(message.encode("utf-8"))
    return encode_bytes(cipher.nonce + tag + ciphertext)


def aes_decrypt(token: str, password: str) -> str:
    raw = decode_text(token)
    nonce, tag, ciphertext = raw[:16], raw[16:32], raw[32:]
    key = hashlib.sha256(password.encode("utf-8")).digest()
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    try:
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)
    except ValueError as error:
        raise ValueError("AES decryption failed: wrong password or modified data.") from error
    return plaintext.decode("utf-8")


# ---------- DES ----------


def des_key(password: str) -> bytes:
    # DES is retained for learning only; use AES for real applications.
    return hashlib.sha256(password.encode("utf-8")).digest()[:8]


def des_encrypt(message: str, password: str) -> str:
    iv = get_random_bytes(DES.block_size)
    cipher = DES.new(des_key(password), DES.MODE_CBC, iv=iv)
    ciphertext = cipher.encrypt(pad(message.encode("utf-8"), DES.block_size))
    return encode_bytes(iv + ciphertext)


def des_decrypt(token: str, password: str) -> str:
    raw = decode_text(token)
    iv, ciphertext = raw[:8], raw[8:]
    cipher = DES.new(des_key(password), DES.MODE_CBC, iv=iv)
    try:
        plaintext = unpad(cipher.decrypt(ciphertext), DES.block_size)
    except ValueError as error:
        raise ValueError("DES decryption failed: wrong password or invalid data.") from error
    return plaintext.decode("utf-8")


# ---------- RSA ----------


def import_rsa_key(key_text: str) -> RSA.RsaKey:
    key_text = key_text.strip().replace("\\n", "\n")
    match = re.fullmatch(
        r"-----BEGIN ([A-Z0-9 ]+)-----\s*(.*?)\s*-----END \1-----",
        key_text,
        re.DOTALL,
    )
    if not match:
        raise ValueError(
            "RSA key must be a complete PEM key, including BEGIN and END lines."
        )

    label, body = match.groups()
    pem_key = f"-----BEGIN {label}-----\n{''.join(body.split())}\n-----END {label}-----"
    try:
        return RSA.import_key(pem_key)
    except (ValueError, IndexError, TypeError) as error:
        raise ValueError("RSA key is invalid or has been copied incorrectly.") from error


def rsa_encrypt(message: str, public_key_text: str) -> str:
    public_key = import_rsa_key(public_key_text)
    ciphertext = PKCS1_OAEP.new(public_key).encrypt(message.encode("utf-8"))
    return encode_bytes(ciphertext)


def rsa_decrypt(token: str, private_key_text: str) -> str:
    private_key = import_rsa_key(private_key_text)
    try:
        plaintext = PKCS1_OAEP.new(private_key).decrypt(decode_text(token))
    except (ValueError, TypeError) as error:
        raise ValueError("RSA decryption failed: wrong private key or modified data.") from error
    return plaintext.decode("utf-8")


def new_rsa_key_pair() -> tuple[str, str]:
    private_key = RSA.generate(2048)
    return private_key.publickey().export_key().decode("ascii"), private_key.export_key().decode("ascii")


# ---------- CLI ----------


def print_result(label: str, value: Any) -> None:
    print(f"\n{label}:\n{value}\n")


def run_hash() -> None:
    message = read_required("Enter text to hash: ")
    digest = hashlib.sha256(message.encode("utf-8")).hexdigest()
    print_result("SHA-256 hash", digest)


def run_blockchain() -> None:
    data = read_required("Enter block data: ")
    chain = Blockchain()
    block = chain.add_block(data)
    print_result("New block", json.dumps({**asdict(block), "hash": block.hash()}, indent=2))
    print(f"Blockchain valid: {'yes' if chain.is_valid() else 'no'}")


def show_crypto_help(algorithm: str, encrypt: bool) -> None:
    operation = "encryption" if encrypt else "decryption"
    print(f"\n{algorithm} {operation}")
    if algorithm == "AES":
        print("AES uses one shared password for both encryption and decryption.")
        print("It creates a new random nonce and an authentication tag each time.")
        print("Use the same password and the complete Base64 output to decrypt.")
    elif algorithm == "DES":
        print("DES uses one shared password and an initialization vector.")
        print("DES is old and less secure than AES; use it only for learning.")
        print("Use the same password and the complete Base64 output to decrypt.")
    else:
        print("RSA uses two keys: a public key and a private key.")
        print("Encrypt with the public key; decrypt with the matching private key.")
        print("The RSA ciphertext is longer than the original message.")


def run_crypto(
    encrypt: bool,
    algorithm: str,
    rsa_public: str,
    rsa_private: str,
) -> None:
    show_crypto_help(algorithm, encrypt)
    if encrypt:
        message_or_token = read_required("Enter message: ")
    else:
        message_or_token = read_required("Paste the complete Base64 ciphertext: ")
    if algorithm == "RSA":
        key = rsa_public if encrypt else rsa_private
        key_label = "RSA public key used for encryption" if encrypt else "RSA private key used for decryption"
        print(f"\n{key_label}:\n{key}")
    else:
        key_prompt = "Enter password"
        print("The result will appear after the next input.")
        key = read_required(f"{key_prompt}: ")

    if algorithm == "AES":
        result = aes_encrypt(message_or_token, key) if encrypt else aes_decrypt(message_or_token, key)
    elif algorithm == "DES":
        result = des_encrypt(message_or_token, key) if encrypt else des_decrypt(message_or_token, key)
    else:
        result = rsa_encrypt(message_or_token, key) if encrypt else rsa_decrypt(message_or_token, key)
    print_result("Encrypted Base64" if encrypt else "Decrypted message", result)


def demo() -> None:
    print("Running round-trip checks...")
    for name, encrypt, decrypt in (
        ("AES", lambda: aes_encrypt("Hello AES", "secret"), lambda token: aes_decrypt(token, "secret")),
        ("DES", lambda: des_encrypt("Hello DES", "secret"), lambda token: des_decrypt(token, "secret")),
    ):
        token = encrypt()
        assert decrypt(token).startswith("Hello")
        print(f"{name}: OK")

    public_key, private_key = new_rsa_key_pair()
    token = rsa_encrypt("Hello RSA", public_key)
    assert rsa_decrypt(token, private_key) == "Hello RSA"
    print("RSA: OK")

    chain = Blockchain()
    chain.add_block("Alice pays Bob 5 coins")
    assert chain.is_valid()
    print("Blockchain validation: OK")


def main() -> None:
    rsa_public, rsa_private = new_rsa_key_pair()
    print("Educational Crypto + Blockchain Demo")
    print("Choose encryption first, then use the matching decryption option.")
    print("RSA keys generated automatically for this session.")
    print(f"\nRSA PUBLIC KEY (used automatically by option 8):\n{rsa_public}")
    print(f"\nRSA PRIVATE KEY (used automatically by option 9; keep it secret):\n{rsa_private}")

    while True:
        print("\n1. SHA-256 hash")
        print("2. Create blockchain block")
        print("3. Run demo checks")
        print("4. AES encrypt\n5. AES decrypt")
        print("6. DES encrypt\n7. DES decrypt")
        print("8. RSA encrypt\n9. RSA decrypt\n0. Exit")
        try:
            choice = input("Choose an option: ").strip()
            if choice == "1":
                run_hash()
            elif choice == "2":
                run_blockchain()
            elif choice == "3":
                demo()
            elif choice in {"4", "5", "6", "7", "8", "9"}:
                algorithm = "AES" if choice in {"4", "5"} else "DES" if choice in {"6", "7"} else "RSA"
                run_crypto(choice in {"4", "6", "8"}, algorithm, rsa_public, rsa_private)
            elif choice == "0":
                print("Goodbye.")
                return
            else:
                print("Choose a number from the menu.")
        except (ValueError, UnicodeDecodeError, IndexError) as error:
            print(f"Error: {error}")
        except KeyboardInterrupt:
            print("\nOperation cancelled. Goodbye.")
            return


if __name__ == "__main__":
    main()
