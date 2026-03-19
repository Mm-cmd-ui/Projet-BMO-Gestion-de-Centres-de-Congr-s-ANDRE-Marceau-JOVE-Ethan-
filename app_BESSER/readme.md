
Accèss Rapide : 


-diagramme de classe : 
[diagramme de classe](./diagramme-de-classe/)



-prise en main : 
[prise en main](./prise-en-main/)






->Limites Techniques & État du Prototype

-Actuellement, l'application déployée via Docker présente certaines limites liées à la jeunesse de l'outil BESSER et à des contraintes techniques de génération :

-Instanciation des Classes : Toutes les classes du diagramme (Gestionnaire, Salle, Réservation, etc.) sont fonctionnelles. Vous pouvez créer, lire, modifier et supprimer (CRUD) tous les éléments du centre de congrès.

-Exécution des Méthodes : Bien que les boutons correspondant aux méthodes (calculerCout, confirmerPaiement, gererIndisponibilite) apparaissent dans l'interface, leur exécution peut être instable.

-Causes identifiées :

.Problèmes lors de la génération du code Python par BESSER

.Problèmes au niveau de BESSER de manière générale

-> Installation et Lancement (Docker)

.Ouvrez un terminal dans le dossier racine du projet.

.Lancer docker depuis terminal :
docker-compose up

.Mettre a jour docker suite à modifications : 
docker-compose down -v
docker compose up --build

.Accédez à l'interface web sur : http://localhost:3000
