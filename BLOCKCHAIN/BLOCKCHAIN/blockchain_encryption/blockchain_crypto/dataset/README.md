# Dataset Contents

## Overview
This dataset contains various file types for testing the CryptoChain encryption system.

## File Types & Descriptions

### Text Documents
- **sample_document.txt**: Confidential security documentation about the blockchain encryption system
- **implementation_notes.txt**: Technical implementation details and architecture notes
- **encryption_guide.md**: User guide and best practices for encryption and decryption

### Data Files
- **user_credentials.json**: Sample user credentials and system configuration data
- **company_data.json**: Organizational structure, employees, and project information
- **financial_report.csv**: Financial transactions and revenue data
- **financial_data_2026.csv**: Quarterly financial analysis and year-over-year growth metrics

## Usage Instructions

### For Encryption Testing
1. Navigate to the Encrypt section
2. Select any file from this dataset
3. Enter a strong password (e.g., "SecurePass123!")
4. Confirm password
5. Click "Encrypt File"
6. Download the encrypted file

### For Decryption Testing
1. Use previously encrypted files from the dataset
2. Navigate to Decrypt section
3. Upload the .enc file
4. Enter original filename
5. Enter the password used during encryption
6. Click "Decrypt & Download"

### For Hash Verification
1. Go to Tools section
2. Select a file
3. Click "Calculate Hash"
4. Note the SHA-256 hash
5. After encryption/decryption, verify the hash hasn't changed

### For File Analysis
1. Select any file from Tools section
2. Click "Analyze File"
3. View file information and SHA-256 hash

## Security Testing Scenarios

### Scenario 1: Single File Encryption
1. Encrypt sample_document.txt with password "Password123!"
2. Verify file appears in blockchain
3. Download and decrypt the file
4. Confirm content matches original

### Scenario 2: Multiple File Encryption
1. Encrypt all CSV files with different passwords
2. Check blockchain contains all transactions
3. Verify chain integrity

### Scenario 3: Password Strength Testing
1. Try weak password (less than 6 chars) - should fail
2. Try strong password (mixed case, numbers, symbols) - should succeed
3. Verify password strength indicator

### Scenario 4: Hash Integrity Testing
1. Calculate hash of original file
2. Encrypt file
3. Decrypt file
4. Calculate hash of decrypted file
5. Compare hashes - should match

### Scenario 5: Blockchain Verification
1. Encrypt multiple files
2. Click "Refresh Ledger" to view blockchain
3. Click "Verify Chain" to check integrity
4. Verify all blocks are valid

## File Statistics

| File | Type | Size | Purpose |
|------|------|------|---------|
| sample_document.txt | Text | 1.3 KB | Confidential document |
| user_credentials.json | JSON | 1.2 KB | User data sample |
| company_data.json | JSON | 1.8 KB | Organizational data |
| financial_report.csv | CSV | 1.1 KB | Transaction history |
| financial_data_2026.csv | CSV | 1.5 KB | Revenue analysis |
| implementation_notes.txt | Text | 2.9 KB | Technical documentation |
| encryption_guide.md | Markdown | 3.3 KB | User guide |

## Recommended Test Passwords

- **Simple**: `Test123!`
- **Medium**: `MySecure@Pass2026`
- **Strong**: `CryptoChain#Secure$Pass2026!`
- **Complex**: `X9#kL2@mP5$nQ7!rS3^tU6%vW8&`

## Notes

- All files are designed for testing purposes only
- No sensitive real data is contained in demo files
- Files support all encryption, decryption, and hashing operations
- Perfect for learning how the CryptoChain system works

## Support

For questions about the dataset or CryptoChain system, contact: support@cryptochain.com

Last Updated: August 19, 2026