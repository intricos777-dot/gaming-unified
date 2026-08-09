"""SQLite database for law storage and search"""

import sqlite3
import json
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any

DB_PATH = Path(__file__).parent.parent / "data" / "law_library.db"


def get_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db():
    conn = get_db()
    cur = conn.cursor()

    cur.executescript("""
        CREATE TABLE IF NOT EXISTS federal_statutes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title INTEGER,
            section TEXT,
            name TEXT,
            text TEXT,
            source TEXT DEFAULT 'uscode',
            url TEXT,
            last_updated TEXT,
            UNIQUE(title, section)
        );

        CREATE TABLE IF NOT EXISTS federal_regulations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cfr_title INTEGER,
            part TEXT,
            section TEXT,
            name TEXT,
            text TEXT,
            url TEXT,
            last_updated TEXT,
            UNIQUE(cfr_title, part, section)
        );

        CREATE TABLE IF NOT EXISTS case_law (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            court TEXT,
            case_name TEXT,
            citation TEXT,
            date_filed TEXT,
            judge TEXT,
            summary TEXT,
            full_text TEXT,
            url TEXT,
            source TEXT DEFAULT 'courtlistener',
            UNIQUE(citation)
        );

        CREATE TABLE IF NOT EXISTS state_statutes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            state TEXT,
            code TEXT,
            section TEXT,
            title TEXT,
            name TEXT,
            text TEXT,
            url TEXT,
            last_updated TEXT,
            UNIQUE(state, code, section)
        );

        CREATE TABLE IF NOT EXISTS legal_topics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT,
            description TEXT,
            related_statutes TEXT,
            related_cases TEXT
        );

        CREATE TABLE IF NOT EXISTS search_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query TEXT,
            search_type TEXT,
            results_count INTEGER,
            timestamp TEXT
        );

        CREATE INDEX IF NOT EXISTS idx_federal_statutes_section ON federal_statutes(section);
        CREATE INDEX IF NOT EXISTS idx_federal_statutes_name ON federal_statutes(name);
        CREATE INDEX IF NOT EXISTS idx_case_law_citation ON case_law(citation);
        CREATE INDEX IF NOT EXISTS idx_case_law_court ON case_law(court);
        CREATE INDEX IF NOT EXISTS idx_state_statutes_state ON state_statutes(state);
        CREATE INDEX IF NOT EXISTS idx_state_statutes_section ON state_statutes(section);
    """)

    conn.commit()
    conn.close()
    return DB_PATH


def insert_federal_statute(title: int, section: str, name: str, text: str,
                           url: str = "", source: str = "uscode"):
    conn = get_db()
    try:
        conn.execute(
            """INSERT OR REPLACE INTO federal_statutes
               (title, section, name, text, source, url, last_updated)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (title, section, name, text, source, url, datetime.now().isoformat())
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Error inserting statute: {e}")
        return False
    finally:
        conn.close()


def insert_case_law(court: str, case_name: str, citation: str,
                    date_filed: str = "", judge: str = "", summary: str = "",
                    full_text: str = "", url: str = "", source: str = "courtlistener"):
    conn = get_db()
    try:
        conn.execute(
            """INSERT OR REPLACE INTO case_law
               (court, case_name, citation, date_filed, judge, summary, full_text, url, source)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (court, case_name, citation, date_filed, judge, summary, full_text, url, source)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Error inserting case: {e}")
        return False
    finally:
        conn.close()


def insert_state_statute(state: str, code: str, section: str, title: str,
                         name: str, text: str, url: str = ""):
    conn = get_db()
    try:
        conn.execute(
            """INSERT OR REPLACE INTO state_statutes
               (state, code, section, title, name, text, url, last_updated)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (state, code, section, title, name, text, url, datetime.now().isoformat())
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Error inserting state statute: {e}")
        return False
    finally:
        conn.close()


def search_federal_statutes(query: str, title: Optional[int] = None) -> List[Dict]:
    conn = get_db()
    try:
        if title:
            rows = conn.execute(
                """SELECT * FROM federal_statutes
                   WHERE title = ? AND (name LIKE ? OR text LIKE ? OR section LIKE ?)
                   ORDER BY title, section LIMIT 50""",
                (title, f"%{query}%", f"%{query}%", f"%{query}%")
            ).fetchall()
        else:
            rows = conn.execute(
                """SELECT * FROM federal_statutes
                   WHERE name LIKE ? OR text LIKE ? OR section LIKE ?
                   ORDER BY title, section LIMIT 50""",
                (f"%{query}%", f"%{query}%", f"%{query}%")
            ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def search_case_law(query: str, court: Optional[str] = None) -> List[Dict]:
    conn = get_db()
    try:
        if court:
            rows = conn.execute(
                """SELECT * FROM case_law
                   WHERE court LIKE ? AND (case_name LIKE ? OR summary LIKE ? OR full_text LIKE ?)
                   ORDER BY date_filed DESC LIMIT 50""",
                (f"%{court}%", f"%{query}%", f"%{query}%", f"%{query}%")
            ).fetchall()
        else:
            rows = conn.execute(
                """SELECT * FROM case_law
                   WHERE case_name LIKE ? OR citation LIKE ? OR summary LIKE ? OR full_text LIKE ?
                   ORDER BY date_filed DESC LIMIT 50""",
                (f"%{query}%", f"%{query}%", f"%{query}%", f"%{query}%")
            ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def search_state_statutes(query: str, state: Optional[str] = None) -> List[Dict]:
    conn = get_db()
    try:
        if state:
            rows = conn.execute(
                """SELECT * FROM state_statutes
                   WHERE state = ? AND (name LIKE ? OR text LIKE ? OR title LIKE ?)
                   ORDER BY state, code, section LIMIT 50""",
                (state, f"%{query}%", f"%{query}%", f"%{query}%")
            ).fetchall()
        else:
            rows = conn.execute(
                """SELECT * FROM state_statutes
                   WHERE name LIKE ? OR text LIKE ? OR title LIKE ?
                   ORDER BY state, code, section LIMIT 50""",
                (f"%{query}%", f"%{query}%", f"%{query}%")
            ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def get_statute_by_citation(citation: str) -> Optional[Dict]:
    conn = get_db()
    try:
        row = conn.execute(
            "SELECT * FROM federal_statutes WHERE section = ?", (citation,)
        ).fetchone()
        if row:
            return dict(row)
        row = conn.execute(
            "SELECT * FROM case_law WHERE citation = ?", (citation,)
        ).fetchone()
        if row:
            return dict(row)
        return None
    finally:
        conn.close()


def log_search(query: str, search_type: str, results_count: int):
    conn = get_db()
    try:
        conn.execute(
            "INSERT INTO search_history (query, search_type, results_count, timestamp) VALUES (?, ?, ?, ?)",
            (query, search_type, results_count, datetime.now().isoformat())
        )
        conn.commit()
    finally:
        conn.close()


def get_stats() -> Dict[str, int]:
    conn = get_db()
    try:
        stats = {}
        for table in ["federal_statutes", "federal_regulations", "case_law", "state_statutes"]:
            row = conn.execute(f"SELECT COUNT(*) as cnt FROM {table}").fetchone()
            stats[table] = row["cnt"]
        return stats
    finally:
        conn.close()
