import os
from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
from fastapi.middleware.cors import CORSMiddleware

MODEL_DIR = "./model"
BASE_MODEL = "distilbert-base-uncased-finetuned-sst-2-english"

class PredictRequest(BaseModel):
    text: str

class PredictResponse(BaseModel):
    label: str
    score: float

def load_model():
    if os.path.exists(MODEL_DIR) and len(os.listdir(MODEL_DIR)) > 0:
        print("Loading fine-tuned model from:", MODEL_DIR)
        tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
        model = AutoModelForSequenceClassification.from_pretrained(MODEL_DIR)
    else:
        print("Fine-tuned model not found. Loading base model:", BASE_MODEL)
        tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)
        model = AutoModelForSequenceClassification.from_pretrained(BASE_MODEL)

    return pipeline("sentiment-analysis", model=model, tokenizer=tokenizer, device=-1)

app = FastAPI()
sentiment_pipeline = load_model()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Electronix AI Sentiment Analysis API"}

@app.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest):
    prediction = sentiment_pipeline(request.text)[0]

    return PredictResponse(label=prediction['label'].lower(), score=prediction['score'])

