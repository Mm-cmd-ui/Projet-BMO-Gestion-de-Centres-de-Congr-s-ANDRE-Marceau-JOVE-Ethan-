import uvicorn
import os, json
import time as time_module
import logging
from fastapi import Depends, FastAPI, HTTPException, Request, status, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from pydantic_classes import *
from sql_alchemy import *

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

############################################
#
#   Initialize the database
#
############################################

def init_db():
    SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/Class_Diagram.db")
    # Ensure local SQLite directory exists (safe no-op for other DBs)
    os.makedirs("data", exist_ok=True)
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,
        echo=False
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    return SessionLocal

app = FastAPI(
    title="Class_Diagram API",
    description="Auto-generated REST API with full CRUD operations, relationship management, and advanced features",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=[
        {"name": "System", "description": "System health and statistics"},
        {"name": "Evenement_Salle", "description": "Operations for Evenement_Salle entities"},
        {"name": "Evenement_Salle Relationships", "description": "Manage Evenement_Salle relationships"},
        {"name": "Evenement_Salle Methods", "description": "Execute Evenement_Salle methods"},
        {"name": "reservation", "description": "Operations for reservation entities"},
        {"name": "reservation Relationships", "description": "Manage reservation relationships"},
        {"name": "reservation Methods", "description": "Execute reservation methods"},
        {"name": "gestionnaire", "description": "Operations for gestionnaire entities"},
        {"name": "gestionnaire Relationships", "description": "Manage gestionnaire relationships"},
        {"name": "gestionnaire Methods", "description": "Execute gestionnaire methods"},
    ]
)

# Enable CORS for all origins (for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or restrict to ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

############################################
#
#   Middleware
#
############################################

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all incoming requests and responses."""
    logger.info(f"Incoming request: {request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response

# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Add processing time header to all responses."""
    start_time = time_module.time()
    response = await call_next(request)
    process_time = time_module.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

############################################
#
#   Exception Handlers
#
############################################

# Global exception handlers
@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    """Handle ValueError exceptions."""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": "Bad Request",
            "message": str(exc),
            "detail": "Invalid input data provided"
        }
    )


@app.exception_handler(IntegrityError)
async def integrity_error_handler(request: Request, exc: IntegrityError):
    """Handle database integrity errors."""
    logger.error(f"Database integrity error: {exc}")

    # Extract more detailed error information
    error_detail = str(exc.orig) if hasattr(exc, 'orig') else str(exc)

    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "error": "Conflict",
            "message": "Data conflict occurred",
            "detail": error_detail
        }
    )


@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_error_handler(request: Request, exc: SQLAlchemyError):
    """Handle general SQLAlchemy errors."""
    logger.error(f"Database error: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal Server Error",
            "message": "Database operation failed",
            "detail": "An internal database error occurred"
        }
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions with consistent format."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail if isinstance(exc.detail, str) else "HTTP Error",
            "message": exc.detail,
            "detail": f"HTTP {exc.status_code} error occurred"
        }
    )

# Initialize database session
SessionLocal = init_db()
# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        logger.error("Database session rollback due to exception")
        raise
    finally:
        db.close()

############################################
#
#   Global API endpoints
#
############################################

@app.get("/", tags=["System"])
def root():
    """Root endpoint - API information"""
    return {
        "name": "Class_Diagram API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health", tags=["System"])
def health_check():
    """Health check endpoint for monitoring"""
    from datetime import datetime
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "database": "connected"
    }


@app.get("/statistics", tags=["System"])
def get_statistics(database: Session = Depends(get_db)):
    """Get database statistics for all entities"""
    stats = {}
    stats["evenement_salle_count"] = database.query(Evenement_Salle).count()
    stats["reservation_count"] = database.query(reservation).count()
    stats["gestionnaire_count"] = database.query(gestionnaire).count()
    stats["total_entities"] = sum(stats.values())
    return stats


############################################
#
#   BESSER Action Language standard lib
#
############################################


async def BAL_size(sequence:list) -> int:
    return len(sequence)

async def BAL_is_empty(sequence:list) -> bool:
    return len(sequence) == 0

async def BAL_add(sequence:list, elem) -> None:
    sequence.append(elem)

async def BAL_remove(sequence:list, elem) -> None:
    sequence.remove(elem)

