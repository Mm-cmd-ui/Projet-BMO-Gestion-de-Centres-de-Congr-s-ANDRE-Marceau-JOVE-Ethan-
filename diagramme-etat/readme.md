
Ce projet utilise un diagramme d'états-transitions pour piloter le cycle de vie d'une réservation. Voici le détail du fonctionnement.

=> script UML
(Vous pouvez visualiser ce diagramme en copiant le code ci-dessous sur PlantUML)

@startuml
title Diagramme d'états - Classe Réservation

[*] --> EnAttentePaiement : Création réservation

state EnAttentePaiement {
  EnAttentePaiement : entry / Démarrer compte à rebours
}
note right of EnAttentePaiement : Le délai est configurable.

EnAttentePaiement --> Confirmee : [Paiement valide] / enregistrer confirmation
EnAttentePaiement --> Annulee : [Délai dépassé] / annulation automatique

Confirmee --> Modifiee : [Action gestionnaire] / éditer détails
Confirmee --> Annulee : [Action gestionnaire ou client] / annuler
Confirmee --> Terminee : [Événement commencé]

Modifiee --> Confirmee : Valider modifications
Modifiee --> Annulee : Annuler réservation
note bottom of Modifiee : Possible tant que l'événement n'a pas commencé.

Annulee --> [*]
Terminee --> [*]
@enduml 

=> Explications

-Initialisation : EnAttentePaiement

Dès qu'une réservation est créée, elle entre dans cet état 

.Action automatique : Un compte à rebours est lancé (délai configurable).
.Issues possibles : * Si le paiement est validé, la réservation passe à Confirmée.
.Si le temps s'écoule sans paiement, elle passe automatiquement à Annulée.

-État Actif : Confirmée & Modifiée

Une fois payée, la réservation est considérée comme valide 

.Modification : Un gestionnaire peut éditer les détails (passage à l'état Modifiée). Une fois les changements validés, elle redevient Confirmée.
.Annulation : Le client ou le gestionnaire peut décider d'annuler la réservation à ce stade.
.Contrainte : Ces actions ne sont possibles que tant que l'événement n'a pas commencé.

-Terminaison : Terminee ou Annulee 

.Terminée : La réservation passe dans cet état final dès que l'événement débute.
.Annulée : État final si le paiement échoue ou si une annulation manuelle intervient.
