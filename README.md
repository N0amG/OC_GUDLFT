# GUDLFT - Competition Booking Platform

## 1. À propos du projet

Ce projet est une preuve de concept (POC) d'une plateforme de réservation de compétitions pour les clubs sportifs. L'objectif est de maintenir une solution légère et d'itérer en fonction des retours utilisateurs.

### Technologies utilisées

- **Python 3.x+**
- **Flask 2.3.3** - Framework web minimaliste et flexible
- **pytest 9.0.2** - Framework de tests
- **Locust 2.43.1** - Outil de tests de performance et de charge

## 2. Prérequis

Avant de commencer, assurez-vous d'avoir installé :
- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)
- Git (pour cloner le projet)

## 3. Installation et Configuration

### 3.1 Cloner le projet

```bash
git clone <url-du-repository>
cd OC_GUDLFT
```

### 3.2 Créer un environnement virtuel

#### Sur Windows (PowerShell) :
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

#### Sur Linux/Mac :
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3.3 Installer les dépendances

```bash
pip install -r requirements.txt
```

### 3.4 Configuration des fichiers de données

Le projet utilise des fichiers JSON pour stocker les données :

- **clubs.json** - Liste des clubs avec leurs informations (email, nom, points)
- **competitions.json** - Liste des compétitions disponibles

Ces fichiers sont déjà configurés et prêts à l'emploi.

### 3.5 Variables d'environnement

Flask nécessite la variable d'environnement `FLASK_APP` :

#### Windows (PowerShell) :
```powershell
$env:FLASK_APP = "server.py"
$env:FLASK_ENV = "development"  # Optionnel, pour le mode développement
```

#### Linux/Mac :
```bash
export FLASK_APP=server.py
export FLASK_ENV=development  # Optionnel, pour le mode développement
```

## 4. Démarrage du serveur

### 4.1 Lancer l'application

```bash
flask run
```

Ou alternativement :

```bash
python -m flask run
```

Le serveur démarre par défaut sur `http://127.0.0.1:5000`

### 4.2 Accéder à l'application

Ouvrez votre navigateur et accédez à : `http://127.0.0.1:5000`

Pour vous connecter, utilisez l'un des emails présents dans le fichier [clubs.json](clubs.json).

## 5. Tests

Le projet utilise pytest avec une structure de tests organisée en trois niveaux :

```
tests/
├── unit/               # Tests unitaires
├── integration/        # Tests d'intégration
└── functional/         # Tests fonctionnels
```

### 5.1 Exécuter tous les tests

```bash
pytest
```

### 5.2 Exécuter des tests spécifiques

```bash
# Tests unitaires uniquement
pytest tests/unit/

# Tests d'intégration uniquement
pytest tests/integration/

# Tests fonctionnels uniquement
pytest tests/functional/

# Un fichier de test spécifique
pytest tests/unit/test_routes.py

# Un test spécifique
pytest tests/unit/test_routes.py::test_index
```

### 5.3 Tests avec verbosité

```bash
# Mode verbose
pytest -v

# Mode très verbose avec détails des assertions
pytest -vv

# Afficher les print() dans les tests
pytest -s
```

### 5.4 Couverture de code

Pour générer un rapport de couverture :

```bash
# Installation de coverage (si non installé)
pip install pytest-cov

# Exécuter les tests avec couverture
pytest --cov=. --cov-report=html

# Voir le rapport
# Le rapport HTML sera généré dans htmlcov/index.html
```

### 5.5 Structure des tests

#### Tests unitaires
- `test_routes.py` - Tests des routes Flask
- `test_load_functions.py` - Tests des fonctions de chargement de données
- `test_booking_validation.py` - Tests de validation des réservations

#### Tests d'intégration
- `test_booking_flow.py` - Tests du flux complet de réservation

#### Tests fonctionnels
- `test_user_journeys.py` - Tests des parcours utilisateurs
- `test_booking_restrictions.py` - Tests des restrictions de réservation

## 6. Tests de Performance

Le projet utilise **Locust** pour les tests de performance et de charge.

### 6.1 Configuration du fichier Locust

