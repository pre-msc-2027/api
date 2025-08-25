from mongomock import MongoClient as MockClient

def test_rules_minimal_insert():
    db = MockClient()['Secuscan']
    rules = db['rules']
    doc = {
        "rule_id": "R-CASING-001",
        "name": "Casing des identifiants",
        "description": "Impose un style de casse.",
        "tags": ["style", "readability"],
        "parameters": [
            {
                "type": "enum",
                "name": "target_casing",
                "default": "snake_case",
                "description": "Style attendu",
                "options": {"allowed": ["snake_case", "camelCase", "PascalCase", "kebab-case"]}
            }
        ]
    }
    ins = rules.insert_one(doc)
    got = rules.find_one({"_id": ins.inserted_id})
    assert got["rule_id"] == "R-CASING-001"
    assert isinstance(got["parameters"], list)
