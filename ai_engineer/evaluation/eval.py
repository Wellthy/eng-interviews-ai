import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from ai.model import classify_urgency
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import numpy as np
import csv

def load_eval_dataset(filepath="data/eval_dataset.csv"):
    """Load evaluation dataset from CSV file."""
    try:
        messages = []
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Handle different column names (message_text vs text)
                text = row.get('message_text') or row.get('text')
                # Handle different label formats (ground_truth_label vs urgent)
                label = row.get('ground_truth_label') or row.get('urgent')
                
                messages.append({
                    "text": text,
                    "urgent": label.lower() in ('true', 'yes', '1', 'urgent'),
                    "category": row.get('category', ''),
                    "difficulty": row.get('difficulty', '')
                })
        return messages
    except FileNotFoundError:
        print(f"Error: {filepath} not found.")
        print("Please create data/eval_dataset.csv with columns: message_text, ground_truth_label")
        sys.exit(1)

# Load evaluation data
sample_messages = load_eval_dataset()

def evaluate_model():
    """Evaluate the urgency classification model on sample data."""
    print("Evaluating urgency classification model...")
    
    # Get predictions
    predictions = []
    actual = []
    confidences = []
    
    for msg in sample_messages:
        result = classify_urgency(msg["text"])
        pred = result["urgent"]
        confidence = result["confidence_score"]
        predictions.append(pred)
        confidences.append(confidence)
        actual.append(msg["urgent"])
        category = f" | Category: {msg['category']}" if msg.get('category') else ""
        print(f"Text: {msg['text'][:50]}... | Predicted: {pred} (conf: {confidence:.2f}) | Actual: {msg['urgent']}{category}")
    
    # Classification report
    print("\nClassification Report:")
    print(classification_report(actual, predictions, target_names=['Not Urgent', 'Urgent']))
    
    # Confusion matrix
    cm = confusion_matrix(actual, predictions)
    print("\nConfusion Matrix:")
    print(cm)
    
    # Plot confusion matrix
    plt.figure(figsize=(6, 4))
    plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    plt.title('Confusion Matrix - Urgency Classification')
    plt.colorbar()
    tick_marks = np.arange(2)
    plt.xticks(tick_marks, ['Not Urgent', 'Urgent'])
    plt.yticks(tick_marks, ['Not Urgent', 'Urgent'])
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    
    # Add text annotations
    thresh = cm.max() / 2.
    for i, j in np.ndindex(cm.shape):
        plt.text(j, i, format(cm[i, j], 'd'),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")
    
    plt.tight_layout()
    plt.savefig('evaluation/confusion_matrix.png')
    print("\nConfusion matrix saved to evaluation/confusion_matrix.png")

if __name__ == "__main__":
    evaluate_model()