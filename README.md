Système de Gestion de Centres de Congrès (Projet BMO)

Objectifs : Appliquer une approche complète de modélisation en mode projet, partant d’un cahier des charges réaliste et allant jusqu’à une application Web en utilisant l’outil en ligne BESSER. L'application devra permettre de configurer chaque centre de congrès, de gérer les réservations, ainsi que les disponibilités et des tarifs

Accès Rapide

-Diagramme de classe : Structure de la base de données.
[diagramme de classe](./diagramme-de-classe/)

-Diagramme d'état : Cycle de vie d'une réservation.
[diagramme etat](./diagramme-etat/)

-Cas utilisation : Panorama des fonctionnalités offertes au Gestionnaire (Configuration, Réservation, Statistiques).
[cas utilisation](./Cas_Utilisation/)

-Sequence nominal : Chemin idéal d'une réservation sans conflit, incluant la vérification de capacité et le calcul automatique du tarif.
[sequence nominal](./Sequence_Nominal/)

-Sequence exceptionnel : Gestion des erreurs métier comme le dépassement de capacité d'un amphi ou l'indisponibilité du matériel (vidéoprojecteurs, micros).
[sequence exceptionnel](./Sequence_exceptionnel/)

-App BESSER : Génération de l'app web BESSER 
[app BESSER](./app_BESSER/)



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

Projet réalisé par ANDRE Marceau & JOVE Ethan
