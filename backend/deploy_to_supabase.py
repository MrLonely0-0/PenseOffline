"""
Deploy schema_postgres.sql and seed_postgres.sql to a Postgres database (e.g. Supabase).
Usage:
  - Set environment variable `DATABASE_URL` or `SUPABASE_DB_URL` with your connection string
  - Run: `python deploy_to_supabase.py`

The script will:
  - Connect to the target DB
  - Execute `schema_postgres.sql`
  - Optionally execute `seed_postgres.sql` (prompted)

Warning: seed will insert sample data; run only on a fresh DB or when you intend to populate test data.
"""

import os
import sys
import psycopg2
from psycopg2 import sql

BASE_DIR = os.path.dirname(__file__)
SCHEMA_FILE = os.path.join(BASE_DIR, "schema_postgres.sql")
SEED_FILE = os.path.join(BASE_DIR, "seed_postgres.sql")

def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def apply_sql(conn, script_text):
    with conn.cursor() as cur:
        cur.execute(script_text)
    conn.commit()


def main():
    db_url = os.getenv("SUPABASE_DB_URL") or os.getenv("DATABASE_URL")
    if not db_url:
        print("ERROR: Set SUPABASE_DB_URL or DATABASE_URL environment variable with your Postgres connection string.")
        sys.exit(1)

    print("Using DB URL:", db_url.split("@")[0] + "@...")

    schema_sql = read_file(SCHEMA_FILE)
    seed_sql = read_file(SEED_FILE)

    print("Connecting to database...")
    conn = psycopg2.connect(db_url)
    try:
        print("Applying schema...")
        apply_sql(conn, schema_sql)
        print("Schema applied successfully.")

        run_seed = input("Run seed inserts? This will insert example data (yes/no): ").strip().lower()
        if run_seed in ("y", "yes"):
            print("Applying seed...")
            apply_sql(conn, seed_sql)
            print("Seed applied successfully.")
        else:
            print("Seed skipped.")

    except Exception as exc:
        print("Error while applying SQL:", exc)
    finally:
        conn.close()
        print("Connection closed.")


if __name__ == "__main__":
    main()
