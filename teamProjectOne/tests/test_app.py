def test_homepage_success(client, mocker):

    mocker.patch("app.cursor.execute")
    mocker.patch("app.cursor.fetchone", return_value={"game_id": 1})
    mocker.patch("app.cursor.fetchall", side_effect=[
        [{"score_id": 1, "username": "TestUser", "score": 123}],
        [{"game_name": "game1"}]
    ])

    response = client.get("/")
    assert response.status_code == 200
    assert b"TestUser" in response.data


def test_submit_score_valid(client, mocker):
    mock_cursor = mocker.patch("app.cursor")
    mock_cursor.execute.return_value = None
    mock_cursor.fetchone.side_effect = [None, {"game_id": 1}]
    mock_cursor.lastrowid = 101

    response = client.post("/submit", data={
        "name": "Player1",
        "score": "200",
        "game": "game1"
    })

    assert response.status_code == 302


def test_submit_score_invalid(client):
    response = client.post("/submit", data={
        "name": "",
        "score": "abc",
        "game": "game1"
    })
    assert response.status_code == 400
    assert b"Invalid name or score" in response.data

def test_leaderboard_get_success(client, mocker):
    mocker.patch("app.cursor.execute")
    mocker.patch("app.cursor.fetchone", return_value={"game_id": 1})
    mocker.patch("app.cursor.fetchall", return_value=[
        {"username": "TestUser", "score": 300}
    ])

    response = client.get("/api/leaderboard?game=game1")
    assert response.status_code == 200
    assert response.json == {
        "game": "game1",
        "leaderboard": [{"username": "TestUser", "score": 300}]
    }


def test_leaderboard_post_add_game(client, mocker):
    mocker.patch("app.cursor.execute")
    mocker.patch("app.cursor.fetchone", return_value=None)
    mocker.patch("app.db.commit")

    response = client.post("/api/leaderboard", json={"game_name": "newgame"})
    assert response.status_code == 201
    assert response.json["message"] == "Game 'newgame' added successfully"


def test_leaderboard_post_existing_game(client, mocker):
    mocker.patch("app.cursor.execute")
    mocker.patch("app.cursor.fetchone", return_value={"game_name": "existinggame"})

    response = client.post("/api/leaderboard", json={"game_name": "existinggame"})
    assert response.status_code == 400
    assert response.json["error"] == "Game already exists"

    def test_update_score_get(client, mocker):
        mocker.patch("app.cursor.execute")
        mocker.patch("app.cursor.fetchone", return_value={"score": 999})

        response = client.get("/update-score/game1/42")
        assert response.status_code == 200
        assert b"999" in response.data

    def test_update_score_post_success(client, mocker):
        mocker.patch("app.cursor.execute")
        mocker.patch("app.db.commit")

        response = client.post("/update-score/game1/42", data={"score": "555"})
        assert response.status_code == 302

def test_delete_score_success(client, mocker):
    mocker.patch("app.cursor.execute")
    mocker.patch("app.db.commit")


    mocker.patch("app.cursor.fetchone", side_effect=[
        {"game_id": 1},
        {"user_id": 42},
        {"count": 0}
    ])

    response = client.post("/api/leaderboard/game1/123")
    assert response.status_code == 302
