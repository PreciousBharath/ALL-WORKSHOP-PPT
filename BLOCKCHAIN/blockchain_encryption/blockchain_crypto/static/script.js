// File type icons mapping
const fileTypeIcons = {
    'Document': '📄',
    'PDF': '📕',
    'Image': '🖼️',
    'Spreadsheet': '📊',
    'Presentation': '🎨',
    'Audio': '🎵',
    'Video': '🎬',
    'Archive': '📦',
    'File': '📄'
};

// Initialize on load
document.addEventListener('DOMContentLoaded', function() {
    setupEventListeners();
    loadStats();
    
    // Auto-load blockchain every 5 seconds
    setInterval(loadStats, 5000);
});

// Setup event listeners
function setupEventListeners() {
    // Encrypt form
    document.getElementById('encryptForm').addEventListener('submit', handleEncrypt);
    document.getElementById('fileInput').addEventListener('change', handleFileSelect);
    document.getElementById('password').addEventListener('input', checkPasswordStrength);
    document.getElementById('confirmPassword').addEventListener('input', validatePasswords);
    
    // File input click handlers
    const fileWrappers = document.querySelectorAll('.file-input-wrapper');
    
    // Encrypt file input
    fileWrappers[0].addEventListener('click', function(e) {
        if (e.target.tagName !== 'INPUT') {
            document.getElementById('fileInput').click();
        }
    });

    // Decrypt form
    document.getElementById('decryptForm').addEventListener('submit', handleDecrypt);
    document.getElementById('encryptedFile').addEventListener('change', handleEncryptedFileSelect);
    
    // Encrypted file input click handler
    if (fileWrappers[1]) {
        fileWrappers[1].addEventListener('click', function(e) {
            if (e.target.tagName !== 'INPUT') {
                document.getElementById('encryptedFile').click();
            }
        });
    }
    
    // Verification file input
    if (fileWrappers[2]) {
        fileWrappers[2].addEventListener('click', function(e) {
            if (e.target.tagName !== 'INPUT') {
                document.getElementById('verifyFileInput').click();
            }
        });
    }
}

// Navigate to section
function goToSection(sectionId) {
    // Remove active class from all nav links
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
    });

    // Add active class to clicked link
    event.target.classList.add('active');

    // Scroll to section
    document.getElementById(sectionId).scrollIntoView({ behavior: 'smooth' });
}

// File selection handlers
function handleFileSelect(e) {
    const file = e.target.files[0];
    if (file) {
        const fileInfo = document.getElementById('fileInfo');
        const fileType = getFileType(file.name);
        const fileSize = formatBytes(file.size);
        
        fileInfo.innerHTML = `
            <strong>${fileTypeIcons[fileType]} ${fileType}</strong><br>
            📝 ${file.name}<br>
            💾 ${fileSize}
        `;
        fileInfo.classList.add('show');
        
        // Update label
        document.querySelector('.file-input-label').innerHTML = `
            <span class="file-input-icon">${fileTypeIcons[fileType]}</span>
            <span>${file.name}</span>
        `;
    }
}

function handleEncryptedFileSelect(e) {
    const file = e.target.files[0];
    if (file) {
        const fileInfo = document.getElementById('encFileInfo');
        const fileSize = formatBytes(file.size);
        
        fileInfo.innerHTML = `
            <strong>🔒 Encrypted File</strong><br>
            📝 ${file.name}<br>
            💾 ${fileSize}
        `;
        fileInfo.classList.add('show');
    }
}

// Get file type
function getFileType(filename) {
    const ext = filename.split('.').pop().toLowerCase();
    
    if (['doc', 'docx', 'txt'].includes(ext)) return 'Document';
    if (ext === 'pdf') return 'PDF';
    if (['jpg', 'jpeg', 'png', 'gif'].includes(ext)) return 'Image';
    if (['xlsx', 'xls', 'csv'].includes(ext)) return 'Spreadsheet';
    if (['pptx', 'ppt'].includes(ext)) return 'Presentation';
    if (['mp3', 'wav', 'flac'].includes(ext)) return 'Audio';
    if (['mp4', 'avi', 'mov', 'mkv'].includes(ext)) return 'Video';
    if (['zip', 'rar', '7z'].includes(ext)) return 'Archive';
    
    return 'File';
}

