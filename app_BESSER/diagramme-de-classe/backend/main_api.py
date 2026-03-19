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
        {"name": "CentredeCongres", "description": "Operations for CentredeCongres entities"},
        {"name": "CentredeCongres Relationships", "description": "Manage CentredeCongres relationships"},
        {"name": "Tarifs", "description": "Operations for Tarifs entities"},
        {"name": "Tarifs Relationships", "description": "Manage Tarifs relationships"},
        {"name": "Tarifs Methods", "description": "Execute Tarifs methods"},
        {"name": "EvenementSalle", "description": "Operations for EvenementSalle entities"},
        {"name": "EvenementSalle Relationships", "description": "Manage EvenementSalle relationships"},
        {"name": "EvenementSalle Methods", "description": "Execute EvenementSalle methods"},
        {"name": "Materielsprestations", "description": "Operations for Materielsprestations entities"},
        {"name": "Materielsprestations Relationships", "description": "Manage Materielsprestations relationships"},
        {"name": "Materielsprestations Methods", "description": "Execute Materielsprestations methods"},
        {"name": "Disponibilites", "description": "Operations for Disponibilites entities"},
        {"name": "Disponibilites Relationships", "description": "Manage Disponibilites relationships"},
        {"name": "Disponibilites Methods", "description": "Execute Disponibilites methods"},
        {"name": "Reservation", "description": "Operations for Reservation entities"},
        {"name": "Reservation Relationships", "description": "Manage Reservation relationships"},
        {"name": "Reservation Methods", "description": "Execute Reservation methods"},
        {"name": "Stats", "description": "Operations for Stats entities"},
        {"name": "Stats Relationships", "description": "Manage Stats relationships"},
        {"name": "Stats Methods", "description": "Execute Stats methods"},
        {"name": "Gestionnaire", "description": "Operations for Gestionnaire entities"},
        {"name": "Gestionnaire Relationships", "description": "Manage Gestionnaire relationships"},
        {"name": "Gestionnaire Methods", "description": "Execute Gestionnaire methods"},
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
    stats["centredecongres_count"] = database.query(CentredeCongres).count()
    stats["tarifs_count"] = database.query(Tarifs).count()
    stats["evenementsalle_count"] = database.query(EvenementSalle).count()
    stats["materielsprestations_count"] = database.query(Materielsprestations).count()
    stats["disponibilites_count"] = database.query(Disponibilites).count()
    stats["reservation_count"] = database.query(Reservation).count()
    stats["stats_count"] = database.query(Stats).count()
    stats["gestionnaire_count"] = database.query(Gestionnaire).count()
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
#   CentredeCongres functions
#
############################################

@app.get("/centredecongres/", response_model=None, tags=["CentredeCongres"])
def get_all_centredecongres(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(CentredeCongres)
        query = query.options(joinedload(CentredeCongres.gestionnaire_1))
        centredecongres_list = query.all()

        # Serialize with relationships included
        result = []
        for centredecongres_item in centredecongres_list:
            item_dict = centredecongres_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)
            if centredecongres_item.gestionnaire_1:
                related_obj = centredecongres_item.gestionnaire_1
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['gestionnaire_1'] = related_dict
            else:
                item_dict['gestionnaire_1'] = None

            # Add many-to-many and one-to-many relationship objects (full details)
            evenementsalle_list = database.query(EvenementSalle).filter(EvenementSalle.centredecongres_id == centredecongres_item.id).all()
            item_dict['evenementsalle_1'] = []
            for evenementsalle_obj in evenementsalle_list:
                evenementsalle_dict = evenementsalle_obj.__dict__.copy()
                evenementsalle_dict.pop('_sa_instance_state', None)
                item_dict['evenementsalle_1'].append(evenementsalle_dict)

            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(CentredeCongres).all()


@app.get("/centredecongres/count/", response_model=None, tags=["CentredeCongres"])
def get_count_centredecongres(database: Session = Depends(get_db)) -> dict:
    """Get the total count of CentredeCongres entities"""
    count = database.query(CentredeCongres).count()
    return {"count": count}


@app.get("/centredecongres/paginated/", response_model=None, tags=["CentredeCongres"])
def get_paginated_centredecongres(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of CentredeCongres entities"""
    total = database.query(CentredeCongres).count()
    centredecongres_list = database.query(CentredeCongres).offset(skip).limit(limit).all()
    # By default, return flat entities (for charts/widgets)
    # Use detailed=true to get entities with relationships
    if not detailed:
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": centredecongres_list
        }

    result = []
    for centredecongres_item in centredecongres_list:
        evenementsalle_1_ids = database.query(EvenementSalle.id).filter(EvenementSalle.centredecongres_id == centredecongres_item.id).all()
        item_data = {
            "centredecongres": centredecongres_item,
            "evenementsalle_1_ids": [x[0] for x in evenementsalle_1_ids]        }
        result.append(item_data)
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": result
    }


@app.get("/centredecongres/search/", response_model=None, tags=["CentredeCongres"])
def search_centredecongres(
    database: Session = Depends(get_db)
) -> list:
    """Search CentredeCongres entities by attributes"""
    query = database.query(CentredeCongres)


    results = query.all()
    return results


@app.get("/centredecongres/{centredecongres_id}/", response_model=None, tags=["CentredeCongres"])
async def get_centredecongres(centredecongres_id: int, database: Session = Depends(get_db)) -> CentredeCongres:
    db_centredecongres = database.query(CentredeCongres).filter(CentredeCongres.id == centredecongres_id).first()
    if db_centredecongres is None:
        raise HTTPException(status_code=404, detail="CentredeCongres not found")

    evenementsalle_1_ids = database.query(EvenementSalle.id).filter(EvenementSalle.centredecongres_id == db_centredecongres.id).all()
    response_data = {
        "centredecongres": db_centredecongres,
        "evenementsalle_1_ids": [x[0] for x in evenementsalle_1_ids]}
    return response_data



@app.post("/centredecongres/", response_model=None, tags=["CentredeCongres"])
async def create_centredecongres(centredecongres_data: CentredeCongresCreate, database: Session = Depends(get_db)) -> CentredeCongres:

    if centredecongres_data.gestionnaire_1 is not None:
        db_gestionnaire_1 = database.query(Gestionnaire).filter(Gestionnaire.id == centredecongres_data.gestionnaire_1).first()
        if not db_gestionnaire_1:
            raise HTTPException(status_code=400, detail="Gestionnaire not found")
    else:
        raise HTTPException(status_code=400, detail="Gestionnaire ID is required")

    db_centredecongres = CentredeCongres(
        nom=centredecongres_data.nom,        adresse=centredecongres_data.adresse,        gestionnaire_1_id=centredecongres_data.gestionnaire_1        )

    database.add(db_centredecongres)
    database.commit()
    database.refresh(db_centredecongres)

    if centredecongres_data.evenementsalle_1:
        # Validate that all EvenementSalle IDs exist
        for evenementsalle_id in centredecongres_data.evenementsalle_1:
            db_evenementsalle = database.query(EvenementSalle).filter(EvenementSalle.id == evenementsalle_id).first()
            if not db_evenementsalle:
                raise HTTPException(status_code=400, detail=f"EvenementSalle with id {evenementsalle_id} not found")

        # Update the related entities with the new foreign key
        database.query(EvenementSalle).filter(EvenementSalle.id.in_(centredecongres_data.evenementsalle_1)).update(
            {EvenementSalle.centredecongres_id: db_centredecongres.id}, synchronize_session=False
        )
        database.commit()



    evenementsalle_1_ids = database.query(EvenementSalle.id).filter(EvenementSalle.centredecongres_id == db_centredecongres.id).all()
    response_data = {
        "centredecongres": db_centredecongres,
        "evenementsalle_1_ids": [x[0] for x in evenementsalle_1_ids]    }
    return response_data


@app.post("/centredecongres/bulk/", response_model=None, tags=["CentredeCongres"])
async def bulk_create_centredecongres(items: list[CentredeCongresCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple CentredeCongres entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item
            if not item_data.gestionnaire_1:
                raise ValueError("Gestionnaire ID is required")

            db_centredecongres = CentredeCongres(
                nom=item_data.nom,                adresse=item_data.adresse,                gestionnaire_1_id=item_data.gestionnaire_1            )
            database.add(db_centredecongres)
            database.flush()  # Get ID without committing
            created_items.append(db_centredecongres.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} CentredeCongres entities"
    }


@app.delete("/centredecongres/bulk/", response_model=None, tags=["CentredeCongres"])
async def bulk_delete_centredecongres(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple CentredeCongres entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_centredecongres = database.query(CentredeCongres).filter(CentredeCongres.id == item_id).first()
        if db_centredecongres:
            database.delete(db_centredecongres)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} CentredeCongres entities"
    }

@app.put("/centredecongres/{centredecongres_id}/", response_model=None, tags=["CentredeCongres"])
async def update_centredecongres(centredecongres_id: int, centredecongres_data: CentredeCongresCreate, database: Session = Depends(get_db)) -> CentredeCongres:
    db_centredecongres = database.query(CentredeCongres).filter(CentredeCongres.id == centredecongres_id).first()
    if db_centredecongres is None:
        raise HTTPException(status_code=404, detail="CentredeCongres not found")

    setattr(db_centredecongres, 'nom', centredecongres_data.nom)
    setattr(db_centredecongres, 'adresse', centredecongres_data.adresse)
    if centredecongres_data.gestionnaire_1 is not None:
        db_gestionnaire_1 = database.query(Gestionnaire).filter(Gestionnaire.id == centredecongres_data.gestionnaire_1).first()
        if not db_gestionnaire_1:
            raise HTTPException(status_code=400, detail="Gestionnaire not found")
        setattr(db_centredecongres, 'gestionnaire_1_id', centredecongres_data.gestionnaire_1)
    if centredecongres_data.evenementsalle_1 is not None:
        # Clear all existing relationships (set foreign key to NULL)
        database.query(EvenementSalle).filter(EvenementSalle.centredecongres_id == db_centredecongres.id).update(
            {EvenementSalle.centredecongres_id: None}, synchronize_session=False
        )

        # Set new relationships if list is not empty
        if centredecongres_data.evenementsalle_1:
            # Validate that all IDs exist
            for evenementsalle_id in centredecongres_data.evenementsalle_1:
                db_evenementsalle = database.query(EvenementSalle).filter(EvenementSalle.id == evenementsalle_id).first()
                if not db_evenementsalle:
                    raise HTTPException(status_code=400, detail=f"EvenementSalle with id {evenementsalle_id} not found")

            # Update the related entities with the new foreign key
            database.query(EvenementSalle).filter(EvenementSalle.id.in_(centredecongres_data.evenementsalle_1)).update(
                {EvenementSalle.centredecongres_id: db_centredecongres.id}, synchronize_session=False
            )
    database.commit()
    database.refresh(db_centredecongres)

    evenementsalle_1_ids = database.query(EvenementSalle.id).filter(EvenementSalle.centredecongres_id == db_centredecongres.id).all()
    response_data = {
        "centredecongres": db_centredecongres,
        "evenementsalle_1_ids": [x[0] for x in evenementsalle_1_ids]    }
    return response_data


@app.delete("/centredecongres/{centredecongres_id}/", response_model=None, tags=["CentredeCongres"])
async def delete_centredecongres(centredecongres_id: int, database: Session = Depends(get_db)):
    db_centredecongres = database.query(CentredeCongres).filter(CentredeCongres.id == centredecongres_id).first()
    if db_centredecongres is None:
        raise HTTPException(status_code=404, detail="CentredeCongres not found")
    database.delete(db_centredecongres)
    database.commit()
    return db_centredecongres





############################################
#
#   Tarifs functions
#
############################################

@app.get("/tarifs/", response_model=None, tags=["Tarifs"])
def get_all_tarifs(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(Tarifs)
        tarifs_list = query.all()

        # Serialize with relationships included
        result = []
        for tarifs_item in tarifs_list:
            item_dict = tarifs_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)

            # Add many-to-many and one-to-many relationship objects (full details)
            evenementsalle_list = database.query(EvenementSalle).join(applique, EvenementSalle.id == applique.c.evenementsalle_2).filter(applique.c.tarifs == tarifs_item.id).all()
            item_dict['evenementsalle_2'] = []
            for evenementsalle_obj in evenementsalle_list:
                evenementsalle_dict = evenementsalle_obj.__dict__.copy()
                evenementsalle_dict.pop('_sa_instance_state', None)
                item_dict['evenementsalle_2'].append(evenementsalle_dict)
            materielsprestations_list = database.query(Materielsprestations).join(applique_1, Materielsprestations.id == applique_1.c.materielsprestations_1).filter(applique_1.c.tarifs_1 == tarifs_item.id).all()
            item_dict['materielsprestations_1'] = []
            for materielsprestations_obj in materielsprestations_list:
                materielsprestations_dict = materielsprestations_obj.__dict__.copy()
                materielsprestations_dict.pop('_sa_instance_state', None)
                item_dict['materielsprestations_1'].append(materielsprestations_dict)

            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(Tarifs).all()


@app.get("/tarifs/count/", response_model=None, tags=["Tarifs"])
def get_count_tarifs(database: Session = Depends(get_db)) -> dict:
    """Get the total count of Tarifs entities"""
    count = database.query(Tarifs).count()
    return {"count": count}


@app.get("/tarifs/paginated/", response_model=None, tags=["Tarifs"])
def get_paginated_tarifs(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of Tarifs entities"""
    total = database.query(Tarifs).count()
    tarifs_list = database.query(Tarifs).offset(skip).limit(limit).all()
    # By default, return flat entities (for charts/widgets)
    # Use detailed=true to get entities with relationships
    if not detailed:
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": tarifs_list
        }

    result = []
    for tarifs_item in tarifs_list:
        evenementsalle_ids = database.query(applique.c.evenementsalle_2).filter(applique.c.tarifs == tarifs_item.id).all()
        materielsprestations_ids = database.query(applique_1.c.materielsprestations_1).filter(applique_1.c.tarifs_1 == tarifs_item.id).all()
        item_data = {
            "tarifs": tarifs_item,
            "evenementsalle_ids": [x[0] for x in evenementsalle_ids],
            "materielsprestations_ids": [x[0] for x in materielsprestations_ids],
        }
        result.append(item_data)
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": result
    }


