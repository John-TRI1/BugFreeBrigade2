from flask import Flask, render_template, request, redirect, jsonify

app = Flask(__name__)

leaderboards = {
    'game1': [
       {"name": "Alice", "score": 120},
       {"name": "Bob", "score": 95}
    ],
    'game2': [
       {"name": "Charlie", "score": 130},
       {"name": "Dave", "score": 80}
    ]
}

@app.route("/")
def index():
    game = request.args.get('game', 'game1')
    scores = leaderboards.get(game, [])
    sorted_scores = sorted(scores, key=lambda x: x["score"], reverse=True)
    games = list(leaderboards.keys())
    return render_template("index.html", scores=sorted_scores, games=games, current_game=game)

@app.route("/submit", methods=["GET"])
def submit_form():
    game = request.args.get('game', 'game1')
    return render_template("submit.html", game=game)

@app.route("/submit", methods=["POST"])
def submit_score():
    game = request.form.get("game", "game1")
    name = request.form.get("name")
    try:
        score = int(request.form.get("score"))
    except (ValueError, TypeError):
        score = 0
    if game not in leaderboards:
        leaderboards[game] = []
    leaderboards[game].append({"name": name, "score": score})
    return redirect(f"/?game={game}")

@app.route("/api/leaderboard", methods=["GET"])
def api_leaderboard():
    game = request.args.get('game', 'game1')
    scores = leaderboards.get(game, [])
    sorted_scores = sorted(scores, key=lambda x: x["score"], reverse=True)
    return jsonify({"game": game, "leaderboard": sorted_scores})

#to the existing update scores
@app.route("/api/leaderboard/<game>/<int:score_id>", methods=["PUT"])
def update_score(game, score_id):
    data = request.get_json()
    new_score = data.get("score")

    if game not in leaderboards:
        return jsonify({"error": "Game not found"}), 404

    if score_id < 0 or score_id >= len(leaderboards[game]):
        return jsonify({"error": "Invalid score ID"}), 400

    try:
        leaderboards[game][score_id]["score"] = int(new_score)
        return jsonify({"message": "Score updated successfully", "leaderboard": leaderboards[game]})
    except ValueError:
        return jsonify({"error": "Invalid score value"}), 400


#to delete scores
@app.route("/api/leaderboard/<game>/<int:score_id>", methods=["DELETE"])
def delete_score(game, score_id):
    if game not in leaderboards:
        return jsonify({"error": "Game not found"}), 404

    if score_id < 0 or score_id >= len(leaderboards[game]):
        return jsonify({"error": "Invalid score ID"}), 400

    remove_score = leaderboards[game].pop(score_id)
    return jsonify({"message": "Score deleted successfully", "removed": remove_score, "leaderboard": leaderboards[game]})




if __name__ == "__main__":
    app.run(debug=True)