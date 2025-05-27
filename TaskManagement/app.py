from flask import Flask, render_template, request, jsonify
import pandas as pd
import joblib
import string
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from collections import defaultdict

app = Flask(__name__)

# Load models
svm_model = joblib.load(r"D:\TaskManagement\models\final_svm_model.pkl")
rf_model = joblib.load(r"D:\TaskManagement\models\final_rf_model.pkl")
tfidf = joblib.load(r"D:\TaskManagement\models\tfidf_vectorizer.pkl")
task_encoder = joblib.load(r"D:\TaskManagement\models\task_label_encoder.pkl")
priority_encoder = joblib.load(r"D:\TaskManagement\models\priority_label_encoder.pkl")

# Load dataset
df = pd.read_csv(r"C:\Users\admin\OneDrive\Documents\ai_task_management_dataset.csv")
workload = defaultdict(int, df['assignee'].value_counts().to_dict())

# NLP Preprocessing
stop_words = set(stopwords.words('english'))
stemmer = PorterStemmer()

def preprocess_text(text):
    text = re.sub(r'\d+', '', text)
    text = text.translate(str.maketrans('', '', string.punctuation)).lower()
    words = text.split()
    words = [stemmer.stem(w) for w in words if w not in stop_words]
    return ' '.join(words)

# Assign user
def assign_user():
    user = min(workload, key=workload.get)
    workload[user] += 1
    return user

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        description = request.form["description"]
        clean_text = preprocess_text(description)
        vector = tfidf.transform([clean_text])
        
        task_pred = task_encoder.inverse_transform(svm_model.predict(vector))[0]
        priority_pred = priority_encoder.inverse_transform(rf_model.predict(vector))[0]
        assigned_user = assign_user()

        result = {
            "description": description,
            "task_type": task_pred,
            "priority": priority_pred,
            "assigned_to": assigned_user,
            "workload": dict(workload)
        }
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