Le fichier [locustfile.py](locustfile.py) contient les scénarios de tests de charge :
- Connexion utilisateur
- Affichage des compétitions
- Réservation de places
- Affichage du tableau des points

### 6.2 Lancer les tests de performance

#### Mode interface web (recommandé) :

```bash
# S'assurer que le serveur Flask tourne sur le port 5000
# Dans un terminal séparé :
locust -f locustfile.py
```

Puis ouvrez votre navigateur sur `http://localhost:8089`

Paramètres recommandés pour démarrer :
- **Number of users** : 10-100 (nombre d'utilisateurs simultanés)
- **Spawn rate** : 5-10 (utilisateurs ajoutés par seconde)
- **Host** : `http://127.0.0.1:5000`

#### Mode ligne de commande (headless) :

```bash
locust -f locustfile.py --headless --users 50 --spawn-rate 5 --run-time 1m --host http://127.0.0.1:5000
```

### 6.3 Interpréter les résultats

Locust fournit plusieurs métriques importantes :

- **RPS (Requests Per Second)** : Nombre de requêtes par seconde
- **Response time** : Temps de réponse (min, max, moyenne, médiane)
- **Failures** : Nombre et pourcentage d'échecs
- **Users** : Nombre d'utilisateurs simulés

#### Résultats attendus :
- Temps de réponse moyen < 200ms pour les pages principales
- Taux d'échec < 1%
- Capacité à gérer 6+ utilisateurs simultanés

### 6.4 Rapport de performance

Les rapports HTML sont générés automatiquement :
- Ils sont sauvegardés dans le dossier [tests/](tests/) avec la nomenclature :  
  `Locust_YYYY-MM-DD-HHhMM_locustfile.py_http___127.0.0.1_5000.html`

Pour télécharger un rapport en cours de test via l'interface web :
1. Accédez à `http://localhost:8089`
2. Cliquez sur "Download Data" → "Download Report"

## 7. Structure du projet

```
OC_GUDLFT/
├── server.py                 # Application Flask principale
├── clubs.json               # Données des clubs
├── competitions.json        # Données des compétitions
├── requirements.txt         # Dépendances Python
├── pytest.ini              # Configuration pytest
├── locustfile.py           # Scénarios de tests de performance
├── templates/              # Templates HTML
│   ├── index.html
│   ├── welcome.html
│   └── booking.html
└── tests/                  # Suite de tests
    ├── unit/
    ├── integration/
    └── functional/
```

## 8. Fonctionnalités principales

### 8.1 Pour les clubs
- Connexion avec email
- Consultation des compétitions disponibles
- Réservation de places (max 12 places par réservation)
- Consultation du tableau des points

### 8.2 Règles métier
- Un club ne peut pas réserver plus de 12 places pour une compétition
- Un club ne peut pas réserver plus de places qu'il n'a de points disponibles
- Les réservations passées ne sont pas autorisées
- Les points sont déduits lors de chaque réservation

## 9. Développement

### 9.1 Ajouter une dépendance

```bash
pip install <package>
pip freeze > requirements.txt
```

### 9.2 Structure du code

L'application suit une architecture simple :
- Routes Flask dans [server.py](server.py)
- Templates Jinja2 dans [templates/](templates/)
- Données JSON pour le stockage

### 9.3 Mode debug

Pour activer le mode debug Flask :

```bash
flask run --debug
```

## 10. Dépannage

### Problème : Flask n'est pas reconnu
**Solution** : Vérifiez que l'environnement virtuel est activé et que Flask est installé

### Problème : Erreur de port déjà utilisé
**Solution** : Changez le port avec `flask run --port 5001`

### Problème : Tests Locust ne se connectent pas
**Solution** : Assurez-vous que le serveur Flask tourne sur le port 5000

### Problème : Import Error dans les tests
**Solution** : Exécutez pytest depuis la racine du projet

## 11. Contributions

Pour contribuer au projet :
1. Créer une branche pour votre fonctionnalité
2. Écrire des tests pour votre code
3. Vérifier que tous les tests passent
4. Soumettre une pull request

## 12. Licence

Ce projet est développé dans le cadre d'une formation OpenClassrooms.

