import streamlit as st
import pandas as pd
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

st.sidebar.header("Instructions")
st.sidebar.write("""
- Enter a single task OR
- Upload a CSV file with a column 'task'
""")

# --- Single task input ---
task_input = st.text_input("Enter a task:")
if st.button("Predict"):
    if task_input.strip() == "":
        st.warning("Please enter a task!")
    else:
        result = classify_task(task_input)
        st.success(f"Predicted Category: {result['label']} ({result['score']*100:.1f}%)")
        st.session_state.tasks[result['label']].append(task_input)

# --- Batch CSV upload ---
uploaded_file = st.file_uploader("Upload CSV of tasks", type=["csv"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    if "task" not in df.columns:
        st.error("CSV must have a column named 'task'.")
    else:
        for task in df["task"]:
            result = classify_task(task)
            st.session_state.tasks[result['label']].append(task)
        st.success("Tasks categorized successfully!")

# --- Display categorized tasks ---
st.subheader("Categorized Tasks")
for category, tasks in st.session_state.tasks.items():
    st.write(f"**{category}:**")
    if tasks:
        for t in tasks:
            st.write(f"- {t}")
    else:
        st.write("- No tasks yet -")

# --- Export categorized tasks ---
if st.button("Download Categorized Tasks as CSV"):
    all_tasks = []
    for category, tasks in st.session_state.tasks.items():
        for t in tasks:
            all_tasks.append({"task": t, "category": category})
    export_df = pd.DataFrame(all_tasks)
    export_df.to_csv("categorized_tasks.csv", index=False)
    st.success("CSV saved as 'categorized_tasks.csv' in local directory!")
