from flask import Flask, render_template, request, jsonify, send_file, session
from werkzeug.utils import secure_filename
import os
import uuid
from datetime import datetime
from blockchain import Blockchain
from crypto_utils import encrypt_file, decrypt_file, hash_file
import json
import io

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max

# Initialize blockchain
blockchain = Blockchain()

# Create uploads folder if not exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {
    'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'docx', 'doc', 
    'xlsx', 'xls', 'pptx', 'ppt', 'zip', 'rar', '7z', 'mp3', 
    'mp4', 'avi', 'mov', 'csv', 'json'
}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_file_type(filename):
    """Categorize file type"""
    ext = filename.rsplit('.', 1)[1].lower()
    
    if ext in ['doc', 'docx', 'txt']:
        return 'Document'
    elif ext == 'pdf':
        return 'PDF'
    elif ext in ['jpg', 'jpeg', 'png', 'gif']:
        return 'Image'
    elif ext in ['xlsx', 'xls', 'csv']:
        return 'Spreadsheet'
    elif ext in ['pptx', 'ppt']:
        return 'Presentation'
    elif ext in ['mp3', 'wav', 'flac']:
        return 'Audio'
    elif ext in ['mp4', 'avi', 'mov', 'mkv']:
        return 'Video'
    elif ext in ['zip', 'rar', '7z']:
        return 'Archive'
    else:
        return 'File'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/encrypt', methods=['POST'])
