from fastapi import FastAPI
from app.routers import ingredients, nutrition, nutrients
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(ingredients.router, prefix="/ingredients")
app.include_router(nutrition.router, prefix="/nutrition")
app.include_router(nutrients.router, prefix="/nutrients")

@app.get("/")
def root():
    return {"message": "Nutrition API running"}
