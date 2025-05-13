Durée indicative : 2h30  

L'objectif de ce test est de monter une API Dockerisée capable de :
- Enregistrer une adresse
- Consulter les risques associés

> Note : Le temps est indicatif. La qualité du code (lisibilité, structure, gestion des erreurs) prime sur la quantité.
> 

---
## 1. Choix de la stack

Vous pouvez choisir entre :

- **NestJS (TypeScript)**
    - CLI & documentation : https://docs.nestjs.com/cli/overview
    - ORM SQLite (TypeORM) : https://typeorm.io/#/
- **Django (Python 3.12)**
    - Guide de démarrage : https://docs.djangoproject.com/fr/4.2/intro/tutorial01/
    - Base SQLite (réglage `DATABASES`) : https://docs.djangoproject.com/fr/4.2/ref/settings/#databases

Ressources : Vous pouvez utiliser ChatGPT ou toute autre ressource pour vous aider.

> Note : Le choix entre NestJS et Django est libre, sans pénalité.
> 

---

## 2. Endpoints  implémenter

### 2.1 `POST /api/addresses/`

### Payload

```json
{ "q": "chaîne de recherche d'adresse" }

```

### Validation

- Le champ `"q"` doit être une chaîne de caractères non vide.
- Si le payload est invalide, retourner HTTP 400 :
    
    ```json
    {
      "error": "Le champ 'q' est requis et doit être une chaîne non vide."
    }
    
    ```
    

### Comportement

1. Appeler l'API Adresse (BAN)
    - Exemple : `GET https://api-adresse.data.gouv.fr/search/?q=8+bd+du+port&limit=1`
2. Si au moins un résultat :
    - Persister en SQLite (table `addresses` avec champs :
        
        `id`, `label`, `housenumber`, `street`, `postcode`, `citycode`, `latitude`, `longitude`)
        
    - Retourner l'objet stocké (HTTP 200 + JSON)
3. Sinon : répondre HTTP 404 sans corps
4. En cas d'erreur lors de l'appel externe ou de la connexion DB : HTTP 500
    
    ```json
    {
      "error": "Erreur serveur : impossible de contacter l'API externe."
    }
    
    ```
    

### **Format de sortie attendu**

| Code HTTP | Corps de réponse |
| --- | --- |
| **200 OK** | `{
  "id": 1,
  "label": "8 bd du Port, 56170 Sarzeau",
  "housenumber": "8",
  "street": "bd du Port",
  "postcode": "56170",
  "citycode": "56242",
  "latitude": 47.58234,
  "longitude": -2.73745
}` |
| **400 Bad Request** | `{
  "error": "Le champ 'q' est requis et doit être une chaîne non vide."
}` |
| **404 Not Found** | `{
"error": "Adresse non trouvée. Aucun résultat ne correspond à votre recherche."
}` |
| **500 Internal Server Error** | `{
  "error": "Erreur serveur : impossible de contacter l'API externe."
}` |

---

### 2.2 `GET /api/addresses/{id}/risks/`

### Paramètre

- `id` de l'adresse en base

### Comportement

1. Lire l'enregistrement (`latitude`