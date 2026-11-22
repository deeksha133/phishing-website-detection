import requests
import json
import sys

# Configuration
API_URL = 'http://127.0.0.1:5000/predict'

# Test Cases: (URL, Expected Result, Description)
TEST_CASES = [
    # 1. Scheme-less URL Handling
    ("google.com", "Legitimate", "Scheme-less URL (google.com)"),
    ("http://google.com", "Legitimate", "Standard URL (http://google.com)"),
    
    # 2. Typosquatting / Digit Detection
    ("https://micros0ft.com", "Phishing", "Typosquatting with digits (micros0ft.com)"),
    
    # 3. Homepage Heuristic & Normalization (www vs non-www)
    ("https://www.instagram.com/", "Legitimate", "Homepage with www (instagram.com)"),
    ("instagram.com", "Legitimate", "Homepage without www (instagram.com)"),
    
    # 4. Confidence Score Calibration
    ("https://www.facebook.com/", "Legitimate", "High Confidence Homepage (facebook.com)"),
    ("facebook.com", "Legitimate", "Short Domain (facebook.com)"),
    
    # 5. Reputation Hijacking (Abused Legitimate Domains)
    ("https://docs.google.com/spreadsheet/viewform?formkey=dG5...", "Phishing", "Abused Google Docs URL"),
    
    # 6. Known Phishing Patterns
    ("http://secure-login.paypal.com.account-update.gq/login.php", "Phishing", "Complex Phishing URL"),
]

def run_tests():
    print(f"{'TEST CASE':<50} | {'EXPECTED':<12} | {'ACTUAL':<12} | {'STATUS':<10}")
    print("-" * 90)
    
    passed = 0
    failed = 0
    
    for url, expected, desc in TEST_CASES:
        try:
            response = requests.post(API_URL, json={'url': url})
            if response.status_code != 200:
                print(f"{desc:<50} | {expected:<12} | {'ERROR':<12} | FAIL (API Error)")
                failed += 1
                continue
                
            data = response.json()
            actual = data.get('result')
            
            # Determine Pass/Fail
            # Note: The API returns "Legitimate" or "Phishing"
            status = "PASS" if actual == expected else "FAIL"
            
            if status == "PASS":
                passed += 1
            else:
                failed += 1
                
            print(f"{desc:<50} | {expected:<12} | {actual:<12} | {status}")
            
        except Exception as e:
            print(f"{desc:<50} | {expected:<12} | {'ERROR':<12} | FAIL ({str(e)})")
            failed += 1

    print("-" * 90)
    print(f"Total: {len(TEST_CASES)} | Passed: {passed} | Failed: {failed}")
    
    if failed > 0:
        sys.exit(1)

if __name__ == "__main__":
    print("Running Phishing Detection Test Suite...\n")
    run_tests()
