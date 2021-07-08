[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com) [![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)](https://forthebadge.com)
# Mini-Projet Convertisseur (Flask)

Ce projet a été implémenté dans le but de s'entrainer au test unitaire à l'aide de Pytest sur un projet Flask (pytest-flask). Le code source
contient un convertisseur qui permet d'effectuer des conversions de nombre vers différentes bases (décimal, binaire et hexadécimal). Vous pourrez ainsi développer l'ensemble des scénarios nécessaires afin de tester 
l'ensemble du code source. À noter que des propositions de corrections sont mises à disposition dans différentes branches 
du répertoire.

## Pré-requis

* Installer Python 3 : [Téléchargement Python 3](https://www.python.org/downloads/)
* Installer git : [Téléchargement Git](https://git-scm.com/book/fr/v2/D%C3%A9marrage-rapide-Installation-de-Git)

## Installation

### 1. Télécharger le projet sur votre répertoire local : 
```
git clone https://github.com/OpenClassrooms-Student-Center/4425126-testing-python-flask.git 
cd 4425126-testing-python-flask
```
### 2. Mettre en place un environnement virtuel :
* Créer l'environnement virtuel: `python -m venv venv`
* Activer l'environnement virtuel :
    * Windows : `venv\Scripts\activate.bat`
    * Unix/MacOS : `source venv/bin/activate`

    
### 3. Installer les dépendances du projet
```
pip install -r requirements.txt
```

## Démarrage
* Lancer le script à l'aide de la commande suivante : `flask run`

## Corrections
Proposition de correction pour les tests unitaires avec pytest-flask :
```
git checkout tests
pytest -v tests/
```
