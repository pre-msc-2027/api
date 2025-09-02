from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
from fastapi.middleware.cors import CORSMiddleware
import time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory database
fake_repos_db: Dict[str, List[Dict]] = {}  # username -> list of repos
fake_scans_db: Dict[str, Dict] = {}  # key = scan_id, value = scan object


class RepoPayload(BaseModel):
    username: str
    repo_url: str
    name: str
    rules: List[str] = []
    branches: List[str] = []  # <-- include branches in payload


class ScanOptions(BaseModel):
    repo_url: str
    use_ai_assistance: bool = True
    max_depth: int = 3
    follow_symlinks: bool = False
    target_type: str = "python"
    target_files: List[str] = []
    severity_min: str = "medium"
    branch_id: str
    commit_hash: Optional[str] = None


class AuthContext(BaseModel):
    user_id: str
    user_role: str
    session_id: str


class NewScanPayload(BaseModel):
    project_name: str
    scanned_by: str
    scan_version: str = "1.0.0"
    scan_options: ScanOptions
    auth_context: AuthContext
    notes: Optional[str] = ""


@app.get("/repositories/user/{username}")
def get_user_repos(username: str):
    return fake_repos_db.get(username, [])


@app.post("/repositories/")
def add_repo(payload: RepoPayload):
    if payload.username not in fake_repos_db:
        fake_repos_db[payload.username] = []

    # check if repo already exists
    for r in fake_repos_db[payload.username]:
        if r["repo_url"] == payload.repo_url:
            raise HTTPException(status_code=400, detail="Repo already added")

    fake_repos_db[payload.username].append({
        "name": payload.name,
        "repo_url": payload.repo_url,
        "rules": payload.rules,
        "branches": payload.branches  # store branches directly
    })
    return {"message": "Repo saved successfully", "repo": payload.dict()}


@app.get("/auth/repos/{repo_name}/branches")
def get_branches(repo_name: str):
    # simulate branches per repo
    branches_map = {
        "School_manager": ["main", "develop"],
        "AdventureQuest": ["main", "feature/quests"],
        "Career-Quest": ["main", "feature/login"]
    }
    return branches_map.get(repo_name, ["main"])


@app.post("/scans/")
def create_scan(payload: NewScanPayload):
    scan_id = f"{int(time.time() * 1000)}"
    fake_scans_db[scan_id] = {
        "scan_id": scan_id,
        "project_name": payload.project_name,
        "scanned_by": payload.scanned_by,
        "scan_version": payload.scan_version,
        "scan_options": payload.scan_options.dict(),
        "auth_context": payload.auth_context.dict(),
        "notes": payload.notes,
        "status": "pending",
        "logs": [],
        "ai_comments": [],
        "analysis_results": None
    }
    return {"message": "Scan created successfully", "scan_id": scan_id}


@app.get("/scans/summary/{username}")
def get_scans_summary(username: str):
    summary = []
    for scan in fake_scans_db.values():
        if scan["scanned_by"] == username:
            repo_entry = next((s for s in summary if s["repo_url"] == scan["scan_options"]["repo_url"]), None)
            if repo_entry:
                repo_entry["analyses"].append({
                    "scan_id": scan["scan_id"],
                    "project_name": scan["project_name"],
                    "branch_id": scan["scan_options"]["branch_id"]
                })
            else:
                summary.append({
                    "repo_url": scan["scan_options"]["repo_url"],
                    "analyses": [{
                        "scan_id": scan["scan_id"],
                        "project_name": scan["project_name"],
                        "branch_id": scan["scan_options"]["branch_id"]
                    }]
                })
    return summary


class LogPayload(BaseModel):
    timestamp: int
    message: str
    error: Optional[str] = None


@app.post("/scans/logs/{scan_id}")
def add_scan_log(scan_id: str, payload: LogPayload):
    scan = fake_scans_db.get(scan_id)
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    scan["logs"].append(payload.dict())
    return {"message": "Log added"}


class AICommentPayload(BaseModel):
    warning_id: int
    original: str
    fixed: str


@app.post("/scans/ai_comment/{scan_id}")
def add_ai_comment(scan_id: str, payload: AICommentPayload):
    scan = fake_scans_db.get(scan_id)
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    scan["ai_comments"].append(payload.dict())
    return {"message": "AI comment added"}


class AnalysePayload(BaseModel):
    status: str
    summary: Dict
    warnings: List[Dict]


