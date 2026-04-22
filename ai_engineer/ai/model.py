from transformers import pipeline
from typing import Dict, Any

# Load model
MODEL_NAME = "facebook/bart-large-mnli"
MODEL_VERSION = "1.0"
classifier = pipeline("zero-shot-classification", model=MODEL_NAME)

def classify_urgency(message: str) -> Dict[str, Any]:
    """
    Classify if a member's message is urgent or not urgent.
    
    Args:
        message (str): The message text to classify.
    
    Returns:
        dict: Contains:
            - urgent (bool): Whether the message is classified as urgent
            - confidence_score (float): Confidence score (0-1) of the prediction
            - model_version (str): Version of the model used
            - reasoning (str): Brief explanation of the classification
    """
    candidate_labels = ["urgent", "not urgent"]
    result = classifier(message, candidate_labels)
    
    # Extract label and its score
    top_label = result['labels'][0]
    confidence = result['scores'][0]
    is_urgent = top_label == "urgent"
    
    # Generate reasoning based on confidence and label
    if confidence < 0.5:
        reasoning = f"Low confidence ({confidence:.2f}). Classification is uncertain."
    elif confidence < 0.7:
        reasoning = f"Moderate confidence ({confidence:.2f}). Message shows some urgency indicators."
    else:
        reasoning = f"High confidence ({confidence:.2f}). Message clearly conveys urgency." if is_urgent else f"High confidence ({confidence:.2f}). Message does not appear urgent."
    
    return {
        "urgent": is_urgent,
        "confidence_score": round(confidence, 4),
        "model_version": MODEL_VERSION,
        "reasoning": reasoning
    }