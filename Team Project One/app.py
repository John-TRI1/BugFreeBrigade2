from flask import Flask, render_template

app = Flask(__name__)

# Sample leaderboard data
leaderboard = [
    {"rank": 1, "name": "Player1", "score": 1500},
    {"rank": 2, "name": "Player2", "score": 1400},
    {"rank": 3, "name": "Player3", "score": 1300},
    {"rank": 4, "name": "Player4", "score": 1200},
    {"rank": 5, "name": "Player5", "score": 1100},
]

@app.route('/')
def show_leaderboard():
    return render_template('leaderboard.html', leaderboard=leaderboard)

if __name__ == '__main__':
    app.run(debug=True)