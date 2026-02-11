from fastapi import FastAPI
import pandas as pd

from app.model_loader import model, label_encoder
from app.feature_engineering import create_features


app = FastAPI()

@app.get("/")
def home():
    return {"message": "YouTube Success Predictor API running"}

@app.post("/predict")
def predict(data: dict):
    """
    Predict video success category from metadata.
    
    Expected input:
    {
        "title": str,
        "description": str,
        "tags": str,
        "views": int,
        "likes": int,
        "comment_count": int,
        "publish_hour": int
    }
    """
    try:
        features = create_features(data)
        
        # Ensure features are in the correct order
        feature_order = [
            'title_length',
            'description_length',
            'num_tags',
            'publish_hour',
            'like_view_ratio',
            'comment_view_ratio',
            'like_comment_ratio',
            'uppercase_words',
            'title_contains_number',
            'title_word_count',
            'description_word_count',
            'average_word_length_title'
        ]
        
        ordered_features = {key: features[key] for key in feature_order}
        df = pd.DataFrame([ordered_features])

        prediction = model.predict(df)
        label = label_encoder.inverse_transform(prediction)

        return {"prediction": label[0]}
    
    except Exception as e:
        return {"error": str(e), "status": 500}
