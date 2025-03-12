from flask import Blueprint, request, render_template
import pickle
import requests
import re
import tldextract

detect_blueprint = Blueprint("detect", __name__, template_folder="templates")

# Load phishing detection model and vectorizer
def load_model():
    try:
        with open("backend/model.pkl", "rb") as model_file:
            model = pickle.load(model_file)

        with open("backend/vectorizer.pkl", "rb") as vectorizer_file:
            vectorizer = pickle.load(vectorizer_file)
        
        return model, vectorizer
    except Exception as e:
        print(f"Error loading model: {e}")
        return None, None

model, vectorizer = load_model()
if model is None or vectorizer is None:
    print("Error: Model or vectorizer could not be loaded.")

VIRUSTOTAL_API_KEY = "b58a93c6d67c4081a4c8562a06116f0be64a73ec2118138425c23f64d1286258"
VIRUSTOTAL_API_URL = "https://www.virustotal.com/api/v3/domains"

# Function to extract URLs from email content
def extract_urls(text):
    url_pattern = re.compile(r'https?://[^\s<>"]+|www\.[^\s<>"]+')
    return url_pattern.findall(text)

# Function to check domain reputation using VirusTotal API
def check_domain_reputation(url):
    try:
        # Extract domain from URL
        domain_info = tldextract.extract(url)
        domain = f"{domain_info.domain}.{domain_info.suffix}"

        headers = {"x-apikey": VIRUSTOTAL_API_KEY}
        response = requests.get(f"{VIRUSTOTAL_API_URL}/{domain}", headers=headers)

        if response.status_code == 200:
            data = response.json()
            if "data" in data:
                analysis_stats = data["data"]["attributes"]["last_analysis_stats"]

                malicious = analysis_stats.get("malicious", 0)
                suspicious = analysis_stats.get("suspicious", 0)

                if malicious > 0:
                    return f"⚠️ Malicious ({malicious} engines flagged it)"
                elif suspicious > 0:
                    return f"⚠️ Suspicious ({suspicious} engines flagged it)"
                else:
                    return "✅ Safe - No threats detected"
            else:
                return "❓ No Data Found"
        else:
            return f"❌ Error: {response.status_code} - {response.text}"

    except Exception as e:
        return f"❌ API Error: {str(e)}"

# Route to display the detection form
@detect_blueprint.route("/detect", methods=["GET"])
def detect_form():
    return render_template("detect/detect.html", email_result=None, url_results=None)

# Route to handle phishing detection
@detect_blueprint.route("/detect", methods=["POST"])
def detect():
    try:
        # Get email content
        email = request.form.get("email", "").strip()
        if not email:
            return render_template("detect/detect.html", email_result="⚠️ Error: Email content is required", url_results=None)

        email_result = None
        url_results = []

        # Check email for phishing using ML model
        vect = vectorizer.transform([email])
        prediction = model.predict(vect)[0]

        email_result = "⚠️ Potential phishing email detected!" if prediction == 1 else "✅ This email appears safe."

        # Extract and check URLs
        urls = extract_urls(email)
        if urls:
            for url in urls:
                reputation = check_domain_reputation(url)
                url_results.append(f"{reputation} - {url}")
        else:
            url_results.append("ℹ️ No URLs found in the email content.")

        return render_template("detect/detect.html", email_result=email_result, url_results=url_results)

    except Exception as e:
        return render_template("detect/detect.html", email_result=f"❌ An error occurred: {str(e)}", url_results=None)
