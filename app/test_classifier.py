from classifier import classify_task

tasks = [
    "Pay electricity bill",
    "Finish machine learning assignment",
    "Go for evening walk",
    "Prepare presentation for meeting"
]

for task in tasks:
    result = classify_task(task)
    print(f"Task: {task} -> Category: {result['label']} (Confidence: {result['score']:.2f})")