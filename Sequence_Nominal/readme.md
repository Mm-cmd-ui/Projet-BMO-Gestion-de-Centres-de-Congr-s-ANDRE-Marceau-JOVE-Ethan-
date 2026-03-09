 Documentation du Scénario Nominal (Flux Standard)

Ce dossier contient la modélisation dynamique des interactions au sein de l'application de gestion des centres de congrès. Le Scénario Nominal décrit le "chemin heureux" : le processus idéal où un utilisateur réserve une ressource sans conflit ni erreur technique.


Accès Rapide : 

Entrée dans l'Application Web : 
[entree app](/.Entree_app/)

Disponibilités : 
[dispo](/.dispo/)

Réservation : 
[reservation](/.reservation/)

Matériels et Prestations : 
[materiel/prestation](/.materiel_prestation/)

Entrée dans l'Application Web

L'interaction débute sur l'interface générée par BESSER (Port 3000) :

Authentification/Identification : Le gestionnaire ou le client accède au tableau de bord.

Consultation : Le système interroge le backend pour afficher la liste des centres de congrès et des éléments (Amphis, Salles) disponibles.

Étape 1 : Vérification des Disponibilités

Avant toute action, le système valide la faisabilité temporelle :

Action : L'utilisateur saisit les dates de début et de fin.

Logique : Le système appelle la méthode estDisponible() sur l'élément visé.

Interaction : Une requête est envoyée à la classe Disponibilites pour vérifier qu'aucun blocage (maintenance/travaux) n'est enregistré sur ce créneau.

Étape 2 : Création de la Réservation

Une fois le créneau validé :

Instanciation : Un nouvel objet Reservation est créé en base de données.

Saisie des informations : L'utilisateur renseigne l'Événement, le nombre de participants et l'e-mail du référent.

Contrôle de Capacité : Le système exécute verifierCapacite(). Si nbParticipants <= capaciteMax, le processus continue.

Étape 3 : Ajout de Matériels et Prestations

Conformément au sujet du TD, la réservation peut être complétée par des ressources additionnelles :

Sélection : L'utilisateur ajoute des micros, vidéoprojecteurs ou des pauses café.

Vérification : Pour chaque matériel, la méthode verifierStockDisponible() est appelée pour s'assurer que la logistique peut suivre la demande.

Calcul du Coût : La méthode calculerCout() agrège le tarif de la salle (selon la saisonnalité définie dans la classe Tarifs) et le prix des options sélectionnées.

Étape 4 : Confirmation et Paiement

La fin du scénario nominal valide la transaction :

Transition d'État : La réservation passe de EnAttentePaiement à Confirmee via l'action confirmerPaiement().

Persistance : Le système met à jour le calendrier global pour rendre la salle indisponible pour d'autres utilisateurs sur ce créneau.
