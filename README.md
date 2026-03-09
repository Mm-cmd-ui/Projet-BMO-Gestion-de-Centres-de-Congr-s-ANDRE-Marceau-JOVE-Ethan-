Système de Gestion de Centres de Congrès (Projet BMO)

Objectifs : Appliquer une approche complète de modélisation en mode projet, partant d’un cahier des charges réaliste et allant jusqu’à une application Web en utilisant l’outil en ligne BESSER. L'application devra permettre de configurer chaque centre de congrès, de gérer les réservations, ainsi que les disponibilités et des tarifs

Accès Rapide

-Diagramme de classe : Structure de la base de données.
*[diagramme de classe](./diagramme-de-classe/)
-Diagramme d'état : Cycle de vie d'une réservation.
*[diagramme etat](./diagramme-etat/)


=> Guide d'Utilisation (TD)

1. Configuration Initiale

L'application permet de configurer l'ensemble du système via l'interface générée :

Création du Centre : Enregistrer le nom et la localisation du complexe.

Ajout de Salles : Définir les capacités maximales (Amphis, Salles de réunion).

Gestionnaire & Staff : Création des profils utilisateurs pour piloter le centre.

2. Processus de Réservation

Le système est conçu pour gérer le flux suivant :

Saisie des dates : Choix des créneaux dateDebut et dateFin.

Objets Métiers : Création des instances de réservations liées aux clients et aux salles.

Cycle de vie : Suivi de l'avancement de la réservation (En attente, Confirmée, Annulée).

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

Projet réalisé par ANDRE Marceau & JOVE Ethan
