# app.py
from flask import Flask, render_template, request, jsonify
import random
import os
import sys

# Initialize Flask app
app = Flask(__name__)

# Available choices
CHOICES = ["rock", "paper", "scissors"]


def decide_winner(user_choice: str, computer_choice: str) -> str:
    """
    Determine the winner of Rock-Paper-Scissors.
    Returns: 'user', 'computer', or 'tie'
    """
    if user_choice == computer_choice:
        return "tie"
    if (
        (user_choice == "rock" and computer_choice == "scissors")
        or (user_choice == "paper" and computer_choice == "rock")
        or (user_choice == "scissors" and computer_choice == "paper")
    ):
        return "user"
    return "computer"


@app.route("/")
def index():
    """Render the main page (templates/index.html)."""
    return render_template("index.html")


@app.route("/api/play", methods=["POST"])
def play():
    """
    Handle the game logic via POST request.
    Expects JSON: { "user": "<rock|paper|scissors>" }
    Returns JSON: { "user": ..., "computer": ..., "result": ... }
    """
    # Use silent=True to avoid raising if body is missing or invalid JSON
    data = request.get_json(silent=True)

    if not data or "user" not in data:
        return jsonify({"error": "Missing 'user' choice"}), 400

    user_choice = str(data.get("user", "")).strip().lower()
    if user_choice not in CHOICES:
        return jsonify({"error": f"Invalid choice: {user_choice}"}), 400

    # Random computer choice
    computer_choice = random.choice(CHOICES)

    # Decide result
    result = decide_winner(user_choice, computer_choice)

    return jsonify({
        "user": user_choice,
        "computer": computer_choice,
        "result": result
    })


if __name__ == "__main__":
    # Local development server. In production use a WSGI server (gunicorn / waitress).
    port = int(os.environ.get("PORT", 5001))
    host = os.environ.get("HOST", "127.0.0.1")
    print("Starting Flask app from:", __file__)
    print("Python executable:", sys.executable)
    print(f"Listening on http://{host}:{port} (debug=True)")
    app.run(debug=True, host=host, port=port)

