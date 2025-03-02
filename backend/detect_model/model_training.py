import pandas as pd
import re
import matplotlib.pyplot as plt 
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
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

# Model training
model = GradientBoostingClassifier(n_estimators=300, learning_rate=0.05, random_state=42)
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
