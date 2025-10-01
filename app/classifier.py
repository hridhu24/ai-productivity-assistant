# app/classifier.py

from transformers import pipeline

# Load the zero-shot classifier once (slow, but only at startup)
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli", framework="pt")  # PyTorch for now

# Define candidate categories
CATEGORIES = [
    "Work / Office Task",
    "Study / Learning Task",
    "Personal / Daily Life Task",
    "Finance / Money Task"
]

def classify_task(task: str) -> dict:
    """
    Classify a single task into a category.
    Returns a dictionary: {'label': category, 'score': confidence}
    """
    if not task.strip():
        return {"label": "Unknown", "score": 0.0}

    result = classifier(task, candidate_labels=CATEGORIES, multi_label=False)
    return {"label": result['labels'][0], "score": result['scores'][0]}
