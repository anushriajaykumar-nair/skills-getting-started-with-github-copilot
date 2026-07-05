from fastapi.testclient import TestClient

import src.app as app_module


client = TestClient(app_module.app)


def test_unregister_participant_removes_email_from_activity():
    activity_name = "Chess Club"
    participant_email = "michael@mergington.edu"
    original_participants = app_module.activities[activity_name]["participants"][:]

    try:
        response = client.delete(
            f"/activities/{activity_name}/participants/{participant_email}"
        )

        assert response.status_code == 200
        assert "Unregistered" in response.json()["message"]

        refreshed = client.get("/activities")
        activity = refreshed.json()[activity_name]
        assert participant_email not in activity["participants"]
    finally:
        app_module.activities[activity_name]["participants"] = original_participants
