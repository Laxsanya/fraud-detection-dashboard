from flask import Flask, render_template, request
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
import re
import os
import sqlite3
import joblib
from datetime import datetime
from werkzeug.utils import secure_filename
from ocr import extract_text, allowed_file

app = Flask(__name__)

# -----------------------------
# Load ML Model
# -----------------------------
model = joblib.load("model/model.pkl")

# -----------------------------
# Upload folder
# -----------------------------
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# -----------------------------
# Database setup
# -----------------------------
def init_db():
    conn = sqlite3.connect("scamshield.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT,
            score INTEGER,
            level TEXT,
            color TEXT,
            timestamp TEXT
        )
    """)

    conn.commit()
    conn.close()

init_db()

# -----------------------------
# Home route
# -----------------------------
@app.route("/")
def home():
    return render_template("index.html")

# -----------------------------
# Analyze route
# -----------------------------
@app.route("/analyze", methods=["POST"])
def analyze():

    message = request.form.get("message", "")
    transaction = request.form.get("transaction", "")

    uploaded_file = request.files.get("image")

    ocr_text = ""

    # -------------------------
    # OCR Processing
    # -------------------------
    if uploaded_file and uploaded_file.filename != "":
        if allowed_file(uploaded_file.filename):

            filename = secure_filename(uploaded_file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            uploaded_file.save(filepath)

            ocr_text = extract_text(filepath)

    # -------------------------
    # Combine all input
    # -------------------------
    text = (message + " " + transaction + " " + ocr_text).lower()

    # -----------------------------
    # ML Prediction
    # -----------------------------
    prediction = model.predict([text])[0]
    confidence = int(max(model.predict_proba([text])[0]) * 100)

    reasons = []

    lower = text.lower()

    # -----------------------------
    # Rule-based reasons
    # -----------------------------
    if re.search(r'https?://', lower):
        reasons.append("Contains suspicious link")

    if re.search(r'\d{10}', lower):
        reasons.append("Contains phone number")

    if "otp" in lower:
        reasons.append("Requests OTP (high risk)")

    if "kyc" in lower:
        reasons.append("KYC verification scam pattern")

    if "₹" in text or "$" in text:
        reasons.append("Mentions money transaction")

    # -----------------------------
    # Prediction result logic
    # -----------------------------
    if prediction == 1:

        if confidence < 60:
            confidence = 60

        level = "Suspicious"
        color = "orange"

        if confidence >= 80:
            level = "Critical Scam"
            color = "red"

        tips = [
            "Do NOT click unknown links.",
            "Never share OTP or passwords.",
            "Verify with official sources.",
            "Contact bank if needed."
        ]

    else:

        if confidence < 60:
            confidence = 60

        level = "Safe"
        color = "green"

        tips = [
            "No major scam indicators found.",
            "Still verify unknown messages."
        ]

    # -----------------------------
    # Save to database
    # -----------------------------
    conn = sqlite3.connect("scamshield.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO history (text, score, level, color, timestamp)
        VALUES (?, ?, ?, ?, ?)
    """, (
        text,
        confidence,
        level,
        color,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()

    # -----------------------------
    # Load history
    # -----------------------------
    conn = sqlite3.connect("scamshield.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT score, level, color, text, timestamp
        FROM history
        ORDER BY id DESC
        LIMIT 10
    """)

    rows = cursor.fetchall()
    conn.close()

    history = []

    for row in rows:
        history.append({
            "score": row[0],
            "level": row[1],
            "color": row[2],
            "text": row[3],
            "timestamp": row[4]
        })

    # -----------------------------
    # Result object
    # -----------------------------
    result = {
        "score": confidence,
        "level": level,
        "color": color,
        "reasons": reasons,
        "tips": tips,
        "text": text
    }

    return render_template(
        "index.html",
        result=result,
        history=history
    )

# -----------------------------
# Analytics route
# -----------------------------
@app.route("/analytics")
def analytics():

    conn = sqlite3.connect("scamshield.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM history")
    total_scans = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM history WHERE level='Safe'")
    safe = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM history WHERE level != 'Safe'")
    scam = cursor.fetchone()[0]

    cursor.execute("SELECT level, COUNT(*) FROM history GROUP BY level")
    rows = cursor.fetchall()

    conn.close()

    labels = []
    values = []

    for row in rows:
        labels.append(row[0])
        values.append(row[1])

    return render_template(
        "analytics.html",
        total_scans=total_scans,
        safe=safe,
        scam=scam,
        labels=labels,
        values=values
    )

# -----------------------------
# Run app
# -----------------------------
@app.route("/download-report")
def download_report():

    conn = sqlite3.connect("scamshield.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT score, level, text, timestamp
        FROM history
        ORDER BY id DESC
        LIMIT 1
    """)

    row = cursor.fetchone()
    conn.close()

    if not row:
        return "No data available"

    score, level, text, timestamp = row

    file_path = "report.pdf"
    doc = SimpleDocTemplate(file_path, pagesize=A4)

    styles = getSampleStyleSheet()
    content = []

    content.append(Paragraph("🛡 ScamShield AI Report", styles["Title"]))
    content.append(Spacer(1, 12))

    content.append(Paragraph(f"<b>Score:</b> {score}%", styles["Normal"]))
    content.append(Paragraph(f"<b>Risk Level:</b> {level}", styles["Normal"]))
    content.append(Paragraph(f"<b>Time:</b> {timestamp}", styles["Normal"]))
    content.append(Spacer(1, 12))

    content.append(Paragraph("<b>Analyzed Text:</b>", styles["Heading2"]))
    content.append(Paragraph(text, styles["Normal"]))

    doc.build(content)

    return f"Report generated successfully! Saved as {file_path}"
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)