# P9_OCR
## Projet 9: LITReview
Django version 4.1.4

## Installation et exécution de l'application :

### Installation :
1. Cloner ce dépôt de code à l'aide de la commande:

    - HTTPS :  git clone https://github.com/motaALI/P9_OCR.git
    - SSH : git clone git@github.com:motaALI/P9_OCR.git
    - Zip file : (vous pouvez également télécharger le code en utilisant un fichier zip)
    
2. Rendez-vous depuis un terminal à la racine du répertoire P9_OCR
3. Créer un environnement virtuel pour le projet avec $ python -m venv env sous windows ou $ python3 -m venv env sous mac os ou linux.
4. Activez l'environnement virtuel avec $ env\Scripts\activate sous windows ou $ source env/bin/activate sous macos ou linux.
5. Installez les dépendances du projet avec la commande : 
    `$ pip install -r requirements.txt`  
6. Créer et alimenter la base de données avec la commande:
    `$ python manage.py createsuperuser`  
7. Faire des migrations pour cerer la base des données: 
    `python .\manage.py makemigrations`  
8. Appliquer les changements sur la base des données:
    `python manage.py migrate`
    
### Exécution :
1. Avec un environnement virtuel activé exécuter la commande suivante pour démarrer l'application:
    `python .\manage.py runserver`
    
2. Une fois démarrer l'application un serveur de développement sera accessible via une url donnée dans le terminal:
    par défaut django serveur est sur : `http://127.0.0.1:8000/`
