#!/usr/bin/env python3
"""
Law Library CLI - Federal & State Law Research Tool
Search statutes, regulations, and case law for legal research
"""

import sys
import os
import json
import click
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from database import (
    init_db, search_federal_statutes, search_case_law, search_state_statutes,
    insert_federal_statute, insert_case_law, insert_state_statute,
    get_statute_by_citation, get_stats, log_search
)
from api_clients import (
    search_federal_legislation, search_case_law as api_search_cases,
    search_us_code, search_lii, get_state_sources, get_state_url,
    STATE_SOURCES, COURTLISTENER_TOKEN, CONGRESS_API_KEY
)

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.syntax import Syntax
    from rich.text import Text
    from rich import box
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

console = Console() if RICH_AVAILABLE else None


def print_rich(text, style=None):
    if console:
        console.print(text, style=style)
    else:
        print(text)


def print_header():
    header = """
╔═══════════════════════════════════════════════════════════════╗
║           ⚖  LAW LIBRARY - Legal Research Tool  ⚖           ║
║         Federal & State Statutes, Regulations, Case Law      ║
╚═══════════════════════════════════════════════════════════════╝"""
    if RICH_AVAILABLE:
        console.print(Panel(header.strip(), style="bold cyan", box=box.DOUBLE))
    else:
        print(header)


def display_results(results, result_type="statutes"):
    if not results:
        print_rich("[yellow]No results found.[/yellow]" if RICH_AVAILABLE else "No results found.")
        return

    if RICH_AVAILABLE:
        if result_type == "statutes":
            table = Table(title="Federal Statutes", box=box.ROUNDED)
            table.add_column("Title", style="cyan", width=8)
            table.add_column("Section", style="green", width=15)
            table.add_column("Name", style="white", max_width=40)
            table.add_column("Source", style="dim")

            for r in results:
                if "error" in r:
                    table.add_row("Error", r["error"], "", "")
                else:
                    table.add_row(
                        str(r.get("title", "")),
                        r.get("section", ""),
                        r.get("name", "")[:40],
                        r.get("source", "")
                    )

        elif result_type == "cases":
            table = Table(title="Case Law Results", box=box.ROUNDED)
            table.add_column("Court", style="cyan", width=20)
            table.add_column("Case Name", style="white", max_width=35)
            table.add_column("Citation", style="green", width=20)
            table.add_column("Date", style="dim", width=12)

            for r in results:
                if "error" in r:
                    table.add_row("Error", r["error"], "", "")
                else:
                    table.add_row(
                        r.get("court", r.get("courtName", ""))[:20],
                        (r.get("caseName", "") or r.get("title", ""))[:35],
                        r.get("citation", r.get("cite", ""))[:20],
                        r.get("date", r.get("dateFiled", ""))[:10]
                    )

        elif result_type == "bills":
            table = Table(title="Federal Legislation", box=box.ROUNDED)
            table.add_column("Type", style="cyan", width=8)
            table.add_column("Number", style="green", width=10)
            table.add_column("Title", style="white", max_width=45)
            table.add_column("Sponsor", style="dim", width=20)

            for r in results:
                if "error" in r:
                    table.add_row("Error", r["error"], "", "")
                else:
                    table.add_row(
                        r.get("type", "").upper(),
                        r.get("number", ""),
                        r.get("title", "")[:45],
                        r.get("sponsor", "")[:20]
                    )

        console.print(table)
    else:
        for i, r in enumerate(results, 1):
            print(f"\n--- Result {i} ---")
            for k, v in r.items():
                print(f"  {k}: {v}")


@click.group()
def cli():
    """Law Library - Federal & State Law Research Tool"""
    init_db()
    pass


@cli.command()
def stats():
    """Show database statistics"""
    init_db()
    s = get_stats()
    if RICH_AVAILABLE:
        table = Table(title="Database Statistics", box=box.ROUNDED)
        table.add_column("Category", style="cyan")
        table.add_column("Count", style="green", justify="right")
        table.add_row("Federal Statutes", str(s.get("federal_statutes", 0)))
        table.add_row("Federal Regulations", str(s.get("federal_regulations", 0)))
        table.add_row("Case Law", str(s.get("case_law", 0)))
        table.add_row("State Statutes", str(s.get("state_statutes", 0)))
        console.print(table)
    else:
        for k, v in s.items():
            print(f"{k}: {v}")


