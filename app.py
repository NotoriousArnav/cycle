from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles
from models import Session as DBSession, Cycle
from schemas import CycleCreate, CycleResponse
from data_viz import generate_cycle_length_plot, generate_distribution_plot
from datetime import timedelta
from typing import List

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Mount static files for Alpine.js
app.mount("/static", StaticFiles(directory="static"), name="static")

# Dependency to get a DB session
def get_db():
    db = DBSession()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=templates.TemplateResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    """Renders the frontend using Jinja2 and Alpine.js."""
    cycles = db.query(Cycle).order_by(Cycle.start_date).all()
    return templates.TemplateResponse("index.html", {"request": request, "cycles": cycles})

@app.post("/add", response_model=CycleResponse)
async def add_cycle(cycle: CycleCreate, db: Session = Depends(get_db)):
    """Adds a new cycle entry."""
    db_cycle = Cycle(**cycle.dict())
    db.add(db_cycle)
    db.commit()
    db.refresh(db_cycle)
    return db_cycle

@app.delete("/cycle")
async def delete_cycle(date: str, name: str, db: Session = Depends(get_db)):
    """Deletes a cycle entry."""
    db.query(Cycle).filter_by(start_date=date, name=name).delete()
    db.commit()
    return {"message": "Cycle deleted successfully."}

@app.get("/history", response_model=List[CycleResponse])
async def get_history(db: Session = Depends(get_db)):
    """Fetches the recorded cycle history."""
    return db.query(Cycle).order_by(Cycle.start_date).all()

@app.get("/predict/{name}")
async def predict_next_cycle(name: str,db: Session = Depends(get_db)):
    """Predicts the next cycle based on past data."""
    cycles = db.query(Cycle).filter_by(name=name).order_by(Cycle.start_date).all()
    if len(cycles) < 2:
        return {"message": "Not enough data to predict the next cycle."}
    
    total_days = sum(
        (cycles[i + 1].start_date - cycles[i].start_date).days
        for i in range(len(cycles) - 1)
    )
    avg_cycle_length = total_days / (len(cycles) - 1)
    next_cycle_start = cycles[-1].start_date + timedelta(days=avg_cycle_length)

    return {"average_cycle_length": avg_cycle_length, "next_cycle_start": next_cycle_start}

@app.get("/visualization/cycle_length")
def get_cycle_length_plot():
    """API endpoint to fetch cycle length visualization"""
    ...

@app.get("/visualization/distribution")
def get_distribution_plot():
    """API endpoint to fetch cycle distribution visualization"""
    ...


