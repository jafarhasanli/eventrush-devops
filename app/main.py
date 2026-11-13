
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.database import check_database, get_engine

app = FastAPI(title="EventRush API", version="0.2.1")


class Event(BaseModel):
    id: int
    title: str
    capacity: int = Field(ge=0)


class ReservationRequest(BaseModel):
    event_id: int = Field(gt=0)
    customer_email: str = Field(min_length=3, max_length=255)





@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/events", response_model=list[Event])

@app.get("/events", response_model=list[Event])
def list_events():
    try:
        with get_engine().connect() as connection:
            rows = connection.execute(
                text("""
                    SELECT id, title, capacity
                    FROM events
                    ORDER BY id
                """)
            ).mappings().all()

        return [Event(**dict(row)) for row in rows]

    except SQLAlchemyError:
        raise HTTPException(
            status_code=503,
            detail="Database unavailable"
        )



@app.get("/db-health")
def database_health():
    try:
        if check_database():
            return {"database": "connected"}
    except (SQLAlchemyError, RuntimeError):
        pass

    raise HTTPException(
        status_code=503,
        detail="Database unavailable"
    )


@app.get("/events/{event_id}/availability")
def event_availability(event_id: int):
    try:
        with get_engine().connect() as connection:
            row = connection.execute(
                text("""
                    SELECT id, title, capacity, available_tickets
                    FROM events
                    WHERE id = :event_id
                """),
                {"event_id": event_id}
            ).mappings().first()

        if row is None:
            raise HTTPException(404, "Event not found")

        return dict(row)

    except SQLAlchemyError:
        raise HTTPException(503, "Database unavailable")


@app.post("/reservations", status_code=201)
def create_reservation(request: ReservationRequest):
    try:
        with get_engine().begin() as connection:

            # Decrease inventory only when tickets remain.
            updated = connection.execute(
                text("""
                    UPDATE events
                    SET available_tickets = available_tickets - 1
                    WHERE id = :event_id
                      AND available_tickets > 0
                    RETURNING id
                """),
                {"event_id": request.event_id}
            ).first()

            if updated is None:
                raise HTTPException(
                    409,
                    "Event unavailable or sold out"
                )

            # Create a reservation for this customer.
            reservation = connection.execute(
                text("""
                    INSERT INTO reservations
                        (event_id, customer_email)
                    VALUES (:event_id, :customer_email)
                    ON CONFLICT (event_id, customer_email)
                    DO NOTHING
                    RETURNING id
                """),
                {
                    "event_id": request.event_id,
                    "customer_email": request.customer_email
                }
            ).first()

            if reservation is None:
                raise HTTPException(
                    409,
                    "Customer already has a reservation"
                )

            reservation_id = reservation[0]

        return {
            "reservation_id": reservation_id,
            "event_id": request.event_id,
            "status": "confirmed"
        }

    except SQLAlchemyError:
        raise HTTPException(
            503,
            "Database unavailable"
        )