async def BAL_contains(sequence:list, elem) -> bool:
    return elem in sequence

async def BAL_filter(sequence:list, predicate) -> list:
    return [elem for elem in sequence if predicate(elem)]

async def BAL_forall(sequence:list, predicate) -> bool:
    for elem in sequence:
        if not predicate(elem):
            return False
    return True

async def BAL_exists(sequence:list, predicate) -> bool:
    for elem in sequence:
        if predicate(elem):
            return True
    return False

async def BAL_one(sequence:list, predicate) -> bool:
    found = False
    for elem in sequence:
        if predicate(elem):
            if found:
                return False
            found = True
    return found

async def BAL_is_unique(sequence:list, mapping) -> bool:
    mapped = [mapping(elem) for elem in sequence]
    return len(set(mapped)) == len(mapped)

async def BAL_map(sequence:list, mapping) -> list:
    return [mapping(elem) for elem in sequence]

async def BAL_reduce(sequence:list, reduce_fn, aggregator) -> any:
    for elem in sequence:
        aggregator = reduce_fn(aggregator, elem)
    return aggregator


############################################
#
#   Evenement_Salle functions
#
############################################

@app.get("/evenement_salle/", response_model=None, tags=["Evenement_Salle"])
def get_all_evenement_salle(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(Evenement_Salle)
        query = query.options(joinedload(Evenement_Salle.reservation_1))
        evenement_salle_list = query.all()

        # Serialize with relationships included
        result = []
        for evenement_salle_item in evenement_salle_list:
            item_dict = evenement_salle_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)
            if evenement_salle_item.reservation_1:
                related_obj = evenement_salle_item.reservation_1
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['reservation_1'] = related_dict
            else:
                item_dict['reservation_1'] = None


            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(Evenement_Salle).all()


@app.get("/evenement_salle/count/", response_model=None, tags=["Evenement_Salle"])
def get_count_evenement_salle(database: Session = Depends(get_db)) -> dict:
    """Get the total count of Evenement_Salle entities"""
    count = database.query(Evenement_Salle).count()
    return {"count": count}


