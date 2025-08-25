import os
from datetime import datetime, timezone
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import PyMongoError

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
MONGODB_DBNAME = os.getenv("MONGODB_DBNAME", "Secuscan")

if not MONGODB_URI:
    raise SystemExit("MONGODB_URI manquant dans .env")

print("Connexion à MongoDB…")
client = MongoClient(MONGODB_URI)
db = client[MONGODB_DBNAME]

try:
    # 1) ping
    db.command("ping")
    print(f"Connecté à la base: {MONGODB_DBNAME}")

    # 2) insertion minimale dans 'scans' (safe: champ scan_id unique pour ce test)
    coll = db["scans"]
    doc = {
        "scan_id": f"test_{datetime.now(timezone.utc).timestamp():.0f}",
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "project_name": "dry-run",
        "scanned_by": "local-test",
        "scan_options": {"target_type": "repository"},
    }
    ins = coll.insert_one(doc)
    print(f"Insert OK, _id={ins.inserted_id}")

    # 3) lecture
    found = coll.find_one({"_id": ins.inserted_id})
    print("Lecture OK:", {"scan_id": found["scan_id"], "project_name": found["project_name"]})

    # 4) (optionnel) nettoyage
    # coll.delete_one({"_id": ins.inserted_id})
    # print("Doc supprimé (nettoyage)")

except PyMongoError as e:
    print("Erreur MongoDB:", e)
finally:
    client.close()
    print("Connexion fermée")