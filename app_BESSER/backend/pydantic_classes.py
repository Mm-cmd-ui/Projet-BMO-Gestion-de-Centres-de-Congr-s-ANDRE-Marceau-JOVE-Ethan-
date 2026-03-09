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
class CentredeCongresCreate(BaseModel):
    adresse: str
    nom: str
    gestionnaire_1: Optional[List[int]] = None  # 1:N Relationship
    evenementsalle_1: Optional[List[int]] = None  # 1:N Relationship


class TarifsCreate(BaseModel):
    saison: str
    montantBase: float
    materielsprestations_1: List[int]  # N:M Relationship
    reservation_4: List[int]  # N:M Relationship
    evenementsalle_2: List[int]  # N:M Relationship


class EvenementSalleCreate(BaseModel):
    nom: str
    capaciteMax: int
    typeElement: str
    tarifs: List[int]  # N:M Relationship
    reservation: Optional[int] = None  # N:1 Relationship (optional)
    centredecongres: Optional[int] = None  # N:1 Relationship (optional)


class MaterielsprestationsCreate(BaseModel):
    quantiteMax: int
    type: str
    nom: str
    prixUnitaire: float
    reservation_3: List[int]  # N:M Relationship
    tarifs_1: List[int]  # N:M Relationship


class DisponibilitesCreate(BaseModel):
    dateDebut: date
    dureeMinim: int
    dateFin: date
    motifDisponibilite: str
    reservation_2: List[int]  # N:M Relationship


class ReservationCreate(BaseModel):
    dateDebut: datetime
    coutTotal: float
    nomEvenement: str
    estConfirmee: bool
    nbParticipantsPrevu: int
    etatActuel: str
    emailReferent: str
    dateFin: datetime
    description: str
    delaiConfirmation: datetime
    gestionnaire: Optional[List[int]] = None  # 1:N Relationship
    evenementsalle: Optional[List[int]] = None  # 1:N Relationship
    materielsprestations: List[int]  # N:M Relationship
    tarifs_2: List[int]  # N:M Relationship
    disponibilites: List[int]  # N:M Relationship


class StatsCreate(BaseModel):
    chiffresAffaires: float
    periode: str
    tauxOccupation: float
    gestionnaire_2: Optional[int] = None  # N:1 Relationship (optional)


class GestionnaireCreate(BaseModel):
    identifiant: str
    nom: str
    centredecongres_1: Optional[int] = None  # N:1 Relationship (optional)
    reservation_1: Optional[int] = None  # N:1 Relationship (optional)
    stats: Optional[List[int]] = None  # 1:N Relationship