@app.get("/evenement_salle/paginated/", response_model=None, tags=["Evenement_Salle"])
def get_paginated_evenement_salle(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of Evenement_Salle entities"""
    total = database.query(Evenement_Salle).count()
    evenement_salle_list = database.query(Evenement_Salle).offset(skip).limit(limit).all()
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": evenement_salle_list
    }


@app.get("/evenement_salle/search/", response_model=None, tags=["Evenement_Salle"])
def search_evenement_salle(
    database: Session = Depends(get_db)
) -> list:
    """Search Evenement_Salle entities by attributes"""
    query = database.query(Evenement_Salle)


    results = query.all()
    return results


@app.get("/evenement_salle/{evenement_salle_id}/", response_model=None, tags=["Evenement_Salle"])
async def get_evenement_salle(evenement_salle_id: int, database: Session = Depends(get_db)) -> Evenement_Salle:
    db_evenement_salle = database.query(Evenement_Salle).filter(Evenement_Salle.id == evenement_salle_id).first()
    if db_evenement_salle is None:
        raise HTTPException(status_code=404, detail="Evenement_Salle not found")

    response_data = {
        "evenement_salle": db_evenement_salle,
}
    return response_data



@app.post("/evenement_salle/", response_model=None, tags=["Evenement_Salle"])
async def create_evenement_salle(evenement_salle_data: Evenement_SalleCreate, database: Session = Depends(get_db)) -> Evenement_Salle:

    if evenement_salle_data.reservation_1 :
        db_reservation_1 = database.query(reservation).filter(reservation.id == evenement_salle_data.reservation_1).first()
        if not db_reservation_1:
            raise HTTPException(status_code=400, detail="reservation not found")

    db_evenement_salle = Evenement_Salle(
        typeElement=evenement_salle_data.typeElement,        capaciteMax=evenement_salle_data.capaciteMax,        nom=evenement_salle_data.nom,        reservation_1_id=evenement_salle_data.reservation_1        )

    database.add(db_evenement_salle)
    database.commit()
    database.refresh(db_evenement_salle)




    return db_evenement_salle


@app.post("/evenement_salle/bulk/", response_model=None, tags=["Evenement_Salle"])
async def bulk_create_evenement_salle(items: list[Evenement_SalleCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple Evenement_Salle entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item

            db_evenement_salle = Evenement_Salle(
                typeElement=item_data.typeElement,                capaciteMax=item_data.capaciteMax,                nom=item_data.nom,                reservation_1_id=item_data.reservation_1            )
            database.add(db_evenement_salle)
            database.flush()  # Get ID without committing
            created_items.append(db_evenement_salle.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} Evenement_Salle entities"
    }


@app.delete("/evenement_salle/bulk/", response_model=None, tags=["Evenement_Salle"])
async def bulk_delete_evenement_salle(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple Evenement_Salle entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_evenement_salle = database.query(Evenement_Salle).filter(Evenement_Salle.id == item_id).first()
        if db_evenement_salle:
            database.delete(db_evenement_salle)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} Evenement_Salle entities"
    }

@app.put("/evenement_salle/{evenement_salle_id}/", response_model=None, tags=["Evenement_Salle"])
async def update_evenement_salle(evenement_salle_id: int, evenement_salle_data: Evenement_SalleCreate, database: Session = Depends(get_db)) -> Evenement_Salle:
    db_evenement_salle = database.query(Evenement_Salle).filter(Evenement_Salle.id == evenement_salle_id).first()
    if db_evenement_salle is None:
        raise HTTPException(status_code=404, detail="Evenement_Salle not found")

    setattr(db_evenement_salle, 'typeElement', evenement_salle_data.typeElement)
    setattr(db_evenement_salle, 'capaciteMax', evenement_salle_data.capaciteMax)
    setattr(db_evenement_salle, 'nom', evenement_salle_data.nom)
    if evenement_salle_data.reservation_1 is not None:
        db_reservation_1 = database.query(reservation).filter(reservation.id == evenement_salle_data.reservation_1).first()
        if not db_reservation_1:
            raise HTTPException(status_code=400, detail="reservation not found")
        setattr(db_evenement_salle, 'reservation_1_id', evenement_salle_data.reservation_1)
    else:
        setattr(db_evenement_salle, 'reservation_1_id', None)
    database.commit()
    database.refresh(db_evenement_salle)

    return db_evenement_salle


@app.delete("/evenement_salle/{evenement_salle_id}/", response_model=None, tags=["Evenement_Salle"])
async def delete_evenement_salle(evenement_salle_id: int, database: Session = Depends(get_db)):
    db_evenement_salle = database.query(Evenement_Salle).filter(Evenement_Salle.id == evenement_salle_id).first()
    if db_evenement_salle is None:
        raise HTTPException(status_code=404, detail="Evenement_Salle not found")
    database.delete(db_evenement_salle)
    database.commit()
    return db_evenement_salle



############################################
#   Evenement_Salle Method Endpoints
############################################




@app.post("/evenement_salle/{evenement_salle_id}/methods/verifierCapacite/", response_model=None, tags=["Evenement_Salle Methods"])
async def execute_evenement_salle_verifierCapacite(
    evenement_salle_id: int,
    params: dict = Body(default=None, embed=True),
    database: Session = Depends(get_db)
):
    """
    Execute the verifierCapacite method on a Evenement_Salle instance.

    Parameters:
    - nb_a_tester: Any    """
    # Retrieve the entity from the database
    _evenement_salle_object = database.query(Evenement_Salle).filter(Evenement_Salle.id == evenement_salle_id).first()
    if _evenement_salle_object is None:
        raise HTTPException(status_code=404, detail="Evenement_Salle not found")

    # Prepare method parameters
    nb_a_tester = params.get('nb_a_tester')

    # Execute the method
    try:
        # Capture stdout to include print outputs in the response
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output

        async def wrapper(_evenement_salle_object):
            try:
                # On teste les 3 variantes de noms les plus courantes
                v1 = getattr(_evenement_salle_object, 'Capacite', None)
                v2 = getattr(_evenement_salle_object, 'capacite', None)
                v3 = getattr(_evenement_salle_object, 'capaciteMax', None)
                
                # On prend la première qui n'est pas vide
                limite = 0
                for v in [v1, v2, v3]:
                    if v is not None:
                        limite = int(v)
                        break
                
                saisie = int(nb_a_tester)
                
                if saisie <= limite:
                    return f"Disponible : {saisie} <= {limite}"
                else:
                    return f"Capacité dépassée : {saisie} > {limite}"
            except:
                return "Erreur de saisie"

        result = await wrapper(_evenement_salle_object)
        # Commit DB
        database.commit()
        database.refresh(_evenement_salle_object)

        # Restore stdout
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        return {
            "evenement_salle_id": evenement_salle_id,
            "method": "verifierCapacite",
            "status": "executed",
            "result": str(result) if result is not None else None,
            "output": output if output else None
        }
    except Exception as e:
        sys.stdout = sys.__stdout__
        raise HTTPException(status_code=500, detail=f"Method execution failed: {str(e)}")



############################################
#
#   reservation functions
#
############################################

@app.get("/reservation/", response_model=None, tags=["reservation"])
def get_all_reservation(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(reservation)
        query = query.options(joinedload(reservation.gestionnaire))
        reservation_list = query.all()

        # Serialize with relationships included
        result = []
        for reservation_item in reservation_list:
            item_dict = reservation_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)
            if reservation_item.gestionnaire:
                related_obj = reservation_item.gestionnaire
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['gestionnaire'] = related_dict
            else:
                item_dict['gestionnaire'] = None

            # Add many-to-many and one-to-many relationship objects (full details)
            evenement_salle_list = database.query(Evenement_Salle).filter(Evenement_Salle.reservation_1_id == reservation_item.id).all()
            item_dict['evenement_salle'] = []
            for evenement_salle_obj in evenement_salle_list:
                evenement_salle_dict = evenement_salle_obj.__dict__.copy()
                evenement_salle_dict.pop('_sa_instance_state', None)
                item_dict['evenement_salle'].append(evenement_salle_dict)

            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(reservation).all()


@app.get("/reservation/count/", response_model=None, tags=["reservation"])
def get_count_reservation(database: Session = Depends(get_db)) -> dict:
    """Get the total count of reservation entities"""
    count = database.query(reservation).count()
    return {"count": count}


@app.get("/reservation/paginated/", response_model=None, tags=["reservation"])
def get_paginated_reservation(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of reservation entities"""
    total = database.query(reservation).count()
    reservation_list = database.query(reservation).offset(skip).limit(limit).all()
    # By default, return flat entities (for charts/widgets)
    # Use detailed=true to get entities with relationships
    if not detailed:
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": reservation_list
        }

    result = []
    for reservation_item in reservation_list:
        evenement_salle_ids = database.query(Evenement_Salle.id).filter(Evenement_Salle.reservation_1_id == reservation_item.id).all()
        item_data = {
            "reservation": reservation_item,
            "evenement_salle_ids": [x[0] for x in evenement_salle_ids]        }
        result.append(item_data)
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": result
    }


