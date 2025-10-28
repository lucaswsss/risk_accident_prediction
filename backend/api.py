from flask import Flask, request, jsonify
from flask_cors import CORS
import duckdb

app = Flask(__name__)
CORS(app) 

DB_PATH = "data/scores.duckdb"

def init_db():
    conn = duckdb.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS scores (
            pseudo TEXT,
            score INTEGER
        );
    """)
    conn.close()

@app.route("/add_score", methods=["POST"])
def add_score():
    data = request.json
    pseudo = data.get("pseudo")
    score = data.get("score")

    if pseudo is None or score is None:
        return jsonify({"error": "Requête invalide : pseudo et score sont requis"}), 400

    conn = duckdb.connect(DB_PATH)
    conn.execute("INSERT INTO scores VALUES (?, ?)", (pseudo, score))
    conn.close()

    return jsonify({"message": "Score ajouté avec succès!"})

@app.route("/leaderboard", methods=["GET"])
def leaderboard():
    conn = duckdb.connect(DB_PATH)
    try:
        rows = conn.execute("SELECT pseudo, score FROM scores ORDER BY score DESC LIMIT 10").fetchall()
    except:
        rows = []
    conn.close()
    return jsonify(rows)

@app.route("/reset_leaderboard", methods=["POST"])
def reset_leaderboard():
    conn = duckdb.connect(DB_PATH)
    conn.execute("DELETE FROM scores")
    conn.close()
    return jsonify({"message": "Leaderboard réinitialisé!"})



if __name__ == "__main__":
    init_db()
