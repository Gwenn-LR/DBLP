# DBLP
Dépôt synthétisant le travail réalisé lors de la réalisation du brief intitulé "Base de publications scientifiques" dans le cadre de la formation Simplon×Microsoft IA 

# Contexte du projet

Le centre de recherche Breizhmeiz International souhaite un petit module d'accès simple aux publications scientifiques. On vous demande de mettre en place une base de données MongoDB, orientée documents, pour gérer l'accès à ces publications. De votre coté, vous allez tester les datas grâce à un petit script Python.

# Modalités pédagogiques

Le projet se fait seul et doit être rendu vendredi soir. Vous allez suivre les étapes suivantes pour réaliser le projet : 
- [x] Créer la base DBLP et y ajouter une collection publis.
- [x] Importer dans la base les données du fichier dblp.json (Ca peut prendre un peu de temps).
- [x] Écrire le script Python pour tester la base.
- [x] Exécuter le script.
- [ ] Vérifier les résultats.

Le script Python doit permettre de : 
- [x] Compter le nombre de documents de la collection publis.
- [x] Lister tous les livres (type “Book”).
- [x] Lister les livres depuis 2014.
- [x] Lister les publications de l’auteur “Toru Ishida”.
- [x] Lister tous les auteurs distincts.
- [x] Trier les publications de “Toru Ishida” par titre de livre.
- [x] Compter le nombre de ses publications.
- [x] Compter le nombre de publications depuis 2011 et par type.
- [x] Compter le nombre de publications par auteur et trier le résultat par ordre croissant.

Tous les affichages se font dans la console.

Et s'il vous reste du temps écrire un petit script qui : 
- [x] Demande le chemin d'un fichier json.
- [x] Insère un ou plusieurs nouveaux documents, à partir de ce fichier, dans la collection publis.
- [ ] Pour tester ce dernier script, créez un fichier json à partir des informations trouvées sur le site proposé en lien.

# Critères de performance

- [x] La connexion à MongoDB doit fonctionner et celle-ci doit contenir la collection publis avec l'ensemble des documents enregistrés.
- [x] Le code Python doit exécuter l'ensemble des requêtes demandées.

# Modalités d'évaluation

Présentation du code au formateur.

# Livrables

Un lien Github vers le code Python.