@cli.command()
@click.argument("query")
@click.option("--title", "-t", type=int, help="Filter by U.S. Code title number")
@click.option("--source", "-s", default="all", help="Source: all, uscode, courtlistener, lii")
def search(query, title, source):
    """Search federal statutes and case law"""
    print_rich(f"[bold]Searching:[/bold] {query}" if RICH_AVAILABLE else f"Searching: {query}")

    # Local database search
    local_results = search_federal_statutes(query, title)
    if local_results:
        print_rich(f"\n[green]Local database results: {len(local_results)}[/green]" if RICH_AVAILABLE
                    else f"\nLocal results: {len(local_results)}")
        display_results(local_results, "statutes")

    # GovInfo search
    if source in ("all", "uscode"):
        print_rich("\n[bold cyan]Searching GovInfo (U.S. Code)...[/bold cyan]" if RICH_AVAILABLE
                    else "\nSearching GovInfo...")
        govinfo_results = search_us_code(query, title)
        display_results(govinfo_results, "statutes")

    # LII search
    if source in ("all", "lii"):
        print_rich("\n[bold cyan]Searching Legal Information Institute...[/bold cyan]" if RICH_AVAILABLE
                    else "\nSearching LII...")
        lii_results = search_lii(query)
        display_results(lii_results, "statutes")

    # Case law search
    if source in ("all", "courtlistener"):
        print_rich("\n[bold cyan]Searching Case Law...[/bold cyan]" if RICH_AVAILABLE
                    else "\nSearching Case Law...")
        case_results = api_search_cases(query)
        display_results(case_results, "cases")

    log_search(query, "statutes", len(local_results))


@cli.command()
@click.argument("query")
@click.option("--court", "-c", help="Filter by court (e.g., scotus, ca9)")
def cases(query, court):
    """Search case law database"""
    print_rich(f"[bold]Searching case law:[/bold] {query}" if RICH_AVAILABLE
               else f"Searching case law: {query}")

    # Local search
    local_results = search_case_law(query, court)
    if local_results:
        print_rich(f"\n[green]Local results: {len(local_results)}[/green]" if RICH_AVAILABLE
                    else f"\nLocal results: {len(local_results)}")
        display_results(local_results, "cases")

    # CourtListener API search
    print_rich("\n[bold cyan]Searching CourtListener...[/bold cyan]" if RICH_AVAILABLE
               else "\nSearching CourtListener...")
    api_results = api_search_cases(query, court)
    display_results(api_results, "cases")

    log_search(query, "cases", len(local_results))


@cli.command()
@click.argument("query")
@click.option("--state", "-s", help="State code (e.g., CA, TX, NY)")
def state(query, state):
    """Search state statutes"""
    print_rich(f"[bold]Searching state laws:[/bold] {query}" if RICH_AVAILABLE
               else f"Searching state laws: {query}")

    if state:
        local_results = search_state_statutes(query, state.upper())
        if local_results:
            display_results(local_results, "statutes")

        # Show state website
        url = get_state_url(state.upper())
        if url:
            print_rich(f"\n[dim]Official state source: {url}[/dim]" if RICH_AVAILABLE
                        else f"\nOfficial state source: {url}")
    else:
        print_rich("\n[bold]State statute sources:[/bold]" if RICH_AVAILABLE
                    else "\nState statute sources:")
        for code, info in sorted(STATE_SOURCES.items()):
            print_rich(f"  [cyan]{code}[/cyan] - {info['name']}: {info['url']}"
                       if RICH_AVAILABLE else f"  {code} - {info['name']}: {info['url']}")

    log_search(query, "state", len(local_results) if state else 0)


@cli.command()
@click.argument("query")
def legislation(query):
    """Search federal legislation (Congress.gov)"""
    print_rich(f"[bold]Searching Congress.gov:[/bold] {query}" if RICH_AVAILABLE
               else f"Searching Congress.gov: {query}")

    results = search_federal_legislation(query)
    display_results(results, "bills")

    log_search(query, "legislation", len(results))


