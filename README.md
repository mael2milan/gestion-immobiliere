
# Gestion immobilière

Application web de gestion immobilière développée avec Python et Django.

Ce projet permet de centraliser les informations relatives aux biens immobiliers, vendeurs, acheteurs et agents, ainsi que de suivre les opérations de vente.

Il intègre également un algorithme de rapprochement permettant d'identifier les biens les plus adaptés aux critères des acheteurs.

## Fonctionnalités

- Consultation des biens immobiliers et de leurs caractéristiques
- Recherche et filtrage par commune, type et prix
- Gestion des acheteurs, vendeurs et agents immobiliers
- Suivi des étapes de vente
- Suivi des propositions, visites, offres et rendez-vous
- Recommandation de biens selon les critères des acheteurs
- Consultation des portefeuilles des agents
- Administration des données avec Django Admin
- Génération automatique de données de démonstration

## Algorithme de rapprochement

Chaque bien disponible reçoit un score de compatibilité sur 100 points selon :

| Critère | Points |
|---|---:|
| Commune | 35 |
| Budget | 30 |
| Superficie | 20 |
| Chambres | 10 |
| Garage | 5 |

Le calcul tolère certains écarts de budget et de superficie.

Les cinq meilleurs biens atteignant au moins 65 points sont proposés, uniquement lorsqu'ils sont à l'étape « Mise en vente ».

## Technologies

- Python
- Django
- SQLite
- HTML et CSS
- Git

## Installation

### 1. Cloner le dépôt

```bash
git clone URL_DU_DEPOT
cd gestion-immobiliere
```

### 2. Créer l'environnement virtuel

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Installer les dépendances

```bash
python -m pip install -r requirements.txt
```

### 4. Préparer la base de données

```bash
python manage.py migrate
```

### 5. Générer les données de démonstration

```bash
python manage.py seed_demo
```

### 6. Démarrer le serveur

```bash
python manage.py runserver
```

L'application est disponible à l'adresse :

http://127.0.0.1:8000/

## Administration

Pour créer un compte administrateur :

```bash
python manage.py createsuperuser
```

L'interface d'administration est disponible sur :

http://127.0.0.1:8000/admin/

## Tests

Pour exécuter les tests automatisés :

```bash
python manage.py test immobilier
```

Les tests couvrent notamment l'algorithme de rapprochement, les filtres, les pages de consultation et certains cas d'erreur.

## Modélisation

Le modèle logique de données est disponible dans :

`docs/mld.md`

## Contexte

Projet personnel réalisé à partir d'un cahier des charges universitaire, avec pour objectif de mettre en pratique Python, la programmation orientée objet, les bases de données relationnelles et Django.
