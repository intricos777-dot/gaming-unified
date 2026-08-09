"""Law Library API Server - HTTP API for lia-skillbridge integration"""

import sys
import json
from pathlib import Path
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

sys.path.insert(0, str(Path(__file__).parent / "src"))

from database import (
    init_db, search_federal_statutes, search_case_law, search_state_statutes,
    get_statute_by_citation, get_stats
)
from api_clients import (
    search_federal_legislation, search_case_law as api_search_cases,
    search_us_code, search_lii, get_state_sources, get_state_url,
    STATE_SOURCES
)

PORT = 4130


class LawLibraryHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # Suppress default logging

    def send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(json.dumps(data, default=str).encode())

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)

        if parsed.path == "/health":
            self.send_json({"status": "ok", "service": "law-library"})

        elif parsed.path == "/stats":
            self.send_json(get_stats())

        elif parsed.path == "/sources":
            sources = []
            for code, info in sorted(STATE_SOURCES.items()):
                sources.append({"code": code, "name": info["name"], "url": info["url"]})
            self.send_json({"state_sources": sources, "count": len(sources)})

        elif parsed.path == "/topics":
            topics = self._get_topics()
            self.send_json({"topics": topics})

        elif parsed.path == "/search":
            query = params.get("q", [""])[0]
            search_type = params.get("type", ["all"])[0]
            state_code = params.get("state", [None])[0]
            court = params.get("court", [None])[0]
            title = params.get("title", [None])[0]

            if not query:
                self.send_json({"error": "Query parameter 'q' is required"}, 400)
                return

            results = self._search(query, search_type, state_code, court, title)
            self.send_json(results)

        elif parsed.path.startswith("/cite/"):
            citation = parsed.path.split("/cite/")[1]
            result = get_statute_by_citation(citation)
            if result:
                self.send_json(result)
            else:
                self.send_json({"error": f"Citation '{citation}' not found"}, 404)

        elif parsed.path == "/state":
            state_code = params.get("code", [None])[0]
            if state_code:
                info = STATE_SOURCES.get(state_code.upper())
                if info:
                    self.send_json({"state": state_code.upper(), "name": info["name"], "url": info["url"]})
                else:
                    self.send_json({"error": f"State '{state_code}' not found"}, 404)
            else:
                self.send_json({"states": list(STATE_SOURCES.keys())})

        else:
            self.send_json({"error": "Not found", "endpoints": [
                "/health", "/stats", "/sources", "/topics",
                "/search?q=query&type=all|statutes|cases|legislation",
                "/cite/CITATION", "/state?code=CA"
            ]}, 404)

    def do_POST(self):
        parsed = urlparse(self.path)
        content_length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(content_length)) if content_length > 0 else {}

        if parsed.path == "/search":
            query = body.get("q", body.get("query", ""))
            search_type = body.get("type", "all")
            state_code = body.get("state")
            court = body.get("court")
            title = body.get("title")

            if not query:
                self.send_json({"error": "Field 'q' or 'query' is required"}, 400)
                return

            results = self._search(query, search_type, state_code, court, title)
            self.send_json(results)

        elif parsed.path == "/chat":
            message = body.get("message", "")
            if not message:
                self.send_json({"error": "Field 'message' is required"}, 400)
                return

            response = self._chat(message)
            self.send_json({"response": response})

        else:
            self.send_json({"error": "Not found"}, 404)

    def _search(self, query, search_type="all", state_code=None, court=None, title=None):
        results = {"query": query, "results": {}}

        if search_type in ("all", "statutes", "federal"):
            local = search_federal_statutes(query, int(title) if title else None)
            govinfo = search_us_code(query, int(title) if title else None)
            results["results"]["federal_statutes"] = {
                "local": local,
                "govinfo": govinfo
            }

        if search_type in ("all", "cases", "case_law"):
            local = search_case_law(query, court)
            api = api_search_cases(query, court)
            results["results"]["case_law"] = {
                "local": local,
                "courtlistener": api
            }

        if search_type in ("all", "legislation"):
            bills = search_federal_legislation(query)
            results["results"]["legislation"] = bills

        if search_type in ("all", "lii"):
            lii = search_lii(query)
            results["results"]["lii"] = lii

        if search_type in ("all", "state"):
            if state_code:
                local = search_state_statutes(query, state_code.upper())
                results["results"]["state_statutes"] = {
                    "state": state_code.upper(),
                    "local": local,
                    "source_url": get_state_url(state_code.upper())
                }
            else:
                results["results"]["state_hint"] = "Add ?state=XX to search state statutes"

        total = sum(
            len(v) if isinstance(v, list) else
            sum(len(vv) for vv in v.values() if isinstance(vv, list))
            for v in results["results"].values() if v
        )
        results["total"] = total

        return results

    def _chat(self, message):
        lower = message.lower()

        if any(w in lower for w in ["search", "find", "look up", "what is", "show me"]):
            clean = message
            for word in ["search for", "find", "look up", "what is", "show me"]:
                clean = clean.replace(word, "").strip()

            results = self._search(clean, "all")
            if results["total"] > 0:
                response = f"I found {results['total']} results for '{clean}':\n\n"
                for category, data in results["results"].items():
                    if data and isinstance(data, dict):
                        for subkey, subdata in data.items():
                            if isinstance(subdata, list) and subdata:
                                response += f"**{category}/{subkey}**: {len(subdata)} results\n"
                    elif isinstance(data, list) and data:
                        response += f"**{category}**: {len(data)} results\n"
                return response
            return f"I searched for '{clean}' but didn't find matching results in the database. Try being more specific or check the sources with /sources."

        elif "topics" in lower:
            topics = self._get_topics()
            return "Available legal topics:\n" + "\n".join(f"- **{t['name']}**: {t['description']}" for t in topics)

        elif "states" in lower or "state law" in lower:
            return f"I have links to {len(STATE_SOURCES)} state statute databases. Use the /state endpoint or specify a state code (e.g., CA, TX, NY)."

        elif "sources" in lower or "help" in lower:
            return """Law Library API Endpoints:
- GET /search?q=query - Search all databases
- GET /search?q=query&type=statutes - Search statutes only
- GET /search?q=query&type=cases - Search case law only
- GET /search?q=query&state=CA - Search state laws
- GET /cite/CITATION - Look up by citation
- GET /topics - Browse legal topics
- GET /sources - View all data sources
- POST /chat - Natural language legal research"""

        return f"I can help you search for laws, cases, and legal information. Try asking me to search for a specific law or legal topic."

    def _get_topics(self):
        return [
            {"name": "Constitutional", "description": "Constitutional law - rights, due process, amendments"},
            {"name": "Criminal", "description": "Criminal law - statutes, procedures, defenses"},
            {"name": "Civil", "description": "Civil law - torts, contracts, property"},
            {"name": "Business", "description": "Business law - corporate, IP, tax, trade"},
            {"name": "Administrative", "description": "Administrative law - agency regulations"},
            {"name": "Property", "description": "Property law - real estate, landlord-tenant"},
            {"name": "Family", "description": "Family law - divorce, custody, adoption"},
            {"name": "Labor", "description": "Labor & employment law - wages, discrimination, safety"},
        ]


def run_server():
    init_db()
    server = HTTPServer(("0.0.0.0", PORT), LawLibraryHandler)
    print(f"Law Library API running on http://localhost:{PORT}")
    print(f"Endpoints: /health, /stats, /search, /cite, /topics, /sources, /state, /chat")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
        server.shutdown()


if __name__ == "__main__":
    run_server()
