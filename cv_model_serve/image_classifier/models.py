from pathlib import Path
from typing import Any, List

from tensorflow.keras import models
from tensorflow.keras.models import Model

DEFAULT_MODEL = "image-content-filtration.h5"
MODELS_DIR = Path(__file__).parent / "cv_models"
LOADED_MODELS: dict[str, Any] = {}


def get_models() -> List[str]:
    """Get the list of available models."""
    return list(str(model_file.name) for model_file in MODELS_DIR.glob("*.h5"))


def get_model(model_name: str) -> Any:
    """Gets the model given a path either from the cache or loads it."""
    if model_name not in LOADED_MODELS:
        model_path = MODELS_DIR / model_name
        LOADED_MODELS[model_name] = _load_model(model_path)

    return LOADED_MODELS[model_name]


def _load_model(path: Path) -> Model:
    return models.load_model(path)
