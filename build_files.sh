#!/bin/bash
set -e  # Arrête l'exécution en cas d'erreur

# Installer les dépendances
pip install -r requirements.txt

# Collecter les fichiers statiques
python manage.py collectstatic --noinput
