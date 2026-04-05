from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.api.literature import router as literature_router
from app.config import DATA_DIR
from app.db import init_db
from app.services.literature_service import list_literatures

app = FastAPI(title="Literature Manager MVP")

templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.mount("/data", StaticFiles(directory=str(DATA_DIR)), name="data")


@app.on_event("startup")
def on_startup() -> None:
    init_db()


@app.get("/", response_class=HTMLResponse)
def home(request: Request, query: str | None = None):
    items = list_literatures(query=query)
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "items": items,
            "query": query or "",
        },
    )


app.include_router(literature_router)
