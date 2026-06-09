from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles  # 1. Added this import
from pydantic import BaseModel
import uvicorn

app = FastAPI()

# 2. Added this line to serve files from a "static" folder
app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class PRRequest(BaseModel):
    url: str

@app.post("/review")
async def review(request: PRRequest):
    try:
        from main import review_pr
        report = review_pr(request.url)
        return {"success": True, "report": report}
    except Exception as e:
        return {"success": False, "error": str(e)}

HTML = open("templates/index.html").read()

@app.get("/", response_class=HTMLResponse)
async def home():
    return HTML

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)