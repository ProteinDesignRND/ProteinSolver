import pytest
from fastapi.testclient import TestClient
from apps.backend.main import app

client = TestClient(app)

def test_api_health():
    res = client.get("/api/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "healthy"
    assert data["model_loaded"] is True
    assert data["parameter_count"] == 567060

def test_api_model():
    res = client.get("/api/model")
    assert res.status_code == 200
    data = res.json()
    assert data["model_name"] == "ProteinSolver"
    assert data["model_class"] == "ProteinNet"
    assert data["architecture"] == "4-block EdgeConv Residual GNN"
    assert data["checkpoint_loaded"] is True
    assert data["parameter_count"] == 567060

def test_api_examples():
    res = client.get("/api/examples")
    assert res.status_code == 200
    examples = res.json()
    assert len(examples) >= 1
    assert any(ex["id"] == "1n5uA03" for ex in examples)

def test_api_example_pdb():
    res = client.get("/api/examples/1n5uA03")
    assert res.status_code == 200
    data = res.json()
    assert "ATOM" in data["pdb_content"]
    assert data["id"] == "1n5uA03"

def test_api_validate_valid(example_1n5u_pdb):
    res = client.post("/api/validate", json={"pdb_content": example_1n5u_pdb})
    assert res.status_code == 200
    data = res.json()
    assert data["valid"] is True
    assert len(data["chains"]) == 1
    assert data["chains"][0]["chain_id"] == "A"
    assert data["chains"][0]["residue_count"] == 92

def test_api_validate_invalid():
    res = client.post("/api/validate", json={"pdb_content": "NOT A PDB FILE"})
    assert res.status_code == 200
    data = res.json()
    assert data["valid"] is False
    assert "error" in data

def test_api_design(example_1n5u_pdb):
    # Verify extra fields (e.g. native_sequence) are rejected by contract
    res_extra = client.post(
        "/api/design",
        json={"pdb_content": example_1n5u_pdb, "native_sequence": "AAAA"},
    )
    assert res_extra.status_code == 422

    # Verify unsupported strategy is rejected
    res_strat = client.post(
        "/api/design",
        json={"pdb_content": example_1n5u_pdb, "strategy": "unsupported"},
    )
    assert res_strat.status_code == 422

    # Verify non-positive temperature is rejected
    res_temp = client.post(
        "/api/design",
        json={"pdb_content": example_1n5u_pdb, "temperature": 0.0},
    )
    assert res_temp.status_code == 422

    res = client.post(
        "/api/design",
        json={
            "pdb_content": example_1n5u_pdb,
            "chain_id": "A",
            "strategy": "map",
            "temperature": 1.0,
        },
    )
    assert res.status_code == 200
    data = res.json()
    assert data["length"] == 92
    assert len(data["sequence"]) == 92
    assert data["strategy"] == "map"
    assert data["mode"] == "DESIGN_ALL_MASKED"
    assert 0.0 <= data["mean_confidence"] <= 1.0

def test_api_diagnostic(example_1n5u_pdb):
    # Verify extra fields are rejected
    res_extra = client.post(
        "/api/diagnostic",
        json={"pdb_content": example_1n5u_pdb, "extra_field": "forbidden"},
    )
    assert res_extra.status_code == 422

    res = client.post(
        "/api/diagnostic",
        json={
            "pdb_content": example_1n5u_pdb,
            "chain_id": "A",
            "strategy": "map",
            "temperature": 1.0,
        },
    )
    assert res.status_code == 200
    data = res.json()
    assert data["recovery_percentage"] == 41.30
    assert data["matches"] == 38
    assert data["total_residues"] == 92
    assert "disclaimer" in data