// Format bytes
function formatBytes(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i];
}

// Toggle password visibility
function togglePassword(inputId) {
    const input = document.getElementById(inputId);
    if (input.type === 'password') {
        input.type = 'text';
    } else {
        input.type = 'password';
    }
}

// Check password strength
function checkPasswordStrength(e) {
    const password = e.target.value;
    const strengthBar = document.querySelector('.strength-bar::after');
    const strengthText = document.querySelector('.strength-text');
    
    let strength = 0;
    let text = 'Weak';
    let color = '#ff3333';
    
    if (password.length >= 6) strength++;
    if (password.length >= 10) strength++;
    if (/[a-z]/.test(password) && /[A-Z]/.test(password)) strength++;
    if (/\d/.test(password)) strength++;
    if (/[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]/.test(password)) strength++;
    
    const widths = ['25%', '50%', '75%', '100%', '100%'];
    const colors = ['#ff3333', '#ffaa00', '#ffaa00', '#00cc66', '#00cc66'];
    const texts = ['Weak', 'Fair', 'Fair', 'Strong', 'Very Strong'];
    
    if (strength > 0) {
        document.querySelector('.strength-bar').style.setProperty('--width', widths[strength - 1]);
        const style = document.createElement('style');
        style.innerHTML = `.strength-bar::after { width: ${widths[strength - 1]}; background-color: ${colors[strength - 1]}; }`;
        document.head.appendChild(style);
        strengthText.textContent = texts[strength - 1];
        strengthText.style.color = colors[strength - 1];
    }
}

// Validate passwords match
function validatePasswords() {
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirmPassword').value;
    
    if (password && confirmPassword) {
        if (password === confirmPassword) {
            document.getElementById('confirmPassword').style.borderColor = '#00cc66';
        } else {
            document.getElementById('confirmPassword').style.borderColor = '#ff3333';
        }
    }
}

// Handle encrypt
async function handleEncrypt(e) {
    e.preventDefault();
    
    const file = document.getElementById('fileInput').files[0];
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirmPassword').value;
    
    if (!file) {
        showNotification('Please select a file', 'error');
        return;
    }
    
    if (password.length < 6) {
        showNotification('Password must be at least 6 characters', 'error');
        return;
    }
    
    if (password !== confirmPassword) {
        showNotification('Passwords do not match', 'error');
        return;
    }
    
    // Show loading
    const btn = e.target.querySelector('button[type="submit"]');
    const originalText = btn.innerHTML;
    btn.innerHTML = '<div class="loader"></div> Encrypting...';
    btn.disabled = true;
    
    try {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('password', password);
        
        const response = await fetch('/api/encrypt', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showNotification('✓ File encrypted successfully!', 'success');
            
            // Add download button
            const fileInfo = document.getElementById('fileInfo');
            if (fileInfo) {
                fileInfo.innerHTML += `<br><button class="btn btn-primary" onclick="downloadEncryptedFile('${data.file_id}', '${data.encrypted_filename}')" style="margin-top: 1rem; width: 100%;">
                    <span>📥</span> Download Encrypted File
                </button>`;
            }
            
            document.getElementById('encryptForm').reset();
            document.querySelector('.file-input-label').innerHTML = `
                <span class="file-input-icon">📁</span>
                <span>Choose a file</span>
            `;
            document.querySelector('.strength-bar').style.setProperty('--width', '0%');
            document.querySelector('.strength-text').textContent = '';
            
            // Update stats
            setTimeout(loadStats, 1000);
        } else {
            showNotification(data.error || 'Encryption failed', 'error');
        }
    } catch (error) {
        showNotification('Error: ' + error.message, 'error');
    } finally {
        btn.innerHTML = originalText;
        btn.disabled = false;
    }
}

// Download encrypted file
function downloadEncryptedFile(fileId, filename) {
    try {
        const url = `/api/download-encrypted/${fileId}`;
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        showNotification(`✓ Downloaded: ${filename}`, 'success');
    } catch (error) {
        showNotification('Error downloading file: ' + error.message, 'error');
    }
}

