import os
from flask import Flask, jsonify
import psycopg
from psycopg import Error as PsycopgError

app = Flask(__name__)


def get_db_dsn() -> str:
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "5432")
    user = os.getenv("DB_USER", "postgres")
    password = os.getenv("DB_PASSWORD", "secret")
    dbname = os.getenv("DB_NAME", "myapp")
    return f"host={host} port={port} user={user} password={password} dbname={dbname}"


def init_db() -> None:
    with psycopg.connect(get_db_dsn()) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS visits (
                    id SERIAL PRIMARY KEY,
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
        conn.commit()


@app.get("/")
def home():
    return jsonify({"message": "Hello from Docker 101 Final Challenge"})


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


@app.get("/visits")
def visits():
    try:
        with psycopg.connect(get_db_dsn()) as conn:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO visits DEFAULT VALUES")
                cur.execute("SELECT COUNT(*) FROM visits")
                total = cur.fetchone()[0]
            conn.commit()
        return jsonify({"total_visits": total})
    except PsycopgError:
        return jsonify({"error": "database not available"}), 503


if __name__ == "__main__":
    try:
        init_db()
    except PsycopgError:
        # The app can still serve non-DB endpoints in standalone mode.
        pass
    app.run(host="0.0.0.0", port=5000)
