import joblib
import numpy as np

from voice_model import BASE_DIR, EMOTIONS, SUPPORTED_AUDIO, CentroidEmotionModel, extract_features, MODEL_PATH

# -------------------------------
# Feature Extraction
# -------------------------------
dataset_path = BASE_DIR / "dataset"

X, y = [], []

for path in dataset_path.rglob("*"):
    if path.is_file() and path.suffix.lower() in SUPPORTED_AUDIO:
        emotion = next((candidate for candidate in EMOTIONS if candidate.lower() == path.parent.name.lower()), None)
        if emotion:
            X.append(extract_features(path))
            y.append(emotion)

X = np.array(X)
y = np.array(y)

if len(X) == 0:
    raise RuntimeError("No audio found. Add labeled files to dataset/<emotion>/ or dataset/Tamil/<emotion>/.")

X = np.asarray(X)
y = np.asarray(y)

# -------------------------------
# Train-Test Split
# -------------------------------
model = CentroidEmotionModel().fit(X, y)
joblib.dump(model, MODEL_PATH)

print(f"Training completed: {len(X)} files, classes={sorted(set(y))}")
print(f"Model saved to {MODEL_PATH}")
