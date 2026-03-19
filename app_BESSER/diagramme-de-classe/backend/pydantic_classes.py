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
    nom: str
    adresse: str
    gestionnaire_1: int  # 1:1 Relationship (mandatory)
    evenementsalle_1: Optional[List[int]] = None  # 1:N Relationship


class TarifsCreate(BaseModel):
    saison: str
    montantBase: float
    evenementsalle_2: List[int]  # N:M Relationship
    materielsprestations_1: List[int]  # N:M Relationship


class EvenementSalleCreate(BaseModel):
    typeElement: str
    nom: str
    capaciteMax: int
    reservation: Optional[int] = None  # N:1 Relationship (optional)
    centredecongres: Optional[int] = None  # N:1 Relationship (optional)
    tarifs: List[int]  # N:M Relationship


class MaterielsprestationsCreate(BaseModel):
    prixUnitaire: float
    type: str
    nom: str
    quantiteMax: int
    reservation_3: int  # N:1 Relationship (mandatory)
    tarifs_1: List[int]  # N:M Relationship


class DisponibilitesCreate(BaseModel):
    dateFin: date
    dateDebut: date
    motifDisponibilite: str
    dureeMinim: int
    reservation_2: List[int]  # N:M Relationship


class ReservationCreate(BaseModel):
    delaiConfirmation: datetime
    dateDebut: datetime
    coutTotal: float
    emailReferent: str
    dateFin: datetime
    nbParticipantsPrevu: int
    nomEvenement: str
    etatActuel: str
    description: str
    estConfirmee: bool
    gestionnaire: Optional[List[int]] = None  # 1:N Relationship
    evenementsalle: Optional[List[int]] = None  # 1:N Relationship
    disponibilites: List[int]  # N:M Relationship
    materielsprestations: Optional[List[int]] = None  # 1:N Relationship


class StatsCreate(BaseModel):
    periode: str
    tauxOccupation: float
    chiffresAffaires: float
    gestionnaire_2: Optional[int] = None  # N:1 Relationship (optional)


class GestionnaireCreate(BaseModel):
    identifiant: str
    nom: str
    reservation_1: Optional[int] = None  # N:1 Relationship (optional)
    stats: Optional[List[int]] = None  # 1:N Relationship
    centredecongres_1: Optional[int] = None  # 1:1 Relationship (optional)


