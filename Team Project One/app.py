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

if __name__ == "__main__":
    app.run(debug=True)