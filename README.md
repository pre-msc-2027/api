# 📃 Documentation de l'API – Système d'analyse de code

Cette API permet de gérer :

- des **dépôts de code source** (repositories)
- des **scans d'analyse de code** avec IA optionnelle
- des **règles d'analyse de sécurité personnalisables**

Elle est construite avec **FastAPI** et utilise **Pydantic** pour la validation de schémas.

---

## 📄 Format des objets JSON

### 📊 Scan (Analyse de projet)

#### Objet `ScanOut`

```json
{
  "scan_id": "string",
  "timestamp": "2024-07-15T12:00:00",
  "project_name": "nom_du_projet",
  "scanned_by": "alice",
  "scan_version": "1.0.0",
  "scan_options": {
    "repo_url": "https://github.com/mon/projet",
    "use_ai_assistance": true,
    "max_depth": 3,
    "follow_symlinks": false,
    "target_type": "python",
    "target_files": ["main.py", "utils.py"],
    "severity_min": "medium",
    "branch_id": "main",
    "commit_hash": "abc123"
  },
  "auth_context": {
    "user_id": "user123",
    "user_role": "admin",
    "session_id": "xyz456"
  },
  "notes": "Scan initial",
  "analysis": {
    "status": "completed",
    "summary": {
      "total_files": 25,
      "files_with_vulnerabilities": 4,
      "vulnerabilities_found": 10
    },
    "vulnerabilities": [
      {
        "file": "main.py",
        "line": 42,
        "type": "SQL Injection",
        "severity": "high",
        "description": "Entrée non filtrée",
        "recommendation": "Utiliser des requêtes paramétrées"
      }
    ],
    "warnings": [
      {
        "file": "main.py",
        "line": 58,
        "rule_id": 5,
        "id": 1,
      }
    ]
  },
  "ai_comment": [
    {
      "warning_id": 42,
      "original": "eval(user_input)",
      "fixed": "ast.literal_eval(user_input)"
    },
  ],
  "dependencies": [
    {
      "name": "requests",
      "version": "2.31.0",
      "vulnerability": {
        "cve_id": "CVE-2023-1234",
        "severity": "critical",
        "description": "Overflow dans la méthode x",
        "recommendation": "Mettre à jour"
      }
    }
  ],
  "logs": [
    {
      "timestamp": 1721500000,
      "message": "Démarrage du scan",
      "error": null
    }
  ]
}
```

### 📁 Repository

#### Objet `RepoOut`

```json
{
  "user": {
    "id": "user123",
    "email": "alice@example.com",
    "name": "Alice"
  },
  "repo_url": "https://github.com/alice/projet",
  "rules": [
    {
      "rule_id": "rule_1",
      "parameters": [
        { "name": "severity", "value": "high" }
      ]
    }
  ]
}
```

### 🔒 Rule (Règle de scan)

#### Objet `RuleOut`

```json
{
  "rule_id": "rule_1",
  "name": "No hardcoded password",
  "description": "Empêche les mots de passe en dur",
  "tags": ["security", "password"],
  "parameters": [
    {
      "type": "string",
      "name": "severity",
      "default": "high",
      "description": "Seuil de sévérité",
      "options": {"low": 1, "medium": 2, "high": 3}
    }
  ]
}
```

---

## 📑 Routes disponibles

### 📊 `/scans`

#### `GET /scans/summary/{user}`

Retourne la liste des dépôts de l'utilisateur avec le nom des scans et leur `branch_id`.

**Réponse :**

```json
[
  {
    "repo_url": "https://github.com/alice/projet",
    "analyses": [
      {"scan_id": "scan_123", "project_name": "projet", "branch_id": "main"}
    ]
  }
]
```

#### `GET /scans/{scan_id}`

Détails complets du scan (voir exemple ScanOut plus haut).

#### `GET /scans/options/{scan_id}`

Retourne uniquement les options du scan (voir `scan_options`).

#### `POST /scans/`

Crée un nouveau scan avec un json au format :
```json
{
  "project_name": "nom_du_projet",
  "scanned_by": "alice",
  "scan_version": "1.0.0",
  "scan_options": {
    "repo_url": "https://github.com/mon/projet",
    "use_ai_assistance": true,
    "max_depth": 3,
    "follow_symlinks": false,
    "target_type": "python",
    "target_files": ["main.py", "utils.py"],
    "severity_min": "medium",
    "branch_id": "main",
    "commit_hash": "abc123"
  },
  "auth_context": {
    "user_id": "user123",
    "user_role": "admin",
    "session_id": "xyz456"
  },
  "notes": "Scan initial",
}
```

#### `POST /scans/logs/{scan_id}`

Ajoute un log à un scan.

```json
{
  "timestamp": 1721500000,
  "message": "Analyse en cours",
  "error": null
}
```

#### `POST /scans/ai_comment/{scan_id}`

Ajoute un ai comment à un scan.

```json
{
  "warning_id": 42,
  "original": "eval(user_input)",
  "fixed": "ast.literal_eval(user_input)"
},
```

#### `POST /scans/analyse/{scan_id}`

