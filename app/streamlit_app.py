import streamlit as st
import pandas as pd
from classifier import classify_task

SAVE_FILE = "data/tasks_persistent.csv"

st.set_page_config(page_title="AI Task Manager", layout="wide")
st.title("📝 AI Task Manager")

# --- Initialize session state ---
if "tasks" not in st.session_state:
    try:
        df_load = pd.read_csv(SAVE_FILE)
        st.session_state.tasks = {
            cat: df_load[df_load["category"]==cat]["task"].tolist()
            for cat in df_load["category"].unique()
        }
        # Ensure all categories exist
        for cat in ["Work / Office Task","Study / Learning Task",
                    "Personal / Daily Life Task","Finance / Money Task"]:
            if cat not in st.session_state.tasks:
                st.session_state.tasks[cat] = []
    except FileNotFoundError:
        st.session_state.tasks = {
            "Work / Office Task": [],
            "Study / Learning Task": [],
            "Personal / Daily Life Task": [],
            "Finance / Money Task": []
        }

# --- Sidebar instructions ---
st.sidebar.header("Instructions")
st.sidebar.write("""
- Enter a single task OR
- Upload a CSV file with a column 'task'
- Edit/Delete tasks directly in the lists
- Save tasks to persist changes
""")

# --- Single task input ---
task_input = st.text_input("Enter a task:")
if st.button("Predict"):
    if task_input.strip() == "":
        st.warning("Please enter a task!")
    else:
        result = classify_task(task_input)
        st.session_state.tasks[result['label']].append(task_input)
        st.success(f"Predicted Category: {result['label']} ({result['score']*100:.1f}%)")

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

# --- Display categorized tasks with Edit/Delete ---
st.subheader("Categorized Tasks")
for category, tasks in st.session_state.tasks.items():
    st.write(f"**{category} ({len(tasks)} tasks):**")
    if tasks:
        for i, t in enumerate(tasks):
            col1, col2, col3 = st.columns([6,1,1])
            with col1:
                new_task = st.text_input(f"{category}-{i}", t)
            with col2:
                if st.button("Edit", key=f"edit-{category}-{i}"):
                    tasks[i] = new_task
                    st.success("Task updated!")
            with col3:
                if st.button("Delete", key=f"del-{category}-{i}"):
                    tasks.pop(i)
                    st.warning("Task deleted!")
    else:
        st.write("- No tasks yet -")

# --- Save tasks for persistence ---
if st.button("Save All Tasks"):
    all_tasks = []
    for cat, ts in st.session_state.tasks.items():
        for t in ts:
            all_tasks.append({"task": t, "category": cat})
    df_save = pd.DataFrame(all_tasks)
    df_save.to_csv(SAVE_FILE, index=False)
    st.success(f"All tasks saved to {SAVE_FILE}")

# --- Export tasks as CSV ---
if st.button("Download Categorized Tasks as CSV"):
    all_tasks = []
    for category, tasks in st.session_state.tasks.items():
        for t in tasks:
            all_tasks.append({"task": t, "category": category})
    export_df = pd.DataFrame(all_tasks)
    export_df.to_csv("categorized_tasks.csv", index=False)
    st.success("CSV saved as 'categorized_tasks.csv' in local directory!")
