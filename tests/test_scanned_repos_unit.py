from mongomock import MongoClient as MockClient

def test_scanned_repos_insert_and_link():
    db = MockClient()['Secuscan']
    scanned = db['scanned_repos']

    doc = {
        "user": {"id": "u-1", "email": "user@example.com", "name": "Aurore"},
        "repo_url": "https://github.com/example/repo",
        "rules": [
            {
                "rule_id": "R-CASING-001",
                "parameters": [
                    {"name": "target_casing", "value": "snake_case"},
                    {"name": "ignore_test_files", "value": True}
                ]
            }
        ]
    }
    ins = scanned.insert_one(doc)
    got = scanned.find_one({"_id": ins.inserted_id})
    assert got["user"]["id"] == "u-1"
    assert got["rules"][0]["rule_id"] == "R-CASING-001"
    assert isinstance(got["rules"][0]["parameters"], list)