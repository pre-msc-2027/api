from datetime import datetime, timezone
from typing import Any, Dict, List
from mongomock import MongoClient as MockClient
import pytest

def make_scan_doc() -> Dict[str, Any]:
    now = datetime.now(timezone.utc)
    ts = now.isoformat().replace("+00:00", "Z")
    return {
        "scan_id": f"unit_{int(now.timestamp())}",
        "timestamp": ts,
        "project_name": "unit-project",
        "scanned_by": "unit-test",
        "repo_url": "https://github.com/example/repo",
        "scan_options": {
            "repo_url": "https://github.com/example/repo",
            "use_ai_assistance": True,
            "max_depth": 3,
            "follow_symlinks": False,
            "target_type": "repository",
            "target_files": ["app.py", "utils/helpers.py"],
            "severity_min": "medium",
            "branch_id": "main",
            "commit_hash": "abc123",
        },
        "analysis": {
            "status": "completed",
            "summary": {
                "total_files": 10,
                "files_with_vulnerabilities": 1,
                "vulnerabilities_found": 2,
            },
            "vulnerabilities": [
                {
                    "file": "app.py",
                    "line": 42,
                    "type": "HardcodedCredentials",
                    "severity": "high",
                    "description": "Password hardcoded.",
                    "recommendation": "Use env vars / secrets manager.",
                }
            ],
        },
        "warnings": [
            {"file": "index.html", "line": 5, "rule_id": 101, "id": 1},
        ],
        "ai_comments": [
            {
                "warning_id": 1,
                "original": '<link Rel="stylesheet">',
                "fixed": '<link rel="stylesheet" href="../src/css/components.css">',
            }
        ],
        "scan_version": "1.0.0",
        "dependencies": [
            {
                "name": "flask",
                "version": "2.3.0",
                "vulnerabilities": [
                    {"id": "CVE-2024-0001", "severity": "medium", "description": "Example"}
                ],
            }
        ],
        "notes": "RAS",
        "auth_context": {"user_id": "user-123", "permissions": ["read", "write"]},
        "logs": [
            {"timestamp": int(now.timestamp()), "message": "Scan start", "error": ""},
            {"timestamp": int(now.timestamp()), "message": "Scan end", "error": ""},
        ],
    }

REQUIRED_TOP_LEVEL = [
    "scan_id", "timestamp", "project_name", "scanned_by", "scan_options",
]

def validate_scan_shape(doc: Dict[str, Any]) -> None:
    for key in REQUIRED_TOP_LEVEL:
        assert key in doc, f"champ manquant: {key}"

    # types de base
    assert isinstance(doc["scan_id"], str)
    assert isinstance(doc["timestamp"], str)
    assert isinstance(doc["project_name"], str)
    assert isinstance(doc["scanned_by"], str)
    assert isinstance(doc["scan_options"], dict)

    # sous-objets clés si présents
    if "analysis" in doc:
        a = doc["analysis"]
        assert isinstance(a, dict)
        if "summary" in a:
            s = a["summary"]
            assert isinstance(s, dict)
            for k in ("total_files", "files_with_vulnerabilities", "vulnerabilities_found"):
                assert isinstance(s.get(k, 0), int)

    if "warnings" in doc:
        w = doc["warnings"]
        assert isinstance(w, list)
        for item in w:
            assert isinstance(item, dict)
            assert isinstance(item.get("line", 0), int)

    if "ai_comments" in doc:
        ac = doc["ai_comments"]
        assert isinstance(ac, list)
        for item in ac:
            assert isinstance(item, dict)
            assert isinstance(item.get("warning_id", 0), int)
            assert isinstance(item.get("original", ""), str)
            assert isinstance(item.get("fixed", ""), str)

@pytest.fixture()
def mock_db():
    client = MockClient()
    db = client["Secuscan"]
    yield db
    client.close()

def test_insert_and_read_scan(mock_db):
    scans = mock_db["scans"]
    doc = make_scan_doc()

    validate_scan_shape(doc)

    ins = scans.insert_one(doc)
    assert ins.inserted_id is not None

    found = scans.find_one({"_id": ins.inserted_id})
    assert found is not None
    assert found["scan_id"].startswith("unit_")
    assert found["project_name"] == "unit-project"

    validate_scan_shape(found)