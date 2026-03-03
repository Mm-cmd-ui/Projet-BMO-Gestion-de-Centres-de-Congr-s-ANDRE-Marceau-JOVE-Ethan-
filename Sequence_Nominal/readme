@startuml
title Diagramme de Séquence Nominal - Interaction Utilisateur / App Web

actor Utilisateur
participant "App Web" as Web

== Consultation ==

Utilisateur -> Web : Consulter options
Web --> Utilisateur : Afficher liste des salles

== Recherche ==

Utilisateur -> Web : Rechercher salle (critères)
Web --> Utilisateur : Afficher résultats

== Sélection salle ==

Utilisateur -> Web : Sélectionner salle
Web --> Utilisateur : Afficher disponibilités et tarifs

== Sélection disponibilité ==

Utilisateur -> Web : Choisir créneau
Web --> Utilisateur : Afficher options matériel

== Options ==

Utilisateur -> Web : Sélectionner options
Web --> Utilisateur : Afficher récapitulatif

== Paiement ==

Utilisateur -> Web : Confirmer et payer
Web --> Utilisateur : Afficher confirmation de réservation

@enduml
