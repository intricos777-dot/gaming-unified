#!/usr/bin/env python3
"""Quick test for legal scanner integration"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from src.database import init_db, search_case_law, search_federal_statutes

print("Testing Law Library integration...")

# Init database
init_db()

# Test searches
test_queries = ["discrimination", "negligence", "civil rights", "contract"]

for q in test_queries:
    cases = search_case_law(q)
    statutes = search_federal_statutes(q)
    print(f"'{q}': {len(cases)} cases, {len(statutes)} statutes")

# Test API server endpoints
import urllib.request
import json

try:
    req = urllib.request.urlopen("http://localhost:4130/health")
    print(f"\nAPI Server: {json.loads(req.read())}")
except:
    print("\nAPI Server: Not running (start with: python api_server.py)")

print("\nTest complete!")
