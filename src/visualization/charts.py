# src/visualization/charts.py
import streamlit as st
import plotly.express as px
import pandas as pd
from textblob import TextBlob

def plot_confidence_scores(history):
    if not history:
        return
    
    scores = [msg.get('confidence', 0) for msg in history if 'confidence' in msg]
    df = pd.DataFrame({
        'Message': range(1, len(scores) + 1),
        'Confidence': scores
    })
    
    fig = px.line(df, x='Message', y='Confidence', 
                  title='Response Confidence Over Time')
    st.plotly_chart(fig)

def plot_sentiment_analysis(history):
    if not history:
        return
    
    sentiments = []
    for msg in history:
        if 'user' in msg:
            blob = TextBlob(msg['user'])
            sentiments.append(blob.sentiment.polarity)
    
    df = pd.DataFrame({
        'Message': range(1, len(sentiments) + 1),
        'Sentiment': sentiments
    })
    
    fig = px.scatter(df, x='Message', y='Sentiment',
                     title='Message Sentiment Analysis')
    st.plotly_chart(fig)