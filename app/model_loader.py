import joblib
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

model_path = os.path.join(BASE_DIR, "models", "youtube_model.pkl")
encoder_path = os.path.join(BASE_DIR, "models", "label_encoder.pkl")

model = joblib.load(model_path)
label_encoder = joblib.load(encoder_path)