@app.get("/reservation/search/", response_model=None, tags=["reservation"])
def search_reservation(
    database: Session = Depends(get_db)
) -> list:
    """Search reservation entities by attributes"""
    query = database.query(reservation)


    results = query.all()
    return results


@app.get("/reservation/{reservation_id}/", response_model=None, tags=["reservation"])
async def get_reservation(reservation_id: int, database: Session = Depends(get_db)) -> reservation:
    db_reservation = database.query(reservation).filter(reservation.id == reservation_id).first()
    if db_reservation is None:
        raise HTTPException(status_code=404, detail="reservation not found")

    evenement_salle_ids = database.query(Evenement_Salle.id).filter(Evenement_Salle.reservation_1_id == db_reservation.id).all()
    response_data = {
        "reservation": db_reservation,
        "evenement_salle_ids": [x[0] for x in evenement_salle_ids]}
    return response_data



@app.post("/reservation/", response_model=None, tags=["reservation"])
async def create_reservation(reservation_data: reservationCreate, database: Session = Depends(get_db)) -> reservation:

    if reservation_data.gestionnaire :
        db_gestionnaire = database.query(gestionnaire).filter(gestionnaire.id == reservation_data.gestionnaire).first()
        if not db_gestionnaire:
            raise HTTPException(status_code=400, detail="gestionnaire not found")

    db_reservation = reservation(
        description=reservation_data.description,        delaiConfirmation=reservation_data.delaiConfirmation,        nomEvenement=reservation_data.nomEvenement,        nbParticipantsPrevu=reservation_data.nbParticipantsPrevu,        dateFin=reservation_data.dateFin,        etatActuel=reservation_data.etatActuel,        dateDebut=reservation_data.dateDebut,        estConfirmee=reservation_data.estConfirmee,        coutTotal=reservation_data.coutTotal,        gestionnaire_id=reservation_data.gestionnaire        )

    database.add(db_reservation)
    database.commit()
    database.refresh(db_reservation)

    if reservation_data.evenement_salle:
        # Validate that all Evenement_Salle IDs exist
        for evenement_salle_id in reservation_data.evenement_salle:
            db_evenement_salle = database.query(Evenement_Salle).filter(Evenement_Salle.id == evenement_salle_id).first()
            if not db_evenement_salle:
                raise HTTPException(status_code=400, detail=f"Evenement_Salle with id {evenement_salle_id} not found")

        # Update the related entities with the new foreign key
        database.query(Evenement_Salle).filter(Evenement_Salle.id.in_(reservation_data.evenement_salle)).update(
            {Evenement_Salle.reservation_1_id: db_reservation.id}, synchronize_session=False
        )
        database.commit()



    evenement_salle_ids = database.query(Evenement_Salle.id).filter(Evenement_Salle.reservation_1_id == db_reservation.id).all()
    response_data = {
        "reservation": db_reservation,
        "evenement_salle_ids": [x[0] for x in evenement_salle_ids]    }
    return response_data


