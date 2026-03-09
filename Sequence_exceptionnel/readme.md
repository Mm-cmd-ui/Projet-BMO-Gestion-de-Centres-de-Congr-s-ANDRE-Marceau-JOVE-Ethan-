Documentation du Scénario d'Exception (Gestion des Erreurs)

Ce dossier détaille les flux alternatifs et les mécanismes de contrôle de l'application. Le Scénario d'Exception modélise les cas où le système doit interrompre le processus de réservation pour garantir l'intégrité des règles métier du centre de congrès.

Accès rapide : 

Entree app :


Dispo :


reservation : 


materiels/prestation : 




Étape 1 : Conflit de Disponibilité (Double Réservation)

Lors de la tentative de réservation, le système interroge la classe Disponibilites.

Événement déclencheur : L'utilisateur sélectionne un créneau déjà occupé ou marqué comme "Indisponible" (maintenance).

Réaction du système :

La méthode estDisponible() renvoie False.

L'IHM affiche un message d'erreur : "La ressource est indisponible sur cette période".

Le processus de création de la réservation est avorté avant l'étape de paiement.

Étape 2 : Dépassement de Capacité

Une fois les dates choisies, le système valide la logistique humaine :

Événement déclencheur : Le nombre de participants saisi pour l'événement est supérieur à l'attribut capaciteMax de la salle sélectionnée.

Réaction du système :

L'appel à verifierCapacite(nbParticipants) échoue.

Le système bloque la transition vers l'étape de tarification et demande à l'utilisateur de choisir un espace plus vaste (ex: passer d'une salle de réunion à un Amphi).

Étape 3 : Rupture de Stock Matériel

Lors de l'ajout de prestations ou de matériels optionnels :

Événement déclencheur : La quantité demandée (ex: 10 micros mobiles) dépasse le stock enregistré dans quantiteMax pour ce matériel.

Réaction du système :

La méthode verifierStockDisponible() renvoie une exception.

Le système propose de réduire la quantité ou de supprimer l'option pour pouvoir valider le reste de la réservation.

Étape 4 : Échec de Paiement ou Délai Dépassé

Conformément au diagramme d'états de la classe Reservation :

Événement déclencheur : Le client ne valide pas son paiement dans le délai imparti par le gestionnaire.

Réaction du système :

Le garde-fou temporel expire.

La réservation passe automatiquement à l'état Annulée.

Le créneau est immédiatement libéré dans la table Disponibilites pour d'autres utilisateurs.
