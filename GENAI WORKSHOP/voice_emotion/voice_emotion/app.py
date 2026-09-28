import os
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

from voice_model import BASE_DIR, SUPPORTED_AUDIO, load_emotion_model, predict_emotion

# -------------------------------
# Flask Configuration
# -------------------------------
app = Flask(__name__)
app.secret_key = "voice_emotion_secret"

UPLOAD_FOLDER = BASE_DIR / "static" / "uploads"

app.config["UPLOAD_FOLDER"] = str(UPLOAD_FOLDER)
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# -------------------------------
# Load Model & Encoder
# -------------------------------
model = load_emotion_model()

# -------------------------------
# Helper Functions
# -------------------------------
def allowed_file(filename):
    return "." in filename and Path(filename).suffix.lower() in SUPPORTED_AUDIO

# -------------------------------
# Routes
# -------------------------------
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        if "audio" not in request.files:
            flash("No file uploaded")
            return redirect(request.url)

        file = request.files["audio"]

        if file.filename == "":
            flash("No file selected")
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(file_path)

            emotion, confidence = predict_emotion(model, file_path)

            print("File saved:", file_path)
            print("Prediction:", emotion, confidence)

            return render_template(
                "result.html",
                emotion=emotion,
                confidence=confidence,
                audio_file=filename
            )

        else:
            flash("Only WAV files are allowed")

    return render_template("index.html")


@app.route("/logout")
def logout():
    return redirect(url_for("index"))


@app.route("/about")
def about():
    return render_template("about.html")

# -------------------------------
# Run Server
# -------------------------------
if __name__ == "__main__":
    app.run()
