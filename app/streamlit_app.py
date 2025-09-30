import streamlit as st
from classifier import classify_task

st.set_page_config(page_title="AI Task Categorizer", layout="centered")

st.title("AI Productivity Assistant")
st.write("Type a task below and the AI will categorize it for you!")

# Input text box
task_input = st.text_input("Enter your task:")

if task_input:
    result = classify_task(task_input)
    st.subheader("Predicted Category:")
    st.write(f"**{result['label']}** (Confidence: {result['score']:.2f})")