@app.post("/reservation/bulk/", response_model=None, tags=["reservation"])
async def bulk_create_reservation(items: list[reservationCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple reservation entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item

            db_reservation = reservation(
                description=item_data.description,                delaiConfirmation=item_data.delaiConfirmation,                nomEvenement=item_data.nomEvenement,                nbParticipantsPrevu=item_data.nbParticipantsPrevu,                dateFin=item_data.dateFin,                etatActuel=item_data.etatActuel,                dateDebut=item_data.dateDebut,                estConfirmee=item_data.estConfirmee,                coutTotal=item_data.coutTotal,                gestionnaire_id=item_data.gestionnaire            )
            database.add(db_reservation)
            database.flush()  # Get ID without committing
            created_items.append(db_reservation.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} reservation entities"
    }


@app.delete("/reservation/bulk/", response_model=None, tags=["reservation"])
async def bulk_delete_reservation(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple reservation entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_reservation = database.query(reservation).filter(reservation.id == item_id).first()
        if db_reservation:
            database.delete(db_reservation)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} reservation entities"
    }

@app.put("/reservation/{reservation_id}/", response_model=None, tags=["reservation"])
async def update_reservation(reservation_id: int, reservation_data: reservationCreate, database: Session = Depends(get_db)) -> reservation:
    db_reservation = database.query(reservation).filter(reservation.id == reservation_id).first()
    if db_reservation is None:
        raise HTTPException(status_code=404, detail="reservation not found")

    setattr(db_reservation, 'description', reservation_data.description)
    setattr(db_reservation, 'delaiConfirmation', reservation_data.delaiConfirmation)
    setattr(db_reservation, 'nomEvenement', reservation_data.nomEvenement)
    setattr(db_reservation, 'nbParticipantsPrevu', reservation_data.nbParticipantsPrevu)
    setattr(db_reservation, 'dateFin', reservation_data.dateFin)
    setattr(db_reservation, 'etatActuel', reservation_data.etatActuel)
    setattr(db_reservation, 'dateDebut', reservation_data.dateDebut)
    setattr(db_reservation, 'estConfirmee', reservation_data.estConfirmee)
    setattr(db_reservation, 'coutTotal', reservation_data.coutTotal)
    if reservation_data.gestionnaire is not None:
        db_gestionnaire = database.query(gestionnaire).filter(gestionnaire.id == reservation_data.gestionnaire).first()
        if not db_gestionnaire:
            raise HTTPException(status_code=400, detail="gestionnaire not found")
        setattr(db_reservation, 'gestionnaire_id', reservation_data.gestionnaire)
    else:
        setattr(db_reservation, 'gestionnaire_id', None)
    if reservation_data.evenement_salle is not None:
        # Clear all existing relationships (set foreign key to NULL)
        database.query(Evenement_Salle).filter(Evenement_Salle.reservation_1_id == db_reservation.id).update(
            {Evenement_Salle.reservation_1_id: None}, synchronize_session=False
        )

        # Set new relationships if list is not empty
        if reservation_data.evenement_salle:
            # Validate that all IDs exist
            for evenement_salle_id in reservation_data.evenement_salle:
                db_evenement_salle = database.query(Evenement_Salle).filter(Evenement_Salle.id == evenement_salle_id).first()
                if not db_evenement_salle:
                    raise HTTPException(status_code=400, detail=f"Evenement_Salle with id {evenement_salle_id} not found")

            # Update the related entities with the new foreign key
            database.query(Evenement_Salle).filter(Evenement_Salle.id.in_(reservation_data.evenement_salle)).update(
                {Evenement_Salle.reservation_1_id: db_reservation.id}, synchronize_session=False
            )
    database.commit()
    database.refresh(db_reservation)

    evenement_salle_ids = database.query(Evenement_Salle.id).filter(Evenement_Salle.reservation_1_id == db_reservation.id).all()
    response_data = {
        "reservation": db_reservation,
        "evenement_salle_ids": [x[0] for x in evenement_salle_ids]    }
    return response_data