@cli.command()
@click.argument("query")
def everything(query):
    """Search across ALL databases"""
    print_rich(f"[bold magenta]Comprehensive search:[/bold magenta] {query}" if RICH_AVAILABLE
               else f"Comprehensive search: {query}")

    all_results = {
        "federal_statutes": [],
        "case_law": [],
        "bills": [],
        "lii": [],
        "govinfo": []
    }

    # Local database
    all_results["federal_statutes"] = search_federal_statutes(query)
    all_results["case_law"] = search_case_law(query)

    # APIs
    all_results["bills"] = search_federal_legislation(query)
    all_results["lii"] = search_lii(query)
    all_results["govinfo"] = search_us_code(query)

    total = sum(len(v) for v in all_results.values())
    print_rich(f"\n[bold green]Total results found: {total}[/bold green]" if RICH_AVAILABLE
               else f"\nTotal results found: {total}")

    for category, results in all_results.items():
        if results:
            print_rich(f"\n[bold cyan]--- {category.replace('_', ' ').title()} ---[/bold cyan]"
                       if RICH_AVAILABLE else f"\n--- {category} ---")
            display_results(results, "statutes" if "statute" in category else "cases" if "case" in category else "bills")

    log_search(query, "everything", total)


@cli.command()
@click.argument("citation")
def cite(citation):
    """Look up a statute or case by citation"""
    result = get_statute_by_citation(citation)
    if result:
        if RICH_AVAILABLE:
            console.print(Panel(json.dumps(result, indent=2, default=str), title=f"Citation: {citation}"))
        else:
            print(json.dumps(result, indent=2, default=str))
    else:
        print_rich(f"[yellow]Citation '{citation}' not found in local database.[/yellow]"
                   if RICH_AVAILABLE else f"Citation '{citation}' not found.")


@cli.command()
def sources():
    """Show all available legal sources and their status"""
    if RICH_AVAILABLE:
        table = Table(title="Legal Data Sources", box=box.ROUNDED)
        table.add_column("Source", style="cyan")
        table.add_column("Status", style="green")
        table.add_column("API Key", style="dim")
        table.add_column("URL")

        sources_list = [
            ("CourtListener", "Available" if COURTLISTENER_TOKEN else "Rate-limited",
             "Optional (free tier)" if not COURTLISTENER_TOKEN else "Set",
             "courtlistener.com"),
            ("Congress.gov", "Available" if CONGRESS_API_KEY else "Key required",
             "Required (free)" if not CONGRESS_API_KEY else "Set",
             "api.congress.gov"),
            ("GovInfo", "Available", "None needed", "api.govinfo.gov"),
            ("LII (Cornell)", "Available", "None needed", "law.cornell.edu"),
            ("State Statutes", f"{len(STATE_SOURCES)} states linked", "N/A",
             "Various state websites"),
        ]

        for name, status, key, url in sources_list:
            table.add_row(name, status, key, url)

        console.print(table)
    else:
        print("Legal Data Sources:")
        print("  CourtListener: courtlistener.com (optional API key)")
        print("  Congress.gov: api.congress.gov (free API key)")
        print("  GovInfo: api.govinfo.gov (no key needed)")
        print("  LII: law.cornell.edu (no key needed)")
        print(f"  State Statutes: {len(STATE_SOURCES)} states linked")


@cli.command()
@click.argument("state_code")
def state_links(state_code):
    """Get official statute links for a state"""
    state_code = state_code.upper()
    info = STATE_SOURCES.get(state_code)
    if info:
        print_rich(f"[bold]{info['name']} ({state_code})[/bold]" if RICH_AVAILABLE
                    else f"{info['name']} ({state_code})")
        print_rich(f"Official statutes: {info['url']}" if RICH_AVAILABLE
                    else f"Official statutes: {info['url']}")
    else:
        print_rich(f"[red]State code '{state_code}' not found.[/red]" if RICH_AVAILABLE
                    else f"State code '{state_code}' not found.")
        print_rich("Available states:" if RICH_AVAILABLE else "Available states:")
        for code in sorted(STATE_SOURCES.keys()):
            print(f"  {code} - {STATE_SOURCES[code]['name']}")


