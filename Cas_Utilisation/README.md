@startuml
title Diagramme de Cas d'Utilisation - Gestion de Centres de Congrès (CDG)

left to right direction

actor "Gestionnaire" as G

package "Système de Gestion de Centres de Congrès" {
    
    package "Configuration & Paramétrage" {
        usecase "Configurer les éléments du centre\n(Amphis, salles, capacité max)" as UC_Config
        usecase "Gérer les tarifs par saison\n(Haute, moyenne, basse)" as UC_Tarifs
        usecase "Définir les contraintes de location\n(Durée min, jours interdits)" as UC_Contraintes
    }

    package "Gestion des Opérations" {
        usecase "Gérer les réservations\n(Salles, matériel, prestations)" as UC_Reserver
        usecase "Gérer les périodes d'indisponibilité\n(Travaux, maintenance)" as UC_Indispo
        usecase "Consulter les disponibilités" as UC_Dispo
        
        usecase "Gérer le cycle de vie d'une réservation" as UC_Cycle
        usecase "Confirmer une réservation (Paiement)" as UC_Pay
        usecase "Modifier / Annuler une réservation" as UC_Modif
    }

    package "Analyse" {
        usecase "Visualiser les statistiques\n(CA, taux d'occupation, services)" as UC_Stats
    }
}

G --> UC_Config
G --> UC_Tarifs
G --> UC_Contraintes
G --> UC_Reserver
G --> UC_Indispo
G --> UC_Dispo
G --> UC_Cycle
G --> UC_Stats

UC_Cycle <.. UC_Pay : <<extend>>
UC_Cycle <.. UC_Modif : <<extend>>

@enduml
