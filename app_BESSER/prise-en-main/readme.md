Voici l'ensemble des dossiers nécessaires pour générer l'app web BESSER :

-backend

-frontend

-docker-compose
 
-> Configuration des données
 
  .Créer une Salle (EvenementSalle) : Remplissez l'attribut Capacite (ex: 600). Cliquez sur "Save/Update".
  .Créer des Réservations : Créez une ou plusieurs instances avec un nom et un prix.
  .Créer un Gestionnaire : Créez l'acteur et, dans la section Associations, liez-le aux réservations créées précédemment. Cliquez impérativement sur "Update".

 -> Test des méthodes métier

   .calculer le cout automatiquement: aller sur une réservation, cliquer sur la méthode et le cout s'affiche
   .Vérifier la Capacité : Allez sur une Salle, cliquez sur verifierCapacite. Saisissez un nombre (ex: 500). Le système compare dynamiquement votre saisie à la limite physique de la salle.
   .Consulter les Statistiques : Allez sur le Gestionnaire, cliquez sur consulterStats. Saisissez une période (ex: "Mars"). Le système affiche la liste des revenus liés.

-> Pb techniques

   .la methode consulter stats ne fonctionne pas, elle ne lie pas les données de réservation
