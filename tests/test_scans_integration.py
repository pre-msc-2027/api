import os
import pytest
from datetime import datetime, UTC
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, WriteError

pytestmark = pytest.mark.skipif(
    os.getenv("USE_ATLAS") != "1",
    reason="Set USE_ATLAS=1 to run integration tests against Atlas.",
)

def _now_iso_utc() -> str:
    return datetime.now(UTC).isoformat()

def _valid_scan_doc(scan_id: str):
    return {
        "scan_id": scan_id,
        "timestamp": _now_iso_utc(),
        "project_name": "integration-test",
        "scanned_by": "pytest",
        "scan_options": { "target_type": "repository" },
        "warnings": [],
        "ai_comments": [],
        "dependencies": [],
        "logs": [],
    }

def test_atlas_ping_and_insert_read_delete():
    load_dotenv()
    uri = os.getenv("MONGODB_URI")
    dbname = os.getenv("MONGODB_DBNAME", "Secuscan")
    assert uri, "MONGODB_URI manquant dans .env"

    client = MongoClient(uri, serverSelectionTimeoutMS=7000)

    try:
        db = client[dbname]

        pong = db.command("ping")
        assert pong.get("ok") == 1.0

        scans = db["scans"]
        scan_id = f"it_{int(datetime.now(UTC).timestamp())}"
        doc = _valid_scan_doc(scan_id)
        ins = scans.insert_one(doc)
        assert ins.inserted_id

        got = scans.find_one({"_id": ins.inserted_id})
        assert got and got["scan_id"] == scan_id
        assert got["project_name"] == "integration-test"

        scans.delete_one({"_id": ins.inserted_id})

    except ServerSelectionTimeoutError as e:
        pytest.fail(f"Connexion Atlas impossible (réseau/IP/URI ?) : {e}")
    finally:
        client.close()


def test_invalid_doc_rejected_if_schema_enabled():
    load_dotenv()
    uri = os.getenv("MONGODB_URI")
    dbname = os.getenv("MONGODB_DBNAME", "Secuscan")
    assert uri, "MONGODB_URI manquant dans .env"

    client = MongoClient(uri, serverSelectionTimeoutMS=7000)
    db = client[dbname]
    scans = db["scans"]

    bad = { "scan_id": "ONLY_ID" }

    try:
        scans.insert_one(bad)
        pytest.xfail("Validation $jsonSchema non active/strict côté Atlas (insert accepté).")
    except WriteError as e:
        assert e.details.get("code") == 121
    finally:
        client.close()