// Upload page functionality

let selectedFile = null;

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    const uploadArea = document.getElementById('uploadArea');
    const fileInput = document.getElementById('fileInput');
    const uploadBtn = document.getElementById('uploadBtn');
    
    // Click to select file
    uploadArea.addEventListener('click', () => {
        fileInput.click();
    });
    
    // File selected
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            selectedFile = e.target.files[0];
            uploadArea.querySelector('.upload-text').innerHTML = 
                `<strong>Selected:</strong> ${selectedFile.name}`;
            uploadBtn.style.display = 'block';
        }
    });
    
    // Drag and drop
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });
    
    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('dragover');
    });
    
    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        
        if (e.dataTransfer.files.length > 0) {
            selectedFile = e.dataTransfer.files[0];
            uploadArea.querySelector('.upload-text').innerHTML = 
                `<strong>Selected:</strong> ${selectedFile.name}`;
            uploadBtn.style.display = 'block';
        }
    });
    
    // Upload button
    uploadBtn.addEventListener('click', uploadFile);
    
    // Load existing files
    loadFiles();
});

async function uploadFile() {
    if (!selectedFile) {
        showMessage('No file selected', 'error');
        return;
    }
    
    const formData = new FormData();
    formData.append('file', selectedFile);
    
    try {
        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            showMessage(data.message, 'success');
            selectedFile = null;
            document.getElementById('uploadArea').querySelector('.upload-text').innerHTML = 
                '<strong>Click to select</strong> or drag and drop a .txt file here';
            document.getElementById('uploadBtn').style.display = 'none';
            loadFiles();
        } else {
            showMessage(data.error, 'error');
        }
    } catch (error) {
        showMessage('Upload failed: ' + error.message, 'error');
    }
}

async function loadFiles() {
    const filesList = document.getElementById('filesList');
    filesList.innerHTML = '<p class="loading">Loading files...</p>';
    
    try {
        const data = await apiCall('/api/files');
        
        if (data.files.length === 0) {
            filesList.innerHTML = '<p class="placeholder">No files uploaded yet. Upload your first file above!</p>';
            document.getElementById('totalFiles').textContent = '0';
            document.getElementById('totalSize').textContent = '0';
            return;
        }
        
        let totalSize = 0;
        filesList.innerHTML = '';
        
        data.files.forEach(file => {
            totalSize += file.size;
            
            const fileItem = document.createElement('div');
            fileItem.className = 'file-item';
            fileItem.innerHTML = `
                <div class="file-info">
                    <div class="file-name">${file.name}</div>
                    <div class="file-size">${formatFileSize(file.size)}</div>
                </div>
                <button class="file-delete" onclick="deleteFile('${file.name}')">Delete</button>
            `;
            filesList.appendChild(fileItem);
        });
        
        document.getElementById('totalFiles').textContent = data.files.length;
        document.getElementById('totalSize').textContent = (totalSize / 1024).toFixed(1);
        
    } catch (error) {
        filesList.innerHTML = '<p class="error">Failed to load files</p>';
        showMessage('Failed to load files: ' + error.message, 'error');
    }
}

async function deleteFile(filename) {
    if (!confirm(`Delete ${filename}?`)) {
        return;
    }
    
    try {
        const data = await apiCall(`/api/files/${filename}`, {
            method: 'DELETE'
        });
        
        showMessage(data.message, 'success');
        loadFiles();
    } catch (error) {
        showMessage('Failed to delete file: ' + error.message, 'error');
    }
}
