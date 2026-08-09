#!/usr/bin/env python3
"""
Legal Case Scanner - Integrates Himalaya emails, Lia memory, and Law Library
Scans emails and memories to compile legal cases in relevant areas
"""

import sys
import json
import subprocess
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# Add law library to path
sys.path.insert(0, str(Path(__file__).parent))
from src.database import init_db, search_case_law, search_federal_statutes
from src.api_clients import search_case_law as api_search_cases, search_us_code

LAW_TOPICS = {
    "constitutional": ["1st amendment", "4th amendment", "14th amendment", "due process", "equal protection", "free speech", "search and seizure", "civil rights"],
    "criminal": ["arrest", "conviction", "sentencing", "bail", "probation", "parole", "criminal defense", "miranda", "plea"],
    "civil": ["lawsuit", "plaintiff", "defendant", "damages", "injunction", "settlement", "negligence", "tort", "contract dispute"],
    "family": ["divorce", "custody", "child support", "alimony", "adoption", "domestic", "restraining order", "marriage"],
    "employment": ["discrimination", "harassment", "wrongful termination", "wage theft", "workers comp", "osha", "labor board"],
    "property": ["eviction", "landlord", "tenant", "foreclosure", "easement", "zoning", "real estate", "property damage"],
    "business": ["llc", "corporation", "contract", "intellectual property", "patent", "trademark", "securities", "fraud"],
    "immigration": ["visa", "green card", "deportation", "asylum", "uscis", "immigration court", "naturalization"]
}


def scan_emails(max_emails=50):
    """Scan emails using himalaya for legal keywords"""
    print("[*] Scanning emails for legal content...")
    legal_emails = []

    try:
        result = subprocess.run(
            ["himalaya", "envelope", "list", "-w", str(max_emails)],
            capture_output=True, text=True, timeout=30
        )

        if result.returncode != 0:
            print(f"[!] Himalaya error: {result.stderr}")
            return []

        # Parse email IDs from output
        email_ids = []
        for line in result.stdout.strip().split("\n"):
            if line.strip():
                parts = line.split()
                if parts:
                    email_ids.append(parts[0])

        for eid in email_ids[:max_emails]:
            try:
                msg_result = subprocess.run(
                    ["himalaya", "message", "read", eid],
                    capture_output=True, text=True, timeout=10
                )
                if msg_result.returncode == 0:
                    content = msg_result.stdout.lower()
                    for topic, keywords in LAW_TOPICS.items():
                        for kw in keywords:
                            if kw in content:
                                legal_emails.append({
                                    "id": eid,
                                    "topic": topic,
                                    "keyword": kw,
                                    "snippet": msg_result.stdout[:200]
                                })
                                break
            except subprocess.TimeoutExpired:
                continue

    except FileNotFoundError:
        print("[!] Himalaya not found. Install with: cargo install himalaya")
    except Exception as e:
        print(f"[!] Email scan error: {e}")

    print(f"[*] Found {len(legal_emails)} emails with legal content")
    return legal_emails


def scan_memory():
    """Scan lia memory vault for legal-related entries"""
    print("[*] Scanning memory vault...")
    memory_file = Path.home() / ".lia-cli" / "data" / "memory" / "lia-memory.vault.json"
    legal_memories = []

    if not memory_file.exists():
        print("[!] Memory vault not found")
        return []

    try:
        with open(memory_file) as f:
            vault = json.load(f)

        for entry in vault.get("entries", []):
            content = entry.get("content", "").lower()
            tags = [t.lower() for t in entry.get("tags", [])]

            for topic, keywords in LAW_TOPICS.items():
                for kw in keywords:
                    if kw in content or any(kw in t for t in tags):
                        legal_memories.append({
                            "id": entry.get("id"),
                            "content": entry.get("content"),
                            "topic": topic,
                            "keyword": kw,
                            "timestamp": entry.get("timestamp")
                        })
                        break

    except Exception as e:
        print(f"[!] Memory scan error: {e}")

    print(f"[*] Found {len(legal_memories)} memory entries with legal content")
    return legal_memories


