import sounddevice as sd
import queue
import sys
import json
from vosk import Model, KaldiRecognizer

def real_time_transcription(model_path="model", sample_rate=16000):

    model = Model(model_path)
    recognizer = KaldiRecognizer(model, sample_rate)
    recognizer.SetWords(True)

    # Queue to store audio data
    audio_queue = queue.Queue()

    # Callback function to feed audio data into the queue
    def callback(indata, frames, time, status):
        if status:
            print(f"Error: {status}", file=sys.stderr)
        audio_queue.put(bytes(indata))

    # Start the audio stream
    try:
        with sd.RawInputStream(samplerate=sample_rate, blocksize=8000, dtype='int16',
                               channels=1, callback=callback):
            print("Listening (press Ctrl+C to stop)...")
            while True:
                # Read data from the queue
                data = audio_queue.get()
                if recognizer.AcceptWaveform(data):
                    result = json.loads(recognizer.Result())
                    print(f"Recognized: {result.get('text', '')}")
                else:
                    partial = json.loads(recognizer.PartialResult())
                    print(f"Partial: {partial.get('partial', '')}", end="\r")
    except KeyboardInterrupt:
        print("\nStopped listening.")
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)

if __name__ == "__main__":
    model_directory = "model" 
    real_time_transcription(model_directory)
