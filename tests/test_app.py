import sys
from pathlib import Path

from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from app import app

client = TestClient(app)


def test_signup_rejects_duplicate_participant():
    response = client.post(
        "/activities/Chess Club/signup?email=michael@mergington.edu"
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_unregister_removes_existing_participant():
    client.post("/activities/Chess Club/signup?email=test@mergington.edu")

    response = client.delete("/activities/Chess Club/unregister?email=test@mergington.edu")

    assert response.status_code == 200
    assert response.json()["message"] == "Removed test@mergington.edu from Chess Club"

    activities_response = client.get("/activities")
    assert "test@mergington.edu" not in activities_response.json()["Chess Club"]["participants"]
