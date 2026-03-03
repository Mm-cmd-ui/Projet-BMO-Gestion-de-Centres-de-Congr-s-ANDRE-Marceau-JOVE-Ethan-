@startuml
left to right direction
title Diagramme de Cas d Utilisation - Gestion Centre de Congres

actor Gestionnaire

rectangle "Systeme de Gestion du Centre de Congres" {

    (Gerer tarifs) as UC1
    (Definir capacite accueil) as UC2
    (Definir equipements disponibles) as UC3
    (Gerer reservations) as UC4
    (Visualiser salles) as UC5
    (Faire reservation) as UC6
    (Consulter reservation) as UC7
}

Gestionnaire --> UC1
Gestionnaire --> UC2
Gestionnaire --> UC3
Gestionnaire --> UC4
Gestionnaire --> UC5
Gestionnaire --> UC6
Gestionnaire --> UC7

@enduml