@app.post("/scans/analyse/{scan_id}")
def add_analysis(scan_id: str, payload: AnalysePayload):
    scan = fake_scans_db.get(scan_id)
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    scan["analysis_results"] = payload.dict()
    return {"message": "Analysis added"}


@app.get("/rules/")
def get_rules():
    """Récupère toutes les règles disponibles"""
    rules = [
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
        },
        {
            "rule_id": "rule_2",
            "name": "SQL Injection Detection",
            "description": "Détecte les vulnérabilités d'injection SQL",
            "tags": ["security", "sql", "injection"],
            "parameters": [
                {
                    "type": "string",
                    "name": "severity",
                    "default": "critical",
                    "description": "Niveau de sévérité",
                    "options": {"low": 1, "medium": 2, "high": 3, "critical": 4}
                },
                {
                    "type": "boolean",
                    "name": "check_prepared_statements",
                    "default": True,
                    "description": "Vérifier les requêtes préparées"
                }
            ]
        },
        {
            "rule_id": "rule_3",
            "name": "Insecure Random Generator",
            "description": "Détecte l'utilisation de générateurs aléatoires non sécurisés",
            "tags": ["security", "crypto", "random"],
            "parameters": [
                {
                    "type": "string",
                    "name": "severity",
                    "default": "medium",
                    "description": "Niveau de sévérité",
                    "options": {"low": 1, "medium": 2, "high": 3}
                }
            ]
        },
        {
            "rule_id": "rule_4",
            "name": "Unsafe File Operations",
            "description": "Détecte les opérations de fichiers dangereuses",
            "tags": ["security", "filesystem", "path-traversal"],
            "parameters": [
                {
                    "type": "string",
                    "name": "severity",
                    "default": "high",
                    "description": "Niveau de sévérité",
                    "options": {"low": 1, "medium": 2, "high": 3}
                },
                {
                    "type": "integer",
                    "name": "max_depth",
                    "default": 5,
                    "description": "Profondeur maximale d'analyse"
                }
            ]
        },
        {
            "rule_id": "rule_5",
            "name": "Weak Cryptography",
            "description": "Détecte l'utilisation d'algorithmes cryptographiques faibles",
            "tags": ["security", "crypto", "encryption"],
            "parameters": [
                {
                    "type": "string",
                    "name": "severity",
                    "default": "high",
                    "description": "Niveau de sévérité",
                    "options": {"low": 1, "medium": 2, "high": 3}
                },
                {
                    "type": "string",
                    "name": "min_key_size",
                    "default": "2048",
                    "description": "Taille minimale de clé en bits"
                }
            ]
        }
    ]
    return rules


@app.get("/scans/{scan_id}")
def get_scan_details(scan_id: str):
    """Récupère les détails d'un scan spécifique"""
    print(f"scan_id reçu par FastAPI: '{scan_id}'")
    # Mock data pour les scans
    mock_scans = {
        "1756669205725": {
            "scan_id": "scan_123",
            "timestamp": "2024-07-15T12:00:00",
            "project_name": "Security Scanner Project",
            "scanned_by": "alice",
            "scan_version": "1.0.0",
            "scan_options": {
                "repo_url": "https://github.com/pre-msc-2027/api",
                "use_ai_assistance": True,
                "max_depth": 3,
                "follow_symlinks": False,
                "target_type": "python",
                "target_files": ["api.py", "utils.py"],
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
                        "file": "api.py",
                        "line": 42,
                        "type": "SQL Injection",
                        "severity": "high",
                        "description": "Entrée non filtrée",
                        "recommendation": "Utiliser des requêtes paramétrées"
                    }
                ],
                "warnings": [
                    {
                        "file": "api.py",
                        "line": 58,
                        "rule_id": 5,
                        "id": 1
                    }
                ]
            },
            "ai_comment": [
                {
                    "warning_id": 42,
                    "original": "eval(user_input)",
                    "fixed": "ast.literal_eval(user_input)"
                }
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
                    "error": 1
                },
                {
                    "timestamp": 1721500000,
                    "message": "Démarrage du scan",
                    "error": 2
                },
                {
                    "timestamp": 1721500000,
                    "message": "Démarrage du scan",
                    "error": 0
                }
            ]
        },
        "1756727909839": {
            "scan_id": "scan_1232",
            "timestamp": "2024-07-16T12:00:00",
            "project_name": "Second Project",
            "scanned_by": "alice",
            "scan_version": "1.0.0",
            "scan_options": {
                "repo_url": "https://github.com/pre-msc-2027/api",
                "use_ai_assistance": False,
                "max_depth": 2,
                "follow_symlinks": True,
                "target_type": "python",
                "target_files": ["app.py"],
                "severity_min": "low",
                "branch_id": "develop",
                "commit_hash": "def456"
            },
            "auth_context": {
                "user_id": "user123",
                "user_role": "admin",
                "session_id": "xyz456"
            },
            "notes": "Second scan test",
            "analysis": {
                "status": "completed",
                "summary": {
                    "total_files": 12,
                    "files_with_vulnerabilities": 2,
                    "vulnerabilities_found": 3
                },
                "vulnerabilities": [],
                "warnings": []
            },
            "ai_comment": [],
            "dependencies": [],
            "logs": [
                {
                    "timestamp": 1721500000,
                    "message": "Démarrage du scan",
                    "error": 0
                },
                {
                    "timestamp": 1721500002,
                    "message": "test du scan",
                    "error": 1
                }, {
                    "timestamp": 1721500003,
                    "message": "aaa du scan",
                    "error": 2
                }
            ]
        }
    }

    scan = mock_scans.get(scan_id)
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")

    return scan


