import enum
from typing import List, Optional
from sqlalchemy import (
    create_engine, Column, ForeignKey, Table, Text, Boolean, String, Date, 
    Time, DateTime, Float, Integer, Enum
)
from sqlalchemy.orm import (
    column_property, DeclarativeBase, Mapped, mapped_column, relationship
)
from datetime import datetime as dt_datetime, time as dt_time, date as dt_date

class Base(DeclarativeBase):
    pass



# Tables definition for many-to-many relationships
verifie = Table(
    "verifie",
    Base.metadata,
    Column("reservation_2", ForeignKey("reservation.id"), primary_key=True),
    Column("disponibilites", ForeignKey("disponibilites.id"), primary_key=True),
)
applique = Table(
    "applique",
    Base.metadata,
    Column("tarifs", ForeignKey("tarifs.id"), primary_key=True),
    Column("evenementsalle_2", ForeignKey("evenementsalle.id"), primary_key=True),
)
applique_1 = Table(
    "applique_1",
    Base.metadata,
    Column("materielsprestations_1", ForeignKey("materielsprestations.id"), primary_key=True),
    Column("tarifs_1", ForeignKey("tarifs.id"), primary_key=True),
)

# Tables definition
class CentredeCongres(Base):
    __tablename__ = "centredecongres"
    id: Mapped[int] = mapped_column(primary_key=True)
    nom: Mapped[str] = mapped_column(String(100))
    adresse: Mapped[str] = mapped_column(String(100))
    gestionnaire_1_id: Mapped[int] = mapped_column(ForeignKey("gestionnaire.id"), unique=True)

class Tarifs(Base):
    __tablename__ = "tarifs"
    id: Mapped[int] = mapped_column(primary_key=True)
    saison: Mapped[str] = mapped_column(String(100))
    montantBase: Mapped[float] = mapped_column(Float)

class EvenementSalle(Base):
    __tablename__ = "evenementsalle"
    id: Mapped[int] = mapped_column(primary_key=True)
    nom: Mapped[str] = mapped_column(String(100))
    capaciteMax: Mapped[int] = mapped_column(Integer)
    typeElement: Mapped[str] = mapped_column(String(100))
    centredecongres_id: Mapped[int] = mapped_column(ForeignKey("centredecongres.id"), nullable=True)
    reservation_id: Mapped[int] = mapped_column(ForeignKey("reservation.id"), nullable=True)

class Materielsprestations(Base):
    __tablename__ = "materielsprestations"
    id: Mapped[int] = mapped_column(primary_key=True)
    nom: Mapped[str] = mapped_column(String(100))
    type: Mapped[str] = mapped_column(String(100))
    quantiteMax: Mapped[int] = mapped_column(Integer)
    prixUnitaire: Mapped[float] = mapped_column(Float)
    reservation_3_id: Mapped[int] = mapped_column(ForeignKey("reservation.id"))

class Disponibilites(Base):
    __tablename__ = "disponibilites"
    id: Mapped[int] = mapped_column(primary_key=True)
    motifDisponibilite: Mapped[str] = mapped_column(String(100))
    dateDebut: Mapped[dt_date] = mapped_column(Date)
    dateFin: Mapped[dt_date] = mapped_column(Date)
    dureeMinim: Mapped[int] = mapped_column(Integer)

class Reservation(Base):
    __tablename__ = "reservation"
    id: Mapped[int] = mapped_column(primary_key=True)
    delaiConfirmation: Mapped[dt_datetime] = mapped_column(DateTime)
    etatActuel: Mapped[str] = mapped_column(String(100))
    coutTotal: Mapped[float] = mapped_column(Float)
    nomEvenement: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(100))
    nbParticipantsPrevu: Mapped[int] = mapped_column(Integer)
    emailReferent: Mapped[str] = mapped_column(String(100))
    dateDebut: Mapped[dt_datetime] = mapped_column(DateTime)
    dateFin: Mapped[dt_datetime] = mapped_column(DateTime)
    estConfirmee: Mapped[bool] = mapped_column(Boolean)

class Stats(Base):
    __tablename__ = "stats"
    id: Mapped[int] = mapped_column(primary_key=True)
    chiffresAffaires: Mapped[float] = mapped_column(Float)
    tauxOccupation: Mapped[float] = mapped_column(Float)
    periode: Mapped[str] = mapped_column(String(100))
    gestionnaire_2_id: Mapped[int] = mapped_column(ForeignKey("gestionnaire.id"), nullable=True)

