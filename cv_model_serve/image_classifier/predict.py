from numpy import argmax, ndarray
from tensorflow.keras.models import Model


def predict(model: Model, sample: ndarray) -> dict:
    """Classify one pre-processed image sample as NSFW or not."""
    # Prediction at index 0 is NSFW
    index_labels = {0: "NSFW", 1: "suitable"}

    prediction = model(sample)
    winner_index = argmax(prediction)

    label = index_labels.get(winner_index)
    if label is None:  # This shouldn't happen
        raise ValueError(
            f"Unexpected prediction shape: {prediction.shape}. Should be (1, 2)"
        )

    return {"prediction": label, "confidence": float(prediction[0, winner_index])}
