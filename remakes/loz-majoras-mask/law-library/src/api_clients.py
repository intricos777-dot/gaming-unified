"""API clients for legal databases - Congress.gov, CourtListener, GovInfo, LII"""

import requests
import json
import time
from typing import Optional, List, Dict, Any
from pathlib import Path

CACHE_DIR = Path(__file__).parent.parent / "cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)


def _cache_get(key: str) -> Optional[Any]:
    cache_file = CACHE_DIR / f"{key.replace('/', '_')}.json"
    if cache_file.exists():
        data = json.loads(cache_file.read_text())
        if time.time() - data.get("ts", 0) < 86400:
            return data.get("value")
    return None


def _cache_set(key: str, value: Any):
    cache_file = CACHE_DIR / f"{key.replace('/', '_')}.json"
    cache_file.write_text(json.dumps({"ts": time.time(), "value": value}, default=str))


# ============================================================
# Congress.gov API (Free, requires API key)
# https://api.congress.gov/
# ============================================================

CONGRESS_API_KEY = ""  # Set via environment or config

def search_federal_legislation(query: str, limit: int = 20) -> List[Dict]:
    """Search federal legislation via Congress.gov API"""
    cache_key = f"congress/{query}/{limit}"
    cached = _cache_get(cache_key)
    if cached:
        return cached

    if not CONGRESS_API_KEY:
        return [{"error": "Congress.gov API key not set. Get one free at api.congress.gov"}]

    results = []
    try:
        url = f"https://api.congress.gov/v3/bill"
        params = {
            "query": query,
            "limit": limit,
            "api_key": CONGRESS_API_KEY,
            "format": "json"
        }
        resp = requests.get(url, params=params, timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            for bill in data.get("bills", []):
                results.append({
                    "title": bill.get("title", ""),
                    "congress": bill.get("congress", ""),
                    "number": bill.get("number", ""),
                    "type": bill.get("type", ""),
                    "introduced": bill.get("introducedDate", ""),
                    "sponsor": bill.get("sponsors", [{}])[0].get("fullName", "") if bill.get("sponsors") else "",
                    "url": bill.get("url", ""),
                    "source": "congress.gov"
                })
    except Exception as e:
        results.append({"error": str(e)})

    _cache_set(cache_key, results)
    return results


def get_bill_text(congress: int, bill_type: str, bill_number: int) -> Optional[Dict]:
    """Get full text of a federal bill"""
    cache_key = f"bill_text/{congress}/{bill_type}/{bill_number}"
    cached = _cache_get(cache_key)
    if cached:
        return cached

    if not CONGRESS_API_KEY:
        return {"error": "API key not set"}

    try:
        url = f"https://api.congress.gov/v3/bill/{congress}/{bill_type}/{bill_number}/text"
        params = {"api_key": CONGRESS_API_KEY, "format": "json"}
        resp = requests.get(url, params=params, timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            text_versions = data.get("textVersions", [])
            if text_versions:
                formats = text_versions[0].get("formats", [])
                if formats:
                    pdf_url = formats[0].get("url", "")
                    result = {
                        "congress": congress,
                        "type": bill_type,
                        "number": bill_number,
                        "formats": formats,
                        "source": "congress.gov"
                    }
                    _cache_set(cache_key, result)
                    return result
    except Exception as e:
        return {"error": str(e)}
    return None


# ============================================================
# CourtListener / Free Law Project (Free tier available)
# https://www.courtlistener.com/api/
# ============================================================

COURTLISTENER_TOKEN = ""  # Set via environment or config

def search_case_law(query: str, court: Optional[str] = None,
                    limit: int = 20) -> List[Dict]:
    """Search case law via CourtListener API"""
    cache_key = f"courtlistener/{query}/{court}/{limit}"
    cached = _cache_get(cache_key)
    if cached:
        return cached

    headers = {}
    if COURTLISTENER_TOKEN:
        headers["Authorization"] = f"Token {COURTLISTENER_TOKEN}"

    results = []
    try:
        params = {
            "q": query,
            "order_by": "-score",
            "page_size": limit
        }
        if court:
            params["court"] = court

        resp = requests.get(
            "https://www.courtlistener.com/api/rest/v4/search/",
            headers=headers, params=params, timeout=15
        )
        if resp.status_code == 200:
            data = resp.json()
            for case in data.get("results", []):
                results.append({
                    "caseName": case.get("caseName", ""),
                    "citation": case.get("cite", ""),
                    "court": case.get("courtName", ""),
                    "date": case.get("dateFiled", ""),
                    "judge": case.get("judge", ""),
                    "snippet": case.get("snippet", ""),
                    "url": case.get("absolute_url", ""),
                    "source": "courtlistener"
                })
    except Exception as e:
        results.append({"error": str(e)})

    _cache_set(cache_key, results)
    return results


# ============================================================
# GovInfo API (Free, no key required for basic access)
# https://www.govinfo.gov/developer
# ============================================================

def search_us_code(query: str, title: Optional[int] = None) -> List[Dict]:
    """Search U.S. Code via GovInfo"""
    cache_key = f"govinfo/uscode/{query}/{title}"
    cached = _cache_get(cache_key)
    if cached:
        return cached

    results = []
    try:
        params = {"query": query}
        if title:
            params["title"] = str(title)

        resp = requests.get(
            "https://api.govinfo.gov/search",
            params=params, timeout=15
        )
        if resp.status_code == 200:
            data = resp.json()
            for item in data.get("results", []):
                if item.get("packageId", "").startswith("USCODE"):
                    results.append({
                        "packageId": item.get("packageId", ""),
                        "title": item.get("title", ""),
                        "subtitle": item.get("subtitle", ""),
                        "summary": item.get("summary", ""),
                        "url": item.get("downloadUrl", ""),
                        "source": "govinfo"
                    })
    except Exception as e:
        results.append({"error": str(e)})

    _cache_set(cache_key, results)
    return results


# ============================================================
# Legal Information Institute (LII) - Cornell
# https://www.law.cornell.edu/
# ============================================================

def search_lii(query: str) -> List[Dict]:
    """Search Legal Information Institute (Cornell Law)"""
    cache_key = f"lii/{query}"
    cached = _cache_get(cache_key)
    if cached:
        return cached

    results = []
    try:
        resp = requests.get(
            "https://www.law.cornell.edu/search/fulltext/search",
            params={"q": query, "type": "statutes+codes"},
            timeout=15,
            headers={"User-Agent": "LawLibrary/1.0"}
        )
        if resp.status_code == 200:
            data = resp.json()
            for item in data.get("results", []):
                results.append({
                    "title": item.get("title", ""),
                    "url": item.get("url", ""),
                    "snippet": item.get("snippet", ""),
                    "source": "lii"
                })
    except Exception as e:
        results.append({"error": str(e)})

    _cache_set(cache_key, results)
    return results


# ============================================================
# State Law Lookups (via various state sources)
# ============================================================

STATE_SOURCES = {
    "AL": {"name": "Alabama", "url": "https://alisondb.legislature.state.al.us/CodeOfAlabama/"},
    "AK": {"name": "Alaska", "url": "https://www.akleg.gov/statutes.asp"},
    "AZ": {"name": "Arizona", "url": "https://www.azleg.gov/statutes/"},
    "AR": {"name": "Arkansas", "url": "https://www.arkleg.state.ar.us/"},
    "CA": {"name": "California", "url": "https://leginfo.legislature.ca.gov/"},
    "CO": {"name": "Colorado", "url": "https://leg.colorado.gov/colorado-revised-statutes"},
    "CT": {"name": "Connecticut", "url": "https://www.cga.ct.gov/current/pub/titles.htm"},
    "DE": {"name": "Delaware", "url": "https://delcode.delaware.gov/"},
    "FL": {"name": "Florida", "url": "http://www.leg.state.fl.us/statutes/"},
    "GA": {"name": "Georgia", "url": "https://www.legis.ga.gov/legislation/all"},
    "HI": {"name": "Hawaii", "url": "https://www.capitol.hawaii.gov/hrscurrent/"},
    "ID": {"name": "Idaho", "url": "https://legislature.idaho.gov/statutesnav/"},
    "IL": {"name": "Illinois", "url": "https://www.ilga.gov/legislation/ilcs/ilcs3.asp"},
    "IN": {"name": "Indiana", "url": "https://www.in.gov/gencod/"},
    "IA": {"name": "Iowa", "url": "https://www.legis.iowa.gov/law/administrativeRules/rules"},
    "KS": {"name": "Kansas", "url": "https://www.kslegislature.org/kor_stat/Statute/0/0-001"},
    "KY": {"name": "Kentucky", "url": "https://legislature.ky.gov/law/statutes/Pages/default.aspx"},
    "LA": {"name": "Louisiana", "url": "https://legis.la.gov/legis/Law.aspx?d=84"},
    "ME": {"name": "Maine", "url": "https://www.mainelegislature.org/legis/statutes/"},
    "MD": {"name": "Maryland", "url": "https://mgaleg.maryland.gov/mgawebsite/Statutes/"},
    "MA": {"name": "Massachusetts", "url": "https://malegislature.gov/Laws/GeneralLaws"},
    "MI": {"name": "Michigan", "url": "https://www.legislature.mi.gov/Laws/MCL"},
    "MN": {"name": "Minnesota", "url": "https://www.revisor.mn.gov/statutes/"},
    "MS": {"name": "Mississippi", "url": "https://billstatus.ls.state.ms.us/statutes/statutes.cfm"},
    "MO": {"name": "Missouri", "url": "https://revisor.mo.gov/main/Home.aspx"},
    "MT": {"name": "Montana", "url": "https://leg.mt.gov/bills/mca/"},
    "NE": {"name": "Nebraska", "url": "https://nebraskalegislature.gov/statutes/"},
    "NV": {"name": "Nevada", "url": "https://www.leg.state.nv.us/NRS/"},
    "NH": {"name": "New Hampshire", "url": "https://www.gencourt.state.nh.us/statutes/"},
    "NJ": {"name": "New Jersey", "url": "https://www.njleg.state.nj.us/statutes/"},
    "NM": {"name": "New Mexico", "url": "https://www.nmonesource.com/nmos/nmsa/en/nav.do"},
    "NY": {"name": "New York", "url": "https://www.nysenate.gov/legislation/laws"},
    "NC": {"name": "North Carolina", "url": "https://www.ncleg.gov/Laws/GeneralStatuteTables"},
    "ND": {"name": "North Dakota", "url": "https://www.ndlegis.gov/coding/codetop.htm"},
    "OH": {"name": "Ohio", "url": "https://codes.ohio.gov/ohio-revised-code"},
    "OK": {"name": "Oklahoma", "url": "https://www.oklahoma.gov/ocs/oklahoma-statutes.html"},
    "OR": {"name": "Oregon", "url": "https://oregonrevstatutes.com/"},
    "PA": {"name": "Pennsylvania", "url": "https://www.legis.pa.gov/cfdocs/legis/li/ucons/index.cfm"},
    "RI": {"name": "Rhode Island", "url": "https://www.rilegislature.gov/statutes/"},
    "SC": {"name": "South Carolina", "url": "https://www.scstatehouse.gov/coderegs/statutes.htm"},
    "SD": {"name": "South Dakota", "url": "https://sdlegislature.com/Statutes"},
    "TN": {"name": "Tennessee", "url": "https://law.justia.com/codes/tennessee/"},
    "TX": {"name": "Texas", "url": "https://statutes.capitol.texas.gov/"},
    "UT": {"name": "Utah", "url": "https://le.utah.gov/xcode/Title01.html"},
    "VT": {"name": "Vermont", "url": "https://legislature.vermont.gov/statutes/"},
    "VA": {"name": "Virginia", "url": "https://law.lis.virginia.gov/"},
    "WA": {"name": "Washington", "url": "https://app.leg.wa.gov/rcw/"},
    "WV": {"name": "West Virginia", "url": "https://code.wvlegislature.gov/"},
    "WI": {"name": "Wisconsin", "url": "https://docs.legis.wisconsin.gov/statutes/"},
    "WY": {"name": "Wyoming", "url": "https://wyoleg.gov/statutes/"},
    "DC": {"name": "Washington DC", "url": "https://code.dccouncil.gov/"},
}


def get_state_sources() -> Dict[str, Dict]:
    """Get all state statute sources"""
    return STATE_SOURCES


def get_state_url(state_code: str) -> Optional[str]:
    """Get the official state statute URL"""
    state = STATE_SOURCES.get(state_code.upper())
    return state["url"] if state else None
