Voici les codes python générer par BESSER (cpature d'ecran) : 

-diagramme de classe (json + capture ecran)

-prise en main (json + capture ecran)

Documentation du Modèle de Classes et Logique Objet

Ce dossier présente la conception structurelle du système de gestion des centres de congrès. Le modèle a été conçu pour traduire fidèlement le cahier des charges de l'ISTIC tout en assurant une génération de code Python cohérente via BESSER.

Justification des Choix de Multiplicités

Chaque relation dans le diagramme a été définie pour respecter les contraintes métier du sujet de TD.

 Organisation des Centres

CentredeCongres (0..1) ── (0..*) EvenementSalle : Un centre est composé de plusieurs éléments (Amphis, Salles). La multiplicité 0..* permet de créer un centre puis d'y ajouter des ressources progressivement.

Gestionnaire (1..*) ── (0..1) CentredeCongres : Le sujet mentionne qu'un gestionnaire configure "son" centre. Nous avons autorisé plusieurs gestionnaires pour simuler une équipe d'administration.

Gestion des Réservations

EvenementSalle (0..*) ── (0..1) Reservation : Une salle peut être réservée plusieurs fois sur des créneaux différents.

Reservation (1..) ── (0..) Materielsprestations : Conformément au cahier des charges, une réservation peut inclure plusieurs matériels et prestations optionnelles.

État de l'Implémentation Python

Note Importante : Limitations Techniques

Bien que l'IHM affiche les boutons d'actions métiers (ex: calculerCout, confirmerPaiement), les méthodes ne sont pas fonctionnelles dans cette version du prototype.

Pourquoi ce choix ?
Initialement, nous avions rédigé l'intégralité de la logique métier en Python dans l'éditeur BESSER. Cependant, lors du passage à la génération et au déploiement via Docker, nous avons rencontré des obstacles techniques majeurs :

Instabilité de la Génération : L'outil BESSER (en version preview) a généré des erreurs d'indentation et des conflits de bibliothèques lors de l'intégration des scripts Python personnalisés dans le backend.

Priorité à la Stabilité : Pour éviter que le conteneur Docker ne crash au démarrage et pour garantir que l'IHM reste accessible pour la démonstration du CRUD (Création, Lecture, Mise à jour des objets), nous avons dû neutraliser les méthodes avec des blocs pass.

Complexité du Pattern State : L'implémentation du pattern State pour la classe Réservation via l'interface BESSER s'est avérée incompatible avec le moteur de transition généré automatiquement.

Logique prévue (Algorithmie)

Le code que nous souhaitions intégrer est documenté dans le dossier code/ sous forme de commentaires. Il prévoyait :

Calcul de tarif : coutTotal = duree * prix_saisonnier.

Vérification OCL : Contrôle du nombre de participants par rapport à la capacité maximale de la salle.

Gestion des stocks : Décrémentation du stock de vidéoprojecteurs lors d'une réservation.
