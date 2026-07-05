import pandas as pd
import random
import os
import joblib

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# -----------------------------
# Scam Messages
# -----------------------------

scam_messages = [

"Congratulations! You won ₹500000. Click here to claim.",
"Your bank account has been blocked. Verify immediately.",
"Share your OTP to receive cashback.",
"Limited offer! Claim your free iPhone now.",
"Update your KYC today to avoid account suspension.",
"Click here to receive your lottery prize.",
"You have won a lucky draw. Verify now.",
"Urgent! Your UPI account is blocked.",
"Claim your refund immediately.",
"Your account is under verification. Login now."

]

# -----------------------------
# Safe Messages
# -----------------------------

safe_messages = [

"Meeting is scheduled at 10 AM tomorrow.",
"Happy Birthday! Have a wonderful day.",
"Please submit your assignment before Friday.",
"Dinner at 8 PM tonight?",
"Your Amazon order has been delivered.",
"Project review meeting starts at 2 PM.",
"Your electricity bill has been paid successfully.",
"Thank you for shopping with us.",
"Bus will arrive in 10 minutes.",
"Your package is out for delivery."

]

data = []

# Generate 500 scam messages
for i in range(500):

    data.append({

        "text": random.choice(scam_messages),

        "label": 1

    })

# Generate 500 safe messages
for i in range(500):

    data.append({

        "text": random.choice(safe_messages),

        "label": 0

    })

random.shuffle(data)

df = pd.DataFrame(data)

# Save dataset
os.makedirs("dataset", exist_ok=True)

df.to_csv("dataset/scam_dataset.csv", index=False)

# Train Model

model = Pipeline([

("tfidf", TfidfVectorizer()),

("classifier", MultinomialNB())

])

model.fit(df["text"], df["label"])

os.makedirs("model", exist_ok=True)

joblib.dump(model, "model/model.pkl")

print("✅ Dataset Created")

print("✅ Model Trained Successfully")

print("✅ model.pkl Saved")