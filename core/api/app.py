from fastapi import FastAPI
from .routes import router

app = FastAPI(title="Neural Shadow API", version="0.1")

app.include_router(router)

@app.get("/")
def root():
    return {"message": "Neural Shadow Gateway Online"}
