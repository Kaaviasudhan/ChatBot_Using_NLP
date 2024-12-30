import os
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
import pickle


def train_model(data_path):
    # Check if 'models' directory exists, create it if not
    if not os.path.exists('models'):
        os.makedirs('models')

    with open(data_path, 'r') as f:
        intents = json.load(f)

    texts = []
    labels = []

    for intent in intents['intents']:
        for pattern in intent['patterns']:
            texts.append(pattern)
            labels.append(intent['tag'])

    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(texts)

    model = SVC(kernel='linear', probability=True)
    model.fit(X, labels)

    with open('models/model.pkl', 'wb') as model_file:
        pickle.dump(model, model_file)
    with open('models/vectorizer.pkl', 'wb') as vec_file:
        pickle.dump(vectorizer, vec_file)

print("Training model...")
train_model('data/intents.json')
print("Model trained successfully!")
