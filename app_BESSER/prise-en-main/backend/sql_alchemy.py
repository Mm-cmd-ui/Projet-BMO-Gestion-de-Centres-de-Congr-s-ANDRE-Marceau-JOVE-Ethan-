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

# Tables definition
class Evenement_Salle(Base):
    __tablename__ = "evenement_salle"
    id: Mapped[int] = mapped_column(primary_key=True)
    nom: Mapped[str] = mapped_column(String(100))
    capaciteMax: Mapped[int] = mapped_column(Integer)
    typeElement: Mapped[str] = mapped_column(String(100))
    reservation_1_id: Mapped[int] = mapped_column(ForeignKey("reservation.id"), nullable=True)

class reservation(Base):
    __tablename__ = "reservation"
    id: Mapped[int] = mapped_column(primary_key=True)
    nomEvenement: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(100))
    nbParticipantsPrevu: Mapped[int] = mapped_column(Integer)
    dateDebut: Mapped[dt_datetime] = mapped_column(DateTime)
    dateFin: Mapped[dt_datetime] = mapped_column(DateTime)
    estConfirmee: Mapped[bool] = mapped_column(Boolean)
    delaiConfirmation: Mapped[dt_datetime] = mapped_column(DateTime)
    etatActuel: Mapped[str] = mapped_column(String(100))
    coutTotal: Mapped[float] = mapped_column(Float)
    gestionnaire_id: Mapped[int] = mapped_column(ForeignKey("gestionnaire.id"), nullable=True)

class gestionnaire(Base):
    __tablename__ = "gestionnaire"
    id: Mapped[int] = mapped_column(primary_key=True)
    identitfiant: Mapped[str] = mapped_column(String(100))
    nom: Mapped[str] = mapped_column(String(100))


#--- Relationships of the evenement_salle table
Evenement_Salle.reservation_1: Mapped["reservation"] = relationship("reservation", back_populates="evenement_salle", foreign_keys=[Evenement_Salle.reservation_1_id])

#--- Relationships of the reservation table
reservation.evenement_salle: Mapped[List["Evenement_Salle"]] = relationship("Evenement_Salle", back_populates="reservation_1", foreign_keys=[Evenement_Salle.reservation_1_id])
reservation.gestionnaire: Mapped["gestionnaire"] = relationship("gestionnaire", back_populates="reservation", foreign_keys=[reservation.gestionnaire_id])

#--- Relationships of the gestionnaire table
gestionnaire.reservation: Mapped[List["reservation"]] = relationship("reservation", back_populates="gestionnaire", foreign_keys=[reservation.gestionnaire_id])

# Database connection
DATABASE_URL = "sqlite:///Class_Diagram.db"  # SQLite connection
engine = create_engine(DATABASE_URL, echo=True)

# Create tables in the database
Base.metadata.create_all(engine, checkfirst=True)