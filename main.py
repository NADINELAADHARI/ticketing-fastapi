from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from uuid import uuid4

app = FastAPI()

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
    tickets.append(ticket)
    return ticket