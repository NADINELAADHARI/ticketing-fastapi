from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List
from uuid import uuid4

app = FastAPI()

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Autorise toutes les origines (à restreindre en production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Monte le dossier static pour servir le frontend
app.mount("/", StaticFiles(directory="static", html=True), name="static")

# Stockage des tickets en mémoire (sera réinitialisé après chaque redémarrage)
tickets = []

class Ticket(BaseModel):
    id: str = None
    service: str
    is_processed: bool = False

@app.get("/api/tickets", response_model=List[Ticket])
def get_all_tickets():
    return tickets

@app.post("/api/tickets", response_model=Ticket)
def create_ticket(ticket: Ticket):
    ticket.id = str(uuid4())
    tickets.append(ticket.dict())
    return ticket

@app.get("/api/tickets/count")
def get_tickets_count():
    return {"count": len(tickets)}