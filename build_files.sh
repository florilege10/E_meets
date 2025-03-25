#!/bin/bash
set -e  # Arrêter en cas d'erreur

# Vérifier si Python3 et pip sont installés
if ! command -v python3 >/dev/null 2>&1; then
  echo "Python3 non trouvé, installation..."
  apt-get update && apt-get install -y python3 python3-pip
fi

# Utiliser explicitement pip3
pip3 install -r requirements.txt

# Collecter les fichiers statiques
python3 manage.py collectstatic --noinput
