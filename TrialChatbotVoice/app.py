from flask import Flask, render_template, request, jsonify
import vosk  # Vosk for voice processing
import json

app = Flask(__name__)

# Load the Vosk model
# Replace with the correct model path you downloaded.
model_path = "model"
model = vosk.Model(model_path)

@app.route("/")
def home():
    return render_template("index.html")  # Ensure your HTML file is in the "templates" folder

@app.route("/process-message", methods=["POST"])
def process_message():
    data = request.json
    user_message = data.get("message", "")

    # For example, respond with an echo
    response_message = f"Echo: {user_message}"
    return jsonify({"response": response_message})

@app.route("/process-voice", methods=["POST"])
def process_voice():
    # Process the uploaded audio file using vosk
    if "audio" not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    audio_file = request.files["audio"]
    audio_data = audio_file.read()

    # Convert audio to text (using Vosk)
    rec = vosk.KaldiRecognizer(model, 16000)
    if rec.AcceptWaveform(audio_data):
        result = json.loads(rec.Result())
        return jsonify({"transcription": result.get("text", "")})
    else:
        return jsonify({"error": "Failed to transcribe"}), 400


if __name__ == "__main__":
    app.run(debug=True)
