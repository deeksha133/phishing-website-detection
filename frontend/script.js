document.addEventListener('DOMContentLoaded', () => {
    const urlInput = document.getElementById('urlInput');
    const scanBtn = document.getElementById('scanBtn');
    const resultContainer = document.getElementById('resultContainer');
    const loader = document.getElementById('loader');
    const resultContent = document.getElementById('resultContent');
    const statusIcon = document.getElementById('statusIcon');
    const statusText = document.getElementById('statusText');
    const statusDescription = document.getElementById('statusDescription');
    const confidenceScore = document.getElementById('confidenceScore');
    const confidenceBar = document.getElementById('confidenceBar');

    scanBtn.addEventListener('click', performScan);
    urlInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') performScan();
    });

    async function performScan() {
        const url = urlInput.value.trim();
        if (!url) return;

        // Reset UI
        resultContainer.classList.remove('hidden');
        loader.classList.remove('hidden');
        resultContent.classList.add('hidden');

        try {
            const response = await fetch('http://127.0.0.1:5000/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ url: url }),
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            displayResult(data);

        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while scanning. Please try again.');
            resultContainer.classList.add('hidden');
        } finally {
            loader.classList.add('hidden');
        }
    }

    function displayResult(data) {
        resultContent.classList.remove('hidden');

        const isPhishing = data.is_phishing;
        const probability = (data.probability * 100).toFixed(1);

        // Update Icon and Text
        statusIcon.className = 'status-icon fa-solid ' + (isPhishing ? 'fa-triangle-exclamation status-danger' : 'fa-circle-check status-safe');
        statusText.textContent = isPhishing ? 'Phishing Detected!' : 'Website is Safe';
        statusText.style.color = isPhishing ? 'var(--danger)' : 'var(--success)';

        const safetyMessage = document.getElementById('safetyMessage');
        safetyMessage.textContent = isPhishing ? 'Safe to use: Phishing' : 'Safe to use: Legitimate';
        safetyMessage.style.color = isPhishing ? 'var(--danger)' : 'var(--success)';
        safetyMessage.style.fontWeight = 'bold';
        safetyMessage.style.fontSize = '1.2em';
        safetyMessage.style.margin = '10px 0';

        statusDescription.textContent = isPhishing
            ? 'This website shows characteristics of a phishing attempt. Do not enter personal information.'
            : 'This website appears to be legitimate based on our analysis.';

        // Update Confidence
        // If phishing, probability is high. If safe, probability is low (probability of being phishing).
        // So for display, we want "Confidence in prediction".
        // If prediction is Phishing (1), confidence is probability.
        // If prediction is Safe (0), confidence is 1 - probability.

        let displayConfidence = isPhishing ? probability : (100 - probability).toFixed(1);

        confidenceScore.textContent = `${displayConfidence}%`;
        confidenceBar.style.width = `${displayConfidence}%`;
        confidenceBar.style.background = isPhishing ? 'var(--danger)' : 'var(--success)';
    }
});
