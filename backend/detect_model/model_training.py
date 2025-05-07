import pandas as pd
import re
import matplotlib.pyplot as plt 
import string
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import pickle

df1 = pd.read_csv('data/Enron.csv')
df2 = pd.read_csv('data/Ling.csv')

df = pd.concat([df1, df2], ignore_index=True) # Combine both datasets

df = df.drop_duplicates()

print("Class Distribution:")
print(df['label'].value_counts())

def clean_text(text):
    if isinstance(text, str):
        text = text.lower()
        text = re.sub(f"[{string.punctuation}]", "", text)  # Remove punctuation
        text = re.sub("\\d+", "", text)  # Remove numbers
        text = re.sub("\\s+", " ", text).strip()  # Remove extra spaces
        return text
    return ""

df['cleaned_text'] = df['body'].apply(clean_text)

# Remove very short emails
df = df[df['cleaned_text'].str.len() > 20]

# Ensure both classifications remain after filtering to avoid training crashes
if df['label'].nunique() < 2:
    print("Warning: Only one class remains after filtering. Adjusting length thresholds...")
    df = df[df['cleaned_text'].str.len() > 10]

X = df['cleaned_text']
y = df['label']

# Text preprocessing and vectorization
vectorizer = TfidfVectorizer(stop_words='english', max_features=5000, ngram_range=(1,2))
X_vectorized = vectorizer.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X_vectorized, y, test_size=0.3, random_state=42)

model = LogisticRegression(max_iter=1000, random_state=42)
model.fit(X_train, y_train)

threshold = 0.5
y_probs = model.predict_proba(X_test)[:, 1]
y_pred = (y_probs > threshold).astype(int)

print("Accuracy:", accuracy_score(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))

# Confusion matrix
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=["Not Phishing", "Phishing"], yticklabels=["Not Phishing", "Phishing"])
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")
plt.show()

# Save the model and vectorizer onto .pkl files for reading
with open('backend/model.pkl', 'wb') as model_file:
    pickle.dump(model, model_file)
    print("Model saved")

with open('backend/vectorizer.pkl', 'wb') as vectorizer_file:
    pickle.dump(vectorizer, vectorizer_file)
    print("Vectorizer saved")