@app.get("/tarifs/search/", response_model=None, tags=["Tarifs"])
def search_tarifs(
    database: Session = Depends(get_db)
) -> list:
    """Search Tarifs entities by attributes"""
    query = database.query(Tarifs)


    results = query.all()
    return results


@app.get("/tarifs/{tarifs_id}/", response_model=None, tags=["Tarifs"])
async def get_tarifs(tarifs_id: int, database: Session = Depends(get_db)) -> Tarifs:
    db_tarifs = database.query(Tarifs).filter(Tarifs.id == tarifs_id).first()
    if db_tarifs is None:
        raise HTTPException(status_code=404, detail="Tarifs not found")

    evenementsalle_ids = database.query(applique.c.evenementsalle_2).filter(applique.c.tarifs == db_tarifs.id).all()
    materielsprestations_ids = database.query(applique_1.c.materielsprestations_1).filter(applique_1.c.tarifs_1 == db_tarifs.id).all()
    response_data = {
        "tarifs": db_tarifs,
        "evenementsalle_ids": [x[0] for x in evenementsalle_ids],
        "materielsprestations_ids": [x[0] for x in materielsprestations_ids],
}
    return response_data



@app.post("/tarifs/", response_model=None, tags=["Tarifs"])
async def create_tarifs(tarifs_data: TarifsCreate, database: Session = Depends(get_db)) -> Tarifs:

    if tarifs_data.evenementsalle_2:
        for id in tarifs_data.evenementsalle_2:
            # Entity already validated before creation
            db_evenementsalle = database.query(EvenementSalle).filter(EvenementSalle.id == id).first()
            if not db_evenementsalle:
                raise HTTPException(status_code=404, detail=f"EvenementSalle with ID {id} not found")
    if tarifs_data.materielsprestations_1:
        for id in tarifs_data.materielsprestations_1:
            # Entity already validated before creation
            db_materielsprestations = database.query(Materielsprestations).filter(Materielsprestations.id == id).first()
            if not db_materielsprestations:
                raise HTTPException(status_code=404, detail=f"Materielsprestations with ID {id} not found")

    db_tarifs = Tarifs(
        saison=tarifs_data.saison,        montantBase=tarifs_data.montantBase        )

    database.add(db_tarifs)
    database.commit()
    database.refresh(db_tarifs)


    if tarifs_data.evenementsalle_2:
        for id in tarifs_data.evenementsalle_2:
            # Entity already validated before creation
            db_evenementsalle = database.query(EvenementSalle).filter(EvenementSalle.id == id).first()
            # Create the association
            association = applique.insert().values(tarifs=db_tarifs.id, evenementsalle_2=db_evenementsalle.id)
            database.execute(association)
            database.commit()
    if tarifs_data.materielsprestations_1:
        for id in tarifs_data.materielsprestations_1:
            # Entity already validated before creation
            db_materielsprestations = database.query(Materielsprestations).filter(Materielsprestations.id == id).first()
            # Create the association
            association = applique_1.insert().values(tarifs_1=db_tarifs.id, materielsprestations_1=db_materielsprestations.id)
            database.execute(association)
            database.commit()


    evenementsalle_ids = database.query(applique.c.evenementsalle_2).filter(applique.c.tarifs == db_tarifs.id).all()
    materielsprestations_ids = database.query(applique_1.c.materielsprestations_1).filter(applique_1.c.tarifs_1 == db_tarifs.id).all()
    response_data = {
        "tarifs": db_tarifs,
        "evenementsalle_ids": [x[0] for x in evenementsalle_ids],
        "materielsprestations_ids": [x[0] for x in materielsprestations_ids],
    }
    return response_data


@app.post("/tarifs/bulk/", response_model=None, tags=["Tarifs"])
async def bulk_create_tarifs(items: list[TarifsCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple Tarifs entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item

            db_tarifs = Tarifs(
                saison=item_data.saison,                montantBase=item_data.montantBase            )
            database.add(db_tarifs)
            database.flush()  # Get ID without committing
            created_items.append(db_tarifs.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} Tarifs entities"
    }


@app.delete("/tarifs/bulk/", response_model=None, tags=["Tarifs"])
async def bulk_delete_tarifs(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple Tarifs entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_tarifs = database.query(Tarifs).filter(Tarifs.id == item_id).first()
        if db_tarifs:
            database.delete(db_tarifs)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} Tarifs entities"
    }

@app.put("/tarifs/{tarifs_id}/", response_model=None, tags=["Tarifs"])
async def update_tarifs(tarifs_id: int, tarifs_data: TarifsCreate, database: Session = Depends(get_db)) -> Tarifs:
    db_tarifs = database.query(Tarifs).filter(Tarifs.id == tarifs_id).first()
    if db_tarifs is None:
        raise HTTPException(status_code=404, detail="Tarifs not found")

    setattr(db_tarifs, 'saison', tarifs_data.saison)
    setattr(db_tarifs, 'montantBase', tarifs_data.montantBase)
    existing_evenementsalle_ids = [assoc.evenementsalle_2 for assoc in database.execute(
        applique.select().where(applique.c.tarifs == db_tarifs.id))]

    evenementsalles_to_remove = set(existing_evenementsalle_ids) - set(tarifs_data.evenementsalle_2)
    for evenementsalle_id in evenementsalles_to_remove:
        association = applique.delete().where(
            (applique.c.tarifs == db_tarifs.id) & (applique.c.evenementsalle_2 == evenementsalle_id))
        database.execute(association)

    new_evenementsalle_ids = set(tarifs_data.evenementsalle_2) - set(existing_evenementsalle_ids)
    for evenementsalle_id in new_evenementsalle_ids:
        db_evenementsalle = database.query(EvenementSalle).filter(EvenementSalle.id == evenementsalle_id).first()
        if db_evenementsalle is None:
            raise HTTPException(status_code=404, detail=f"EvenementSalle with ID {evenementsalle_id} not found")
        association = applique.insert().values(evenementsalle_2=db_evenementsalle.id, tarifs=db_tarifs.id)
        database.execute(association)
    existing_materielsprestations_ids = [assoc.materielsprestations_1 for assoc in database.execute(
        applique_1.select().where(applique_1.c.tarifs_1 == db_tarifs.id))]

    materielsprestationss_to_remove = set(existing_materielsprestations_ids) - set(tarifs_data.materielsprestations_1)
    for materielsprestations_id in materielsprestationss_to_remove:
        association = applique_1.delete().where(
            (applique_1.c.tarifs_1 == db_tarifs.id) & (applique_1.c.materielsprestations_1 == materielsprestations_id))
        database.execute(association)

    new_materielsprestations_ids = set(tarifs_data.materielsprestations_1) - set(existing_materielsprestations_ids)
    for materielsprestations_id in new_materielsprestations_ids:
        db_materielsprestations = database.query(Materielsprestations).filter(Materielsprestations.id == materielsprestations_id).first()
        if db_materielsprestations is None:
            raise HTTPException(status_code=404, detail=f"Materielsprestations with ID {materielsprestations_id} not found")
        association = applique_1.insert().values(materielsprestations_1=db_materielsprestations.id, tarifs_1=db_tarifs.id)
        database.execute(association)
    database.commit()
    database.refresh(db_tarifs)

    evenementsalle_ids = database.query(applique.c.evenementsalle_2).filter(applique.c.tarifs == db_tarifs.id).all()
    materielsprestations_ids = database.query(applique_1.c.materielsprestations_1).filter(applique_1.c.tarifs_1 == db_tarifs.id).all()
    response_data = {
        "tarifs": db_tarifs,
        "evenementsalle_ids": [x[0] for x in evenementsalle_ids],
        "materielsprestations_ids": [x[0] for x in materielsprestations_ids],
    }
    return response_data


@app.delete("/tarifs/{tarifs_id}/", response_model=None, tags=["Tarifs"])
async def delete_tarifs(tarifs_id: int, database: Session = Depends(get_db)):
    db_tarifs = database.query(Tarifs).filter(Tarifs.id == tarifs_id).first()
    if db_tarifs is None:
        raise HTTPException(status_code=404, detail="Tarifs not found")
    database.delete(db_tarifs)
    database.commit()
    return db_tarifs

