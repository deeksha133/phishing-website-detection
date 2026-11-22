from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
from features import FeatureExtractor
import os

app = Flask(__name__)
CORS(app)

# Load model
model_path = os.path.join(os.path.dirname(__file__), 'model.pkl')
try:
    model = joblib.load(model_path)
    print("Model loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

@app.route('/predict', methods=['POST'])
def predict():
    if not model:
        return jsonify({'error': 'Model not loaded'}), 500

    data = request.get_json()
    url = data.get('url')

    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    try:
        # Extract features
        extractor = FeatureExtractor(url)
        features = extractor.extract()
        
        # Convert to DataFrame for prediction (to match training input)
        # Ensure column order matches training
        feature_names = FeatureExtractor.get_feature_names()
        df = pd.DataFrame([features], columns=feature_names)
        
        # Predict
        prediction = model.predict(df)[0]
        probability = model.predict_proba(df)[0][1] # Probability of class 1 (Phishing)

        # --- Heuristic Overrides ---
        # The model might miss typosquatting like 'micros0ft.com' if not trained on it.
        # We add a manual check for digits in the domain which often indicate phishing in this context.
        if features.get('qty_digits_domain', 0) > 0:
            # Check if it looks like a typosquatting attempt (e.g. 0 instead of o, 1 instead of l)
            # For now, we'll be aggressive: if there are digits in the domain and the model is unsure (< 0.9), bump it up.
            # Or simply: if it contains '0' and looks like 'microsoft', etc.
            
            # Simple heuristic: If domain has digits and probability is low, increase suspicion.
            # Specifically for the user's case 'micros0ft':
            if '0' in extractor.domain or '1' in extractor.domain:
                 # If model says Safe but we have suspicious digits, force a review or increase prob.
                 if prediction == 0:
                     print("Heuristic: Suspicious digits detected. Adjusting probability.")
                     # Boost probability significantly if it was low
                     probability = max(probability, 0.65) 
                     prediction = 1

        # --- Homepage Heuristic ---
        # If it's a root URL (homepage) and the domain looks "clean" (no hyphens, few dots, no digits),
        # it's less likely to be phishing. The model penalizes the protocol slashes too much.
        if extractor.path in ['', '/']:
            # Check for clean domain: no hyphens, max 2 dots, NO digits (to avoid typosquatting like micros0ft)
            if (features.get('qty_hyphen_domain', 0) == 0 and 
                features.get('qty_dot_domain', 0) <= 2 and 
                features.get('qty_digits_domain', 0) == 0):
                
                print("Heuristic: Clean homepage detected. Forcing low probability.")
                # Force a very low probability to reflect high confidence in safety for major homepages
                probability = 0.05
                prediction = 0

        # --- Reputation Hijacking Heuristic ---
        # Check for known legitimate domains that are often abused for phishing (e.g. Google Docs, Forms)
        # If the domain is trusted but the path indicates user-generated content, we should be cautious.
        high_risk_domains = ['docs.google.com', 'drive.google.com', 'dropbox.com', 'forms.gle']
        if extractor.domain in high_risk_domains and extractor.path not in ['', '/']:
             print(f"Heuristic: High-risk domain '{extractor.domain}' with path detected. Increasing suspicion.")
             # Boost probability to ensure it's flagged, but maybe not as confident as a known bad domain
             probability = max(probability, 0.60)
             prediction = 1

        result = "Phishing" if prediction == 1 else "Legitimate"
        
        return jsonify({
            'url': url,
            'result': result,
            'probability': float(probability),
            'is_phishing': bool(prediction == 1)
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
