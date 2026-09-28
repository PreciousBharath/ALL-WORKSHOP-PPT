# BlockChain File Encryption System

A secure file encryption and decryption application with blockchain-based operation tracking. Encrypt your files with AES-256 encryption and track all operations in a tamper-proof blockchain ledger.

## 🔐 Features

- **Military-Grade Encryption**: AES-256 encryption using Fernet (symmetric encryption)
- **Blockchain Ledger**: All encryption/decryption operations logged in a blockchain
- **Multi-File Support**: Supports documents, PDFs, images, videos, spreadsheets, and more
- **Attractive UI**: Modern, responsive interface with real-time statistics
- **Secure Password Management**: Password strength indicator and validation
- **Blockchain Verification**: Verify blockchain integrity at any time
- **File Hashing**: SHA-256 hashing for file integrity verification
- **Proof of Work**: Simple mining mechanism for blockchain blocks

## 📋 System Requirements

- Python 3.8 or higher
- 200 MB free disk space
- Modern web browser (Chrome, Firefox, Safari, Edge)

## 🚀 Installation

### 1. Extract the Project
```bash
unzip blockchain_crypto.zip
cd blockchain_crypto
```

### 2. Create Virtual Environment (Optional but Recommended)
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

## 🎯 Usage

### Start the Application
```bash
python app.py
```

The application will start on `http://localhost:5000`

### Access the Web Interface
Open your browser and navigate to:
```
http://localhost:5000
```

## 📖 How to Use

### Encrypting a File

1. **Navigate to Encrypt Section**
   - Click "Encrypt" in the navigation menu or click "Start Encrypting" button

2. **Select File**
   - Click on the file input area or drag and drop a file
   - Supported formats: documents, PDFs, images, videos, spreadsheets, etc.

3. **Set Password**
   - Enter a strong password (minimum 6 characters)
   - Password strength indicator shows security level
   - Confirm the password

4. **Encrypt**
   - Click "Encrypt File" button
   - Wait for the encryption to complete
   - The encrypted file is stored internally
   - Blockchain record is created automatically

### Decrypting a File

1. **Navigate to Decrypt Section**
   - Click "Decrypt" in the navigation menu

2. **Upload Encrypted File**
   - Select the encrypted file you received

3. **Enter Details**
   - Enter the original filename (with extension)
   - Enter the decryption password

4. **Decrypt**
   - Click "Decrypt & Download" button
   - The file will be decrypted and automatically downloaded
   - Blockchain record is created

### View Blockchain

1. **Navigate to Blockchain Section**
   - Click "Blockchain" in the navigation menu

2. **View Ledger**
   - See all encryption/decryption operations
   - Each block shows: operation type, file name, file type, size, hashes, and timestamp

3. **Verify Blockchain**
   - Click "Verify Chain" button
   - Verifies integrity of all blocks
   - Ensures no tampering has occurred

## 🔒 Security Features

### Encryption
- **Algorithm**: Fernet (symmetric encryption based on AES-128)
- **Key Derivation**: PBKDF2 with SHA-256
- **Iterations**: 100,000 iterations for key derivation
- **Salt**: 16-byte random salt for each encryption

### Blockchain
- **Hash Algorithm**: SHA-256
- **Proof of Work**: Mining mechanism with configurable difficulty
- **Block Structure**: Index, timestamp, transaction, previous hash, nonce, hash
- **Verification**: Complete blockchain validation on demand

### File Protection
- **File Hashing**: SHA-256 hashing for integrity verification
- **Format**: Encrypted files stored with salt prepended for authentication

## 📁 Project Structure

```
blockchain_crypto/
├── app.py                  # Main Flask application
├── blockchain.py           # Blockchain implementation
├── crypto_utils.py         # Encryption/decryption utilities
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── templates/
│   └── index.html         # Main HTML template
├── static/
│   ├── style.css          # CSS styling
│   └── script.js          # JavaScript interactions
└── uploads/               # Directory for encrypted files (auto-created)
```

