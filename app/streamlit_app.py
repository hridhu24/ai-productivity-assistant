import streamlit as st
from classifier import classify_task

st.set_page_config(page_title="AI Task Manager", layout="wide")
st.title("📝 AI Task Manager")

# Initialize session state for tasks
if "tasks" not in st.session_state:
    st.session_state.tasks = {
        "Work / Office Task": [],
        "Study / Learning Task": [],
        "Personal / Daily Life Task": [],
        "Finance / Money Task": []
    }

# Input box
task_input = st.text_input("Enter your task:")

# Predict button
if st.button("Predict"):
    if task_input.strip() == "":
        st.warning("Please enter a task!")
    else:
        result = classify_task(task_input)
        st.success(f"Predicted Category: {result['label']} ({result['score']*100:.1f}%)")

        # Add task to appropriate category list
        st.session_state.tasks[result['label']].append(task_input)

# Display all tasks in categorized lists
st.subheader("Categorized Tasks")
for category, tasks in st.session_state.tasks.items():
    st.write(f"**{category}:**")
    if tasks:
        for t in tasks:
            st.write(f"- {t}")
    else:
        st.write("- No tasks yet -")
