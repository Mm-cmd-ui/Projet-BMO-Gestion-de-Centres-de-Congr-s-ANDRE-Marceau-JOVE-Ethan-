from datetime import datetime, date, time
from typing import Any, List, Optional, Union, Set
from enum import Enum
from pydantic import BaseModel, field_validator


############################################
# Enumerations are defined here
############################################

############################################
# Classes are defined here
############################################
class Evenement_SalleCreate(BaseModel):
    typeElement: str
    capaciteMax: int
    nom: str
    reservation_1: Optional[int] = None  # N:1 Relationship (optional)


class reservationCreate(BaseModel):
    description: str
    delaiConfirmation: datetime
    nomEvenement: str
    nbParticipantsPrevu: int
    dateFin: datetime
    etatActuel: str
    dateDebut: datetime
    estConfirmee: bool
    coutTotal: float
    gestionnaire: Optional[int] = None  # N:1 Relationship (optional)
    evenement_salle: Optional[List[int]] = None  # 1:N Relationship


class gestionnaireCreate(BaseModel):
    identitfiant: str
    nom: str
    reservation: Optional[List[int]] = None  # 1:N Relationship