def encrypt():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        password = request.form.get('password')
        
        if not file or not password:
            return jsonify({'error': 'File and password required'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'File type not allowed'}), 400
        
        if len(password) < 6:
            return jsonify({'error': 'Password must be at least 6 characters'}), 400
        
        # Read file content
        file_content = file.read()
        original_filename = secure_filename(file.filename)
        file_type = get_file_type(original_filename)
        
        # Encrypt the file
        encrypted_content = encrypt_file(file_content, password)
        
        # Generate unique ID and hash
        file_id = str(uuid.uuid4())[:8]
        file_hash = hash_file(file_content)
        encrypted_hash = hash_file(encrypted_content)
        
        # Save encrypted file
        encrypted_filename = f"{file_id}_{original_filename}.enc"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], encrypted_filename)
        
        with open(filepath, 'wb') as f:
            f.write(encrypted_content)
        
        # Create blockchain record
        transaction = {
            'file_id': file_id,
            'original_filename': original_filename,
            'file_type': file_type,
            'file_size': len(file_content),
            'original_hash': file_hash,
            'encrypted_hash': encrypted_hash,
            'encrypted_filename': encrypted_filename,
            'timestamp': datetime.now().isoformat(),
            'operation': 'ENCRYPT',
            'status': 'SUCCESS'
        }
        
        blockchain.add_transaction(transaction)
        
        return jsonify({
            'success': True,
            'file_id': file_id,
            'filename': original_filename,
            'file_type': file_type,
            'file_size': len(file_content),
            'encrypted_filename': encrypted_filename,
            'download_url': f'/api/download-encrypted/{file_id}',
            'message': 'File encrypted successfully!'
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/decrypt', methods=['POST'])
def decrypt():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        password = request.form.get('password')
        
        if not file or not password:
            return jsonify({'error': 'File and password required'}), 400
        
        # Read encrypted file
        encrypted_content = file.read()
        original_filename = request.form.get('original_filename', 'decrypted_file')
        
        try:
            # Decrypt the file
            decrypted_content = decrypt_file(encrypted_content, password)
        except Exception as e:
            return jsonify({'error': 'Decryption failed - wrong password or corrupted file'}), 400
        
        # Get file ID from filename
        file_id = secure_filename(file.filename).split('_')[0] if '_' in file.filename else str(uuid.uuid4())[:8]
        
        # Create blockchain record
        transaction = {
            'file_id': file_id,
            'original_filename': original_filename,
            'file_size': len(decrypted_content),
            'timestamp': datetime.now().isoformat(),
            'operation': 'DECRYPT',
            'status': 'SUCCESS'
        }
        
        blockchain.add_transaction(transaction)
        
        # Return decrypted file
        return send_file(
            io.BytesIO(decrypted_content),
            as_attachment=True,
            download_name=original_filename
        )
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/download-encrypted/<file_id>', methods=['GET'])
def download_encrypted(file_id):
    """Download encrypted file by file ID"""
    try:
        # Find the encrypted file
        uploads_dir = app.config['UPLOAD_FOLDER']
        
        # Search for file starting with the file_id
        for filename in os.listdir(uploads_dir):
            if filename.startswith(file_id) and filename.endswith('.enc'):
                filepath = os.path.join(uploads_dir, filename)
                return send_file(
                    filepath,
                    as_attachment=True,
                    download_name=filename
                )
        
        return jsonify({'error': 'Encrypted file not found'}), 404
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/blockchain', methods=['GET'])
def get_blockchain():
    try:
        chain = blockchain.get_chain()
        return jsonify({
            'success': True,
            'total_blocks': len(chain),
            'blocks': chain
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/blockchain/stats', methods=['GET'])
def get_stats():
    try:
        chain = blockchain.get_chain()
        
        total_operations = 0
        encrypted_files = 0
        decrypted_files = 0
        total_size = 0
        
        for block in chain:
            if 'transaction' in block:
                trans = block['transaction']
                total_operations += 1
                if trans.get('operation') == 'ENCRYPT':
                    encrypted_files += 1
                    total_size += trans.get('file_size', 0)
                elif trans.get('operation') == 'DECRYPT':
                    decrypted_files += 1
        
        return jsonify({
            'success': True,
            'total_operations': total_operations,
            'encrypted_files': encrypted_files,
            'decrypted_files': decrypted_files,
            'total_size_mb': round(total_size / (1024*1024), 2)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/blockchain/verify', methods=['GET'])
def verify_blockchain():
    try:
        is_valid = blockchain.is_valid()
        return jsonify({
            'success': True,
            'is_valid': is_valid,
            'message': 'Blockchain is valid' if is_valid else 'Blockchain has been tampered with!'
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/blockchain/search', methods=['GET'])
def search_blockchain():
    """Search blockchain by file ID or filename"""
    try:
        query = request.args.get('q', '').lower()
        chain = blockchain.get_chain()
        results = []
        
        for block in chain:
            if 'transaction' in block:
                trans = block['transaction']
                if (query in str(trans.get('file_id', '')).lower() or 
                    query in str(trans.get('original_filename', '')).lower()):
                    results.append({
                        'block_index': block['index'],
                        'timestamp': block['timestamp'],
                        'transaction': trans,
                        'hash': block['hash']
                    })
        
        return jsonify({
            'success': True,
            'query': query,
            'results_count': len(results),
            'results': results
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/file-info', methods=['POST'])
def get_file_info():
    """Get detailed information about an encrypted file"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if not file:
            return jsonify({'error': 'File required'}), 400
        
        file_content = file.read()
        original_filename = secure_filename(file.filename)
        file_type = get_file_type(original_filename)
        file_hash = hash_file(file_content)
        
        return jsonify({
            'success': True,
            'filename': original_filename,
            'file_type': file_type,
            'file_size': len(file_content),
            'file_size_mb': round(len(file_content) / (1024*1024), 2),
            'sha256_hash': file_hash,
            'encryption_status': 'encrypted' if original_filename.endswith('.enc') else 'unencrypted'
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/crypto-info', methods=['GET'])
def get_crypto_info():
    """Get detailed cryptography information"""
    try:
        chain = blockchain.get_chain()
        total_blocks = len(chain)
        
        # Calculate average nonce across blocks
        total_nonce = sum(block.get('nonce', 0) for block in chain)
        avg_nonce = total_nonce / total_blocks if total_blocks > 0 else 0
        
        return jsonify({
            'success': True,
            'encryption_algorithm': 'AES-256 (Fernet)',
            'key_derivation': 'PBKDF2-SHA256 (100,000 iterations)',
            'hashing_algorithm': 'SHA-256',
            'blockchain_consensus': f'Proof of Work (Difficulty: {blockchain.difficulty})',
            'total_blocks': total_blocks,
            'total_hashes_computed': int(total_nonce),
            'average_nonce_per_block': round(avg_nonce, 2),
            'security_features': [
                'Military-grade AES-256 encryption',
                'Salt-based key derivation',
                'Tamper-proof blockchain',
                'Proof of Work consensus',
                'SHA-256 hashing for integrity'
            ]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
