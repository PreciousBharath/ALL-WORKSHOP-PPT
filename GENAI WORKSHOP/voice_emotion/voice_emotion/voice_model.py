from pathlib import Path

import joblib
import librosa
import numpy as np


BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "voice_emotion_model.joblib"
EMOTIONS = ("Angry", "Happy", "Neutral", "Sad")
SUPPORTED_AUDIO = {".wav", ".mp3", ".m4a", ".ogg", ".webm"}


class CentroidEmotionModel:
    def fit(self, features, labels):
        self.classes_ = np.array(sorted(set(labels)))
        self.mean_ = features.mean(axis=0)
        self.scale_ = features.std(axis=0)
        self.scale_[self.scale_ == 0] = 1
        normalized = (features - self.mean_) / self.scale_
        self.centroids_ = np.array([normalized[labels == label].mean(axis=0) for label in self.classes_])
        return self

    def decision_function(self, features):
        normalized = (features - self.mean_) / self.scale_
        return -np.linalg.norm(normalized[:, None, :] - self.centroids_[None, :, :], axis=2)

    def predict(self, features):
        return self.classes_[np.argmax(self.decision_function(features), axis=1)]


def extract_features(file_path, n_mfcc=20):
    audio, sample_rate = librosa.load(file_path, sr=16000, duration=4, offset=0)
    if audio.size == 0:
        raise ValueError("The audio file contains no readable samples.")

    mfcc = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=n_mfcc)
    return np.concatenate((mfcc.mean(axis=1), mfcc.std(axis=1))).astype(np.float32)


def load_emotion_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError("The model has not been trained yet. Run train_voice_emotion.py first.")
    return joblib.load(MODEL_PATH)


def predict_emotion(model, audio_path):
    features = extract_features(audio_path).reshape(1, -1)
    scores = model.decision_function(features)[0]
    probabilities = np.exp(scores - np.max(scores))
    probabilities /= probabilities.sum()
    emotion_index = int(np.argmax(scores))
    return model.classes_[emotion_index], round(float(probabilities[emotion_index]) * 100, 2)