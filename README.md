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

#### `POST /scans/analyse/{scan_id}`

Ajoute les résultats d'analyse à un scan.

#### `GET /scans/analyse_with_rules/{scan_id}`

Retourne les résultats d'analyse enrichis avec les règles associées.

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