@app.delete("/reservation/{reservation_id}/", response_model=None, tags=["reservation"])
async def delete_reservation(reservation_id: int, database: Session = Depends(get_db)):
    db_reservation = database.query(reservation).filter(reservation.id == reservation_id).first()
    if db_reservation is None:
        raise HTTPException(status_code=404, detail="reservation not found")
    database.delete(db_reservation)
    database.commit()
    return db_reservation



############################################
#   reservation Method Endpoints
############################################




@app.post("/reservation/{reservation_id}/methods/calculerCout/", response_model=None, tags=["reservation Methods"])
async def execute_reservation_calculerCout(
    reservation_id: int,
    params: dict = Body(default=None, embed=True),
    database: Session = Depends(get_db)
):
    """
    Execute the calculerCout method on a reservation instance.
    """
    # Retrieve the entity from the database
    _reservation_object = database.query(reservation).filter(reservation.id == reservation_id).first()
    if _reservation_object is None:
        raise HTTPException(status_code=404, detail="reservation not found")

    # Prepare method parameters

    # Execute the method
    try:
        # Capture stdout to include print outputs in the response
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output

        async def wrapper(_reservation_object):
            # On essaye de récupérer 'prix' ou 'prixTotal' avec une majuscule si besoin
            cout = getattr(_reservation_object, 'prix', getattr(_reservation_object, 'coutTotal', 0))
            print(f"DEBUG: Coût récupéré = {cout}")
            return cout

        result = await wrapper(_reservation_object)
        # Commit DB
        database.commit()
        database.refresh(_reservation_object)

        # Restore stdout
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        return {
            "reservation_id": reservation_id,
            "method": "calculerCout",
            "status": "executed",
            "result": str(result) if result is not None else None,
            "output": output if output else None
        }
    except Exception as e:
        sys.stdout = sys.__stdout__
        raise HTTPException(status_code=500, detail=f"Method execution failed: {str(e)}")



############################################
#
#   gestionnaire functions
#
############################################

@app.get("/gestionnaire/", response_model=None, tags=["gestionnaire"])
def get_all_gestionnaire(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(gestionnaire)
        gestionnaire_list = query.all()

        # Serialize with relationships included
        result = []
        for gestionnaire_item in gestionnaire_list:
            item_dict = gestionnaire_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)

            # Add many-to-many and one-to-many relationship objects (full details)
            reservation_list = database.query(reservation).filter(reservation.gestionnaire_id == gestionnaire_item.id).all()
            item_dict['reservation'] = []
            for reservation_obj in reservation_list:
                reservation_dict = reservation_obj.__dict__.copy()
                reservation_dict.pop('_sa_instance_state', None)
                item_dict['reservation'].append(reservation_dict)

            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(gestionnaire).all()


@app.get("/gestionnaire/count/", response_model=None, tags=["gestionnaire"])
def get_count_gestionnaire(database: Session = Depends(get_db)) -> dict:
    """Get the total count of gestionnaire entities"""
    count = database.query(gestionnaire).count()
    return {"count": count}


