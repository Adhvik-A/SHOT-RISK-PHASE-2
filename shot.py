from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from schemas import ShotRiskRequest, ShotRiskResponse
from services import process_shot_risk

app = FastAPI(
    title="Shot Risk Efficiency API",
    description="Evaluates whether a cricket shot is strategically efficient using expected value and contextual wicket cost.",
    version="2.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {
        "message": "Shot Risk Efficiency API is running",
        "version": "2.0"
    }





# 🔹 Health Check
@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "shot-risk-api"
    }


# 🔹 Description Endpoint
@app.get("/description")
def description():
    return {
        "The API Evaluates whether a shot is worth playing using expected value.",
            }


@app.post("/shot-risk", response_model=ShotRiskResponse)
def shot_risk(payload: ShotRiskRequest):
    return process_shot_risk(payload.dict())