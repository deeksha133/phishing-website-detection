import pandas as pd
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib
from features import FeatureExtractor

def train_model():
    print("Loading dataset...")
    try:
        df = pd.read_csv('backend/dataset_full.csv')
    except FileNotFoundError:
        print("Dataset not found!")
        return

    # Select only the features we implemented
    feature_names = FeatureExtractor.get_feature_names()
    
    # Check if all features exist in dataset
    missing_features = [f for f in feature_names if f not in df.columns]
    if missing_features:
        print(f"Warning: The following features are missing from the dataset: {missing_features}")
        # We might need to handle this, but for now let's assume they match or we drop them
        feature_names = [f for f in feature_names if f in df.columns]

    print(f"Training with {len(feature_names)} features: {feature_names}")

    X = df[feature_names]
    y = df['phishing'] # Assuming 'phishing' is the target column based on previous inspection (it was 0/1)

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train model
    print("Training XGBoost Classifier...")
    clf = XGBClassifier(n_estimators=100, random_state=42, use_label_encoder=False, eval_metric='logloss')
    clf.fit(X_train, y_train)

    # Evaluate
    y_pred = clf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy: {accuracy:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

    # Save model
    joblib.dump(clf, 'backend/model.pkl')
    print("Model saved to backend/model.pkl")

if __name__ == "__main__":
    train_model()
