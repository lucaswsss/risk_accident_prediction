from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import os

app = Flask(__name__)
CORS(app)

# URL de connexion PostgreSQL (tu la mets dans Render comme variable d'environnement)
DB_URL = os.getenv("DATABASE_URL")

def get_connection():
    return psycopg2.connect(DB_URL)

def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS scores (
            pseudo TEXT,
            score INTEGER
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

@app.route("/add_score", methods=["POST"])
def add_score():
    data = request.json
    pseudo = data.get("pseudo")
    score = data.get("score")

    if pseudo is None or score is None:
        return jsonify({"error": "Requête invalide : pseudo et score sont requis"}), 400

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO scores (pseudo, score) VALUES (%s, %s);", (pseudo, score))
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Score ajouté avec succès!"})

@app.route("/leaderboard", methods=["GET"])
def leaderboard():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT pseudo, score FROM scores ORDER BY score DESC LIMIT 10;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(rows)

@app.route("/reset_leaderboard", methods=["POST"])
def reset_leaderboard():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM scores;")
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Leaderboard réinitialisé!"})