## 🔑 Password Security Tips

1. **Use Strong Passwords**
   - Mix uppercase and lowercase letters
   - Include numbers and special characters
   - Minimum 12 characters recommended

2. **Never Share Passwords**
   - Only share encrypted files, not passwords
   - Use secure channels to communicate passwords

3. **Remember Your Passwords**
   - If you forget the password, the file cannot be decrypted
   - No recovery option available

4. **Unique Passwords**
   - Use different passwords for different files
   - Don't reuse passwords across files

## 📊 API Endpoints

### Encrypt File
```
POST /api/encrypt
Form Data:
  - file: (binary file data)
  - password: (string)

Response:
  {
    "success": true,
    "file_id": "abc123",
    "filename": "document.pdf",
    "file_type": "PDF",
    "file_size": 1024000
  }
```

### Decrypt File
```
POST /api/decrypt
Form Data:
  - file: (binary encrypted file)
  - password: (string)
  - original_filename: (string)

Response: Downloads decrypted file
```

### Get Blockchain
```
GET /api/blockchain

Response:
  {
    "success": true,
    "total_blocks": 10,
    "blocks": [...]
  }
```

### Get Statistics
```
GET /api/blockchain/stats

Response:
  {
    "success": true,
    "total_operations": 5,
    "encrypted_files": 3,
    "decrypted_files": 2,
    "total_size_mb": 45.5
  }
```

### Verify Blockchain
```
GET /api/blockchain/verify

Response:
  {
    "success": true,
    "is_valid": true,
    "message": "Blockchain is valid"
  }
```

## 🛠️ Configuration

Edit `app.py` to modify:

```python
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # Max file size (100MB)
blockchain = Blockchain(difficulty=2)  # Mining difficulty
app.run(debug=True, host='0.0.0.0', port=5000)  # Host and port
```

## 🐛 Troubleshooting

### Port Already in Use
If port 5000 is already in use:
```bash
# Windows
netstat -ano | findstr :5000

# macOS/Linux
lsof -i :5000
```

Then modify the port in `app.py`:
```python
app.run(port=5001)  # Use different port
```

### Permission Denied (uploads folder)
Ensure the `uploads` folder has write permissions:
```bash
chmod 755 uploads  # macOS/Linux
```

### Module Not Found
Reinstall dependencies:
```bash
pip install -r requirements.txt --upgrade
```

### Decryption Failed
- Verify you're using the correct password
- Ensure the file is a valid encrypted file
- Check if the file hasn't been corrupted

## ⚠️ Important Notes

1. **Backup Your Files**
   - Always keep backups of important files
   - Encryption is secure but irreversible

2. **Password Recovery**
   - No password recovery mechanism exists
   - Lost passwords mean lost access to files

3. **File Integrity**
   - Don't modify encrypted files
   - Corruption will prevent decryption

4. **Blockchain Data**
   - Blockchain data is stored in memory
   - Data is lost when application restarts
   - Use blockchain verification to ensure integrity

5. **Development Mode**
   - Current setup uses Flask development server
   - For production, use a proper WSGI server (Gunicorn, etc.)

## 🚀 Production Deployment

For production use:

```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 📝 License

This project is provided as-is for educational and personal use.

## 👨‍💻 Technical Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Encryption**: cryptography library (Fernet/AES)
- **Blockchain**: Custom implementation
- **Hashing**: SHA-256

## 🤝 Support

For issues or questions:
1. Check the Troubleshooting section
2. Verify all dependencies are installed
3. Ensure Python version is 3.8 or higher
4. Check browser console for JavaScript errors

## 📚 Learning Resources

- [Cryptography Library Docs](https://cryptography.io/)
- [Blockchain Basics](https://en.wikipedia.org/wiki/Blockchain)
- [AES Encryption](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard)
- [PBKDF2](https://en.wikipedia.org/wiki/PBKDF2)

---

**Created**: 2024
**Status**: Active Development
**Version**: 1.0.0
