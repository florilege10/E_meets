#!/bin/bash
set -ex  # Afficher chaque commande et arrêter à la première erreur

# Vérifier si Python3 et pip sont installés
if ! command -v python3 >/dev/null 2>&1; then
  echo "Python3 non trouvé, installation..."
  apt-get update && apt-get install -y python3 python3-pip
fi

# Vérifier les versions installées
python3 --version
pip3 --version

# Installer les dépendances
pip3 install -r requirements.txt

# Vérifier si manage.py existe
if [ ! -f "manage.py" ]; then
  echo "Erreur: manage.py introuvable dans le répertoire actuel."
  exit 1
fi

# Collecter les fichiers statiques
python3 manage.py collectstatic --noinput
