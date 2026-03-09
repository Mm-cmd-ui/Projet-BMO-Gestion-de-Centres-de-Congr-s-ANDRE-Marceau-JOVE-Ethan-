Voici l'ensemble des dossiers necessiares pour générer l'app web BESSER : 

-backend

-frontend

-docker-compose


->Limites Techniques & État du Prototype

Actuellement, l'application déployée via Docker présente certaines limites liées à la jeunesse de l'outil BESSER et à des contraintes techniques de génération :

Instanciation des Classes : Toutes les classes du diagramme (Gestionnaire, Salle, Réservation, etc.) sont fonctionnelles. Vous pouvez créer, lire, modifier et supprimer (CRUD) tous les éléments du centre de congrès.

Exécution des Méthodes : Bien que les boutons correspondant aux méthodes (calculerCout, confirmerPaiement, gererIndisponibilite) apparaissent dans l'interface, leur exécution peut être instable.

Causes identifiées :

Problèmes d'indentation automatique lors de la génération du code Python par BESSER.

Incompatibilités mineures entre certaines versions de la librairie backend et les scripts personnalisés.

Pour garantir la stabilité du déploiement Docker, certaines méthodes ont été passées en mode pass (code neutre) afin d'éviter le crash du serveur backend.

🛠️ Installation et Lancement (Docker)

Ouvrez un terminal dans le dossier racine du projet.

docker-compose up
Lancez la construction de l'environnement :

docker compose down -v
docker compose up --build

Accédez à l'interface web sur : http://localhost:3000

⚙️ Logique de Conception

Le projet respecte les principes de la modélisation objet :

Héritage et Associations : Liens stricts entre les centres, les ressources et les réservations.

Indépendance des données : Séparation claire entre les statistiques et les données opérationnelles.
