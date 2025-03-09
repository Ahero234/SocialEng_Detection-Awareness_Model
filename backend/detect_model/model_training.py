import pandas as pd
import re
import matplotlib.pyplot as plt 
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression  # Changed to Logistic Regression
from sklearn.metrics import accuracy_score, classification_report
import pickle

# Load dataset
df = pd.read_csv('data/Enron.csv')

# Remove duplicates
df = df.drop_duplicates()

# Check class distribution
print("Class Distribution:")
print(df['label'].value_counts())

# Display basic info and first few rows
print(df.info())
print(df.head())

# Preprocessing function
def clean_text(text):
    if isinstance(text, str):
        text = text.lower()
        text = re.sub(f"[{string.punctuation}]", "", text)  # Remove punctuation
        text = re.sub("\\d+", "", text)  # Remove numbers
        text = re.sub("\\s+", " ", text).strip()  # Remove extra spaces
        return text
    return ""

df['cleaned_text'] = df['body'].apply(clean_text)

# Remove very short and very long emails
df = df[df['cleaned_text'].str.len() > 20]

# Ensure both classes remain after filtering
if df['label'].nunique() < 2:
    print("Warning: Only one class remains after filtering. Adjusting thresholds...")
    df = df[df['cleaned_text'].str.len() > 10]

# Prepare features and labels
X = df['cleaned_text']
y = df['label']

# Text preprocessing and vectorization
vectorizer = TfidfVectorizer(stop_words='english', max_features=5000, ngram_range=(1,2))
X_vectorized = vectorizer.fit_transform(X)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X_vectorized, y, test_size=0.3, random_state=42)

# Model training with Logistic Regression
model = LogisticRegression(max_iter=1000, random_state=42)  # Use Logistic Regression
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))

# Create the bar chart
fig, ax = plt.subplots()
labels = df['label'].value_counts().index
values = df['label'].value_counts().values
colors = ['blue' if label == 0 else 'red' for label in labels]
ax.bar(labels, values, color=colors)
ax.set_xlabel('Category')
ax.set_ylabel('Count')
ax.set_title('Categorical Distribution')
for i, v in enumerate(values):
    ax.text(i, v + 50, str(v), ha='center', fontsize=10)
plt.show()

# Save the model and vectorizer
with open('backend/model.pkl', 'wb') as model_file:
    pickle.dump(model, model_file)
    print("Model saved")

with open('backend/vectorizer.pkl', 'wb') as vectorizer_file:
    pickle.dump(vectorizer, vectorizer_file)
    print("Vectorizer saved")


'''import string
import numpy as np
import pandas as pd

import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier


nltk.download('stopwords')

df = pd.read_csv('data/Enron.csv')

df['text'] = df['text'].apply(lambda x: x.replace('\r\n', ' '))
df.info()

stemmer = PorterStemmer()
corpus = []

stopwords_set = set(stopwords.words('english'))     

for i in range(len(df)):
    text = df['text'].iloc[i].lower()
    text = text.translate(str.maketrans('', '', string.punctuation)).split()
    text = [stemmer.stem(word) for word in text if word not in stopwords_set]
    text = ''.join(text)
    corpus.append(text)

vectorizer = CountVectorizer()

X = vectorizer.fit_transform(corpus).toarray()
y = df.label

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

classifier = RandomForestClassifier(n_jobs=-1)
classifier(X_train, y_train)

classifier.score(X_test, y_test)

email = df.text.values[10]

email_text = email.lower().translate(str.maketrans('', '', string.punctuation)).split()
email_text = [stemmer.stem(word) for word in email_text if word not in stopwords_set]
email_text = ''.join(email_text)

email_corpus = [email_text]

X_email = vectorizer.transform(email_corpus)

classifier.predict(X_email)

df.label.iloc[10]'''