from voice_model import load_emotion_model, predict_emotion

# -------------------------------
# Test with Audio File
# -------------------------------
audio_file = "dataset/Sad/03a05Tc.wav"
model = load_emotion_model()
print("Predicted Emotion:", predict_emotion(model, audio_file)[0])
