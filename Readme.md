Yosra Moumtaz et Ichraq Essadeq
# Statistique et Probabilité avec Django

Ce projet est une application web qui permet d'effectuer des opérations statistiques et de probabilité de base. Il est développé en Python à l'aide du framework Django.

## Fonctionnalités

L'application propose les fonctionnalités suivantes :

- Visualisation de données à partir de fichiers Excel, CSV ou texte
- Parcourir les données et effectuer des opérations de filtrage et de recherche
- Générer des distributions de probabilité pour différentes lois (Binomiale, Bernoulli, Normale, Poisson, Uniforme, Exponentielle)
- Calculer des statistiques de base (moyenne, médiane, mode, variance, écart-type)
- Calculer les testes (T-test,Z-test et régression linéaire)


## Structure du code

Le code est organisé en plusieurs fichiers et répertoires :

- `index.html` : Page d'accueil de l'application
- `visualiser_data.html` : Page de visualisation des données
- `diagramme.html` : Page de génération de diagrammes
- `text.html` : Page de traitement des fichiers texte
- `csv.html` : Page de traitement des fichiers CSV
- `parcourir.html` : Page de parcours des données
- `binomiale.html` : Page de génération de la distribution binomiale
- `bernoulli.html` : Page de génération de la distribution de Bernoulli
- `normale.html` : Page de génération de la distribution normale
- `poisson.html` : Page de génération de la distribution de Poisson
- `uniforme.html` : Page de génération de la distribution uniforme
- `exponentielle.html` : Page de génération de la distribution exponentielle
- `calcules.html` : Page de calcul des statistiques de base
- `testes.html` :Page de calcul des testes
- `forms.py` : Fichier contenant les formulaires utilisés dans l'application
- `views.py` : Fichier contenant les vues de l'application
- `static/` : Répertoire contenant les fichiers statiques (CSS, JavaScript, images)
- `templates/` : Répertoire contenant les fichiers de templates HTML

## Fonctionnement de l'application

L'application fonctionne de la manière suivante :

1. L'utilisateur accède à la page d'accueil de l'application (`index.html`).
2. Il peut choisir de visualiser des données à partir d'un fichier Excel, CSV ou texte, ou de générer des distributions de probabilité ou de calculer

##  Installation et prérequis 

- `pip install django/`: Commande utilisée dans Python pour installer le framework Django, un outil robuste pour le développement web.
- `pip install pandas/` : Commande pour installer la bibliothèque Pandas, souvent utilisée pour la manipulation et l'analyse des données dans Python.
- `pip install requests/` : Commande pour installer la bibliothèque Requests, qui permet d'envoyer des requêtes HTTP/1.1 de manière simple en Python.
- `pip install matplotlib/` : Commande pour installer la bibliothèque Matplotlib, utilisée pour la création de graphiques et de visualisations en Python.
- `pip install seaborn/` : Commande pour installer la bibliothèque Seaborn, qui offre une interface de haut niveau pour créer des graphiques statistiques attrayants en Python.
- `pip install plotly/` : Commande pour installer la bibliothèque Plotly, permettant la création de graphiques interactifs et dynamiques en Python.
- `pip install openpyxl/` : Commande pour installer la bibliothèque Openpyxl, utilisée pour la manipulation des fichiers Excel (xlsx) en Python.
- `python -m venv venv/`: Commande pour créer un environnement virtuel Python nommé "venv", isolant les dépendances d'un projet Python des autres projets.
- `.\venv\Scripts\activate/`  : Commande pour activer l'environnement virtuel créé précédemment (sous Windows).
- `python manage.py runserver/` : Commande pour démarrer le serveur de développement dans un projet Django. Il lance l'application web et permet de la visualiser localement dans un navigateur