Ajoute les résultats d'analyse à un scan.

#### `GET /scans/analyse_with_rules/{scan_id}`

Retourne les résultats d'analyse enrichis avec les règles associées.

```json
{
  "analysis": {
    "status": "completed",
    "summary": {
      "total_files": 10,
      "files_with_vulnerabilities": 3,
      "vulnerabilities_found": 5
    },
    "warnings": [
      {
        "file": "src/app.py",
        "line": 42,
        "rule_id": 101,
        "id": 1
      },
      {
        "file": "src/utils.py",
        "line": 12,
        "rule_id": 102,
        "id": 2
      }
    ]
  },
  "rules": [
    {
      "rule_id": "101",
      "name": "Detect SQL Injection",
      "description": "This rule flags SQL queries built using string concatenation.",
      "tags": ["security", "sql", "injection"],
      "parameters": [
        {
          "type": "string",
          "name": "pattern",
          "default": "SELECT * FROM",
          "description": "Pattern to search for in SQL strings",
          "options": {
            "case_sensitive": false
          }
        }
      ]
    },
    {
      "rule_id": "102",
      "name": "Unsafe System Call",
      "description": "Detects usage of dangerous system calls like os.system.",
      "tags": ["security", "command"],
      "parameters": []
    }
  ]
}
```

---

### 📁 `/repositories`

#### `GET /repositories/user/{user}`

Liste tous les dépôts appartenant à un utilisateur donné.

#### `POST /repositories/`

Crée un dépôt. Corps attendu : même format.

#### `GET /repositories/{repo_url}`

Retourne les informations d'un dépôt à partir de son URL.

---

### 🔒 `/rules`

#### `GET /rules/`

Liste toutes les règles enregistrées.

#### `GET /rules/{rule_id}`

Retourne une règle précise par son identifiant.

#### `POST /rules/`

Crée une règle personnalisée. Corps attendu : même format

---

# Documentation Base de Données (MongoDB Atlas)

## Vue d’ensemble
- **Serveur** : MongoDB Atlas
- **DB principale** : `Secuscan`
- **Collections** : `scans`, `rules` (optionnel : `scanned_repos`)
- **Accès** : via URI dans `.env`

## Variables d’environnement (.env)
```env
MONGODB_URI=mongodb+srv://<user>:<password>@cluster0.xxxx.mongodb.net/?retryWrites=true&w=majority
MONGODB_DBNAME=Secuscan
```
## Collections & Schémas
### Scans
Exemple de document :
```json
{
  "scan_id": "scan_001",
  "timestamp": "2025-08-25T06:30:00Z",
  "project_name": "Secuscan",
  "scanned_by": "aurore",
  "repo_url": "https://github.com/example/repo",
  "scan_options": {
    "repo_url": "https://github.com/example/repo",
    "use_ai_assistance": true,
    "max_depth": 5,
    "follow_symlinks": false,
    "target_type": "repository",
    "target_files": ["app.py", "utils/helpers.py"],
    "severity_min": "medium",
    "branch_id": "main",
    "commit_hash": "a1b2c3d4"
  },
  "analysis": {
    "status": "completed",
    "summary": {
      "total_files": 10,
      "files_with_vulnerabilities": 2,
      "vulnerabilities_found": 5
    },
    "vulnerabilities": [
      {
        "file": "app.py",
        "line": 42,
        "type": "Hardcoded secret",
        "severity": "high",
        "description": "Mot de passe en clair trouvé dans le code",
        "recommendation": "Utiliser une variable d’environnement au lieu d’un mot de passe en dur"
      }
    ]
  },
  "warnings": [
    {
      "file": "app.py",
      "line": 42,
      "rule_id": 101,
      "id": 1
    }
  ],
  "ai_comments": [
    {
      "warning_id": 1,
      "original": "password = '123456'",
      "fixed": "password = os.getenv('APP_PASSWORD')"
    },
    {
      "warning_id": 2,
      "original": "print('Erreur critique')",
      "fixed": "logging.error('Erreur critique')"
    }
  ],
  "scan_version": "1.0.0",
  "dependencies": [
    {
      "name": "requests",
      "version": "2.32.3",
      "vulnerabilities": [
        {
          "id": "CVE-2024-1234",
          "severity": "medium",
          "description": "Vulnérabilité sur les certificats SSL"
        }
      ]
    }
  ],
  "notes": "RAS",
  "auth_context": {
    "user_id": "aurorekouakou",
    "permissions": ["read", "write"]
  },
  "logs": [
    {
      "timestamp": 1724569200,
      "message": "Scan démarré",
      "error": ""
    },
    {
      "timestamp": 1724569250,
      "message": "Scan terminé",
      "error": ""
    }
  ]
}
```

Champs obligatoires :
scan_id, timestamp, project_name, scanned_by, scan_options

ai_comments[] : liste de corrections IA par warning: 
— warning_id (int) fait le lien vers warnings.id
— original, fixed : texte/code avant/après

warnings[] : issues brutes remontées par l’analyseur (fichier, ligne, règle…)

Validation MongoDB :
Activée via $jsonSchema (voir Compass > Validation).
