# fraud-detection-dashboard
https://fraud-detection-dashboard-production-b376.up.railway.app/
# 🛡️ ScamShield AI

An AI-powered fraud detection platform that helps users identify potential online scams by analyzing text messages, transaction details, and screenshots. ScamShield AI combines Machine Learning, OCR, and rule-based analysis to detect suspicious patterns and generate actionable security recommendations.

---

## 🚀 Features

- 📩 Analyze SMS, WhatsApp, Email, and other text messages
- 💳 Detect suspicious transaction details
- 🖼️ OCR-based screenshot analysis
- 🤖 Machine Learning scam classification
- 📊 AI-generated fraud risk score
- ⚠️ Risk levels (Safe, Suspicious, Critical Scam)
- 📝 Detailed scam indicators and reasons
- 💡 Personalized safety recommendations
- 📜 Scan history using SQLite
- 📄 Generate downloadable PDF reports
- 📈 Analytics dashboard for scan statistics
- 🎨 Modern responsive web interface

---

## 🛠️ Tech Stack

### Frontend
- HTML5
- CSS3
- JavaScript

### Backend
- Python
- Flask

### Machine Learning
- Scikit-learn
- Joblib

### OCR
- Tesseract OCR
- Pillow

### Database
- SQLite

### Reporting
- ReportLab

---

## 📂 Project Structure

```
ScamShield-AI/
│
├── app.py
├── ocr.py
├── requirements.txt
├── scamshield.db
├── model/
│   └── model.pkl
├── uploads/
├── templates/
│   ├── index.html
│   └── analytics.html
├── static/
│   ├── style.css
│   ├── script.js
│   └── assets/
└── README.md
```

---

## ⚙️ Installation

```bash
git clone https://github.com/yourusername/scamshield-ai.git

cd scamshield-ai

pip install -r requirements.txt

python app.py
```

Open your browser and visit:

```
http://127.0.0.1:5000
```

---

## 🧠 How It Works

1. User enters a suspicious message, transaction details, or uploads a screenshot.
2. OCR extracts text from uploaded images.
3. The Machine Learning model predicts whether the content is safe or potentially fraudulent.
4. Rule-based checks identify indicators such as:
   - Suspicious links
   - OTP requests
   - KYC verification scams
   - Phone numbers
   - Money-related keywords
5. The application generates:
   - Fraud Risk Score
   - Risk Level
   - Reasons for detection
   - Security recommendations
6. Results are stored in SQLite and can be exported as a PDF report.

---

## 📊 Example Use Cases

- Banking SMS scams
- Fake KYC verification messages
- UPI payment fraud
- WhatsApp phishing
- Email scams
- QR code payment scams
- Fake parcel delivery messages

---

## 🔮 Future Enhancements

- Gemini AI-powered scam explanation
- URL reputation checking
- QR code scanner
- Multi-language support
- Voice scam detection
- Email phishing detection
- Real-time browser extension
- Mobile application
- Cloud deployment
- Admin dashboard with advanced analytics

---

## 📸 Screenshots

Add screenshots here:

- Home Page
- AI Analysis Report
- Screenshot Analysis
- Analytics Dashboard
- PDF Report

---

## 👨‍💻 Author

**Laxsanya RJ**

---

## 📄 License

This project is licensed under the MIT License.