@app.get("/gestionnaire/paginated/", response_model=None, tags=["gestionnaire"])
def get_paginated_gestionnaire(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of gestionnaire entities"""
    total = database.query(gestionnaire).count()
    gestionnaire_list = database.query(gestionnaire).offset(skip).limit(limit).all()
    # By default, return flat entities (for charts/widgets)
    # Use detailed=true to get entities with relationships
    if not detailed:
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": gestionnaire_list
        }

    result = []
    for gestionnaire_item in gestionnaire_list:
        reservation_ids = database.query(reservation.id).filter(reservation.gestionnaire_id == gestionnaire_item.id).all()
        item_data = {
            "gestionnaire": gestionnaire_item,
            "reservation_ids": [x[0] for x in reservation_ids]        }
        result.append(item_data)
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": result
    }


@app.get("/gestionnaire/search/", response_model=None, tags=["gestionnaire"])
def search_gestionnaire(
    database: Session = Depends(get_db)
) -> list:
    """Search gestionnaire entities by attributes"""
    query = database.query(gestionnaire)


    results = query.all()
    return results


@app.get("/gestionnaire/{gestionnaire_id}/", response_model=None, tags=["gestionnaire"])
async def get_gestionnaire(gestionnaire_id: int, database: Session = Depends(get_db)) -> gestionnaire:
    db_gestionnaire = database.query(gestionnaire).filter(gestionnaire.id == gestionnaire_id).first()
    if db_gestionnaire is None:
        raise HTTPException(status_code=404, detail="gestionnaire not found")

    reservation_ids = database.query(reservation.id).filter(reservation.gestionnaire_id == db_gestionnaire.id).all()
    response_data = {
        "gestionnaire": db_gestionnaire,
        "reservation_ids": [x[0] for x in reservation_ids]}
    return response_data



@app.post("/gestionnaire/", response_model=None, tags=["gestionnaire"])
async def create_gestionnaire(gestionnaire_data: gestionnaireCreate, database: Session = Depends(get_db)) -> gestionnaire:


    db_gestionnaire = gestionnaire(
        identitfiant=gestionnaire_data.identitfiant,        nom=gestionnaire_data.nom        )

    database.add(db_gestionnaire)
    database.commit()
    database.refresh(db_gestionnaire)

    if gestionnaire_data.reservation:
        # Validate that all reservation IDs exist
        for reservation_id in gestionnaire_data.reservation:
            db_reservation = database.query(reservation).filter(reservation.id == reservation_id).first()
            if not db_reservation:
                raise HTTPException(status_code=400, detail=f"reservation with id {reservation_id} not found")

        # Update the related entities with the new foreign key
        database.query(reservation).filter(reservation.id.in_(gestionnaire_data.reservation)).update(
            {reservation.gestionnaire_id: db_gestionnaire.id}, synchronize_session=False
        )
        database.commit()



    reservation_ids = database.query(reservation.id).filter(reservation.gestionnaire_id == db_gestionnaire.id).all()
    response_data = {
        "gestionnaire": db_gestionnaire,
        "reservation_ids": [x[0] for x in reservation_ids]    }
    return response_data


@app.post("/gestionnaire/bulk/", response_model=None, tags=["gestionnaire"])
async def bulk_create_gestionnaire(items: list[gestionnaireCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple gestionnaire entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item

            db_gestionnaire = gestionnaire(
                identitfiant=item_data.identitfiant,                nom=item_data.nom            )
            database.add(db_gestionnaire)
            database.flush()  # Get ID without committing
            created_items.append(db_gestionnaire.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} gestionnaire entities"
    }


@app.delete("/gestionnaire/bulk/", response_model=None, tags=["gestionnaire"])
async def bulk_delete_gestionnaire(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple gestionnaire entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_gestionnaire = database.query(gestionnaire).filter(gestionnaire.id == item_id).first()
        if db_gestionnaire:
            database.delete(db_gestionnaire)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} gestionnaire entities"
    }

@app.put("/gestionnaire/{gestionnaire_id}/", response_model=None, tags=["gestionnaire"])
async def update_gestionnaire(gestionnaire_id: int, gestionnaire_data: gestionnaireCreate, database: Session = Depends(get_db)) -> gestionnaire:
    db_gestionnaire = database.query(gestionnaire).filter(gestionnaire.id == gestionnaire_id).first()
    if db_gestionnaire is None:
        raise HTTPException(status_code=404, detail="gestionnaire not found")

    setattr(db_gestionnaire, 'identitfiant', gestionnaire_data.identitfiant)
    setattr(db_gestionnaire, 'nom', gestionnaire_data.nom)
    if gestionnaire_data.reservation is not None:
        # Clear all existing relationships (set foreign key to NULL)
        database.query(reservation).filter(reservation.gestionnaire_id == db_gestionnaire.id).update(
            {reservation.gestionnaire_id: None}, synchronize_session=False
        )

        # Set new relationships if list is not empty
        if gestionnaire_data.reservation:
            # Validate that all IDs exist
            for reservation_id in gestionnaire_data.reservation:
                db_reservation = database.query(reservation).filter(reservation.id == reservation_id).first()
                if not db_reservation:
                    raise HTTPException(status_code=400, detail=f"reservation with id {reservation_id} not found")

            # Update the related entities with the new foreign key
            database.query(reservation).filter(reservation.id.in_(gestionnaire_data.reservation)).update(
                {reservation.gestionnaire_id: db_gestionnaire.id}, synchronize_session=False
            )
    database.commit()
    database.refresh(db_gestionnaire)

    reservation_ids = database.query(reservation.id).filter(reservation.gestionnaire_id == db_gestionnaire.id).all()
    response_data = {
        "gestionnaire": db_gestionnaire,
        "reservation_ids": [x[0] for x in reservation_ids]    }
    return response_data


@app.delete("/gestionnaire/{gestionnaire_id}/", response_model=None, tags=["gestionnaire"])
async def delete_gestionnaire(gestionnaire_id: int, database: Session = Depends(get_db)):
    db_gestionnaire = database.query(gestionnaire).filter(gestionnaire.id == gestionnaire_id).first()
    if db_gestionnaire is None:
        raise HTTPException(status_code=404, detail="gestionnaire not found")
    database.delete(db_gestionnaire)
    database.commit()
    return db_gestionnaire



############################################
#   gestionnaire Method Endpoints
############################################




@app.post("/gestionnaire/{gestionnaire_id}/methods/consulterStats/", response_model=None, tags=["gestionnaire Methods"])
async def execute_gestionnaire_consulterStats(
    gestionnaire_id: int,
    params: dict = Body(default=None, embed=True),
    database: Session = Depends(get_db)
):
    """
    Execute the consulterStats method on a gestionnaire instance.

    Parameters:
    - periode_nom: Any    """
    # Retrieve the entity from the database
    _gestionnaire_object = database.query(gestionnaire).filter(gestionnaire.id == gestionnaire_id).first()
    if _gestionnaire_object is None:
        raise HTTPException(status_code=404, detail="gestionnaire not found")

    # Prepare method parameters
    periode_nom = params.get('periode_nom')

    # Execute the method
    try:
        # Capture stdout to include print outputs in the response
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output

        async def wrapper(_gestionnaire_object):
            # On tente de récupérer la liste des réservations par différents noms
            # 1. 'reservations' (minuscule)
            # 2. 'Reservations' (majuscule)
            # 3. 'ses_reservations' (nom de rôle courant)
            resas = getattr(_gestionnaire_object, 'reservations', getattr(_gestionnaire_object, 'Reservations', []))
            
            if not resas:
                # Message d'aide spécifique pour ne pas paniquer en démo
                return [f"Période: {periode_nom}", "Info: Reliez les réservations au Gestionnaire dans l'IHM."]
            
            # Affichage propre des résultats
            stats = []
            for r in resas:
                nom = getattr(r, 'nom', 'Resa')
                prix = getattr(r, 'prix', getattr(r, 'Prix', 0))
                stats.append(f"{nom} | {prix}€")
                
            return stats

        result = await wrapper(_gestionnaire_object)
        # Commit DB
        database.commit()
        database.refresh(_gestionnaire_object)

        # Restore stdout
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        return {
            "gestionnaire_id": gestionnaire_id,
            "method": "consulterStats",
            "status": "executed",
            "result": str(result) if result is not None else None,
            "output": output if output else None
        }
    except Exception as e:
        sys.stdout = sys.__stdout__
        raise HTTPException(status_code=500, detail=f"Method execution failed: {str(e)}")





############################################
# Maintaining the server
############################################
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)



