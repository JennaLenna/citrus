// Generate page functionality

document.addEventListener('DOMContentLoaded', function() {
    const generateForm = document.getElementById('generateForm');
    const lengthSlider = document.getElementById('length');
    const lengthValue = document.getElementById('lengthValue');
    const temperatureSlider = document.getElementById('temperature');
    const temperatureValue = document.getElementById('temperatureValue');
    const exampleBtns = document.querySelectorAll('.example-btn');
    const promptInput = document.getElementById('prompt');
    
    // Update sliders
    lengthSlider.addEventListener('input', () => {
        lengthValue.textContent = lengthSlider.value;
    });
    
    temperatureSlider.addEventListener('input', () => {
        temperatureValue.textContent = temperatureSlider.value;
    });
    
    // Example prompts
    exampleBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            promptInput.value = btn.dataset.prompt;
        });
    });
    
    // Form submission
    generateForm.addEventListener('submit', (e) => {
        e.preventDefault();
        generateText();
    });
    
    // Copy button
    document.getElementById('copyBtn')?.addEventListener('click', copyText);
    
    // Regenerate button
    document.getElementById('regenerateBtn')?.addEventListener('click', () => {
        generateForm.dispatchEvent(new Event('submit'));
    });
    
    // Load checkpoints
    loadCheckpoints();
});

async function loadCheckpoints() {
    const checkpointSelect = document.getElementById('checkpoint');
    checkpointSelect.innerHTML = '<option value="">Loading checkpoints...</option>';
    
    try {
        const data = await apiCall('/api/checkpoints');
        
        if (data.checkpoints.length === 0) {
            checkpointSelect.innerHTML = '<option value="">No trained models found - train a model first!</option>';
            return;
        }
        
        checkpointSelect.innerHTML = '';
        
        data.checkpoints.forEach(checkpoint => {
            const option = document.createElement('option');
            option.value = checkpoint.name;
            const date = new Date(checkpoint.modified * 1000);
            option.textContent = `${checkpoint.name} (${date.toLocaleDateString()})`;
            checkpointSelect.appendChild(option);
        });
        
        // Select the first one by default
        checkpointSelect.selectedIndex = 0;
        
    } catch (error) {
        checkpointSelect.innerHTML = '<option value="">Failed to load checkpoints</option>';
        showMessage('Failed to load checkpoints: ' + error.message, 'error');
    }
}

async function generateText() {
    const generateBtn = document.getElementById('generateBtn');
    const outputSection = document.getElementById('outputSection');
    const checkpoint = document.getElementById('checkpoint').value;
    const prompt = document.getElementById('prompt').value;
    const length = parseInt(document.getElementById('length').value);
    const temperature = parseFloat(document.getElementById('temperature').value);
    
    if (!checkpoint) {
        showMessage('Please select a trained model first', 'error');
        return;
    }
    
    generateBtn.disabled = true;
    generateBtn.textContent = 'Generating... ⏳';
    outputSection.innerHTML = '<p class="loading">Generating text, please wait...</p>';
    
    try {
        const data = await apiCall('/api/generate', {
            method: 'POST',
            body: JSON.stringify({
                checkpoint: checkpoint,
                prompt: prompt,
                length: length,
                temperature: temperature
            })
        });
        
        outputSection.textContent = data.text;
        document.getElementById('outputActions').style.display = 'flex';
        showMessage('Text generated successfully!', 'success');
        
    } catch (error) {
        outputSection.innerHTML = `<p class="error">Failed to generate text: ${error.message}</p>`;
        showMessage('Generation failed: ' + error.message, 'error');
    } finally {
        generateBtn.disabled = false;
        generateBtn.textContent = 'Generate Text ✨';
    }
}

function copyText() {
    const outputSection = document.getElementById('outputSection');
    const text = outputSection.textContent;
    
    navigator.clipboard.writeText(text).then(() => {
        showMessage('Text copied to clipboard!', 'success');
    }).catch(err => {
        showMessage('Failed to copy text', 'error');
    });
}
