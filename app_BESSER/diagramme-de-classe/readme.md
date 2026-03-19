Voici l'ensemble du projet : 

 .Backend : Logique métier développée en Python.

  Frontend : Interface utilisateur web générée automatiquement.

   Docker : Conteneurisation pour assurer le déploiement immédiat du service.
   
2. Analyse des 9 Méthodes Implémentées
Gestion des Salles & Stocks

    verifierCapacite (Salle) : Compare le nombre de participants à capaciteMax. Garantit la sécurité et le respect des normes d'accueil.

    verifierStockDisponible (Matériel) : Vérifie si la quantiteMax en stock permet de couvrir la demande (ex: chaises, micros).

    ajouterIndisponibilite (Dispo) : Permet de bloquer une salle (motif, dates). Note : Gère les erreurs de format date spécifiques au prototype.

Cycle de Vie des Réservations

    calculerCout : Automatise la facturation en multipliant les participants par un tarif unitaire (50€). Met à jour l'attribut coutTotal.

    confirmerPaiement : Change l'attribut etatActuel en "Confirmée". Valide officiellement le dossier.

    annuler : Bascule l'état en "Annulée" pour libérer le créneau tout en gardant une trace en base de données.

Tarification & Analyse

    appliquerTarif : Système de Yield Management. Ajuste le montantBase selon la saison (Été +20%, Hiver +10%, Printemps +5%, Automne -10%).

    consulterStatistiques (Gestionnaire) : Affiche une synthèse de l'activité (CA, occupation) pour une période donnée.

    calculerCA (Stats) : Consolide et affiche le chiffre d'affaires total stocké dans le système.

3. Limitations Techniques & Solutions

    Données Orphelines : La méthode consulterStatistiques peut afficher une liste vide. Cela est dû à l'impossibilité de créer manuellement les liens (associations) entre le Gestionnaire et les Réservations dans l'interface de test actuelle. La logique Python est toutefois validée.

    Erreur HTTP 500 (Dates) : Un mécanisme de sécurité (try/except) a été ajouté à ajouterIndisponibilite pour empêcher le crash du serveur lors de l'envoi de dates au format texte (String) vers des attributs de type Date.
