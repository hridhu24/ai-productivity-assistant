from classifier import classify_task

tasks = [
    "Finish project report",
    "Read a book on AI",
    "Pay electricity bill",
    "Go for a walk"
]

for task in tasks:
    result = classify_task(task)
    print(f"Task: {task}\nPredicted: {result['label']} ({result['score']*100:.1f}%)\n")