// Handle decrypt
async function handleDecrypt(e) {
    e.preventDefault();
    
    const file = document.getElementById('encryptedFile').files[0];
    const originalFilename = document.getElementById('originalFilename').value;
    const password = document.getElementById('decryptPassword').value;
    
    if (!file) {
        showNotification('Please select an encrypted file', 'error');
        return;
    }
    
    if (!originalFilename) {
        showNotification('Please enter the original filename', 'error');
        return;
    }
    
    if (!password) {
        showNotification('Please enter the password', 'error');
        return;
    }
    
    // Show loading
    const btn = e.target.querySelector('button[type="submit"]');
    const originalText = btn.innerHTML;
    btn.innerHTML = '<div class="loader"></div> Decrypting...';
    btn.disabled = true;
    
    try {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('password', password);
        formData.append('original_filename', originalFilename);
        
        const response = await fetch('/api/decrypt', {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            // Download the file
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = originalFilename;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
            
            showNotification('✓ File decrypted and downloaded!', 'success');
            document.getElementById('decryptForm').reset();
            document.getElementById('encFileInfo').classList.remove('show');
            
            // Update stats
            setTimeout(loadStats, 1000);
        } else {
            const data = await response.json();
            showNotification(data.error || 'Decryption failed', 'error');
        }
    } catch (error) {
        showNotification('Error: ' + error.message, 'error');
    } finally {
        btn.innerHTML = originalText;
        btn.disabled = false;
    }
}

// Load statistics
async function loadStats() {
    try {
        const response = await fetch('/api/blockchain/stats');
        const data = await response.json();
        
        if (data.success) {
            document.getElementById('stat-ops').textContent = data.total_operations;
            document.getElementById('stat-encrypted').textContent = data.encrypted_files;
            document.getElementById('stat-decrypted').textContent = data.decrypted_files;
        }
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

// Load blockchain
async function loadBlockchain() {
    try {
        const response = await fetch('/api/blockchain');
        const data = await response.json();
        
        if (data.success) {
            renderBlockchain(data.blocks);
            loadBlockchainStats();
        }
    } catch (error) {
        console.error('Error loading blockchain:', error);
        showNotification('Error loading blockchain', 'error');
    }
}

// Render blockchain
function renderBlockchain(blocks) {
    const ledger = document.getElementById('blockchainLedger');
    
    if (blocks.length === 0) {
        ledger.innerHTML = '<p style="text-align: center; color: var(--text-secondary);">No blocks yet</p>';
        return;
    }
    
    let html = '';
    
    blocks.forEach((block, index) => {
        const transaction = block.transaction || {};
        const operation = transaction.operation || 'UNKNOWN';
        const timestamp = new Date(block.timestamp).toLocaleString();
        
        let operationColor = 'var(--primary-color)';
        let operationIcon = '⚙️';
        
        if (operation === 'ENCRYPT') {
            operationColor = '#0066ff';
            operationIcon = '🔒';
        } else if (operation === 'DECRYPT') {
            operationColor = '#00d4ff';
            operationIcon = '🔓';
        } else if (operation === 'GENESIS') {
            operationIcon = '⛓️';
            operationColor = '#00cc66';
        }
        
        html += `
            <div class="block">
                <div class="block-header">
                    <div class="block-index">${operationIcon} Block #${block.index}</div>
                    <div class="block-timestamp">${timestamp}</div>
                </div>
                <div class="block-content">
                    <div class="block-data">
                        <div class="block-data-label">Operation</div>
                        <div class="block-data-value" style="color: ${operationColor};">${operation}</div>
                    </div>
                    ${transaction.original_filename ? `
                    <div class="block-data">
                        <div class="block-data-label">File</div>
                        <div class="block-data-value">${transaction.original_filename}</div>
                    </div>
                    ` : ''}
                    ${transaction.file_type ? `
                    <div class="block-data">
                        <div class="block-data-label">Type</div>
                        <div class="block-data-value">${transaction.file_type}</div>
                    </div>
                    ` : ''}
                    ${transaction.file_size ? `
                    <div class="block-data">
                        <div class="block-data-label">Size</div>
                        <div class="block-data-value">${formatBytes(transaction.file_size)}</div>
                    </div>
                    ` : ''}
                    ${transaction.file_id ? `
                    <div class="block-data">
                        <div class="block-data-label">File ID</div>
                        <div class="block-data-value">${transaction.file_id}</div>
                    </div>
                    ` : ''}
                    <div class="block-data">
                        <div class="block-data-label">Hash</div>
                        <div class="block-data-value">${block.hash.substring(0, 16)}...</div>
                    </div>
                    <div class="block-data">
                        <div class="block-data-label">Previous Hash</div>
                        <div class="block-data-value">${block.previous_hash.substring(0, 16)}...</div>
                    </div>
                    <div class="block-data">
                        <div class="block-data-label">Nonce</div>
                        <div class="block-data-value">${block.nonce}</div>
                    </div>
                </div>
            </div>
        `;
    });
    
    ledger.innerHTML = html;
}

// Load blockchain stats
async function loadBlockchainStats() {
    try {
        const response = await fetch('/api/blockchain/stats');
        const data = await response.json();
        
        if (data.success) {
            const statsHtml = `
                <div class="stat-card">
                    <h3>${data.total_operations}</h3>
                    <p>Total Operations</p>
                </div>
                <div class="stat-card">
                    <h3>${data.encrypted_files}</h3>
                    <p>Encrypted Files</p>
                </div>
                <div class="stat-card">
                    <h3>${data.decrypted_files}</h3>
                    <p>Decrypted Files</p>
                </div>
                <div class="stat-card">
                    <h3>${data.total_size_mb}</h3>
                    <p>Data Processed (MB)</p>
                </div>
            `;
            
            document.getElementById('blockchainStats').innerHTML = statsHtml;
        }
    } catch (error) {
        console.error('Error loading blockchain stats:', error);
    }
}

// Verify blockchain
async function verifyBlockchain() {
    try {
        const response = await fetch('/api/blockchain/verify');
        const data = await response.json();
        
        const statusDiv = document.getElementById('blockchainStatus');
        
        if (data.is_valid) {
            statusDiv.className = 'blockchain-status valid';
            statusDiv.innerHTML = '<p>✅ ' + data.message + '</p>';
            showNotification('Blockchain verified successfully!', 'success');
        } else {
            statusDiv.className = 'blockchain-status invalid';
            statusDiv.innerHTML = '<p>❌ ' + data.message + '</p>';
            showNotification('Blockchain verification failed!', 'error');
        }
    } catch (error) {
        showNotification('Error verifying blockchain: ' + error.message, 'error');
    }
}

// Show notification
function showNotification(message, type = 'info') {
    const notification = document.getElementById('notification');
    notification.textContent = message;
    notification.className = `notification show ${type}`;
    
    setTimeout(() => {
        notification.classList.remove('show');
    }, 4000);
}

// Calculate SHA-256 hash of file
async function calculateFileHash() {
    const file = document.getElementById('verifyFileInput').files[0];
    if (!file) {
        showNotification('Please select a file first', 'error');
        return;
    }
    
    try {
        const buffer = await file.arrayBuffer();
        const hashBuffer = await crypto.subtle.digest('SHA-256', buffer);
        const hashArray = Array.from(new Uint8Array(hashBuffer));
        const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
        
        const message = `✓ File: ${file.name}\n📊 SHA-256: ${hashHex}\n💾 Size: ${formatBytes(file.size)}`;
        showNotification(message, 'success');
        return hashHex;
    } catch (error) {
        showNotification('Error calculating hash: ' + error.message, 'error');
    }
}

// Export blockchain as JSON
async function exportBlockchain() {
    try {
        const response = await fetch('/api/blockchain');
        const data = await response.json();
        
        if (data.success) {
            const json = JSON.stringify(data.blocks, null, 2);
            const blob = new Blob([json], { type: 'application/json' });
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `blockchain_${new Date().toISOString().split('T')[0]}.json`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
            
            showNotification('✅ Blockchain exported successfully!', 'success');
        }
    } catch (error) {
        showNotification('Error exporting blockchain: ' + error.message, 'error');
    }
}

// Search transactions by filename
function searchTransactions() {
    const searchTerm = prompt('Enter filename to search:');
    if (!searchTerm) return;
    
    const blocks = document.querySelectorAll('.block');
    let found = 0;
    
    blocks.forEach(block => {
        const text = block.textContent.toLowerCase();
        if (text.includes(searchTerm.toLowerCase())) {
            block.style.opacity = '1';
            block.style.transform = 'scale(1)';
            found++;
        } else {
            block.style.opacity = '0.3';
            block.style.transform = 'scale(0.95)';
        }
    });
    
    if (found === 0) {
        showNotification('❌ No transactions found matching: ' + searchTerm, 'error');
    } else {
        showNotification(`✓ Found ${found} transaction(s) matching: ${searchTerm}`, 'success');
    }
}

// Reset search
function resetSearch() {
    const blocks = document.querySelectorAll('.block');
    blocks.forEach(block => {
        block.style.opacity = '1';
        block.style.transform = 'scale(1)';
    });
}

// Show crypto statistics
async function showCryptoStats() {
    try {
        const response = await fetch('/api/blockchain/stats');
        const data = await response.json();
        
        if (data.success) {
            const statsMessage = `
🔐 BLOCKCHAIN STATISTICS
━━━━━━━━━━━━━━━━━━━━━━━━
📊 Total Operations: ${data.total_operations}
🔒 Files Encrypted: ${data.encrypted_files}
🔓 Files Decrypted: ${data.decrypted_files}
💾 Data Processed: ${data.total_size_mb} MB
🏆 Encryption Level: AES-256
⛓️  Algorithm: SHA-256 + Proof of Work
            `;
            showNotification(statsMessage, 'info');
        }
    } catch (error) {
        showNotification('Error loading stats: ' + error.message, 'error');
    }
}

// Validate password strength (0-5 levels)
function getPasswordStrengthLevel(password) {
    let strength = 0;
    if (password.length >= 6) strength++;
    if (password.length >= 10) strength++;
    if (/[a-z]/.test(password) && /[A-Z]/.test(password)) strength++;
    if (/\d/.test(password)) strength++;
    if (/[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]/.test(password)) strength++;
    return strength;
}

// Get password strength recommendation
function getPasswordRecommendation(strength) {
    const recommendations = [
        'Very Weak - Add numbers and special characters',
        'Weak - Use uppercase and lowercase letters',
        'Fair - Add numbers for more security',
        'Good - Add special characters for extra security',
        'Strong - This is a secure password',
        'Very Strong - Excellent security level'
    ];
    return recommendations[strength] || 'Unknown';
}

// Show detailed crypto information
async function showDetailedCryptoInfo() {
    try {
        const response = await fetch('/api/crypto-info');
        const data = await response.json();
        
        if (data.success) {
            const features = data.security_features.map(f => '  ✓ ' + f).join('\n');
            const infoMessage = `
🔐 CRYPTOGRAPHY DETAILS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔒 Encryption: ${data.encryption_algorithm}
🔑 Key Derivation: ${data.key_derivation}
💾 Hashing: ${data.hashing_algorithm}
⛓️  Consensus: ${data.blockchain_consensus}
📊 Total Blocks: ${data.total_blocks}
💪 Total Hashes: ${data.total_hashes_computed}
📈 Avg Nonce/Block: ${data.average_nonce_per_block}

🛡️ Security Features:
${features}
            `;
            showNotification(infoMessage, 'info');
        }
    } catch (error) {
        showNotification('Error loading crypto info: ' + error.message, 'error');
    }
}

// Get file information
async function analyzeFile() {
    const file = document.getElementById('verifyFileInput').files[0];
    if (!file) {
        showNotification('Please select a file first', 'error');
        return;
    }
    
    try {
        const formData = new FormData();
        formData.append('file', file);
        
        const response = await fetch('/api/file-info', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            const infoMessage = `
📋 FILE INFORMATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 Filename: ${data.filename}
📂 Type: ${data.file_type}
💾 Size: ${formatBytes(data.file_size)}
🔐 Encryption: ${data.encryption_status.toUpperCase()}

📊 INTEGRITY VERIFICATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔗 SHA-256: ${data.sha256_hash.substring(0, 32)}...
            `;
            showNotification(infoMessage, 'success');
        } else {
            showNotification(data.error || 'Error analyzing file', 'error');
        }
    } catch (error) {
        showNotification('Error: ' + error.message, 'error');
    }
}