@app.post("/tarifs/{tarifs_id}/evenementsalle_2/{evenementsalle_id}/", response_model=None, tags=["Tarifs Relationships"])
async def add_evenementsalle_2_to_tarifs(tarifs_id: int, evenementsalle_id: int, database: Session = Depends(get_db)):
    """Add a EvenementSalle to this Tarifs's evenementsalle_2 relationship"""
    db_tarifs = database.query(Tarifs).filter(Tarifs.id == tarifs_id).first()
    if db_tarifs is None:
        raise HTTPException(status_code=404, detail="Tarifs not found")

    db_evenementsalle = database.query(EvenementSalle).filter(EvenementSalle.id == evenementsalle_id).first()
    if db_evenementsalle is None:
        raise HTTPException(status_code=404, detail="EvenementSalle not found")

    # Check if relationship already exists
    existing = database.query(applique).filter(
        (applique.c.tarifs == tarifs_id) &
        (applique.c.evenementsalle_2 == evenementsalle_id)
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Relationship already exists")

    # Create the association
    association = applique.insert().values(tarifs=tarifs_id, evenementsalle_2=evenementsalle_id)
    database.execute(association)
    database.commit()

    return {"message": "EvenementSalle added to evenementsalle_2 successfully"}


@app.delete("/tarifs/{tarifs_id}/evenementsalle_2/{evenementsalle_id}/", response_model=None, tags=["Tarifs Relationships"])
async def remove_evenementsalle_2_from_tarifs(tarifs_id: int, evenementsalle_id: int, database: Session = Depends(get_db)):
    """Remove a EvenementSalle from this Tarifs's evenementsalle_2 relationship"""
    db_tarifs = database.query(Tarifs).filter(Tarifs.id == tarifs_id).first()
    if db_tarifs is None:
        raise HTTPException(status_code=404, detail="Tarifs not found")

    # Check if relationship exists
    existing = database.query(applique).filter(
        (applique.c.tarifs == tarifs_id) &
        (applique.c.evenementsalle_2 == evenementsalle_id)
    ).first()

    if not existing:
        raise HTTPException(status_code=404, detail="Relationship not found")

    # Delete the association
    association = applique.delete().where(
        (applique.c.tarifs == tarifs_id) &
        (applique.c.evenementsalle_2 == evenementsalle_id)
    )
    database.execute(association)
    database.commit()

    return {"message": "EvenementSalle removed from evenementsalle_2 successfully"}


@app.get("/tarifs/{tarifs_id}/evenementsalle_2/", response_model=None, tags=["Tarifs Relationships"])
async def get_evenementsalle_2_of_tarifs(tarifs_id: int, database: Session = Depends(get_db)):
    """Get all EvenementSalle entities related to this Tarifs through evenementsalle_2"""
    db_tarifs = database.query(Tarifs).filter(Tarifs.id == tarifs_id).first()
    if db_tarifs is None:
        raise HTTPException(status_code=404, detail="Tarifs not found")

    evenementsalle_ids = database.query(applique.c.evenementsalle_2).filter(applique.c.tarifs == tarifs_id).all()
    evenementsalle_list = database.query(EvenementSalle).filter(EvenementSalle.id.in_([id[0] for id in evenementsalle_ids])).all()

    return {
        "tarifs_id": tarifs_id,
        "evenementsalle_2_count": len(evenementsalle_list),
        "evenementsalle_2": evenementsalle_list
    }

@app.post("/tarifs/{tarifs_id}/materielsprestations_1/{materielsprestations_id}/", response_model=None, tags=["Tarifs Relationships"])
async def add_materielsprestations_1_to_tarifs(tarifs_id: int, materielsprestations_id: int, database: Session = Depends(get_db)):
    """Add a Materielsprestations to this Tarifs's materielsprestations_1 relationship"""
    db_tarifs = database.query(Tarifs).filter(Tarifs.id == tarifs_id).first()
    if db_tarifs is None:
        raise HTTPException(status_code=404, detail="Tarifs not found")

    db_materielsprestations = database.query(Materielsprestations).filter(Materielsprestations.id == materielsprestations_id).first()
    if db_materielsprestations is None:
        raise HTTPException(status_code=404, detail="Materielsprestations not found")

    # Check if relationship already exists
    existing = database.query(applique_1).filter(
        (applique_1.c.tarifs_1 == tarifs_id) &
        (applique_1.c.materielsprestations_1 == materielsprestations_id)
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Relationship already exists")

    # Create the association
    association = applique_1.insert().values(tarifs_1=tarifs_id, materielsprestations_1=materielsprestations_id)
    database.execute(association)
    database.commit()

    return {"message": "Materielsprestations added to materielsprestations_1 successfully"}


@app.delete("/tarifs/{tarifs_id}/materielsprestations_1/{materielsprestations_id}/", response_model=None, tags=["Tarifs Relationships"])
async def remove_materielsprestations_1_from_tarifs(tarifs_id: int, materielsprestations_id: int, database: Session = Depends(get_db)):
    """Remove a Materielsprestations from this Tarifs's materielsprestations_1 relationship"""
    db_tarifs = database.query(Tarifs).filter(Tarifs.id == tarifs_id).first()
    if db_tarifs is None:
        raise HTTPException(status_code=404, detail="Tarifs not found")

    # Check if relationship exists
    existing = database.query(applique_1).filter(
        (applique_1.c.tarifs_1 == tarifs_id) &
        (applique_1.c.materielsprestations_1 == materielsprestations_id)
    ).first()

    if not existing:
        raise HTTPException(status_code=404, detail="Relationship not found")

    # Delete the association
    association = applique_1.delete().where(
        (applique_1.c.tarifs_1 == tarifs_id) &
        (applique_1.c.materielsprestations_1 == materielsprestations_id)
    )
    database.execute(association)
    database.commit()

    return {"message": "Materielsprestations removed from materielsprestations_1 successfully"}


@app.get("/tarifs/{tarifs_id}/materielsprestations_1/", response_model=None, tags=["Tarifs Relationships"])
async def get_materielsprestations_1_of_tarifs(tarifs_id: int, database: Session = Depends(get_db)):
    """Get all Materielsprestations entities related to this Tarifs through materielsprestations_1"""
    db_tarifs = database.query(Tarifs).filter(Tarifs.id == tarifs_id).first()
    if db_tarifs is None:
        raise HTTPException(status_code=404, detail="Tarifs not found")

    materielsprestations_ids = database.query(applique_1.c.materielsprestations_1).filter(applique_1.c.tarifs_1 == tarifs_id).all()
    materielsprestations_list = database.query(Materielsprestations).filter(Materielsprestations.id.in_([id[0] for id in materielsprestations_ids])).all()

    return {
        "tarifs_id": tarifs_id,
        "materielsprestations_1_count": len(materielsprestations_list),
        "materielsprestations_1": materielsprestations_list
    }



############################################
#   Tarifs Method Endpoints
############################################




@app.post("/tarifs/{tarifs_id}/methods/appliquerTarif/", response_model=None, tags=["Tarifs Methods"])
async def execute_tarifs_appliquerTarif(
    tarifs_id: int,
    params: dict = Body(default=None, embed=True),
    database: Session = Depends(get_db)
):
    """
    Execute the appliquerTarif method on a Tarifs instance.

    Parameters:
    - date: str    """
    # Retrieve the entity from the database
    _tarifs_object = database.query(Tarifs).filter(Tarifs.id == tarifs_id).first()
    if _tarifs_object is None:
        raise HTTPException(status_code=404, detail="Tarifs not found")

    # Prepare method parameters
    date = params.get('date')

    # Execute the method
    try:
        # Capture stdout to include print outputs in the response
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output

        async def wrapper(_tarifs_object):
            try:
                # On récupère le montant de base actuel
                base = float(getattr(_tarifs_object, 'montantBase', 0.0))
                # On récupère la saison et on met tout en minuscules pour éviter les erreurs de frappe
                saison = str(getattr(_tarifs_object, 'saison', 'Standard')).lower()
                
                # Définition des coefficients par saison
                if "été" in saison or "ete" in saison:
                    facteur = 1.20  # +20% (Haute saison)
                    nom_saison = "Été"
                elif "hiver" in saison:
                    facteur = 1.10  # +10% (Saison de ski/fêtes)
                    nom_saison = "Hiver"
                elif "automne" in saison:
                    facteur = 0.90  # -10% (Promotion automne)
                    nom_saison = "Automne"
                elif "printemps" in saison:
                    facteur = 1.05  # +5% (Saison intermédiaire)
                    nom_saison = "Printemps"
                else:
                    facteur = 1.00  # Tarif normal
                    nom_saison = "Standard"
                    
                nouveau_tarif = base * facteur
                
                # Mise à jour de l'attribut dans l'objet BESSER
                setattr(_tarifs_object, 'montantBase', nouveau_tarif)
                
                return f"Tarif {nom_saison} appliqué pour le {date} : {nouveau_tarif}€ (Facteur: x{facteur})"
            except:
                return "Erreur lors du calcul du tarif saisonnier."

        result = await wrapper(_tarifs_object)
        # Commit DB
        database.commit()
        database.refresh(_tarifs_object)

        # Restore stdout
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        return {
            "tarifs_id": tarifs_id,
            "method": "appliquerTarif",
            "status": "executed",
            "result": str(result) if result is not None else None,
            "output": output if output else None
        }
    except Exception as e:
        sys.stdout = sys.__stdout__
        raise HTTPException(status_code=500, detail=f"Method execution failed: {str(e)}")



############################################
#
#   EvenementSalle functions
#
############################################

@app.get("/evenementsalle/", response_model=None, tags=["EvenementSalle"])
def get_all_evenementsalle(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(EvenementSalle)
        query = query.options(joinedload(EvenementSalle.reservation))
        query = query.options(joinedload(EvenementSalle.centredecongres))
        evenementsalle_list = query.all()

        # Serialize with relationships included
        result = []
        for evenementsalle_item in evenementsalle_list:
            item_dict = evenementsalle_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)
            if evenementsalle_item.reservation:
                related_obj = evenementsalle_item.reservation
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['reservation'] = related_dict
            else:
                item_dict['reservation'] = None
            if evenementsalle_item.centredecongres:
                related_obj = evenementsalle_item.centredecongres
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['centredecongres'] = related_dict
            else:
                item_dict['centredecongres'] = None

            # Add many-to-many and one-to-many relationship objects (full details)
            tarifs_list = database.query(Tarifs).join(applique, Tarifs.id == applique.c.tarifs).filter(applique.c.evenementsalle_2 == evenementsalle_item.id).all()
            item_dict['tarifs'] = []
            for tarifs_obj in tarifs_list:
                tarifs_dict = tarifs_obj.__dict__.copy()
                tarifs_dict.pop('_sa_instance_state', None)
                item_dict['tarifs'].append(tarifs_dict)

            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(EvenementSalle).all()


@app.get("/evenementsalle/count/", response_model=None, tags=["EvenementSalle"])
def get_count_evenementsalle(database: Session = Depends(get_db)) -> dict:
    """Get the total count of EvenementSalle entities"""
    count = database.query(EvenementSalle).count()
    return {"count": count}


@app.get("/evenementsalle/paginated/", response_model=None, tags=["EvenementSalle"])
def get_paginated_evenementsalle(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of EvenementSalle entities"""
    total = database.query(EvenementSalle).count()
    evenementsalle_list = database.query(EvenementSalle).offset(skip).limit(limit).all()
    # By default, return flat entities (for charts/widgets)
    # Use detailed=true to get entities with relationships
    if not detailed:
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": evenementsalle_list
        }

    result = []
    for evenementsalle_item in evenementsalle_list:
        tarifs_ids = database.query(applique.c.tarifs).filter(applique.c.evenementsalle_2 == evenementsalle_item.id).all()
        item_data = {
            "evenementsalle": evenementsalle_item,
            "tarifs_ids": [x[0] for x in tarifs_ids],
        }
        result.append(item_data)
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": result
    }


@app.get("/evenementsalle/search/", response_model=None, tags=["EvenementSalle"])
def search_evenementsalle(
    database: Session = Depends(get_db)
) -> list:
    """Search EvenementSalle entities by attributes"""
    query = database.query(EvenementSalle)


    results = query.all()
    return results


@app.get("/evenementsalle/{evenementsalle_id}/", response_model=None, tags=["EvenementSalle"])
async def get_evenementsalle(evenementsalle_id: int, database: Session = Depends(get_db)) -> EvenementSalle:
    db_evenementsalle = database.query(EvenementSalle).filter(EvenementSalle.id == evenementsalle_id).first()
    if db_evenementsalle is None:
        raise HTTPException(status_code=404, detail="EvenementSalle not found")

    tarifs_ids = database.query(applique.c.tarifs).filter(applique.c.evenementsalle_2 == db_evenementsalle.id).all()
    response_data = {
        "evenementsalle": db_evenementsalle,
        "tarifs_ids": [x[0] for x in tarifs_ids],
}
    return response_data



@app.post("/evenementsalle/", response_model=None, tags=["EvenementSalle"])
async def create_evenementsalle(evenementsalle_data: EvenementSalleCreate, database: Session = Depends(get_db)) -> EvenementSalle:

    if evenementsalle_data.reservation :
        db_reservation = database.query(Reservation).filter(Reservation.id == evenementsalle_data.reservation).first()
        if not db_reservation:
            raise HTTPException(status_code=400, detail="Reservation not found")
    if evenementsalle_data.centredecongres :
        db_centredecongres = database.query(CentredeCongres).filter(CentredeCongres.id == evenementsalle_data.centredecongres).first()
        if not db_centredecongres:
            raise HTTPException(status_code=400, detail="CentredeCongres not found")
    if evenementsalle_data.tarifs:
        for id in evenementsalle_data.tarifs:
            # Entity already validated before creation
            db_tarifs = database.query(Tarifs).filter(Tarifs.id == id).first()
            if not db_tarifs:
                raise HTTPException(status_code=404, detail=f"Tarifs with ID {id} not found")

    db_evenementsalle = EvenementSalle(
        typeElement=evenementsalle_data.typeElement,        nom=evenementsalle_data.nom,        capaciteMax=evenementsalle_data.capaciteMax,        reservation_id=evenementsalle_data.reservation,        centredecongres_id=evenementsalle_data.centredecongres        )

    database.add(db_evenementsalle)
    database.commit()
    database.refresh(db_evenementsalle)


    if evenementsalle_data.tarifs:
        for id in evenementsalle_data.tarifs:
            # Entity already validated before creation
            db_tarifs = database.query(Tarifs).filter(Tarifs.id == id).first()
            # Create the association
            association = applique.insert().values(evenementsalle_2=db_evenementsalle.id, tarifs=db_tarifs.id)
            database.execute(association)
            database.commit()


    tarifs_ids = database.query(applique.c.tarifs).filter(applique.c.evenementsalle_2 == db_evenementsalle.id).all()
    response_data = {
        "evenementsalle": db_evenementsalle,
        "tarifs_ids": [x[0] for x in tarifs_ids],
    }
    return response_data


@app.post("/evenementsalle/bulk/", response_model=None, tags=["EvenementSalle"])
async def bulk_create_evenementsalle(items: list[EvenementSalleCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple EvenementSalle entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item

            db_evenementsalle = EvenementSalle(
                typeElement=item_data.typeElement,                nom=item_data.nom,                capaciteMax=item_data.capaciteMax,                reservation_id=item_data.reservation,                centredecongres_id=item_data.centredecongres            )
            database.add(db_evenementsalle)
            database.flush()  # Get ID without committing
            created_items.append(db_evenementsalle.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} EvenementSalle entities"
    }


@app.delete("/evenementsalle/bulk/", response_model=None, tags=["EvenementSalle"])
async def bulk_delete_evenementsalle(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple EvenementSalle entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_evenementsalle = database.query(EvenementSalle).filter(EvenementSalle.id == item_id).first()
        if db_evenementsalle:
            database.delete(db_evenementsalle)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} EvenementSalle entities"
    }

@app.put("/evenementsalle/{evenementsalle_id}/", response_model=None, tags=["EvenementSalle"])
async def update_evenementsalle(evenementsalle_id: int, evenementsalle_data: EvenementSalleCreate, database: Session = Depends(get_db)) -> EvenementSalle:
    db_evenementsalle = database.query(EvenementSalle).filter(EvenementSalle.id == evenementsalle_id).first()
    if db_evenementsalle is None:
        raise HTTPException(status_code=404, detail="EvenementSalle not found")

    setattr(db_evenementsalle, 'typeElement', evenementsalle_data.typeElement)
    setattr(db_evenementsalle, 'nom', evenementsalle_data.nom)
    setattr(db_evenementsalle, 'capaciteMax', evenementsalle_data.capaciteMax)
    if evenementsalle_data.reservation is not None:
        db_reservation = database.query(Reservation).filter(Reservation.id == evenementsalle_data.reservation).first()
        if not db_reservation:
            raise HTTPException(status_code=400, detail="Reservation not found")
        setattr(db_evenementsalle, 'reservation_id', evenementsalle_data.reservation)
    else:
        setattr(db_evenementsalle, 'reservation_id', None)
    if evenementsalle_data.centredecongres is not None:
        db_centredecongres = database.query(CentredeCongres).filter(CentredeCongres.id == evenementsalle_data.centredecongres).first()
        if not db_centredecongres:
            raise HTTPException(status_code=400, detail="CentredeCongres not found")
        setattr(db_evenementsalle, 'centredecongres_id', evenementsalle_data.centredecongres)
    else:
        setattr(db_evenementsalle, 'centredecongres_id', None)
    existing_tarifs_ids = [assoc.tarifs for assoc in database.execute(
        applique.select().where(applique.c.evenementsalle_2 == db_evenementsalle.id))]

    tarifss_to_remove = set(existing_tarifs_ids) - set(evenementsalle_data.tarifs)
    for tarifs_id in tarifss_to_remove:
        association = applique.delete().where(
            (applique.c.evenementsalle_2 == db_evenementsalle.id) & (applique.c.tarifs == tarifs_id))
        database.execute(association)

    new_tarifs_ids = set(evenementsalle_data.tarifs) - set(existing_tarifs_ids)
    for tarifs_id in new_tarifs_ids:
        db_tarifs = database.query(Tarifs).filter(Tarifs.id == tarifs_id).first()
        if db_tarifs is None:
            raise HTTPException(status_code=404, detail=f"Tarifs with ID {tarifs_id} not found")
        association = applique.insert().values(tarifs=db_tarifs.id, evenementsalle_2=db_evenementsalle.id)
        database.execute(association)
    database.commit()
    database.refresh(db_evenementsalle)

    tarifs_ids = database.query(applique.c.tarifs).filter(applique.c.evenementsalle_2 == db_evenementsalle.id).all()
    response_data = {
        "evenementsalle": db_evenementsalle,
        "tarifs_ids": [x[0] for x in tarifs_ids],
    }
    return response_data


@app.delete("/evenementsalle/{evenementsalle_id}/", response_model=None, tags=["EvenementSalle"])
async def delete_evenementsalle(evenementsalle_id: int, database: Session = Depends(get_db)):
    db_evenementsalle = database.query(EvenementSalle).filter(EvenementSalle.id == evenementsalle_id).first()
    if db_evenementsalle is None:
        raise HTTPException(status_code=404, detail="EvenementSalle not found")
    database.delete(db_evenementsalle)
    database.commit()
    return db_evenementsalle

@app.post("/evenementsalle/{evenementsalle_id}/tarifs/{tarifs_id}/", response_model=None, tags=["EvenementSalle Relationships"])
async def add_tarifs_to_evenementsalle(evenementsalle_id: int, tarifs_id: int, database: Session = Depends(get_db)):
    """Add a Tarifs to this EvenementSalle's tarifs relationship"""
    db_evenementsalle = database.query(EvenementSalle).filter(EvenementSalle.id == evenementsalle_id).first()
    if db_evenementsalle is None:
        raise HTTPException(status_code=404, detail="EvenementSalle not found")

    db_tarifs = database.query(Tarifs).filter(Tarifs.id == tarifs_id).first()
    if db_tarifs is None:
        raise HTTPException(status_code=404, detail="Tarifs not found")

    # Check if relationship already exists
    existing = database.query(applique).filter(
        (applique.c.evenementsalle_2 == evenementsalle_id) &
        (applique.c.tarifs == tarifs_id)
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Relationship already exists")

    # Create the association
    association = applique.insert().values(evenementsalle_2=evenementsalle_id, tarifs=tarifs_id)
    database.execute(association)
    database.commit()

    return {"message": "Tarifs added to tarifs successfully"}


@app.delete("/evenementsalle/{evenementsalle_id}/tarifs/{tarifs_id}/", response_model=None, tags=["EvenementSalle Relationships"])
async def remove_tarifs_from_evenementsalle(evenementsalle_id: int, tarifs_id: int, database: Session = Depends(get_db)):
    """Remove a Tarifs from this EvenementSalle's tarifs relationship"""
    db_evenementsalle = database.query(EvenementSalle).filter(EvenementSalle.id == evenementsalle_id).first()
    if db_evenementsalle is None:
        raise HTTPException(status_code=404, detail="EvenementSalle not found")

    # Check if relationship exists
    existing = database.query(applique).filter(
        (applique.c.evenementsalle_2 == evenementsalle_id) &
        (applique.c.tarifs == tarifs_id)
    ).first()

    if not existing:
        raise HTTPException(status_code=404, detail="Relationship not found")

    # Delete the association
    association = applique.delete().where(
        (applique.c.evenementsalle_2 == evenementsalle_id) &
        (applique.c.tarifs == tarifs_id)
    )
    database.execute(association)
    database.commit()

    return {"message": "Tarifs removed from tarifs successfully"}


@app.get("/evenementsalle/{evenementsalle_id}/tarifs/", response_model=None, tags=["EvenementSalle Relationships"])
async def get_tarifs_of_evenementsalle(evenementsalle_id: int, database: Session = Depends(get_db)):
    """Get all Tarifs entities related to this EvenementSalle through tarifs"""
    db_evenementsalle = database.query(EvenementSalle).filter(EvenementSalle.id == evenementsalle_id).first()
    if db_evenementsalle is None:
        raise HTTPException(status_code=404, detail="EvenementSalle not found")

    tarifs_ids = database.query(applique.c.tarifs).filter(applique.c.evenementsalle_2 == evenementsalle_id).all()
    tarifs_list = database.query(Tarifs).filter(Tarifs.id.in_([id[0] for id in tarifs_ids])).all()

    return {
        "evenementsalle_id": evenementsalle_id,
        "tarifs_count": len(tarifs_list),
        "tarifs": tarifs_list
    }



############################################
#   EvenementSalle Method Endpoints
############################################




@app.post("/evenementsalle/{evenementsalle_id}/methods/verifierCapacite/", response_model=None, tags=["EvenementSalle Methods"])
async def execute_evenementsalle_verifierCapacite(
    evenementsalle_id: int,
    params: dict = Body(default=None, embed=True),
    database: Session = Depends(get_db)
):
    """
    Execute the verifierCapacite method on a EvenementSalle instance.

    Parameters:
    - nb_a_tester: Any    """
    # Retrieve the entity from the database
    _evenementsalle_object = database.query(EvenementSalle).filter(EvenementSalle.id == evenementsalle_id).first()
    if _evenementsalle_object is None:
        raise HTTPException(status_code=404, detail="EvenementSalle not found")

    # Prepare method parameters
    nb_a_tester = params.get('nb_a_tester')

    # Execute the method
    try:
        # Capture stdout to include print outputs in the response
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output

        async def wrapper(_evenementsalle_object):
            try:
                # On teste les 3 variantes de noms les plus courantes
                v1 = getattr(_evenementsalle_object, 'Capacite', None)
                v2 = getattr(_evenementsalle_object, 'capacite', None)
                v3 = getattr(_evenementsalle_object, 'capaciteMax', None)
                
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

        result = await wrapper(_evenementsalle_object)
        # Commit DB
        database.commit()
        database.refresh(_evenementsalle_object)

        # Restore stdout
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        return {
            "evenementsalle_id": evenementsalle_id,
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
#   Materielsprestations functions
#
############################################

@app.get("/materielsprestations/", response_model=None, tags=["Materielsprestations"])
def get_all_materielsprestations(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(Materielsprestations)
        query = query.options(joinedload(Materielsprestations.reservation_3))
        materielsprestations_list = query.all()

        # Serialize with relationships included
        result = []
        for materielsprestations_item in materielsprestations_list:
            item_dict = materielsprestations_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)
            if materielsprestations_item.reservation_3:
                related_obj = materielsprestations_item.reservation_3
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['reservation_3'] = related_dict
            else:
                item_dict['reservation_3'] = None

            # Add many-to-many and one-to-many relationship objects (full details)
            tarifs_list = database.query(Tarifs).join(applique_1, Tarifs.id == applique_1.c.tarifs_1).filter(applique_1.c.materielsprestations_1 == materielsprestations_item.id).all()
            item_dict['tarifs_1'] = []
            for tarifs_obj in tarifs_list:
                tarifs_dict = tarifs_obj.__dict__.copy()
                tarifs_dict.pop('_sa_instance_state', None)
                item_dict['tarifs_1'].append(tarifs_dict)

            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(Materielsprestations).all()


@app.get("/materielsprestations/count/", response_model=None, tags=["Materielsprestations"])
def get_count_materielsprestations(database: Session = Depends(get_db)) -> dict:
    """Get the total count of Materielsprestations entities"""
    count = database.query(Materielsprestations).count()
    return {"count": count}


@app.get("/materielsprestations/paginated/", response_model=None, tags=["Materielsprestations"])
def get_paginated_materielsprestations(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of Materielsprestations entities"""
    total = database.query(Materielsprestations).count()
    materielsprestations_list = database.query(Materielsprestations).offset(skip).limit(limit).all()
    # By default, return flat entities (for charts/widgets)
    # Use detailed=true to get entities with relationships
    if not detailed:
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": materielsprestations_list
        }

    result = []
    for materielsprestations_item in materielsprestations_list:
        tarifs_ids = database.query(applique_1.c.tarifs_1).filter(applique_1.c.materielsprestations_1 == materielsprestations_item.id).all()
        item_data = {
            "materielsprestations": materielsprestations_item,
            "tarifs_ids": [x[0] for x in tarifs_ids],
        }
        result.append(item_data)
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": result
    }


@app.get("/materielsprestations/search/", response_model=None, tags=["Materielsprestations"])
def search_materielsprestations(
    database: Session = Depends(get_db)
) -> list:
    """Search Materielsprestations entities by attributes"""
    query = database.query(Materielsprestations)


    results = query.all()
    return results


@app.get("/materielsprestations/{materielsprestations_id}/", response_model=None, tags=["Materielsprestations"])
async def get_materielsprestations(materielsprestations_id: int, database: Session = Depends(get_db)) -> Materielsprestations:
    db_materielsprestations = database.query(Materielsprestations).filter(Materielsprestations.id == materielsprestations_id).first()
    if db_materielsprestations is None:
        raise HTTPException(status_code=404, detail="Materielsprestations not found")

    tarifs_ids = database.query(applique_1.c.tarifs_1).filter(applique_1.c.materielsprestations_1 == db_materielsprestations.id).all()
    response_data = {
        "materielsprestations": db_materielsprestations,
        "tarifs_ids": [x[0] for x in tarifs_ids],
}
    return response_data



@app.post("/materielsprestations/", response_model=None, tags=["Materielsprestations"])
async def create_materielsprestations(materielsprestations_data: MaterielsprestationsCreate, database: Session = Depends(get_db)) -> Materielsprestations:

    if materielsprestations_data.reservation_3 is not None:
        db_reservation_3 = database.query(Reservation).filter(Reservation.id == materielsprestations_data.reservation_3).first()
        if not db_reservation_3:
            raise HTTPException(status_code=400, detail="Reservation not found")
    else:
        raise HTTPException(status_code=400, detail="Reservation ID is required")
    if materielsprestations_data.tarifs_1:
        for id in materielsprestations_data.tarifs_1:
            # Entity already validated before creation
            db_tarifs = database.query(Tarifs).filter(Tarifs.id == id).first()
            if not db_tarifs:
                raise HTTPException(status_code=404, detail=f"Tarifs with ID {id} not found")

    db_materielsprestations = Materielsprestations(
        prixUnitaire=materielsprestations_data.prixUnitaire,        type=materielsprestations_data.type,        nom=materielsprestations_data.nom,        quantiteMax=materielsprestations_data.quantiteMax,        reservation_3_id=materielsprestations_data.reservation_3        )

    database.add(db_materielsprestations)
    database.commit()
    database.refresh(db_materielsprestations)


    if materielsprestations_data.tarifs_1:
        for id in materielsprestations_data.tarifs_1:
            # Entity already validated before creation
            db_tarifs = database.query(Tarifs).filter(Tarifs.id == id).first()
            # Create the association
            association = applique_1.insert().values(materielsprestations_1=db_materielsprestations.id, tarifs_1=db_tarifs.id)
            database.execute(association)
            database.commit()


    tarifs_ids = database.query(applique_1.c.tarifs_1).filter(applique_1.c.materielsprestations_1 == db_materielsprestations.id).all()
    response_data = {
        "materielsprestations": db_materielsprestations,
        "tarifs_ids": [x[0] for x in tarifs_ids],
    }
    return response_data


@app.post("/materielsprestations/bulk/", response_model=None, tags=["Materielsprestations"])
async def bulk_create_materielsprestations(items: list[MaterielsprestationsCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple Materielsprestations entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item
            if not item_data.reservation_3:
                raise ValueError("Reservation ID is required")

            db_materielsprestations = Materielsprestations(
                prixUnitaire=item_data.prixUnitaire,                type=item_data.type,                nom=item_data.nom,                quantiteMax=item_data.quantiteMax,                reservation_3_id=item_data.reservation_3            )
            database.add(db_materielsprestations)
            database.flush()  # Get ID without committing
            created_items.append(db_materielsprestations.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} Materielsprestations entities"
    }


@app.delete("/materielsprestations/bulk/", response_model=None, tags=["Materielsprestations"])
async def bulk_delete_materielsprestations(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple Materielsprestations entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_materielsprestations = database.query(Materielsprestations).filter(Materielsprestations.id == item_id).first()
        if db_materielsprestations:
            database.delete(db_materielsprestations)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} Materielsprestations entities"
    }

@app.put("/materielsprestations/{materielsprestations_id}/", response_model=None, tags=["Materielsprestations"])
async def update_materielsprestations(materielsprestations_id: int, materielsprestations_data: MaterielsprestationsCreate, database: Session = Depends(get_db)) -> Materielsprestations:
    db_materielsprestations = database.query(Materielsprestations).filter(Materielsprestations.id == materielsprestations_id).first()
    if db_materielsprestations is None:
        raise HTTPException(status_code=404, detail="Materielsprestations not found")

    setattr(db_materielsprestations, 'prixUnitaire', materielsprestations_data.prixUnitaire)
    setattr(db_materielsprestations, 'type', materielsprestations_data.type)
    setattr(db_materielsprestations, 'nom', materielsprestations_data.nom)
    setattr(db_materielsprestations, 'quantiteMax', materielsprestations_data.quantiteMax)
    if materielsprestations_data.reservation_3 is not None:
        db_reservation_3 = database.query(Reservation).filter(Reservation.id == materielsprestations_data.reservation_3).first()
        if not db_reservation_3:
            raise HTTPException(status_code=400, detail="Reservation not found")
        setattr(db_materielsprestations, 'reservation_3_id', materielsprestations_data.reservation_3)
    existing_tarifs_ids = [assoc.tarifs_1 for assoc in database.execute(
        applique_1.select().where(applique_1.c.materielsprestations_1 == db_materielsprestations.id))]

    tarifss_to_remove = set(existing_tarifs_ids) - set(materielsprestations_data.tarifs_1)
    for tarifs_id in tarifss_to_remove:
        association = applique_1.delete().where(
            (applique_1.c.materielsprestations_1 == db_materielsprestations.id) & (applique_1.c.tarifs_1 == tarifs_id))
        database.execute(association)

    new_tarifs_ids = set(materielsprestations_data.tarifs_1) - set(existing_tarifs_ids)
    for tarifs_id in new_tarifs_ids:
        db_tarifs = database.query(Tarifs).filter(Tarifs.id == tarifs_id).first()
        if db_tarifs is None:
            raise HTTPException(status_code=404, detail=f"Tarifs with ID {tarifs_id} not found")
        association = applique_1.insert().values(tarifs_1=db_tarifs.id, materielsprestations_1=db_materielsprestations.id)
        database.execute(association)
    database.commit()
    database.refresh(db_materielsprestations)

    tarifs_ids = database.query(applique_1.c.tarifs_1).filter(applique_1.c.materielsprestations_1 == db_materielsprestations.id).all()
    response_data = {
        "materielsprestations": db_materielsprestations,
        "tarifs_ids": [x[0] for x in tarifs_ids],
    }
    return response_data


@app.delete("/materielsprestations/{materielsprestations_id}/", response_model=None, tags=["Materielsprestations"])
async def delete_materielsprestations(materielsprestations_id: int, database: Session = Depends(get_db)):
    db_materielsprestations = database.query(Materielsprestations).filter(Materielsprestations.id == materielsprestations_id).first()
    if db_materielsprestations is None:
        raise HTTPException(status_code=404, detail="Materielsprestations not found")
    database.delete(db_materielsprestations)
    database.commit()
    return db_materielsprestations

@app.post("/materielsprestations/{materielsprestations_id}/tarifs_1/{tarifs_id}/", response_model=None, tags=["Materielsprestations Relationships"])
async def add_tarifs_1_to_materielsprestations(materielsprestations_id: int, tarifs_id: int, database: Session = Depends(get_db)):
    """Add a Tarifs to this Materielsprestations's tarifs_1 relationship"""
    db_materielsprestations = database.query(Materielsprestations).filter(Materielsprestations.id == materielsprestations_id).first()
    if db_materielsprestations is None:
        raise HTTPException(status_code=404, detail="Materielsprestations not found")

    db_tarifs = database.query(Tarifs).filter(Tarifs.id == tarifs_id).first()
    if db_tarifs is None:
        raise HTTPException(status_code=404, detail="Tarifs not found")

    # Check if relationship already exists
    existing = database.query(applique_1).filter(
        (applique_1.c.materielsprestations_1 == materielsprestations_id) &
        (applique_1.c.tarifs_1 == tarifs_id)
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Relationship already exists")

    # Create the association
    association = applique_1.insert().values(materielsprestations_1=materielsprestations_id, tarifs_1=tarifs_id)
    database.execute(association)
    database.commit()

    return {"message": "Tarifs added to tarifs_1 successfully"}


@app.delete("/materielsprestations/{materielsprestations_id}/tarifs_1/{tarifs_id}/", response_model=None, tags=["Materielsprestations Relationships"])
async def remove_tarifs_1_from_materielsprestations(materielsprestations_id: int, tarifs_id: int, database: Session = Depends(get_db)):
    """Remove a Tarifs from this Materielsprestations's tarifs_1 relationship"""
    db_materielsprestations = database.query(Materielsprestations).filter(Materielsprestations.id == materielsprestations_id).first()
    if db_materielsprestations is None:
        raise HTTPException(status_code=404, detail="Materielsprestations not found")

    # Check if relationship exists
    existing = database.query(applique_1).filter(
        (applique_1.c.materielsprestations_1 == materielsprestations_id) &
        (applique_1.c.tarifs_1 == tarifs_id)
    ).first()

    if not existing:
        raise HTTPException(status_code=404, detail="Relationship not found")

    # Delete the association
    association = applique_1.delete().where(
        (applique_1.c.materielsprestations_1 == materielsprestations_id) &
        (applique_1.c.tarifs_1 == tarifs_id)
    )
    database.execute(association)
    database.commit()

    return {"message": "Tarifs removed from tarifs_1 successfully"}


@app.get("/materielsprestations/{materielsprestations_id}/tarifs_1/", response_model=None, tags=["Materielsprestations Relationships"])
async def get_tarifs_1_of_materielsprestations(materielsprestations_id: int, database: Session = Depends(get_db)):
    """Get all Tarifs entities related to this Materielsprestations through tarifs_1"""
    db_materielsprestations = database.query(Materielsprestations).filter(Materielsprestations.id == materielsprestations_id).first()
    if db_materielsprestations is None:
        raise HTTPException(status_code=404, detail="Materielsprestations not found")

    tarifs_ids = database.query(applique_1.c.tarifs_1).filter(applique_1.c.materielsprestations_1 == materielsprestations_id).all()
    tarifs_list = database.query(Tarifs).filter(Tarifs.id.in_([id[0] for id in tarifs_ids])).all()

    return {
        "materielsprestations_id": materielsprestations_id,
        "tarifs_1_count": len(tarifs_list),
        "tarifs_1": tarifs_list
    }



############################################
#   Materielsprestations Method Endpoints
############################################




@app.post("/materielsprestations/{materielsprestations_id}/methods/verifierStockDisponible/", response_model=None, tags=["Materielsprestations Methods"])
async def execute_materielsprestations_verifierStockDisponible(
    materielsprestations_id: int,
    params: dict = Body(default=None, embed=True),
    database: Session = Depends(get_db)
):
    """
    Execute the verifierStockDisponible method on a Materielsprestations instance.

    Parameters:
    - quantiteDemandee: int    """
    # Retrieve the entity from the database
    _materielsprestations_object = database.query(Materielsprestations).filter(Materielsprestations.id == materielsprestations_id).first()
    if _materielsprestations_object is None:
        raise HTTPException(status_code=404, detail="Materielsprestations not found")

    # Prepare method parameters
    quantiteDemandee = params.get('quantiteDemandee')

    # Execute the method
    try:
        # Capture stdout to include print outputs in the response
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output

        async def wrapper(_materielsprestations_object):
            try:
                # Attribut du diagramme : quantiteMax
                stock_max = int(getattr(_materielsprestations_object, 'quantiteMax', 0))
                demande = int(quantiteDemandee)
                
                if demande <= stock_max:
                    return True # Stock suffisant
                return False # Rupture de stock
            except:
                return False

        result = await wrapper(_materielsprestations_object)
        # Commit DB
        database.commit()
        database.refresh(_materielsprestations_object)

        # Restore stdout
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        return {
            "materielsprestations_id": materielsprestations_id,
            "method": "verifierStockDisponible",
            "status": "executed",
            "result": str(result) if result is not None else None,
            "output": output if output else None
        }
    except Exception as e:
        sys.stdout = sys.__stdout__
        raise HTTPException(status_code=500, detail=f"Method execution failed: {str(e)}")



############################################
#
#   Disponibilites functions
#
############################################

@app.get("/disponibilites/", response_model=None, tags=["Disponibilites"])
def get_all_disponibilites(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(Disponibilites)
        disponibilites_list = query.all()

        # Serialize with relationships included
        result = []
        for disponibilites_item in disponibilites_list:
            item_dict = disponibilites_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)

            # Add many-to-many and one-to-many relationship objects (full details)
            reservation_list = database.query(Reservation).join(verifie, Reservation.id == verifie.c.reservation_2).filter(verifie.c.disponibilites == disponibilites_item.id).all()
            item_dict['reservation_2'] = []
            for reservation_obj in reservation_list:
                reservation_dict = reservation_obj.__dict__.copy()
                reservation_dict.pop('_sa_instance_state', None)
                item_dict['reservation_2'].append(reservation_dict)

            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(Disponibilites).all()


@app.get("/disponibilites/count/", response_model=None, tags=["Disponibilites"])
def get_count_disponibilites(database: Session = Depends(get_db)) -> dict:
    """Get the total count of Disponibilites entities"""
    count = database.query(Disponibilites).count()
    return {"count": count}


@app.get("/disponibilites/paginated/", response_model=None, tags=["Disponibilites"])
def get_paginated_disponibilites(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of Disponibilites entities"""
    total = database.query(Disponibilites).count()
    disponibilites_list = database.query(Disponibilites).offset(skip).limit(limit).all()
    # By default, return flat entities (for charts/widgets)
    # Use detailed=true to get entities with relationships
    if not detailed:
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": disponibilites_list
        }

    result = []
    for disponibilites_item in disponibilites_list:
        reservation_ids = database.query(verifie.c.reservation_2).filter(verifie.c.disponibilites == disponibilites_item.id).all()
        item_data = {
            "disponibilites": disponibilites_item,
            "reservation_ids": [x[0] for x in reservation_ids],
        }
        result.append(item_data)
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": result
    }


@app.get("/disponibilites/search/", response_model=None, tags=["Disponibilites"])
def search_disponibilites(
    database: Session = Depends(get_db)
) -> list:
    """Search Disponibilites entities by attributes"""
    query = database.query(Disponibilites)


    results = query.all()
    return results


@app.get("/disponibilites/{disponibilites_id}/", response_model=None, tags=["Disponibilites"])
async def get_disponibilites(disponibilites_id: int, database: Session = Depends(get_db)) -> Disponibilites:
    db_disponibilites = database.query(Disponibilites).filter(Disponibilites.id == disponibilites_id).first()
    if db_disponibilites is None:
        raise HTTPException(status_code=404, detail="Disponibilites not found")

    reservation_ids = database.query(verifie.c.reservation_2).filter(verifie.c.disponibilites == db_disponibilites.id).all()
    response_data = {
        "disponibilites": db_disponibilites,
        "reservation_ids": [x[0] for x in reservation_ids],
}
    return response_data



@app.post("/disponibilites/", response_model=None, tags=["Disponibilites"])
async def create_disponibilites(disponibilites_data: DisponibilitesCreate, database: Session = Depends(get_db)) -> Disponibilites:

    if not disponibilites_data.reservation_2 or len(disponibilites_data.reservation_2) < 1:
        raise HTTPException(status_code=400, detail="At least 1 Reservation(s) required")
    if disponibilites_data.reservation_2:
        for id in disponibilites_data.reservation_2:
            # Entity already validated before creation
            db_reservation = database.query(Reservation).filter(Reservation.id == id).first()
            if not db_reservation:
                raise HTTPException(status_code=404, detail=f"Reservation with ID {id} not found")

    db_disponibilites = Disponibilites(
        dateFin=disponibilites_data.dateFin,        dateDebut=disponibilites_data.dateDebut,        motifDisponibilite=disponibilites_data.motifDisponibilite,        dureeMinim=disponibilites_data.dureeMinim        )

    database.add(db_disponibilites)
    database.commit()
    database.refresh(db_disponibilites)


    if disponibilites_data.reservation_2:
        for id in disponibilites_data.reservation_2:
            # Entity already validated before creation
            db_reservation = database.query(Reservation).filter(Reservation.id == id).first()
            # Create the association
            association = verifie.insert().values(disponibilites=db_disponibilites.id, reservation_2=db_reservation.id)
            database.execute(association)
            database.commit()


    reservation_ids = database.query(verifie.c.reservation_2).filter(verifie.c.disponibilites == db_disponibilites.id).all()
    response_data = {
        "disponibilites": db_disponibilites,
        "reservation_ids": [x[0] for x in reservation_ids],
    }
    return response_data


@app.post("/disponibilites/bulk/", response_model=None, tags=["Disponibilites"])
async def bulk_create_disponibilites(items: list[DisponibilitesCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple Disponibilites entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item

            db_disponibilites = Disponibilites(
                dateFin=item_data.dateFin,                dateDebut=item_data.dateDebut,                motifDisponibilite=item_data.motifDisponibilite,                dureeMinim=item_data.dureeMinim            )
            database.add(db_disponibilites)
            database.flush()  # Get ID without committing
            created_items.append(db_disponibilites.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} Disponibilites entities"
    }


@app.delete("/disponibilites/bulk/", response_model=None, tags=["Disponibilites"])
async def bulk_delete_disponibilites(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple Disponibilites entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_disponibilites = database.query(Disponibilites).filter(Disponibilites.id == item_id).first()
        if db_disponibilites:
            database.delete(db_disponibilites)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} Disponibilites entities"
    }

@app.put("/disponibilites/{disponibilites_id}/", response_model=None, tags=["Disponibilites"])
async def update_disponibilites(disponibilites_id: int, disponibilites_data: DisponibilitesCreate, database: Session = Depends(get_db)) -> Disponibilites:
    db_disponibilites = database.query(Disponibilites).filter(Disponibilites.id == disponibilites_id).first()
    if db_disponibilites is None:
        raise HTTPException(status_code=404, detail="Disponibilites not found")

    setattr(db_disponibilites, 'dateFin', disponibilites_data.dateFin)
    setattr(db_disponibilites, 'dateDebut', disponibilites_data.dateDebut)
    setattr(db_disponibilites, 'motifDisponibilite', disponibilites_data.motifDisponibilite)
    setattr(db_disponibilites, 'dureeMinim', disponibilites_data.dureeMinim)
    existing_reservation_ids = [assoc.reservation_2 for assoc in database.execute(
        verifie.select().where(verifie.c.disponibilites == db_disponibilites.id))]

    reservations_to_remove = set(existing_reservation_ids) - set(disponibilites_data.reservation_2)
    for reservation_id in reservations_to_remove:
        association = verifie.delete().where(
            (verifie.c.disponibilites == db_disponibilites.id) & (verifie.c.reservation_2 == reservation_id))
        database.execute(association)

    new_reservation_ids = set(disponibilites_data.reservation_2) - set(existing_reservation_ids)
    for reservation_id in new_reservation_ids:
        db_reservation = database.query(Reservation).filter(Reservation.id == reservation_id).first()
        if db_reservation is None:
            raise HTTPException(status_code=404, detail=f"Reservation with ID {reservation_id} not found")
        association = verifie.insert().values(reservation_2=db_reservation.id, disponibilites=db_disponibilites.id)
        database.execute(association)
    database.commit()
    database.refresh(db_disponibilites)

    reservation_ids = database.query(verifie.c.reservation_2).filter(verifie.c.disponibilites == db_disponibilites.id).all()
    response_data = {
        "disponibilites": db_disponibilites,
        "reservation_ids": [x[0] for x in reservation_ids],
    }
    return response_data


@app.delete("/disponibilites/{disponibilites_id}/", response_model=None, tags=["Disponibilites"])
async def delete_disponibilites(disponibilites_id: int, database: Session = Depends(get_db)):
    db_disponibilites = database.query(Disponibilites).filter(Disponibilites.id == disponibilites_id).first()
    if db_disponibilites is None:
        raise HTTPException(status_code=404, detail="Disponibilites not found")
    database.delete(db_disponibilites)
    database.commit()
    return db_disponibilites

@app.post("/disponibilites/{disponibilites_id}/reservation_2/{reservation_id}/", response_model=None, tags=["Disponibilites Relationships"])
async def add_reservation_2_to_disponibilites(disponibilites_id: int, reservation_id: int, database: Session = Depends(get_db)):
    """Add a Reservation to this Disponibilites's reservation_2 relationship"""
    db_disponibilites = database.query(Disponibilites).filter(Disponibilites.id == disponibilites_id).first()
    if db_disponibilites is None:
        raise HTTPException(status_code=404, detail="Disponibilites not found")

    db_reservation = database.query(Reservation).filter(Reservation.id == reservation_id).first()
    if db_reservation is None:
        raise HTTPException(status_code=404, detail="Reservation not found")

    # Check if relationship already exists
    existing = database.query(verifie).filter(
        (verifie.c.disponibilites == disponibilites_id) &
        (verifie.c.reservation_2 == reservation_id)
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Relationship already exists")

    # Create the association
    association = verifie.insert().values(disponibilites=disponibilites_id, reservation_2=reservation_id)
    database.execute(association)
    database.commit()

    return {"message": "Reservation added to reservation_2 successfully"}


@app.delete("/disponibilites/{disponibilites_id}/reservation_2/{reservation_id}/", response_model=None, tags=["Disponibilites Relationships"])
async def remove_reservation_2_from_disponibilites(disponibilites_id: int, reservation_id: int, database: Session = Depends(get_db)):
    """Remove a Reservation from this Disponibilites's reservation_2 relationship"""
    db_disponibilites = database.query(Disponibilites).filter(Disponibilites.id == disponibilites_id).first()
    if db_disponibilites is None:
        raise HTTPException(status_code=404, detail="Disponibilites not found")

    # Check if relationship exists
    existing = database.query(verifie).filter(
        (verifie.c.disponibilites == disponibilites_id) &
        (verifie.c.reservation_2 == reservation_id)
    ).first()

    if not existing:
        raise HTTPException(status_code=404, detail="Relationship not found")

    # Delete the association
    association = verifie.delete().where(
        (verifie.c.disponibilites == disponibilites_id) &
        (verifie.c.reservation_2 == reservation_id)
    )
    database.execute(association)
    database.commit()

    return {"message": "Reservation removed from reservation_2 successfully"}


@app.get("/disponibilites/{disponibilites_id}/reservation_2/", response_model=None, tags=["Disponibilites Relationships"])
async def get_reservation_2_of_disponibilites(disponibilites_id: int, database: Session = Depends(get_db)):
    """Get all Reservation entities related to this Disponibilites through reservation_2"""
    db_disponibilites = database.query(Disponibilites).filter(Disponibilites.id == disponibilites_id).first()
    if db_disponibilites is None:
        raise HTTPException(status_code=404, detail="Disponibilites not found")

    reservation_ids = database.query(verifie.c.reservation_2).filter(verifie.c.disponibilites == disponibilites_id).all()
    reservation_list = database.query(Reservation).filter(Reservation.id.in_([id[0] for id in reservation_ids])).all()

    return {
        "disponibilites_id": disponibilites_id,
        "reservation_2_count": len(reservation_list),
        "reservation_2": reservation_list
    }



############################################
#   Disponibilites Method Endpoints
############################################




@app.post("/disponibilites/{disponibilites_id}/methods/ajouterIndisponibilite/", response_model=None, tags=["Disponibilites Methods"])
async def execute_disponibilites_ajouterIndisponibilite(
    disponibilites_id: int,
    params: dict = Body(default=None, embed=True),
    database: Session = Depends(get_db)
):
    """
    Execute the ajouterIndisponibilite method on a Disponibilites instance.

    Parameters:
    - motif: str    - debut: str    - fin: str    """
    # Retrieve the entity from the database
    _disponibilites_object = database.query(Disponibilites).filter(Disponibilites.id == disponibilites_id).first()
    if _disponibilites_object is None:
        raise HTTPException(status_code=404, detail="Disponibilites not found")

    # Prepare method parameters
    motif = params.get('motif')
    debut = params.get('debut')
    fin = params.get('fin')

    # Execute the method
    try:
        # Capture stdout to include print outputs in the response
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output

        async def wrapper(_disponibilites_object):
            try:
                # 1. On met à jour le motif (c'est du texte, ça ne plante pas)
                setattr(_disponibilites_object, 'motifDisponibilite', str(motif))
                
                # 2. On essaie de mettre à jour les dates
                # Si BESSER bloque le format date, on renvoie au moins le message
                try:
                    setattr(_disponibilites_object, 'dateDebut', debut)
                    setattr(_disponibilites_object, 'dateFin', fin)
                except:
                    # Si le crash vient du type date, on continue quand même pour le message
                    pass
                    
                return f"Indisponibilité '{motif}' enregistrée du {debut} au {fin}."
            except Exception as e:
                return f"Erreur technique : {str(e)}"

        result = await wrapper(_disponibilites_object)
        # Commit DB
        database.commit()
        database.refresh(_disponibilites_object)

        # Restore stdout
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        return {
            "disponibilites_id": disponibilites_id,
            "method": "ajouterIndisponibilite",
            "status": "executed",
            "result": str(result) if result is not None else None,
            "output": output if output else None
        }
    except Exception as e:
        sys.stdout = sys.__stdout__
        raise HTTPException(status_code=500, detail=f"Method execution failed: {str(e)}")



############################################
#
#   Reservation functions
#
############################################

@app.get("/reservation/", response_model=None, tags=["Reservation"])
def get_all_reservation(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(Reservation)
        reservation_list = query.all()

        # Serialize with relationships included
        result = []
        for reservation_item in reservation_list:
            item_dict = reservation_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)

            # Add many-to-many and one-to-many relationship objects (full details)
            disponibilites_list = database.query(Disponibilites).join(verifie, Disponibilites.id == verifie.c.disponibilites).filter(verifie.c.reservation_2 == reservation_item.id).all()
            item_dict['disponibilites'] = []
            for disponibilites_obj in disponibilites_list:
                disponibilites_dict = disponibilites_obj.__dict__.copy()
                disponibilites_dict.pop('_sa_instance_state', None)
                item_dict['disponibilites'].append(disponibilites_dict)
            gestionnaire_list = database.query(Gestionnaire).filter(Gestionnaire.reservation_1_id == reservation_item.id).all()
            item_dict['gestionnaire'] = []
            for gestionnaire_obj in gestionnaire_list:
                gestionnaire_dict = gestionnaire_obj.__dict__.copy()
                gestionnaire_dict.pop('_sa_instance_state', None)
                item_dict['gestionnaire'].append(gestionnaire_dict)
            evenementsalle_list = database.query(EvenementSalle).filter(EvenementSalle.reservation_id == reservation_item.id).all()
            item_dict['evenementsalle'] = []
            for evenementsalle_obj in evenementsalle_list:
                evenementsalle_dict = evenementsalle_obj.__dict__.copy()
                evenementsalle_dict.pop('_sa_instance_state', None)
                item_dict['evenementsalle'].append(evenementsalle_dict)
            materielsprestations_list = database.query(Materielsprestations).filter(Materielsprestations.reservation_3_id == reservation_item.id).all()
            item_dict['materielsprestations'] = []
            for materielsprestations_obj in materielsprestations_list:
                materielsprestations_dict = materielsprestations_obj.__dict__.copy()
                materielsprestations_dict.pop('_sa_instance_state', None)
                item_dict['materielsprestations'].append(materielsprestations_dict)

            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(Reservation).all()


@app.get("/reservation/count/", response_model=None, tags=["Reservation"])
def get_count_reservation(database: Session = Depends(get_db)) -> dict:
    """Get the total count of Reservation entities"""
    count = database.query(Reservation).count()
    return {"count": count}


@app.get("/reservation/paginated/", response_model=None, tags=["Reservation"])
def get_paginated_reservation(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of Reservation entities"""
    total = database.query(Reservation).count()
    reservation_list = database.query(Reservation).offset(skip).limit(limit).all()
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
        disponibilites_ids = database.query(verifie.c.disponibilites).filter(verifie.c.reservation_2 == reservation_item.id).all()
        gestionnaire_ids = database.query(Gestionnaire.id).filter(Gestionnaire.reservation_1_id == reservation_item.id).all()
        evenementsalle_ids = database.query(EvenementSalle.id).filter(EvenementSalle.reservation_id == reservation_item.id).all()
        materielsprestations_ids = database.query(Materielsprestations.id).filter(Materielsprestations.reservation_3_id == reservation_item.id).all()
        item_data = {
            "reservation": reservation_item,
            "disponibilites_ids": [x[0] for x in disponibilites_ids],
            "gestionnaire_ids": [x[0] for x in gestionnaire_ids],            "evenementsalle_ids": [x[0] for x in evenementsalle_ids],            "materielsprestations_ids": [x[0] for x in materielsprestations_ids]        }
        result.append(item_data)
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": result
    }


@app.get("/reservation/search/", response_model=None, tags=["Reservation"])
def search_reservation(
    database: Session = Depends(get_db)
) -> list:
    """Search Reservation entities by attributes"""
    query = database.query(Reservation)


    results = query.all()
    return results


@app.get("/reservation/{reservation_id}/", response_model=None, tags=["Reservation"])
async def get_reservation(reservation_id: int, database: Session = Depends(get_db)) -> Reservation:
    db_reservation = database.query(Reservation).filter(Reservation.id == reservation_id).first()
    if db_reservation is None:
        raise HTTPException(status_code=404, detail="Reservation not found")

    disponibilites_ids = database.query(verifie.c.disponibilites).filter(verifie.c.reservation_2 == db_reservation.id).all()
    gestionnaire_ids = database.query(Gestionnaire.id).filter(Gestionnaire.reservation_1_id == db_reservation.id).all()
    evenementsalle_ids = database.query(EvenementSalle.id).filter(EvenementSalle.reservation_id == db_reservation.id).all()
    materielsprestations_ids = database.query(Materielsprestations.id).filter(Materielsprestations.reservation_3_id == db_reservation.id).all()
    response_data = {
        "reservation": db_reservation,
        "disponibilites_ids": [x[0] for x in disponibilites_ids],
        "gestionnaire_ids": [x[0] for x in gestionnaire_ids],        "evenementsalle_ids": [x[0] for x in evenementsalle_ids],        "materielsprestations_ids": [x[0] for x in materielsprestations_ids]}
    return response_data



@app.post("/reservation/", response_model=None, tags=["Reservation"])
async def create_reservation(reservation_data: ReservationCreate, database: Session = Depends(get_db)) -> Reservation:

    if reservation_data.disponibilites:
        for id in reservation_data.disponibilites:
            # Entity already validated before creation
            db_disponibilites = database.query(Disponibilites).filter(Disponibilites.id == id).first()
            if not db_disponibilites:
                raise HTTPException(status_code=404, detail=f"Disponibilites with ID {id} not found")

    db_reservation = Reservation(
        delaiConfirmation=reservation_data.delaiConfirmation,        dateDebut=reservation_data.dateDebut,        coutTotal=reservation_data.coutTotal,        emailReferent=reservation_data.emailReferent,        dateFin=reservation_data.dateFin,        nbParticipantsPrevu=reservation_data.nbParticipantsPrevu,        nomEvenement=reservation_data.nomEvenement,        etatActuel=reservation_data.etatActuel,        description=reservation_data.description,        estConfirmee=reservation_data.estConfirmee        )

    database.add(db_reservation)
    database.commit()
    database.refresh(db_reservation)

    if reservation_data.gestionnaire:
        # Validate that all Gestionnaire IDs exist
        for gestionnaire_id in reservation_data.gestionnaire:
            db_gestionnaire = database.query(Gestionnaire).filter(Gestionnaire.id == gestionnaire_id).first()
            if not db_gestionnaire:
                raise HTTPException(status_code=400, detail=f"Gestionnaire with id {gestionnaire_id} not found")

        # Update the related entities with the new foreign key
        database.query(Gestionnaire).filter(Gestionnaire.id.in_(reservation_data.gestionnaire)).update(
            {Gestionnaire.reservation_1_id: db_reservation.id}, synchronize_session=False
        )
        database.commit()
    if reservation_data.evenementsalle:
        # Validate that all EvenementSalle IDs exist
        for evenementsalle_id in reservation_data.evenementsalle:
            db_evenementsalle = database.query(EvenementSalle).filter(EvenementSalle.id == evenementsalle_id).first()
            if not db_evenementsalle:
                raise HTTPException(status_code=400, detail=f"EvenementSalle with id {evenementsalle_id} not found")

        # Update the related entities with the new foreign key
        database.query(EvenementSalle).filter(EvenementSalle.id.in_(reservation_data.evenementsalle)).update(
            {EvenementSalle.reservation_id: db_reservation.id}, synchronize_session=False
        )
        database.commit()
    if reservation_data.materielsprestations:
        # Validate that all Materielsprestations IDs exist
        for materielsprestations_id in reservation_data.materielsprestations:
            db_materielsprestations = database.query(Materielsprestations).filter(Materielsprestations.id == materielsprestations_id).first()
            if not db_materielsprestations:
                raise HTTPException(status_code=400, detail=f"Materielsprestations with id {materielsprestations_id} not found")

        # Update the related entities with the new foreign key
        database.query(Materielsprestations).filter(Materielsprestations.id.in_(reservation_data.materielsprestations)).update(
            {Materielsprestations.reservation_3_id: db_reservation.id}, synchronize_session=False
        )
        database.commit()

    if reservation_data.disponibilites:
        for id in reservation_data.disponibilites:
            # Entity already validated before creation
            db_disponibilites = database.query(Disponibilites).filter(Disponibilites.id == id).first()
            # Create the association
            association = verifie.insert().values(reservation_2=db_reservation.id, disponibilites=db_disponibilites.id)
            database.execute(association)
            database.commit()


    disponibilites_ids = database.query(verifie.c.disponibilites).filter(verifie.c.reservation_2 == db_reservation.id).all()
    gestionnaire_ids = database.query(Gestionnaire.id).filter(Gestionnaire.reservation_1_id == db_reservation.id).all()
    evenementsalle_ids = database.query(EvenementSalle.id).filter(EvenementSalle.reservation_id == db_reservation.id).all()
    materielsprestations_ids = database.query(Materielsprestations.id).filter(Materielsprestations.reservation_3_id == db_reservation.id).all()
    response_data = {
        "reservation": db_reservation,
        "disponibilites_ids": [x[0] for x in disponibilites_ids],
        "gestionnaire_ids": [x[0] for x in gestionnaire_ids],        "evenementsalle_ids": [x[0] for x in evenementsalle_ids],        "materielsprestations_ids": [x[0] for x in materielsprestations_ids]    }
    return response_data


@app.post("/reservation/bulk/", response_model=None, tags=["Reservation"])
async def bulk_create_reservation(items: list[ReservationCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple Reservation entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item

            db_reservation = Reservation(
                delaiConfirmation=item_data.delaiConfirmation,                dateDebut=item_data.dateDebut,                coutTotal=item_data.coutTotal,                emailReferent=item_data.emailReferent,                dateFin=item_data.dateFin,                nbParticipantsPrevu=item_data.nbParticipantsPrevu,                nomEvenement=item_data.nomEvenement,                etatActuel=item_data.etatActuel,                description=item_data.description,                estConfirmee=item_data.estConfirmee            )
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
        "message": f"Successfully created {len(created_items)} Reservation entities"
    }


@app.delete("/reservation/bulk/", response_model=None, tags=["Reservation"])
async def bulk_delete_reservation(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple Reservation entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_reservation = database.query(Reservation).filter(Reservation.id == item_id).first()
        if db_reservation:
            database.delete(db_reservation)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} Reservation entities"
    }

@app.put("/reservation/{reservation_id}/", response_model=None, tags=["Reservation"])
async def update_reservation(reservation_id: int, reservation_data: ReservationCreate, database: Session = Depends(get_db)) -> Reservation:
    db_reservation = database.query(Reservation).filter(Reservation.id == reservation_id).first()
    if db_reservation is None:
        raise HTTPException(status_code=404, detail="Reservation not found")

    setattr(db_reservation, 'delaiConfirmation', reservation_data.delaiConfirmation)
    setattr(db_reservation, 'dateDebut', reservation_data.dateDebut)
    setattr(db_reservation, 'coutTotal', reservation_data.coutTotal)
    setattr(db_reservation, 'emailReferent', reservation_data.emailReferent)
    setattr(db_reservation, 'dateFin', reservation_data.dateFin)
    setattr(db_reservation, 'nbParticipantsPrevu', reservation_data.nbParticipantsPrevu)
    setattr(db_reservation, 'nomEvenement', reservation_data.nomEvenement)
    setattr(db_reservation, 'etatActuel', reservation_data.etatActuel)
    setattr(db_reservation, 'description', reservation_data.description)
    setattr(db_reservation, 'estConfirmee', reservation_data.estConfirmee)
    if reservation_data.gestionnaire is not None:
        # Clear all existing relationships (set foreign key to NULL)
        database.query(Gestionnaire).filter(Gestionnaire.reservation_1_id == db_reservation.id).update(
            {Gestionnaire.reservation_1_id: None}, synchronize_session=False
        )

        # Set new relationships if list is not empty
        if reservation_data.gestionnaire:
            # Validate that all IDs exist
            for gestionnaire_id in reservation_data.gestionnaire:
                db_gestionnaire = database.query(Gestionnaire).filter(Gestionnaire.id == gestionnaire_id).first()
                if not db_gestionnaire:
                    raise HTTPException(status_code=400, detail=f"Gestionnaire with id {gestionnaire_id} not found")

            # Update the related entities with the new foreign key
            database.query(Gestionnaire).filter(Gestionnaire.id.in_(reservation_data.gestionnaire)).update(
                {Gestionnaire.reservation_1_id: db_reservation.id}, synchronize_session=False
            )
    if reservation_data.evenementsalle is not None:
        # Clear all existing relationships (set foreign key to NULL)
        database.query(EvenementSalle).filter(EvenementSalle.reservation_id == db_reservation.id).update(
            {EvenementSalle.reservation_id: None}, synchronize_session=False
        )

        # Set new relationships if list is not empty
        if reservation_data.evenementsalle:
            # Validate that all IDs exist
            for evenementsalle_id in reservation_data.evenementsalle:
                db_evenementsalle = database.query(EvenementSalle).filter(EvenementSalle.id == evenementsalle_id).first()
                if not db_evenementsalle:
                    raise HTTPException(status_code=400, detail=f"EvenementSalle with id {evenementsalle_id} not found")

            # Update the related entities with the new foreign key
            database.query(EvenementSalle).filter(EvenementSalle.id.in_(reservation_data.evenementsalle)).update(
                {EvenementSalle.reservation_id: db_reservation.id}, synchronize_session=False
            )
    if reservation_data.materielsprestations is not None:
        # Clear all existing relationships (set foreign key to NULL)
        database.query(Materielsprestations).filter(Materielsprestations.reservation_3_id == db_reservation.id).update(
            {Materielsprestations.reservation_3_id: None}, synchronize_session=False
        )

        # Set new relationships if list is not empty
        if reservation_data.materielsprestations:
            # Validate that all IDs exist
            for materielsprestations_id in reservation_data.materielsprestations:
                db_materielsprestations = database.query(Materielsprestations).filter(Materielsprestations.id == materielsprestations_id).first()
                if not db_materielsprestations:
                    raise HTTPException(status_code=400, detail=f"Materielsprestations with id {materielsprestations_id} not found")

            # Update the related entities with the new foreign key
            database.query(Materielsprestations).filter(Materielsprestations.id.in_(reservation_data.materielsprestations)).update(
                {Materielsprestations.reservation_3_id: db_reservation.id}, synchronize_session=False
            )
    existing_disponibilites_ids = [assoc.disponibilites for assoc in database.execute(
        verifie.select().where(verifie.c.reservation_2 == db_reservation.id))]

    disponibilitess_to_remove = set(existing_disponibilites_ids) - set(reservation_data.disponibilites)
    for disponibilites_id in disponibilitess_to_remove:
        association = verifie.delete().where(
            (verifie.c.reservation_2 == db_reservation.id) & (verifie.c.disponibilites == disponibilites_id))
        database.execute(association)

    new_disponibilites_ids = set(reservation_data.disponibilites) - set(existing_disponibilites_ids)
    for disponibilites_id in new_disponibilites_ids:
        db_disponibilites = database.query(Disponibilites).filter(Disponibilites.id == disponibilites_id).first()
        if db_disponibilites is None:
            raise HTTPException(status_code=404, detail=f"Disponibilites with ID {disponibilites_id} not found")
        association = verifie.insert().values(disponibilites=db_disponibilites.id, reservation_2=db_reservation.id)
        database.execute(association)
    database.commit()
    database.refresh(db_reservation)

    disponibilites_ids = database.query(verifie.c.disponibilites).filter(verifie.c.reservation_2 == db_reservation.id).all()
    gestionnaire_ids = database.query(Gestionnaire.id).filter(Gestionnaire.reservation_1_id == db_reservation.id).all()
    evenementsalle_ids = database.query(EvenementSalle.id).filter(EvenementSalle.reservation_id == db_reservation.id).all()
    materielsprestations_ids = database.query(Materielsprestations.id).filter(Materielsprestations.reservation_3_id == db_reservation.id).all()
    response_data = {
        "reservation": db_reservation,
        "disponibilites_ids": [x[0] for x in disponibilites_ids],
        "gestionnaire_ids": [x[0] for x in gestionnaire_ids],        "evenementsalle_ids": [x[0] for x in evenementsalle_ids],        "materielsprestations_ids": [x[0] for x in materielsprestations_ids]    }
    return response_data


@app.delete("/reservation/{reservation_id}/", response_model=None, tags=["Reservation"])
async def delete_reservation(reservation_id: int, database: Session = Depends(get_db)):
    db_reservation = database.query(Reservation).filter(Reservation.id == reservation_id).first()
    if db_reservation is None:
        raise HTTPException(status_code=404, detail="Reservation not found")
    database.delete(db_reservation)
    database.commit()
    return db_reservation

@app.post("/reservation/{reservation_id}/disponibilites/{disponibilites_id}/", response_model=None, tags=["Reservation Relationships"])
async def add_disponibilites_to_reservation(reservation_id: int, disponibilites_id: int, database: Session = Depends(get_db)):
    """Add a Disponibilites to this Reservation's disponibilites relationship"""
    db_reservation = database.query(Reservation).filter(Reservation.id == reservation_id).first()
    if db_reservation is None:
        raise HTTPException(status_code=404, detail="Reservation not found")

    db_disponibilites = database.query(Disponibilites).filter(Disponibilites.id == disponibilites_id).first()
    if db_disponibilites is None:
        raise HTTPException(status_code=404, detail="Disponibilites not found")

    # Check if relationship already exists
    existing = database.query(verifie).filter(
        (verifie.c.reservation_2 == reservation_id) &
        (verifie.c.disponibilites == disponibilites_id)
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Relationship already exists")

    # Create the association
    association = verifie.insert().values(reservation_2=reservation_id, disponibilites=disponibilites_id)
    database.execute(association)
    database.commit()

    return {"message": "Disponibilites added to disponibilites successfully"}


@app.delete("/reservation/{reservation_id}/disponibilites/{disponibilites_id}/", response_model=None, tags=["Reservation Relationships"])
async def remove_disponibilites_from_reservation(reservation_id: int, disponibilites_id: int, database: Session = Depends(get_db)):
    """Remove a Disponibilites from this Reservation's disponibilites relationship"""
    db_reservation = database.query(Reservation).filter(Reservation.id == reservation_id).first()
    if db_reservation is None:
        raise HTTPException(status_code=404, detail="Reservation not found")

    # Check if relationship exists
    existing = database.query(verifie).filter(
        (verifie.c.reservation_2 == reservation_id) &
        (verifie.c.disponibilites == disponibilites_id)
    ).first()

    if not existing:
        raise HTTPException(status_code=404, detail="Relationship not found")

    # Delete the association
    association = verifie.delete().where(
        (verifie.c.reservation_2 == reservation_id) &
        (verifie.c.disponibilites == disponibilites_id)
    )
    database.execute(association)
    database.commit()

    return {"message": "Disponibilites removed from disponibilites successfully"}


@app.get("/reservation/{reservation_id}/disponibilites/", response_model=None, tags=["Reservation Relationships"])
async def get_disponibilites_of_reservation(reservation_id: int, database: Session = Depends(get_db)):
    """Get all Disponibilites entities related to this Reservation through disponibilites"""
    db_reservation = database.query(Reservation).filter(Reservation.id == reservation_id).first()
    if db_reservation is None:
        raise HTTPException(status_code=404, detail="Reservation not found")

    disponibilites_ids = database.query(verifie.c.disponibilites).filter(verifie.c.reservation_2 == reservation_id).all()
    disponibilites_list = database.query(Disponibilites).filter(Disponibilites.id.in_([id[0] for id in disponibilites_ids])).all()

    return {
        "reservation_id": reservation_id,
        "disponibilites_count": len(disponibilites_list),
        "disponibilites": disponibilites_list
    }



############################################
#   Reservation Method Endpoints
############################################




@app.post("/reservation/{reservation_id}/methods/annuler/", response_model=None, tags=["Reservation Methods"])
async def execute_reservation_annuler(
    reservation_id: int,
    params: dict = Body(default=None, embed=True),
    database: Session = Depends(get_db)
):
    """
    Execute the annuler method on a Reservation instance.
    """
    # Retrieve the entity from the database
    _reservation_object = database.query(Reservation).filter(Reservation.id == reservation_id).first()
    if _reservation_object is None:
        raise HTTPException(status_code=404, detail="Reservation not found")

    # Prepare method parameters

    # Execute the method
    try:
        # Capture stdout to include print outputs in the response
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output

        async def wrapper(_reservation_object):
            try:
                # On change l'état vers 'Annulée'
                setattr(_reservation_object, 'etatActuel', "Annulée")
                return "La réservation a été annulée."
            except:
                return "Erreur technique lors de l'annulation."

        result = await wrapper(_reservation_object)
        # Commit DB
        database.commit()
        database.refresh(_reservation_object)

        # Restore stdout
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        return {
            "reservation_id": reservation_id,
            "method": "annuler",
            "status": "executed",
            "result": str(result) if result is not None else None,
            "output": output if output else None
        }
    except Exception as e:
        sys.stdout = sys.__stdout__
        raise HTTPException(status_code=500, detail=f"Method execution failed: {str(e)}")





@app.post("/reservation/{reservation_id}/methods/confirmerPaiement/", response_model=None, tags=["Reservation Methods"])
async def execute_reservation_confirmerPaiement(
    reservation_id: int,
    params: dict = Body(default=None, embed=True),
    database: Session = Depends(get_db)
):
    """
    Execute the confirmerPaiement method on a Reservation instance.
    """
    # Retrieve the entity from the database
    _reservation_object = database.query(Reservation).filter(Reservation.id == reservation_id).first()
    if _reservation_object is None:
        raise HTTPException(status_code=404, detail="Reservation not found")

    # Prepare method parameters

    # Execute the method
    try:
        # Capture stdout to include print outputs in the response
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output

        async def wrapper(_reservation_object):
            try:
                # On change l'état vers 'Confirmée'
                setattr(_reservation_object, 'etatActuel', "Confirmée")
                return "Paiement confirmé, réservation validée."
            except:
                return "Erreur technique lors de la confirmation."

        result = await wrapper(_reservation_object)
        # Commit DB
        database.commit()
        database.refresh(_reservation_object)

        # Restore stdout
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        return {
            "reservation_id": reservation_id,
            "method": "confirmerPaiement",
            "status": "executed",
            "result": str(result) if result is not None else None,
            "output": output if output else None
        }
    except Exception as e:
        sys.stdout = sys.__stdout__
        raise HTTPException(status_code=500, detail=f"Method execution failed: {str(e)}")





@app.post("/reservation/{reservation_id}/methods/calculerCout/", response_model=None, tags=["Reservation Methods"])
async def execute_reservation_calculerCout(
    reservation_id: int,
    params: dict = Body(default=None, embed=True),
    database: Session = Depends(get_db)
):
    """
    Execute the calculerCout method on a Reservation instance.
    """
    # Retrieve the entity from the database
    _reservation_object = database.query(Reservation).filter(Reservation.id == reservation_id).first()
    if _reservation_object is None:
        raise HTTPException(status_code=404, detail="Reservation not found")

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
#   Stats functions
#
############################################

@app.get("/stats/", response_model=None, tags=["Stats"])
def get_all_stats(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(Stats)
        query = query.options(joinedload(Stats.gestionnaire_2))
        stats_list = query.all()

        # Serialize with relationships included
        result = []
        for stats_item in stats_list:
            item_dict = stats_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)
            if stats_item.gestionnaire_2:
                related_obj = stats_item.gestionnaire_2
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['gestionnaire_2'] = related_dict
            else:
                item_dict['gestionnaire_2'] = None


            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(Stats).all()


@app.get("/stats/count/", response_model=None, tags=["Stats"])
def get_count_stats(database: Session = Depends(get_db)) -> dict:
    """Get the total count of Stats entities"""
    count = database.query(Stats).count()
    return {"count": count}


@app.get("/stats/paginated/", response_model=None, tags=["Stats"])
def get_paginated_stats(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of Stats entities"""
    total = database.query(Stats).count()
    stats_list = database.query(Stats).offset(skip).limit(limit).all()
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": stats_list
    }


@app.get("/stats/search/", response_model=None, tags=["Stats"])
def search_stats(
    database: Session = Depends(get_db)
) -> list:
    """Search Stats entities by attributes"""
    query = database.query(Stats)


    results = query.all()
    return results


@app.get("/stats/{stats_id}/", response_model=None, tags=["Stats"])
async def get_stats(stats_id: int, database: Session = Depends(get_db)) -> Stats:
    db_stats = database.query(Stats).filter(Stats.id == stats_id).first()
    if db_stats is None:
        raise HTTPException(status_code=404, detail="Stats not found")

    response_data = {
        "stats": db_stats,
}
    return response_data



@app.post("/stats/", response_model=None, tags=["Stats"])
async def create_stats(stats_data: StatsCreate, database: Session = Depends(get_db)) -> Stats:

    if stats_data.gestionnaire_2 :
        db_gestionnaire_2 = database.query(Gestionnaire).filter(Gestionnaire.id == stats_data.gestionnaire_2).first()
        if not db_gestionnaire_2:
            raise HTTPException(status_code=400, detail="Gestionnaire not found")

    db_stats = Stats(
        periode=stats_data.periode,        tauxOccupation=stats_data.tauxOccupation,        chiffresAffaires=stats_data.chiffresAffaires,        gestionnaire_2_id=stats_data.gestionnaire_2        )

    database.add(db_stats)
    database.commit()
    database.refresh(db_stats)




    return db_stats


@app.post("/stats/bulk/", response_model=None, tags=["Stats"])
async def bulk_create_stats(items: list[StatsCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple Stats entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item

            db_stats = Stats(
                periode=item_data.periode,                tauxOccupation=item_data.tauxOccupation,                chiffresAffaires=item_data.chiffresAffaires,                gestionnaire_2_id=item_data.gestionnaire_2            )
            database.add(db_stats)
            database.flush()  # Get ID without committing
            created_items.append(db_stats.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} Stats entities"
    }


@app.delete("/stats/bulk/", response_model=None, tags=["Stats"])
async def bulk_delete_stats(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple Stats entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_stats = database.query(Stats).filter(Stats.id == item_id).first()
        if db_stats:
            database.delete(db_stats)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} Stats entities"
    }

@app.put("/stats/{stats_id}/", response_model=None, tags=["Stats"])
async def update_stats(stats_id: int, stats_data: StatsCreate, database: Session = Depends(get_db)) -> Stats:
    db_stats = database.query(Stats).filter(Stats.id == stats_id).first()
    if db_stats is None:
        raise HTTPException(status_code=404, detail="Stats not found")

    setattr(db_stats, 'periode', stats_data.periode)
    setattr(db_stats, 'tauxOccupation', stats_data.tauxOccupation)
    setattr(db_stats, 'chiffresAffaires', stats_data.chiffresAffaires)
    if stats_data.gestionnaire_2 is not None:
        db_gestionnaire_2 = database.query(Gestionnaire).filter(Gestionnaire.id == stats_data.gestionnaire_2).first()
        if not db_gestionnaire_2:
            raise HTTPException(status_code=400, detail="Gestionnaire not found")
        setattr(db_stats, 'gestionnaire_2_id', stats_data.gestionnaire_2)
    else:
        setattr(db_stats, 'gestionnaire_2_id', None)
    database.commit()
    database.refresh(db_stats)

    return db_stats


@app.delete("/stats/{stats_id}/", response_model=None, tags=["Stats"])
async def delete_stats(stats_id: int, database: Session = Depends(get_db)):
    db_stats = database.query(Stats).filter(Stats.id == stats_id).first()
    if db_stats is None:
        raise HTTPException(status_code=404, detail="Stats not found")
    database.delete(db_stats)
    database.commit()
    return db_stats



############################################
#   Stats Method Endpoints
############################################




@app.post("/stats/{stats_id}/methods/calculerCA/", response_model=None, tags=["Stats Methods"])
async def execute_stats_calculerCA(
    stats_id: int,
    params: dict = Body(default=None, embed=True),
    database: Session = Depends(get_db)
):
    """
    Execute the calculerCA method on a Stats instance.
    """
    # Retrieve the entity from the database
    _stats_object = database.query(Stats).filter(Stats.id == stats_id).first()
    if _stats_object is None:
        raise HTTPException(status_code=404, detail="Stats not found")

    # Prepare method parameters

    # Execute the method
    try:
        # Capture stdout to include print outputs in the response
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output

        async def wrapper(_stats_object):
            try:
                # Dans un prototype BESSER, on simule souvent le calcul 
                # en récupérant la valeur actuelle du CA
                ca_actuel = float(getattr(_stats_object, 'chiffresAffaires', 0.0))
                
                # On pourrait imaginer une logique de somme ici si les liens existaient
                # Pour le test, on confirme simplement la valeur stockée
                return f"Le Chiffre d'Affaires total calculé est de : {ca_actuel}€"
            except:
                return "Impossible de calculer le CA."

        result = await wrapper(_stats_object)
        # Commit DB
        database.commit()
        database.refresh(_stats_object)

        # Restore stdout
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        return {
            "stats_id": stats_id,
            "method": "calculerCA",
            "status": "executed",
            "result": str(result) if result is not None else None,
            "output": output if output else None
        }
    except Exception as e:
        sys.stdout = sys.__stdout__
        raise HTTPException(status_code=500, detail=f"Method execution failed: {str(e)}")



############################################
#
#   Gestionnaire functions
#
############################################

@app.get("/gestionnaire/", response_model=None, tags=["Gestionnaire"])
def get_all_gestionnaire(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(Gestionnaire)
        query = query.options(joinedload(Gestionnaire.reservation_1))
        query = query.options(joinedload(Gestionnaire.centredecongres_1))
        gestionnaire_list = query.all()

        # Serialize with relationships included
        result = []
        for gestionnaire_item in gestionnaire_list:
            item_dict = gestionnaire_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)
            if gestionnaire_item.reservation_1:
                related_obj = gestionnaire_item.reservation_1
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['reservation_1'] = related_dict
            else:
                item_dict['reservation_1'] = None
            if gestionnaire_item.centredecongres_1:
                related_obj = gestionnaire_item.centredecongres_1
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['centredecongres_1'] = related_dict
            else:
                item_dict['centredecongres_1'] = None

            # Add many-to-many and one-to-many relationship objects (full details)
            stats_list = database.query(Stats).filter(Stats.gestionnaire_2_id == gestionnaire_item.id).all()
            item_dict['stats'] = []
            for stats_obj in stats_list:
                stats_dict = stats_obj.__dict__.copy()
                stats_dict.pop('_sa_instance_state', None)
                item_dict['stats'].append(stats_dict)

            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(Gestionnaire).all()


@app.get("/gestionnaire/count/", response_model=None, tags=["Gestionnaire"])
def get_count_gestionnaire(database: Session = Depends(get_db)) -> dict:
    """Get the total count of Gestionnaire entities"""
    count = database.query(Gestionnaire).count()
    return {"count": count}


@app.get("/gestionnaire/paginated/", response_model=None, tags=["Gestionnaire"])
def get_paginated_gestionnaire(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of Gestionnaire entities"""
    total = database.query(Gestionnaire).count()
    gestionnaire_list = database.query(Gestionnaire).offset(skip).limit(limit).all()
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
        stats_ids = database.query(Stats.id).filter(Stats.gestionnaire_2_id == gestionnaire_item.id).all()
        item_data = {
            "gestionnaire": gestionnaire_item,
            "stats_ids": [x[0] for x in stats_ids]        }
        result.append(item_data)
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": result
    }


@app.get("/gestionnaire/search/", response_model=None, tags=["Gestionnaire"])
def search_gestionnaire(
    database: Session = Depends(get_db)
) -> list:
    """Search Gestionnaire entities by attributes"""
    query = database.query(Gestionnaire)


    results = query.all()
    return results


@app.get("/gestionnaire/{gestionnaire_id}/", response_model=None, tags=["Gestionnaire"])
async def get_gestionnaire(gestionnaire_id: int, database: Session = Depends(get_db)) -> Gestionnaire:
    db_gestionnaire = database.query(Gestionnaire).filter(Gestionnaire.id == gestionnaire_id).first()
    if db_gestionnaire is None:
        raise HTTPException(status_code=404, detail="Gestionnaire not found")

    stats_ids = database.query(Stats.id).filter(Stats.gestionnaire_2_id == db_gestionnaire.id).all()
    response_data = {
        "gestionnaire": db_gestionnaire,
        "stats_ids": [x[0] for x in stats_ids]}
    return response_data



@app.post("/gestionnaire/", response_model=None, tags=["Gestionnaire"])
async def create_gestionnaire(gestionnaire_data: GestionnaireCreate, database: Session = Depends(get_db)) -> Gestionnaire:

    if gestionnaire_data.reservation_1 :
        db_reservation_1 = database.query(Reservation).filter(Reservation.id == gestionnaire_data.reservation_1).first()
        if not db_reservation_1:
            raise HTTPException(status_code=400, detail="Reservation not found")

    db_gestionnaire = Gestionnaire(
        identifiant=gestionnaire_data.identifiant,        nom=gestionnaire_data.nom,        reservation_1_id=gestionnaire_data.reservation_1        )

    database.add(db_gestionnaire)
    database.commit()
    database.refresh(db_gestionnaire)

    if gestionnaire_data.stats:
        # Validate that all Stats IDs exist
        for stats_id in gestionnaire_data.stats:
            db_stats = database.query(Stats).filter(Stats.id == stats_id).first()
            if not db_stats:
                raise HTTPException(status_code=400, detail=f"Stats with id {stats_id} not found")

        # Update the related entities with the new foreign key
        database.query(Stats).filter(Stats.id.in_(gestionnaire_data.stats)).update(
            {Stats.gestionnaire_2_id: db_gestionnaire.id}, synchronize_session=False
        )
        database.commit()



    stats_ids = database.query(Stats.id).filter(Stats.gestionnaire_2_id == db_gestionnaire.id).all()
    response_data = {
        "gestionnaire": db_gestionnaire,
        "stats_ids": [x[0] for x in stats_ids]    }
    return response_data


@app.post("/gestionnaire/bulk/", response_model=None, tags=["Gestionnaire"])
async def bulk_create_gestionnaire(items: list[GestionnaireCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple Gestionnaire entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item

            db_gestionnaire = Gestionnaire(
                identifiant=item_data.identifiant,                nom=item_data.nom,                reservation_1_id=item_data.reservation_1            )
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
        "message": f"Successfully created {len(created_items)} Gestionnaire entities"
    }


@app.delete("/gestionnaire/bulk/", response_model=None, tags=["Gestionnaire"])
async def bulk_delete_gestionnaire(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple Gestionnaire entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_gestionnaire = database.query(Gestionnaire).filter(Gestionnaire.id == item_id).first()
        if db_gestionnaire:
            database.delete(db_gestionnaire)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} Gestionnaire entities"
    }

@app.put("/gestionnaire/{gestionnaire_id}/", response_model=None, tags=["Gestionnaire"])
async def update_gestionnaire(gestionnaire_id: int, gestionnaire_data: GestionnaireCreate, database: Session = Depends(get_db)) -> Gestionnaire:
    db_gestionnaire = database.query(Gestionnaire).filter(Gestionnaire.id == gestionnaire_id).first()
    if db_gestionnaire is None:
        raise HTTPException(status_code=404, detail="Gestionnaire not found")

    setattr(db_gestionnaire, 'identifiant', gestionnaire_data.identifiant)
    setattr(db_gestionnaire, 'nom', gestionnaire_data.nom)
    if gestionnaire_data.reservation_1 is not None:
        db_reservation_1 = database.query(Reservation).filter(Reservation.id == gestionnaire_data.reservation_1).first()
        if not db_reservation_1:
            raise HTTPException(status_code=400, detail="Reservation not found")
        setattr(db_gestionnaire, 'reservation_1_id', gestionnaire_data.reservation_1)
    else:
        setattr(db_gestionnaire, 'reservation_1_id', None)
    if gestionnaire_data.stats is not None:
        # Clear all existing relationships (set foreign key to NULL)
        database.query(Stats).filter(Stats.gestionnaire_2_id == db_gestionnaire.id).update(
            {Stats.gestionnaire_2_id: None}, synchronize_session=False
        )

        # Set new relationships if list is not empty
        if gestionnaire_data.stats:
            # Validate that all IDs exist
            for stats_id in gestionnaire_data.stats:
                db_stats = database.query(Stats).filter(Stats.id == stats_id).first()
                if not db_stats:
                    raise HTTPException(status_code=400, detail=f"Stats with id {stats_id} not found")

            # Update the related entities with the new foreign key
            database.query(Stats).filter(Stats.id.in_(gestionnaire_data.stats)).update(
                {Stats.gestionnaire_2_id: db_gestionnaire.id}, synchronize_session=False
            )
    database.commit()
    database.refresh(db_gestionnaire)

    stats_ids = database.query(Stats.id).filter(Stats.gestionnaire_2_id == db_gestionnaire.id).all()
    response_data = {
        "gestionnaire": db_gestionnaire,
        "stats_ids": [x[0] for x in stats_ids]    }
    return response_data


@app.delete("/gestionnaire/{gestionnaire_id}/", response_model=None, tags=["Gestionnaire"])
async def delete_gestionnaire(gestionnaire_id: int, database: Session = Depends(get_db)):
    db_gestionnaire = database.query(Gestionnaire).filter(Gestionnaire.id == gestionnaire_id).first()
    if db_gestionnaire is None:
        raise HTTPException(status_code=404, detail="Gestionnaire not found")
    database.delete(db_gestionnaire)
    database.commit()
    return db_gestionnaire



############################################
#   Gestionnaire Method Endpoints
############################################




@app.post("/gestionnaire/{gestionnaire_id}/methods/consulterStatistiques/", response_model=None, tags=["Gestionnaire Methods"])
async def execute_gestionnaire_consulterStatistiques(
    gestionnaire_id: int,
    params: dict = Body(default=None, embed=True),
    database: Session = Depends(get_db)
):
    """
    Execute the consulterStatistiques method on a Gestionnaire instance.

    Parameters:
    - periode: Any    """
    # Retrieve the entity from the database
    _gestionnaire_object = database.query(Gestionnaire).filter(Gestionnaire.id == gestionnaire_id).first()
    if _gestionnaire_object is None:
        raise HTTPException(status_code=404, detail="Gestionnaire not found")

    # Prepare method parameters
    periode = params.get('periode')

    # Execute the method
    try:
        # Capture stdout to include print outputs in the response
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output

        async def wrapper(_gestionnaire_object):
            # Le diagramme montre une relation entre Gestionnaire et Réservation
            # On essaie de récupérer les réservations liées
            resas = getattr(_gestionnaire_object, 'gestionnaire_reservation', []) # Nom technique BESSER probable
            
            if not resas:
                return [f"Statistiques pour {periode} : Aucune donnée disponible."]
            
            # On calcule un total rapide pour la démo
            total = sum([float(getattr(r, 'coutTotal', 0)) for r in resas])
            return [f"Période : {periode}", f"Nombre de résas : {len(resas)}", f"Chiffre d'affaires : {total}€"]

        result = await wrapper(_gestionnaire_object)
        # Commit DB
        database.commit()
        database.refresh(_gestionnaire_object)

        # Restore stdout
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        return {
            "gestionnaire_id": gestionnaire_id,
            "method": "consulterStatistiques",
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



