from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import models
import schemas
import database

# Create tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Flight Booking API", version="1.0.0")

# Users Endpoints
@app.post("/users", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/{user_id}", response_model=schemas.User)
def get_user(user_id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Flights Endpoints
@app.get("/flights", response_model=List[schemas.Flight])
def search_flights(
    departure_city: str, 
    arrival_city: str, 
    departure_date: str, 
    return_date: str = None, 
    travel_class: str = None, 
    db: Session = Depends(database.get_db)
):
    query = db.query(models.Flight).filter(
        models.Flight.departure_city == departure_city,
        models.Flight.arrival_city == arrival_city,
        models.Flight.departure_date == departure_date
    )
    
    if return_date:
        query = query.filter(models.Flight.return_date == return_date)
    
    if travel_class:
        query = query.filter(models.Flight.travel_class == travel_class)
    
    flights = query.all()
    return flights

@app.get("/flights/{flight_id}", response_model=schemas.Flight)
def get_flight(flight_id: int, db: Session = Depends(database.get_db)):
    flight = db.query(models.Flight).filter(models.Flight.flight_id == flight_id).first()
    if not flight:
        raise HTTPException(status_code=404, detail="Flight not found")
    return flight

# Bookings Endpoints
@app.post("/bookings", response_model=schemas.Booking, status_code=status.HTTP_201_CREATED)
def create_booking(booking: schemas.BookingCreate, db: Session = Depends(database.get_db)):
    db_booking = models.Booking(**booking.dict())
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking

@app.get("/bookings/{booking_id}", response_model=schemas.Booking)
def get_booking(booking_id: int, db: Session = Depends(database.get_db)):
    booking = db.query(models.Booking).filter(models.Booking.booking_id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking

# Fares Endpoints
@app.get("/fares", response_model=List[schemas.Fare])
def list_fares(db: Session = Depends(database.get_db)):
    fares = db.query(models.Fare).all()
    return fares

@app.get("/fares/{fare_id}", response_model=schemas.Fare)
def get_fare(fare_id: int, db: Session = Depends(database.get_db)):
    fare = db.query(models.Fare).filter(models.Fare.fare_id == fare_id).first()
    if not fare:
        raise HTTPException(status_code=404, detail="Fare not found")
    return fare