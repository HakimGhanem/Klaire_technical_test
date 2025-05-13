# Klaire Technical Test – API Adresses & Risques

## Objectif

API Dockerisée permettant :
- d'enregistrer une adresse via l'API BAN,
- de consulter les risques associés via l'API Géorisques.

---

## Démarrage rapide

### 1. Cloner le dépôt

```bash
git clone https://github.com/HakimGhanem/Klaire_technical_test.git
cd Klaire_technical_test
```

> **Remarque :** L'application nécessite un accès internet aux API publiques suivantes :
> - [API Adresse (BAN)](https://api-adresse.data.gouv.fr/)
> - [API Géorisques](https://georisques.gouv.fr/)
>
> Assurez-vous que votre environnement réseau permet d'accéder à ces services pour le bon fonctionnement de l'application.

### 2. Variables d'environnement

Copiez le fichier `.env.example` en `.env` si besoin :

```bash
cp .env.example .env
```

### 3. Lancer avec Docker Compose

```bash
docker compose build
docker compose up
```

L'API sera disponible sur [http://localhost:8000]

---

## Endpoints

### 1. Enregistrer une adresse

**POST** `/api/addresses/`

**Payload :**
```json
{ "q": "8 bd du Port, 56170 Sarzeau" }
```

**Réponses :**
- `200 OK` : adresse enregistrée
- `400 Bad Request` : champ `q` manquant ou vide
- `404 Not Found` : adresse non trouvée
- `500 Internal Server Error` : erreur externe

### 2. Consulter les risques

**GET** `/api/addresses/{id}/risks/`

**Réponses :**
- `200 OK` : JSON complet de Géorisques
- `404 Not Found` : adresse non trouvée
- `500 Internal Server Error` : erreur externe

---

## Variables d'environnement

- `DATABASE_URL=sqlite:////data/db.sqlite`

---

## Tests

Des tests unitaires sont présents dans `addresses/tests.py` pour garantir le bon fonctionnement de l'API.

### Lancer les tests

En local (dans le venv) :
```bash
python manage.py test addresses
```

Ou via Docker Compose :
```bash
docker compose run web python manage.py test addresses
```

### Couverture des tests

- **Création d'une adresse valide** : Vérifie qu'une adresse réelle est bien enregistrée et retournée.
- **Validation du champ `q`** :
  - Test si le champ `q` est manquant (erreur 400)
  - Test si le champ `q` est vide (erreur 400)
- **Adresse non trouvée** : Vérifie qu'une recherche d'adresse improbable retourne une erreur 404.
- **Consultation des risques** :
  - Pour une adresse existante (vérifie le code HTTP, dépend de l'API externe)
  - Pour une adresse inexistante (erreur 404)
- **Double création** : Vérifie que deux adresses identiques peuvent être créées (pas de contrainte d'unicité dans le modèle).

Chaque test vérifie le code de retour HTTP et la présence des champs attendus dans la réponse JSON.

---

## Interface web

Une interface simple est disponible sur [http://localhost:8000/](http://localhost:8000/) pour tester les endpoints.

---

## Structure du projet

- `klaire_api/` : projet Django principal
- `addresses/` : app Django pour la gestion des adresses et risques
- `Dockerfile`, `docker-compose.yml` : conteneurisation
- `requirements.txt` : dépendances Python
- `.env.example` : exemple de configuration

---

## Futures évolutions possibles

Voici quelques pistes d'amélioration pour aller plus loin :

- **Ajouter un front-end moderne** :
  - Développer une interface utilisateur complète (React, Vue, Angular, etc.) pour une meilleure expérience.
  - Permettre la gestion des adresses, la visualisation des risques sur une carte, etc.

- **Suggestions d'adresses avancées** :
  - Intégrer une API de suggestions d'adresses (ex : Google Places, Algolia Places, ou l'autocomplétion de l'API BAN).
  - Afficher une liste de choix lors de la saisie (ex : "118 bd Gabriel Péri" → choix entre Champigny, Rosny, etc.).

- **Sécurité et robustesse** :
  - Ajouter des timeouts, gestion avancée des erreurs, monitoring.
  - Authentification (JWT, OAuth) pour sécuriser l'API.

- **Tests avancés** :
  - Couverture de tests plus large (tests d'intégration, tests front-end).

- **Déploiement** :
  - Automatiser le déploiement (CI/CD), héberger sur un cloud public.

- **Documentation interactive** :
  - Ajouter une documentation Swagger/OpenAPI générée automatiquement.

N'hésitez pas à forker ce projet et à proposer vos propres évolutions !

---

