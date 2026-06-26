from src.app import activities


def test_root_redirects_to_static_index(client):
    response = client.get("/", follow_redirects=False)

    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_expected_structure(client):
    response = client.get("/activities")

    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]
    assert isinstance(data["Chess Club"]["participants"], list)


def test_signup_adds_participant(client):
    new_email = "newstudent@mergington.edu"

    response = client.post("/activities/Chess%20Club/signup", params={"email": new_email})

    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {new_email} for Chess Club"
    assert new_email in activities["Chess Club"]["participants"]


def test_signup_duplicate_participant_returns_400(client):
    existing_email = "michael@mergington.edu"

    response = client.post("/activities/Chess%20Club/signup", params={"email": existing_email})

    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"


def test_signup_unknown_activity_returns_404(client):
    response = client.post("/activities/Unknown%20Club/signup", params={"email": "a@mergington.edu"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_removes_participant(client):
    existing_email = "michael@mergington.edu"

    response = client.delete("/activities/Chess%20Club/participants", params={"email": existing_email})

    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {existing_email} from Chess Club"
    assert existing_email not in activities["Chess Club"]["participants"]


def test_unregister_unknown_activity_returns_404(client):
    response = client.delete("/activities/Unknown%20Club/participants", params={"email": "a@mergington.edu"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_missing_participant_returns_404(client):
    response = client.delete(
        "/activities/Chess%20Club/participants", params={"email": "not-enrolled@mergington.edu"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"
