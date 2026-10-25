"""
FastAPI app — Water Bucket Puzzle.

Endpoints:
  GET  /           HTML UI
  POST /api/move   Apply fill / empty / pour (stateless: client sends current state)
  POST /api/reset  Fresh game

Run: uvicorn main:app --reload --port 3007
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Literal

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

_DEMO_ROOT = Path(__file__).resolve().parent.parent
if str(_DEMO_ROOT) not in sys.path:
    sys.path.insert(0, str(_DEMO_ROOT))

from water_bucket_core import (  # noqa: E402
    BUCKET_CAPACITY,
    BUCKET_IDS,
    GOAL,
    apply_move,
    initial_state,
    state_for_client,
)

app = FastAPI(title="Water Bucket Puzzle")
templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))
app.mount("/static", StaticFiles(directory=str(Path(__file__).parent / "static")), name="static")


class WaterState(BaseModel):
    water: dict[str, int] = Field(..., description="Liters in each bucket")
    steps: int = Field(0, ge=0)


class MoveRequest(BaseModel):
    state: WaterState
    action: Literal["fill", "empty", "pour"]
    source: Literal["8", "5", "3"]
    dest: Literal["8", "5", "3"] | None = None


@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "goal": GOAL,
            "bucket_ids": BUCKET_IDS,
            "capacities": BUCKET_CAPACITY,
        },
    )


@app.post("/api/reset")
async def api_reset() -> JSONResponse:
    return JSONResponse(state_for_client(initial_state()))


@app.post("/api/move")
async def api_move(body: MoveRequest) -> JSONResponse:
    try:
        new_state = apply_move(
            body.state.model_dump(),
            body.action,
            body.source,
            body.dest,
        )
        return JSONResponse(state_for_client(new_state))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
