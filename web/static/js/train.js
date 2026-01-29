// Train page functionality

let trainingCheckInterval = null;

document.addEventListener('DOMContentLoaded', function() {
    const trainForm = document.getElementById('trainForm');
    const epochsSlider = document.getElementById('epochs');
    const epochsValue = document.getElementById('epochsValue');
    const useDefaults = document.getElementById('useDefaults');
    const advancedSettings = document.getElementById('advancedSettings');
    
    // Update epoch display
    epochsSlider.addEventListener('input', () => {
        epochsValue.textContent = epochsSlider.value;
    });
    
    // Toggle advanced settings
    useDefaults.addEventListener('change', () => {
        advancedSettings.style.display = useDefaults.checked ? 'none' : 'block';
    });
    
    // Form submission
    trainForm.addEventListener('submit', (e) => {
        e.preventDefault();
        startTraining();
    });
    
    // Check for ongoing training
    checkTrainingStatus();
});

async function startTraining() {
    const startBtn = document.getElementById('startTrainBtn');
    const epochs = parseInt(document.getElementById('epochs').value);
    const hiddenSize = parseInt(document.getElementById('hiddenSize').value);
    const seqLength = parseInt(document.getElementById('seqLength').value || 50);
    const batchSize = parseInt(document.getElementById('batchSize').value || 16);
    
    startBtn.disabled = true;
    
    try {
        const data = await apiCall('/api/train', {
            method: 'POST',
            body: JSON.stringify({
                epochs: epochs,
                hidden_size: hiddenSize,
                seq_length: seqLength,
                batch_size: batchSize
            })
        });
        
        showMessage(data.message, 'success');
        
        // Start polling for status
        document.getElementById('trainingStats').style.display = 'block';
        trainingCheckInterval = setInterval(checkTrainingStatus, 2000);
        
    } catch (error) {
        showMessage('Failed to start training: ' + error.message, 'error');
        startBtn.disabled = false;
    }
}

async function checkTrainingStatus() {
    try {
        const data = await apiCall('/api/train/status');
        const status = data.status;
        
        // Update progress bar
        document.getElementById('progressBar').style.width = status.progress + '%';
        document.getElementById('progressPercent').textContent = status.progress;
        
        // Update stats
        document.getElementById('currentEpoch').textContent = status.current_epoch;
        document.getElementById('totalEpochs').textContent = status.total_epochs;
        document.getElementById('currentLoss').textContent = status.loss.toFixed(4);
        document.getElementById('statusMessage').textContent = status.message;
        
        // Check if training is complete
        if (!status.is_training && status.progress === 100) {
            clearInterval(trainingCheckInterval);
            showMessage('Training complete! You can now generate text.', 'success');
            document.getElementById('nextStepSection').style.display = 'block';
            document.getElementById('startTrainBtn').disabled = false;
        } else if (!status.is_training && status.progress === 0) {
            // Ready to train
            document.getElementById('startTrainBtn').disabled = false;
        }
        
    } catch (error) {
        console.error('Failed to check status:', error);
    }
}
