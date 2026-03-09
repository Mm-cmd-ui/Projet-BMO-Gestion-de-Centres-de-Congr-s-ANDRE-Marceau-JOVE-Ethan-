Analyse du Cycle de Vie de la Réservation

Le diagramme d'états de la classe Réservation modélise les règles métier strictes définies dans le cahier des charges de l'ISTIC. Voici le guide de lecture de ce cycle de vie :

1. Initialisation : EnAttentePaiement

Dès qu'une réservation est créée, elle entre dans l'état EnAttentePaiement.

Règle métier : Conformément au sujet, un compte à rebours est lancé. Ce délai est configurable pour chaque réservation.

Issue A (Succès) : Si l'action [Paiement valide] survient, la réservation passe à l'état Confirmee.

Issue B (Échec) : Si le [Délai dépassé] survient, le système déclenche une Annulation automatique.

2. État Stable : Confirmee

Une fois le paiement enregistré, la réservation est officiellement verrouillée.

Dans cet état, les ressources (Amphis, matériels) sont garanties pour l'événement.

3. Flexibilité : Modifiee

Le cahier des charges précise qu'une réservation peut être modifiée tant que l'événement n'a pas commencé.

L'action du gestionnaire [éditer détails] fait basculer la réservation vers l'état Modifiee.

Une fois les modifications validées, elle retourne à l'état Confirmee.

4. Annulation et Fin de vie

Droit à l'oubli : Une annulation est possible depuis les états En attente, Confirmée ou Modifiée, à condition que l'événement n'ait pas débuté.

Terminee : Une fois que l'événement a eu lieu (Événement commencé), la réservation passe à l'état Terminee. Elle ne peut plus être modifiée et sert désormais de base pour la génération des Statistiques (Chiffre d'affaires, taux d'occupation).

Implémentation technique (Pattern State)

Dans notre projet BESSER, cette logique est conçue pour être implémentée via le Pattern State :

Chaque état est une sous-classe ou une valeur d'énumération qui restreint les actions possibles (par exemple, on ne peut pas "confirmer le paiement" d'une réservation déjà "Annulée").

Les transitions garantissent que le centre de congrès ne perd jamais la trace d'un paiement ou d'un créneau horaire.
