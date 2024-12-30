# src/nlp/infer.py
import pickle
import json
import random

def generate_response(input_text):
    try:
        # Load the model and vectorizer
        with open('models/model.pkl', 'rb') as model_file:
            model = pickle.load(model_file)
        with open('models/vectorizer.pkl', 'rb') as vec_file:
            vectorizer = pickle.load(vec_file)
            
        # Load intents for responses
        with open('data/intents.json', 'r') as f:
            intents = json.load(f)

        # Transform input text
        X = vectorizer.transform([input_text])
        
        # Get prediction and probability
        tag = model.predict(X)[0]
        probabilities = model.predict_proba(X)[0]
        confidence = max(probabilities)
        
        # Find matching intent and get random response
        for intent in intents['intents']:
            if intent['tag'] == tag:
                response = random.choice(intent['responses'])
                return response, confidence
                
        # Fallback response if no match found
        return "I'm not sure I understand. Could you please rephrase that?", 0.0
        
    except Exception as e:
        print(f"Error in generate_response: {e}")
        return "I'm having trouble processing your request right now.", 0.0