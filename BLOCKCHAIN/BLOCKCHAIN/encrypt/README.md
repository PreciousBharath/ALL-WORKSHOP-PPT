# Crypto and Blockchain Demo

This educational Python program demonstrates:

- AES-GCM encryption and decryption
- DES-CBC encryption and decryption (legacy; included only for learning)
- RSA-OAEP encryption and decryption
- Blockchain classes are included in the source as a related hashing example.

## Run it

From this folder:

```powershell
python -m pip install -r requirements.txt
python crypto_blockchain_demo.py
```

The menu uses this order:

```text
1. SHA-256 hash
2. Create blockchain block
3. Run demo checks
4. AES encrypt
5. AES decrypt
6. DES encrypt
7. DES decrypt
8. RSA encrypt
9. RSA decrypt
0. Exit
```

Choose `4`, enter a message, then enter a password. Copy the complete Base64 result, choose `5`, paste it, and enter the same password to see the decrypted message. The program generates and displays an RSA public/private key pair at startup. Option `8` automatically uses the public key, and option `9` automatically uses the matching private key. Option `1` hashes text, option `2` creates and validates a blockchain block, and option `3` runs the built-in checks.

Encryption returns Base64 text. Copy the complete Base64 output and paste it into the matching decrypt option. AES and DES use the same password for both operations. RSA encryption and decryption automatically use the matching temporary key pair shown at startup. The keys change each time the program starts.

For a quick non-interactive developer check, call `demo()` from Python. It tests AES, DES, RSA, and blockchain validation.

## How it works

- AES uses one password-derived shared key, authenticated GCM mode, a random nonce, and a tag. Decryption checks the tag, so modified data or a wrong password fails.
- DES uses one shared password, an initialization vector, and padded CBC ciphertext. DES is obsolete and should not protect real data.
- RSA uses a public/private key pair and OAEP padding. Anyone can encrypt with the public key; only the matching private key can decrypt.
- Encryption changes readable plaintext into Base64 ciphertext. Decryption reverses that process only with the correct password or key.

This is a learning project, not a production wallet, cryptocurrency, or key-management system.
