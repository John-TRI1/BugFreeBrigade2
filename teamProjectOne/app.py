from flask import Flask, render_template, request, redirect, jsonify
import mysql.connector

app = Flask(__name__)



db = mysql.connector.connect(
    host="leaderboard.czwwke00wit5.us-east-2.rds.amazonaws.com",
    port=3306,
    user="admin",
    password="Blaster12",
    database="leaderboard"
)


cursor = db.cursor(dictionary=True)

@app.route("/")
def index():
    game_name = request.args.get('game', 'game1')
    search_query = request.args.get('search', '').strip().lower()  # <-- new

    cursor.execute("SELECT game_id FROM games WHERE game_name = %s", (game_name,))
    game = cursor.fetchone()

    if not game:
        return "Game not found", 404

    game_id = game["game_id"]

    if search_query:
        cursor.execute("""
            SELECT scores.score_id, users.username, scores.score 
            FROM scores
            JOIN users ON scores.user_id = users.user_id
            WHERE scores.game_id = %s AND LOWER(users.username) LIKE %s
            ORDER BY scores.score DESC
        """, (game_id, f"%{search_query}%"))
    else:
        cursor.execute("""
            SELECT scores.score_id, users.username, scores.score 
            FROM scores
            JOIN users ON scores.user_id = users.user_id
            WHERE scores.game_id = %s
            ORDER BY scores.score DESC
        """, (game_id,))

    scores = cursor.fetchall()

    cursor.execute("SELECT game_name FROM games")
    games = [row["game_name"] for row in cursor.fetchall()]

    return render_template("index.html", scores=scores, games=games, current_game=game_name)

@app.route("/submit", methods=["GET"])
def submit_form():
    game = request.args.get('game', 'game1')
    return render_template("submit.html", game=game)

@app.route("/submit", methods=["POST"])
def submit_score():

    game_name = request.form.get("game", "game1")
    name = request.form.get("name")
    score_input = request.form.get("score")


    if not name or not score_input or not score_input.isdigit():
        return jsonify({"error": "Invalid name or score"}), 400

    score = int(score_input)

    try:

        cursor.execute("SELECT user_id FROM users WHERE username = %s", (name,))
        user = cursor.fetchone()
        if not user:
            cursor.execute("INSERT INTO users (username, user_rank) VALUES (%s, %s)", (name, None))
            user_id = cursor.lastrowid
        else:
            user_id = user["user_id"]


        cursor.execute("SELECT game_id FROM games WHERE game_name = %s", (game_name,))
        game = cursor.fetchone()
        if not game:
            return jsonify({"error": "Game not found"}), 404

        game_id = game["game_id"]


        cursor.execute("INSERT INTO scores (user_id, game_id, score) VALUES (%s, %s, %s)", (user_id, game_id, score))
        score_id = cursor.lastrowid


        db.commit()


        return redirect(f"/?game={game_name}")

    except mysql.connector.Error as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500


@app.route("/api/leaderboard", methods=["GET", "POST"])
def api_leaderboard():

    if request.method == "POST":

        game_name = request.json.get('game_name')

        if not game_name:
            return jsonify({"error": "Game name is required"}), 400


        cursor.execute("SELECT game_name FROM games WHERE game_name = %s", (game_name,))
        existing_game = cursor.fetchone()

        if existing_game:
            return jsonify({"error": "Game already exists"}), 400

        cursor.execute("INSERT INTO games (game_name) VALUES (%s)", (game_name,))
        db.commit()

        return jsonify({"message": f"Game '{game_name}' added successfully"}), 201


    game_name = request.args.get('game', 'game1')

    cursor.execute("SELECT game_id FROM games WHERE game_name = %s", (game_name,))
    game = cursor.fetchone()

    if not game:
        return jsonify({"error": "Game not found"}), 404

    game_id = game["game_id"]

    cursor.execute("""
        SELECT users.username, scores.score 
        FROM scores
        JOIN users ON scores.user_id = users.user_id
        WHERE scores.game_id = %s
        ORDER BY scores.score DESC  
    """, (game_id,))

    leaderboard = cursor.fetchall()

    return jsonify({"game": game_name, "leaderboard": leaderboard})


@app.route("/api/leaderboard/<string:game>/<int:score_id>", methods=["POST"])
def delete_score(game, score_id):
    try:

        cursor.execute("SELECT game_id FROM games WHERE game_name = %s", (game,))
        game_data = cursor.fetchone()
        if not game_data:
            return jsonify({"error": "Game not found"}), 404

        game_id = game_data["game_id"]


        cursor.execute("SELECT user_id FROM scores WHERE score_id = %s AND game_id = %s", (score_id, game_id))
        score_data = cursor.fetchone()
        if not score_data:
            return jsonify({"error": "Score not found"}), 404

        user_id = score_data["user_id"]


        cursor.execute("DELETE FROM scores WHERE score_id = %s", (score_id,))
        db.commit()


        cursor.execute("SELECT COUNT(*) as count FROM scores WHERE user_id = %s", (user_id,))
        result = cursor.fetchone()
        if result["count"] == 0:

            cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
            db.commit()
            print(f"User {user_id} deleted because they had no remaining scores.")

        return redirect(f"/?game={game}")

    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        return jsonify({"error": "An error occurred"}), 500


@app.route("/update-score/<string:game>/<int:score_id>", methods=["GET", "POST"])
def update_score(game, score_id):
    if request.method == "GET":
        cursor.execute("SELECT score FROM scores WHERE score_id = %s", (score_id,))
        score_data = cursor.fetchone()
        if not score_data:
            return "Score not found", 404
        return render_template("update.html", game=game, score_id=score_id, current_score=score_data["score"])

    elif request.method == "POST":
        new_score = request.form.get("score")

        if not new_score or not new_score.isdigit():
            return jsonify({"error": "Invalid score value"}), 400

        new_score = int(new_score)
        cursor.execute("UPDATE scores SET score = %s WHERE score_id = %s", (new_score, score_id))
        db.commit()

        return redirect(f"/?game={game}")


if __name__ == "__main__":
    app.run(debug=True)