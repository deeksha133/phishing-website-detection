# Phishing Detection System - Architecture Overview

## 🏗️ System Architecture

This document explains how all files in the Phishing Detection System are connected and work together.

```mermaid
graph TB
    subgraph Frontend["🌐 Frontend (Browser)"]
        HTML[index.html<br/>User Interface]
        CSS[style.css<br/>Styling]
        JS[script.js<br/>Logic & API Calls]
    end

    subgraph Backend["⚙️ Backend (Flask Server)"]
        APP[app.py<br/>Flask API Server]
        FEATURES[features.py<br/>Feature Extraction]
        MODEL[model.pkl<br/>Trained XGBoost Model]
    end

    subgraph Training["🎓 Training Pipeline"]
        TRAIN[train.py<br/>Model Training]
        DATASET[dataset_full.csv<br/>Training Data]
    end

    subgraph Testing["🧪 Testing"]
        TESTS[tests.py<br/>API Test Suite]
    end

    subgraph Config["📦 Configuration"]
        REQ[requirements.txt<br/>Python Dependencies]
        LAUNCH[.vscode/launch.json<br/>Debug Config]
    end

    HTML -->|loads| CSS
    HTML -->|loads| JS
    JS -->|HTTP POST /predict| APP
    APP -->|uses| FEATURES
    APP -->|loads| MODEL
    FEATURES -->|extracts features| APP
    TRAIN -->|imports| FEATURES
    TRAIN -->|reads| DATASET
    TRAIN -->|saves| MODEL
    TESTS -->|calls| APP
    REQ -.->|installs deps for| APP
    REQ -.->|installs deps for| TRAIN
    LAUNCH -.->|debugs| APP

    style HTML fill:#e1f5ff
    style CSS fill:#e1f5ff
    style JS fill:#e1f5ff
    style APP fill:#ffe1e1
    style FEATURES fill:#ffe1e1
    style MODEL fill:#fff4e1
    style TRAIN fill:#e1ffe1
    style DATASET fill:#e1ffe1
    style TESTS fill:#f0e1ff
```

---

## 📁 File Connections & Data Flow

### **1. Frontend Layer** 🌐