@app.get("/scans/analyse_with_rules/{scan_id}")
def get_scan_details(scan_id: str):
    # Mock data pour les scans groupés par scan_id
    mock_scans = {
        "1756727909839": {
            "analysis": {
                "status": "completed",
                "summary": {
                    "total_files": 15,
                    "files_with_vulnerabilities": 5,
                    "vulnerabilities_found": 12
                },
                "warnings": [
                    {"file": "src/app.py", "line": 42, "rule_id": 101, "id": 1},
                    {"file": "src/utils.py", "line": 12, "rule_id": 102, "id": 2},
                    {"file": "src/auth.py", "line": 23, "rule_id": 103, "id": 3},
                    {"file": "src/database.py", "line": 67, "rule_id": 101, "id": 4},
                    {"file": "src/api.py", "line": 89, "rule_id": 104, "id": 5},
                    {"file": "src/models.py", "line": 34, "rule_id": 103, "id": 7},
                    {"file": "src/helpers.py", "line": 56, "rule_id": 102, "id": 9},
                    {"file": "src/validators.py", "line": 91, "rule_id": 104, "id": 11},
                ]
            },
            "rules": [
                {
                    "rule_id": "101",
                    "name": "SQL Injection Detection",
                    "description": "Flags SQL queries built using string concatenation.",
                    "tags": ["security", "sql", "injection"],
                    "parameters": [
                        {
                            "type": "string",
                            "name": "pattern",
                            "default": "SELECT * FROM",
                            "description": "Pattern to search for in SQL strings",
                            "options": {"case_sensitive": False}
                        }
                    ]
                },
                {
                    "rule_id": "102",
                    "name": "Unsafe System Call",
                    "description": "Detects usage of dangerous system calls like os.system.",
                    "tags": ["security", "command"],
                    "parameters": []
                },
                {
                    "rule_id": "103",
                    "name": "Hardcoded Secrets",
                    "description": "Detects hardcoded passwords, API keys, and secrets.",
                    "tags": ["security", "secrets", "credentials"],
                    "parameters": [
                        {
                            "type": "integer",
                            "name": "min_length",
                            "default": 8,
                            "description": "Minimum length for secret detection"
                        }
                    ]
                },
                {
                    "rule_id": "104",
                    "name": "Cross-Site Scripting (XSS)",
                    "description": "Identifies potential XSS vulnerabilities in web applications.",
                    "tags": ["security", "web", "xss"],
                    "parameters": []
                },
                {
                    "rule_id": "105",
                    "name": "Insecure Random Generator",
                    "description": "Flags usage of weak random number generators.",
                    "tags": ["security", "cryptography", "random"],
                    "parameters": []
                },
                {
                    "rule_id": "106",
                    "name": "Path Traversal",
                    "description": "Detects potential directory traversal vulnerabilities.",
                    "tags": ["security", "file", "traversal"],
                    "parameters": []
                },
                {
                    "rule_id": "107",
                    "name": "Weak Encryption",
                    "description": "Identifies usage of deprecated encryption algorithms.",
                    "tags": ["security", "cryptography", "encryption"],
                    "parameters": [
                        {
                            "type": "array",
                            "name": "weak_algorithms",
                            "default": ["MD5", "SHA1", "DES"],
                            "description": "List of weak encryption algorithms to detect"
                        }
                    ]
                }
            ]
        },
        "scan_002": {
            "analysis": {
                "status": "completed",
                "summary": {
                    "total_files": 8,
                    "files_with_vulnerabilities": 3,
                    "vulnerabilities_found": 7
                },
                "warnings": [
                    {"file": "backend/server.js", "line": 25, "rule_id": 201, "id": 1},
                    {"file": "backend/routes.js", "line": 67, "rule_id": 202, "id": 2},
                    {"file": "frontend/login.js", "line": 34, "rule_id": 203, "id": 3},
                    {"file": "backend/auth.js", "line": 12, "rule_id": 201, "id": 4},
                    {"file": "utils/crypto.js", "line": 45, "rule_id": 204, "id": 5},
                    {"file": "config/database.js", "line": 78, "rule_id": 202, "id": 6},
                ]
            },
            "rules": [
                {
                    "rule_id": "201",
                    "name": "NoSQL Injection",
                    "description": "Detects potential NoSQL injection vulnerabilities.",
                    "tags": ["security", "nosql", "injection"],
                    "parameters": []
                },
                {
                    "rule_id": "202",
                    "name": "CORS Misconfiguration",
                    "description": "Identifies insecure CORS configuration patterns.",
                    "tags": ["security", "web", "cors"],
                    "parameters": []
                },
                {
                    "rule_id": "203",
                    "name": "Weak Authentication",
                    "description": "Flags weak authentication mechanisms.",
                    "tags": ["security", "authentication"],
                    "parameters": []
                },
                {
                    "rule_id": "204",
                    "name": "Insecure Cryptographic Storage",
                    "description": "Detects insecure storage of cryptographic materials.",
                    "tags": ["security", "cryptography", "storage"],
                    "parameters": []
                },
                {
                    "rule_id": "205",
                    "name": "Information Disclosure",
                    "description": "Identifies potential information leakage vulnerabilities.",
                    "tags": ["security", "disclosure", "privacy"],
                    "parameters": []
                }
            ]
        },
        "1756727574071": {
            "analysis": {
                "status": "completed",
                "summary": {
                    "total_files": 22,
                    "files_with_vulnerabilities": 8,
                    "vulnerabilities_found": 18
                },
                "warnings": [
                    {"file": "api/user.py", "line": 156, "rule_id": 301, "id": 1},
                    {"file": "api/admin.py", "line": 89, "rule_id": 302, "id": 2},
                    {"file": "core/security.py", "line": 45, "rule_id": 303, "id": 3},
                    {"file": "models/user.py", "line": 23, "rule_id": 301, "id": 4},
                    {"file": "utils/validator.py", "line": 67, "rule_id": 304, "id": 5},
                    {"file": "core/middleware.py", "line": 78, "rule_id": 303, "id": 8}
                ]
            },
            "rules": [
                {
                    "rule_id": "301",
                    "name": "Buffer Overflow Risk",
                    "description": "Detects potential buffer overflow vulnerabilities.",
                    "tags": ["security", "memory", "overflow"],
                    "parameters": []
                },
                {
                    "rule_id": "302",
                    "name": "Information Leakage",
                    "description": "Identifies code that may leak sensitive information.",
                    "tags": ["security", "privacy", "logging"],
                    "parameters": []
                },
                {
                    "rule_id": "303",
                    "name": "Race Condition",
                    "description": "Detects potential race condition vulnerabilities.",
                    "tags": ["security", "concurrency", "threading"],
                    "parameters": []
                },
                {
                    "rule_id": "304",
                    "name": "Input Validation Bypass",
                    "description": "Flags insufficient input validation mechanisms.",
                    "tags": ["security", "validation", "input"],
                    "parameters": []
                },
                {
                    "rule_id": "305",
                    "name": "Session Fixation",
                    "description": "Detects session fixation vulnerabilities.",
                    "tags": ["security", "session", "authentication"],
                    "parameters": []
                },
                {
                    "rule_id": "306",
                    "name": "Privilege Escalation",
                    "description": "Identifies potential privilege escalation risks.",
                    "tags": ["security", "authorization", "privilege"],
                    "parameters": []
                },
                {
                    "rule_id": "307",
                    "name": "Insecure Deserialization",
                    "description": "Flags insecure object deserialization practices.",
                    "tags": ["security", "serialization", "deserialization"],
                    "parameters": []
                },
                {
                    "rule_id": "308",
                    "name": "File Upload Vulnerability",
                    "description": "Detects insecure file upload implementations.",
                    "tags": ["security", "file", "upload"],
                    "parameters": []
                }
            ]
        }
    }

    scan = mock_scans.get(scan_id)
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")

    return scan