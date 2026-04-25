from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from schemas import ShotRiskRequest, ShotRiskResponse
from services import process_shot_risk

app = FastAPI(
    title="Shot Risk Efficiency API",
    description=(
        "Evaluates whether a cricket shot is strategically efficient "
        
    ),
    version="2.0",
)

# ── CORS ──────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── / ─────────────────────────────────────────────────────────────────────────
@app.get("/")
def home():
    return {
        "meta": {
            "api": "shot-risk",
            "version": "2.0",
            "status": "success",
        },
        "data": {
            "message": "Shot Risk Efficiency API is running",
            "docs": "/docs",
            "health": "/health",
            "description": "/description",
        },
        "errors": None,
    }


# ── /health ───────────────────────────────────────────────────────────────────
@app.get("/health")
def health():
    return {
        "meta": {
            "api": "shot-risk",
            "version": "2.0",
            "status": "success",
        },
        "data": {
            "status": "ok",
            "service": "shot-risk-api",
        },
        "errors": None,
    }


# ── /description ──────────────────────────────────────────────────────────────
@app.get("/description")
def description():
    return {
        "meta": {
            "api": "shot-risk",
            "version": "2.0",
            "status": "success",
        },
        
        "errors": None,
    }


# ── /shot-risk ────────────────────────────────────────────────────────────────
@app.post("/shot-risk", response_model=ShotRiskResponse)
def shot_risk(payload: ShotRiskRequest):
    return process_shot_risk(payload.dict())