#### [index.html](file:///d:/Phishing%20Websites%20Detection/frontend/index.html)
- **Purpose**: User interface structure
- **Connections**:
  - Links to [style.css](file:///d:/Phishing%20Websites%20Detection/frontend/style.css) for styling
  - Links to [script.js](file:///d:/Phishing%20Websites%20Detection/frontend/script.js) for functionality
  - Includes Font Awesome for icons
- **Key Elements**:
  - URL input field (`#urlInput`)
  - Scan button (`#scanBtn`)
  - Result display container (`#resultContainer`)

#### [style.css](file:///d:/Phishing%20Websites%20Detection/frontend/style.css)
- **Purpose**: Visual styling and animations
- **Features**:
  - Modern gradient backgrounds
  - Responsive design
  - Status indicators (safe/phishing)
  - Loading animations

#### [script.js](file:///d:/Phishing%20Websites%20Detection/frontend/script.js)
- **Purpose**: Frontend logic and API communication
- **Key Functions**:
  - `performScan()`: Sends URL to backend API
  - `displayResult()`: Shows prediction results
- **API Connection**:
  ```javascript
  POST http://127.0.0.1:5000/predict
  Body: { "url": "example.com" }
  ```
- **Response Handling**:
  - Displays phishing/safe status
  - Shows confidence score
  - Updates UI with color-coded results

---

### **2. Backend Layer** ⚙️

#### [app.py](file:///d:/Phishing%20Websites%20Detection/backend/app.py)
- **Purpose**: Flask REST API server
- **Port**: 5000
- **Endpoints**:
  - `POST /predict`: Analyzes URLs for phishing
- **Dependencies**:
  - Imports `FeatureExtractor` from [features.py](file:///d:/Phishing%20Websites%20Detection/backend/features.py)
  - Loads trained model from [model.pkl](file:///d:/Phishing%20Websites%20Detection/backend/model.pkl)
- **Workflow**:
  1. Receives URL from frontend
  2. Extracts features using `FeatureExtractor`
  3. Predicts using XGBoost model
  4. Applies heuristic rules:
     - **Typosquatting detection**: Flags domains with suspicious digits (e.g., `micros0ft.com`)
     - **Homepage heuristic**: Trusts clean homepages
     - **Reputation hijacking**: Flags abused legitimate domains (Google Docs, Dropbox)
  5. Returns JSON response with prediction and probability

#### [features.py](file:///d:/Phishing%20Websites%20Detection/backend/features.py)
- **Purpose**: URL feature extraction
- **Class**: `FeatureExtractor`
- **Used By**:
  - [app.py](file:///d:/Phishing%20Websites%20Detection/backend/app.py) (prediction)
  - [train.py](file:///d:/Phishing%20Websites%20Detection/backend/train.py) (training)
- **Extracted Features** (25 total):
  - **URL features**: length, slash count
  - **Domain features**: length, dots, vowels, digits
  - **Directory features**: length, special characters
  - **File features**: length, special characters
- **Methods**:
  - `extract()`: Returns feature dictionary
  - `get_feature_names()`: Returns feature list (ensures consistency)

#### [model.pkl](file:///d:/Phishing%20Websites%20Detection/backend/model.pkl)
- **Purpose**: Serialized XGBoost classifier
- **Created By**: [train.py](file:///d:/Phishing%20Websites%20Detection/backend/train.py)
- **Loaded By**: [app.py](file:///d:/Phishing%20Websites%20Detection/backend/app.py)
- **Size**: ~309 KB
- **Algorithm**: XGBoost with 100 estimators

---

### **3. Training Pipeline** 🎓

#### [train.py](file:///d:/Phishing%20Websites%20Detection/backend/train.py)
- **Purpose**: Train the XGBoost model
- **Workflow**:
  1. Loads [dataset_full.csv](file:///d:/Phishing%20Websites%20Detection/backend/dataset_full.csv)
  2. Imports feature names from [features.py](file:///d:/Phishing%20Websites%20Detection/backend/features.py)
  3. Trains XGBoost classifier
  4. Evaluates accuracy and classification report
  5. Saves model to [model.pkl](file:///d:/Phishing%20Websites%20Detection/backend/model.pkl)
- **Run Command**:
  ```bash
  python backend/train.py
  ```

#### [dataset_full.csv](file:///d:/Phishing%20Websites%20Detection/backend/dataset_full.csv)
- **Purpose**: Training dataset
- **Size**: ~25 MB
- **Contains**: Pre-extracted features and labels
- **Target Column**: `phishing` (0 = legitimate, 1 = phishing)

---

### **4. Testing** 🧪

#### [tests.py](file:///d:/Phishing%20Websites%20Detection/backend/tests.py)
- **Purpose**: Automated API testing
- **Tests**:
  - Scheme-less URL handling
  - Typosquatting detection
  - Homepage heuristics
  - Reputation hijacking
  - Known phishing patterns
- **Connects To**: [app.py](file:///d:/Phishing%20Websites%20Detection/backend/app.py) API
- **Run Command**:
  ```bash
  python backend/tests.py
  ```

---

### **5. Configuration** 📦

#### [requirements.txt](file:///d:/Phishing%20Websites%20Detection/backend/requirements.txt)
- **Purpose**: Python dependencies
- **Packages**:
  - `Flask` - Web server
  - `flask-cors` - Cross-origin requests
  - `scikit-learn` - ML utilities
  - `xgboost` - Model algorithm
  - `pandas` - Data manipulation
  - `joblib` - Model serialization
  - `requests` - HTTP testing
- **Install Command**:
  ```bash
  pip install -r backend/requirements.txt
  ```

#### [.vscode/launch.json](file:///d:/Phishing%20Websites%20Detection/.vscode/launch.json)
- **Purpose**: VS Code debugging configuration
- **Enables**: Debugging [app.py](file:///d:/Phishing%20Websites%20Detection/backend/app.py) with breakpoints

---

## 🔄 Complete Data Flow

````carousel
### Step 1: User Interaction
```mermaid
sequenceDiagram
    participant User
    participant HTML as index.html
    participant JS as script.js
    
    User->>HTML: Opens webpage
    HTML->>JS: Loads script
    User->>HTML: Enters URL
    User->>HTML: Clicks "Scan Now"
    HTML->>JS: Triggers click event
```

<!-- slide -->

### Step 2: API Request
```mermaid
sequenceDiagram
    participant JS as script.js
    participant API as app.py
    
    JS->>JS: performScan()
    JS->>API: POST /predict<br/>{"url": "example.com"}
    Note over JS,API: HTTP Request to<br/>localhost:5000
```

<!-- slide -->

### Step 3: Feature Extraction
```mermaid
sequenceDiagram
    participant API as app.py
    participant FE as features.py
    
    API->>FE: FeatureExtractor(url)
    FE->>FE: Parse URL
    FE->>FE: Extract 25 features
    FE->>API: Return feature dict
```

<!-- slide -->

### Step 4: Prediction
```mermaid
sequenceDiagram
    participant API as app.py
    participant Model as model.pkl
    
    API->>Model: predict(features)
    Model->>API: prediction (0 or 1)
    API->>Model: predict_proba(features)
    Model->>API: probability (0.0-1.0)
    API->>API: Apply heuristics
```

<!-- slide -->

### Step 5: Response & Display
```mermaid
sequenceDiagram
    participant API as app.py
    participant JS as script.js
    participant HTML as index.html
    participant User
    
    API->>JS: JSON response<br/>{result, probability, is_phishing}
    JS->>JS: displayResult(data)
    JS->>HTML: Update DOM elements
    HTML->>User: Show result with<br/>color-coded status
```
````

---

## 🚀 How to Run the System

### **Start Backend Server**
```bash
cd "d:\Phishing Websites Detection"
python backend/app.py
```
Server runs on `http://127.0.0.1:5000`

### **Open Frontend**
Open `frontend/index.html` in a web browser

### **Test the System**
```bash
python backend/tests.py
```

---

## 🔧 Key Integration Points

| Component | Connects To | Connection Type | Purpose |
|-----------|-------------|-----------------|---------|
| `script.js` | `app.py` | HTTP POST | Send URL for analysis |
| `app.py` | `features.py` | Python import | Extract URL features |
| `app.py` | `model.pkl` | File load | Make predictions |
| `train.py` | `features.py` | Python import | Get feature names |
| `train.py` | `dataset_full.csv` | File read | Load training data |
| `train.py` | `model.pkl` | File write | Save trained model |
| `tests.py` | `app.py` | HTTP POST | Validate API |

---

## 📊 Feature Flow

```mermaid
graph LR
    URL[User URL Input] --> FE[FeatureExtractor]
    FE --> F1[URL Features<br/>length, slashes]
    FE --> F2[Domain Features<br/>length, dots, digits]
    FE --> F3[Directory Features<br/>special chars]
    FE --> F4[File Features<br/>special chars]
    F1 --> DF[DataFrame<br/>25 features]
    F2 --> DF
    F3 --> DF
    F4 --> DF
    DF --> MODEL[XGBoost Model]
    MODEL --> PRED[Prediction<br/>+ Probability]
    PRED --> HEUR[Heuristic Rules]
    HEUR --> RESULT[Final Result]
```

---

## 🎯 Summary

The system follows a **3-tier architecture**:

1. **Frontend** (`index.html`, `style.css`, `script.js`): User interface
2. **Backend** (`app.py`, `features.py`, `model.pkl`): API and ML inference
3. **Training** (`train.py`, `dataset_full.csv`): Model development

**Core workflow**: User → Frontend → API → Feature Extraction → ML Model → Heuristics → Response → UI Update

All components are loosely coupled, making the system maintainable and scalable.
