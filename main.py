from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List
from uuid import uuid4
import logging
import os

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Pour le développement, à restreindre en production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Monte le dossier static pour servir le frontend
app.mount("/", StaticFiles(directory="static", html=True), name="static")

# Stockage des tickets en mémoire
tickets = []

class Ticket(BaseModel):
    id: str = None
    service: str
    is_processed: bool = False

@app.post("/api/tickets")
async def create_ticket(ticket: Ticket):
    try:
        ticket.id = str(uuid4())
        ticket_data = ticket.dict()
        tickets.append(ticket_data)
        return ticket_data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/tickets", response_model=List[Ticket])
async def get_all_tickets():
    return tickets

@app.get("/api/tickets/count")
async def get_tickets_count():
    return {"count": len(tickets)}

@app.get("/healthcheck")
async def healthcheck():
    return {"status": "ok", "version": "1.0.0"}