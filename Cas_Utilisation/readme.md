Voci Cas Utilisation du projet : 

-le brouillon

-le propre


=>script PlantUML (propre)

@startuml
title Diagramme de Cas d'Utilisation - Gestion de Centres de Congrès (CDG)
left to right direction

actor "Gestionnaire" as G

rectangle "Système de Gestion de Centres de Congrès" {

   package "Configuration & Paramétrage" {
        usecase UC1 as "Configurer les éléments du centre\n(Amphis, salles, capacité max)"
        usecase UC2 as "Gérer les tarifs par saison\n(Haute, moyenne, basse)"
        usecase UC3 as "Définir les contraintes de location\n(Durée min, jours interdits)"
    }

   package "Gestion des Opérations" {
        usecase UC4 as "Gérer les réservations\n(Salles, matériel, prestations)"
        usecase UC5 as "Gérer les périodes d'indisponibilité\n(Travaux, maintenance)"
        usecase UC6 as "Consulter les disponibilités"
        usecase UC7 as "Gérer le cycle de vie d'une réservation"
        usecase UC8 as "Modifier / Annuler une réservation"
        usecase UC9 as "Confirmer une réservation (Paiement)"
        UC8 ..> UC7 : <<extend>>
        UC9 ..> UC7 : <<extend>>
    }

   package "Analyse" {
        usecase UC10 as "Visualiser les statistiques\n(CA, taux d'occupation, services)"
    }
}

' Liaisons de l'acteur unique
G --> UC1
G --> UC2
G --> UC3
G --> UC4
G --> UC5
G --> UC6
G --> UC7
G --> UC10

@enduml


=> Explication du Cas d'Utilsation

Dans ce système, le Gestionnaire est l'unique utilisateur responsable de l'intégralité du cycle de vie du centre de congrès. Il intervient sur trois pôles stratégiques : la configuration, les opérations quotidiennes et l'analyse.

-Configuration & Paramétrage (Back-Office)

.Il configure les éléments physiques (Amphis, salles) et définit leur capacité maximale.
.Il gère les tarifs en fonction de la saisonnalité (Haute, moyenne, basse).
.Il définit les contraintes de location, comme la durée minimale ou les jours interdits à la réservation.

-Gestion des Opérations (Quotidien)

.Il gère les réservations incluant les salles, le matériel et les prestations annexes.
.Il bloque les périodes d'indisponibilité pour travaux ou entretien.
.Il a une vue d'ensemble sur les disponibilités en temps réel.
.Il supervise l'évolution des réservations. Ce cas d'utilisation inclut des actions spécifiques via des extensions («extend») :

La modification ou l'annulation d'un dossier.
La confirmation finale après validation du paiement.

-Analyse & Pilotage

.Il visualise les indicateurs clés comme le Chiffre d'Affaires (CA), le taux d'occupation des salles et la rentabilité des services.