class Gestionnaire(Base):
    __tablename__ = "gestionnaire"
    id: Mapped[int] = mapped_column(primary_key=True)
    identifiant: Mapped[str] = mapped_column(String(100))
    nom: Mapped[str] = mapped_column(String(100))
    reservation_1_id: Mapped[int] = mapped_column(ForeignKey("reservation.id"), nullable=True)


#--- Relationships of the centredecongres table
CentredeCongres.evenementsalle_1: Mapped[List["EvenementSalle"]] = relationship("EvenementSalle", back_populates="centredecongres", foreign_keys=[EvenementSalle.centredecongres_id])
CentredeCongres.gestionnaire_1: Mapped["Gestionnaire"] = relationship("Gestionnaire", back_populates="centredecongres_1", foreign_keys=[CentredeCongres.gestionnaire_1_id])

#--- Relationships of the tarifs table
Tarifs.materielsprestations_1: Mapped[List["Materielsprestations"]] = relationship("Materielsprestations", secondary=applique_1, back_populates="tarifs_1")
Tarifs.evenementsalle_2: Mapped[List["EvenementSalle"]] = relationship("EvenementSalle", secondary=applique, back_populates="tarifs")

#--- Relationships of the evenementsalle table
EvenementSalle.centredecongres: Mapped["CentredeCongres"] = relationship("CentredeCongres", back_populates="evenementsalle_1", foreign_keys=[EvenementSalle.centredecongres_id])
EvenementSalle.tarifs: Mapped[List["Tarifs"]] = relationship("Tarifs", secondary=applique, back_populates="evenementsalle_2")
EvenementSalle.reservation: Mapped["Reservation"] = relationship("Reservation", back_populates="evenementsalle", foreign_keys=[EvenementSalle.reservation_id])

#--- Relationships of the materielsprestations table
Materielsprestations.reservation_3: Mapped["Reservation"] = relationship("Reservation", back_populates="materielsprestations", foreign_keys=[Materielsprestations.reservation_3_id])
Materielsprestations.tarifs_1: Mapped[List["Tarifs"]] = relationship("Tarifs", secondary=applique_1, back_populates="materielsprestations_1")

#--- Relationships of the disponibilites table
Disponibilites.reservation_2: Mapped[List["Reservation"]] = relationship("Reservation", secondary=verifie, back_populates="disponibilites")

#--- Relationships of the reservation table
Reservation.materielsprestations: Mapped[List["Materielsprestations"]] = relationship("Materielsprestations", back_populates="reservation_3", foreign_keys=[Materielsprestations.reservation_3_id])
Reservation.disponibilites: Mapped[List["Disponibilites"]] = relationship("Disponibilites", secondary=verifie, back_populates="reservation_2")
Reservation.evenementsalle: Mapped[List["EvenementSalle"]] = relationship("EvenementSalle", back_populates="reservation", foreign_keys=[EvenementSalle.reservation_id])
Reservation.gestionnaire: Mapped[List["Gestionnaire"]] = relationship("Gestionnaire", back_populates="reservation_1", foreign_keys=[Gestionnaire.reservation_1_id])

#--- Relationships of the stats table
Stats.gestionnaire_2: Mapped["Gestionnaire"] = relationship("Gestionnaire", back_populates="stats", foreign_keys=[Stats.gestionnaire_2_id])

#--- Relationships of the gestionnaire table
Gestionnaire.reservation_1: Mapped["Reservation"] = relationship("Reservation", back_populates="gestionnaire", foreign_keys=[Gestionnaire.reservation_1_id])
Gestionnaire.centredecongres_1: Mapped["CentredeCongres"] = relationship("CentredeCongres", back_populates="gestionnaire_1", foreign_keys=[CentredeCongres.gestionnaire_1_id])
Gestionnaire.stats: Mapped[List["Stats"]] = relationship("Stats", back_populates="gestionnaire_2", foreign_keys=[Stats.gestionnaire_2_id])

# Database connection
DATABASE_URL = "sqlite:///Class_Diagram.db"  # SQLite connection
engine = create_engine(DATABASE_URL, echo=True)

# Create tables in the database
Base.metadata.create_all(engine, checkfirst=True)