@cli.command()
@click.argument("topic")
def topic(topic):
    """Browse legal topics and related resources"""
    topics = {
        "constitutional": {
            "description": "Constitutional Law - Federal and state constitutional rights",
            "statutes": ["U.S. Constitution", "14th Amendment", "1st Amendment"],
            "areas": ["Due Process", "Equal Protection", "First Amendment", "Search & Seizure"]
        },
        "criminal": {
            "description": "Criminal Law - Federal and state criminal statutes",
            "statutes": ["18 U.S.C.", "State Penal Codes"],
            "areas": ["Theft", "Assault", "Drug Offenses", "Fraud", "Homicide"]
        },
        "civil": {
            "description": "Civil Law - Torts, contracts, property",
            "statutes": ["State Civil Codes", "UCC"],
            "areas": ["Contracts", "Torts", "Property", "Employment", "Family"]
        },
        "business": {
            "description": "Business Law - Corporate, securities, trade",
            "statutes": ["15 U.S.C.", "17 U.S.C.", "26 U.S.C."],
            "areas": ["Corporations", "Intellectual Property", "Tax", "Trade Regulation"]
        },
        "administrative": {
            "description": "Administrative Law - Agency regulations",
            "statutes": ["5 U.S.C.", "CFR"],
            "areas": ["Agency Rules", "FOIA", "Administrative Procedure"]
        },
        "property": {
            "description": "Property Law - Real and personal property",
            "statutes": ["State Property Codes"],
            "areas": ["Real Estate", "Landlord-Tenant", "Easements", "Zoning"]
        },
        "family": {
            "description": "Family Law - Marriage, divorce, custody",
            "statutes": ["State Family Codes"],
            "areas": ["Divorce", "Child Custody", "Adoption", "Domestic Relations"]
        },
        "labor": {
            "description": "Labor & Employment Law",
            "statutes": ["29 U.S.C.", "42 U.S.C."],
            "areas": ["Wages", "Discrimination", "Safety", "Unions", "Benefits"]
        }
    }

    topic_lower = topic.lower()
    found = False
    for key, info in topics.items():
        if topic_lower in key or topic_lower in info["description"].lower():
            found = True
            if RICH_AVAILABLE:
                panel_content = f"""[bold]{info['description']}[/bold]

Related Statutes:
{chr(10).join(f'  • {s}' for s in info['statutes'])}

Legal Areas:
{chr(10).join(f'  • {a}' for a in info['areas'])}"""
                console.print(Panel(panel_content, title=f"Topic: {key.title()}", box=box.ROUNDED))
            else:
                print(f"\n{info['description']}")
                print("Related Statutes:", ", ".join(info["statutes"]))
                print("Legal Areas:", ", ".join(info["areas"]))

    if not found:
        print_rich(f"[yellow]Topic '{topic}' not found. Available topics:[/yellow]"
                   if RICH_AVAILABLE else f"Topic '{topic}' not found. Available topics:")
        for key in topics:
            print(f"  - {key}")


@cli.command()
def configure():
    """Configure API keys for enhanced search"""
    print_rich("[bold]Law Library Configuration[/bold]" if RICH_AVAILABLE
               else "Law Library Configuration")

    config_file = Path(__file__).parent / ".env"
    config = {}
    if config_file.exists():
        for line in config_file.read_text().splitlines():
            if "=" in line:
                key, val = line.split("=", 1)
                config[key.strip()] = val.strip()

    print_rich("\n[dim]Get free API keys:[/dim]" if RICH_AVAILABLE
               else "\nGet free API keys:")
    print("  Congress.gov: https://api.congress.gov/")
    print("  CourtListener: https://www.courtlistener.com/api/rest-info/")

    congress_key = input(f"\nCongress.gov API key [{config.get('CONGRESS_API_KEY', '')}]: ").strip()
    if congress_key:
        config["CONGRESS_API_KEY"] = congress_key

    courtlistener_token = input(f"CourtListener token [{config.get('COURTLISTENER_TOKEN', '')}]: ").strip()
    if courtlistener_token:
        config["COURTLISTENER_TOKEN"] = courtlistener_token

    config_content = "\n".join(f"{k}={v}" for k, v in config.items())
    config_file.write_text(config_content)
    print_rich("\n[green]Configuration saved.[/green]" if RICH_AVAILABLE else "\nConfiguration saved.")


if __name__ == "__main__":
    cli()
