import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

load_dotenv()

import app.models  # noqa: ensure all models registered  # type: ignore[unused-import]
from app.seed import seed as run_seed
from app.database import engine, Base


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    run_seed()
    yield


app = FastAPI(title="CS7053 Study App", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost", "https://cs7053.citycontrol.me"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


from app.routers import auth as auth_router, paths as paths_router, topics as topics_router, mock as mock_router, graph as graph_router
app.include_router(auth_router.router)
app.include_router(paths_router.router)
app.include_router(topics_router.router)
app.include_router(mock_router.router)
app.include_router(graph_router.router)

_MATERIALS_DIR = os.path.normpath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../..", "materials")
)
if os.path.isdir(_MATERIALS_DIR):
    app.mount("/materials", StaticFiles(directory=_MATERIALS_DIR), name="materials")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/cheatsheet")
def cheatsheet():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "cheatsheet.md")
    with open(path, "r") as f:
        return {"content": f.read()}
