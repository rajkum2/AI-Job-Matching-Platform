from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.logging import configure_logging
from app.db.mongo import ensure_indexes
from app.db.qdrant import ensure_collection
from app.routers import admin, audit, auth, candidates, config, jobs, mappings, matches

app = FastAPI(title="JobMatch MVP API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def on_startup() -> None:
    configure_logging()
    await ensure_indexes()
    ensure_collection()


@app.get("/health")
async def health():
    return {"status": "ok"}


app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(candidates.router)
app.include_router(jobs.router)
app.include_router(matches.router)
app.include_router(mappings.router)
app.include_router(config.router)
app.include_router(audit.router)
