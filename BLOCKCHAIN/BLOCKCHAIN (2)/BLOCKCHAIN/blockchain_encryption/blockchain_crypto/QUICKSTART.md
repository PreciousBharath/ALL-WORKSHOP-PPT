# 🚀 Quick Start Guide

Get BlockChain File Encryption up and running in 2 minutes!

## Prerequisites
- Python 3.8 or higher installed
- Internet connection (for initial setup)

## Installation & Running

### Windows Users

**Easiest Method:**
1. Extract the ZIP file
2. Double-click `run.bat`
3. Wait for the application to start
4. Your browser will open automatically

**Manual Method:**
```bash
cd blockchain_crypto
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

### macOS & Linux Users

**Easiest Method:**
```bash
cd blockchain_crypto
chmod +x run.sh
./run.sh
```

**Manual Method:**
```bash
cd blockchain_crypto
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 app.py
```

## Access the Application

Once running, open your browser and go to:
```
http://localhost:5000
```

## First Steps

### 1. Encrypt Your First File
- Click **"Encrypt"** in the menu
- Select a file (try with a text document first)
- Create a **strong password** (mix of letters, numbers, symbols)
- Click **"Encrypt File"**
- ✅ File is now encrypted!

### 2. View the Blockchain
- Click **"Blockchain"** in the menu
- See your encryption operation recorded
- Click **"Verify Chain"** to check integrity
- Notice the hash chain of blocks

### 3. Decrypt a File
- Click **"Decrypt"** in the menu
- Upload your encrypted file
- Enter the **original filename** (e.g., document.txt)
- Enter your **password**
- Click **"Decrypt & Download"**
- ✅ File is decrypted and downloaded!

## File Types Supported

| Type | Extensions | Icon |
|------|-----------|------|
| Documents | .doc, .docx, .txt | 📄 |
| PDF | .pdf | 📕 |
| Images | .jpg, .png, .gif, .bmp | 🖼️ |
| Spreadsheets | .xlsx, .xls, .csv | 📊 |
| Presentations | .pptx, .ppt | 🎨 |
| Audio | .mp3, .wav, .flac | 🎵 |
| Video | .mp4, .avi, .mov | 🎬 |
| Archives | .zip, .rar, .7z | 📦 |

## Important ⚠️

1. **Save Your Password** - If you forget it, the file is lost forever
2. **Keep Encrypted Files** - They're unreadable without the password
3. **Share Safely** - Send encrypted files and password separately
4. **Backup** - Always keep backups of important original files

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl + Shift + E` | Jump to Encrypt |
| `Ctrl + Shift + D` | Jump to Decrypt |
| `Ctrl + Shift + B` | Jump to Blockchain |

## Troubleshooting

### "Port already in use"
```bash
# Windows: Find process using port 5000
netstat -ano | findstr :5000

# macOS/Linux: Find process
lsof -i :5000

# Then kill the process or use a different port in app.py
```

### "Python not found"
Make sure Python is installed and added to PATH:
```bash
python --version
```

### "Module not found"
Reinstall requirements:
```bash
pip install -r requirements.txt --upgrade
```

### "Permission denied" (macOS/Linux)
Make the script executable:
```bash
chmod +x run.sh
```

## Tips & Tricks

### Creating Secure Passwords
✅ **Good Password:**
```
Th1s!Is@MyStr0ng#Pass
```
- 20+ characters
- Mix of uppercase, lowercase, numbers, symbols

❌ **Bad Password:**
```
password123
```
- Too short
- Predictable
- Easily guessed

### Testing the Application
1. **Create a test file** with some text
2. **Encrypt it** with a strong password
3. **Try wrong password** - see error message
4. **Decrypt with correct password** - see it work
5. **Check blockchain** - see the transaction history

## Features Explained

### 🔐 AES-256 Encryption
- Military-grade encryption standard
- Used by governments and banks
- File size increases slightly due to encryption metadata

### ⛓️ Blockchain Ledger
- Every operation is recorded
- Impossible to tamper with (with verification)
- Shows operation history with timestamps

### 📊 Statistics Dashboard
- Track total operations
- Monitor files encrypted/decrypted
- See data processing metrics

### 🔍 Blockchain Verification
- Verify chain hasn't been tampered with
- Check all block hashes
- Confirm Proof of Work

## Performance Notes

- **Small files** (< 10 MB): Instant encryption/decryption
- **Medium files** (10-100 MB): A few seconds
- **Large files** (100+ MB): May take longer, check browser

## Security Notes

- Encrypted files stored with salt for security
- Passwords never stored or logged
- PBKDF2 key derivation with 100,000 iterations
- SHA-256 hashing throughout

## Need More Help?

Check the full README.md for:
- Detailed API documentation
- Advanced configuration
- Production deployment
- Technical architecture

## Next Steps

After mastering the basics:
1. Try encrypting different file types
2. Experiment with blockchain verification
3. Share encrypted files with friends
4. Explore the blockchain ledger details

---

**Enjoy your secure file encryption! 🎉**
