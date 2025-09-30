# app/classifier.py

from transformers import pipeline

# Load the zero-shot classifier once (slow, but only at startup)
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli", framework="pt")  # PyTorch for now

# Define candidate categories
CATEGORIES = ["Work", "Study", "Personal", "Finance"]

def classify_task(task_text):
    """
    Classify a task into one of the predefined categories using zero-shot classification.
    
    Args:
        task_text (str): Text description of the task.
        
    Returns:
        dict: Contains 'label' (predicted category) and 'score' (confidence)
    """
    result = classifier(task_text, candidate_labels=CATEGORIES)
    return {"label": result['labels'][0], "score": float(result['scores'][0])}