def search_legal_cases(queries):
    """Search law library for cases related to queries"""
    print("[*] Searching law library for cases...")
    all_cases = []

    init_db()

    for query in queries[:10]:  # Limit to prevent too many API calls
        try:
            # Local database search
            local_cases = search_case_law(query)
            for case in local_cases:
                all_cases.append({
                    "source": "local_db",
                    "query": query,
                    "case": case
                })

            # CourtListener API
            api_cases = api_search_cases(query)
            for case in api_cases:
                all_cases.append({
                    "source": "courtlistener",
                    "query": query,
                    "case": case
                })
        except Exception as e:
            print(f"[!] Search error for '{query}': {e}")

    print(f"[*] Found {len(all_cases)} cases in law library")
    return all_cases


def compile_report(emails, memories, cases):
    """Compile findings into a structured report"""
    report = {
        "generated": datetime.now().isoformat(),
        "summary": {
            "emails_scanned": len(emails),
            "memories_found": len(memories),
            "cases_found": len(cases)
        },
        "by_topic": defaultdict(lambda: {
            "emails": [],
            "memories": [],
            "cases": []
        })
    }

    for email in emails:
        report["by_topic"][email["topic"]]["emails"].append(email)

    for mem in memories:
        report["by_topic"][mem["topic"]]["memories"].append(mem)

    for case in cases:
        query = case["query"]
        for topic, keywords in LAW_TOPICS.items():
            if any(kw in query.lower() for kw in keywords):
                report["by_topic"][topic]["cases"].append(case)
                break

    return report


def display_report(report):
    """Display the compiled report"""
    print("\n" + "=" * 70)
    print("LEGAL CASE RESEARCH REPORT")
    print("=" * 70)
    print(f"Generated: {report['generated']}")
    print(f"Emails scanned: {report['summary']['emails_scanned']}")
    print(f"Memory entries: {report['summary']['memories_found']}")
    print(f"Cases found: {report['summary']['cases_found']}")
    print("=" * 70)

    for topic, data in sorted(report["by_topic"].items()):
        if any([data["emails"], data["memories"], data["cases"]]):
            print(f"\n{'=' * 50}")
            print(f"TOPIC: {topic.upper()}")
            print(f"{'=' * 50}")

            if data["emails"]:
                print(f"\nEmails ({len(data['emails'])}):")
                for e in data["emails"][:3]:
                    print(f"  - [{e['keyword']}] {e['snippet'][:80]}...")

            if data["memories"]:
                print(f"\nMemory Entries ({len(data['memories'])}):")
                for m in data["memories"][:3]:
                    print(f"  - [{m['keyword']}] {m['content'][:80]}")

            if data["cases"]:
                print(f"\nCases ({len(data['cases'])}):")
                for c in data["cases"][:5]:
                    case_data = c.get("case", {})
                    name = case_data.get("caseName", case_data.get("name", "Unknown"))
                    cite = case_data.get("citation", case_data.get("cite", "N/A"))
                    print(f"  - {name} ({cite})")

    print("\n" + "=" * 70)


def save_report(report, output_dir=None):
    """Save report to file"""
    if output_dir is None:
        output_dir = Path(__file__).parent / "data"
    else:
        output_dir = Path(output_dir)

    output_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = output_dir / f"legal_report_{timestamp}.json"

    with open(filepath, "w") as f:
        json.dump(report, f, indent=2, default=str)

    print(f"\n[*] Report saved to: {filepath}")
    return filepath


def main():
    """Main entry point"""
    print("Legal Case Scanner - Starting...")
    print("=" * 50)

    # Scan sources
    emails = scan_emails(max_emails=30)
    memories = scan_memory()

    # Extract search queries from findings
    queries = set()
    for e in emails:
        queries.add(e["keyword"])
    for m in memories:
        queries.add(m["keyword"])

    if not queries:
        queries = {"civil rights", "employment discrimination", "contract dispute"}

    # Search law library
    cases = search_legal_cases(list(queries))

    # Compile and display report
    report = compile_report(emails, memories, cases)
    display_report(report)

    # Save report
    save_report(report)

    return report


if __name__ == "__main__":
    main()
