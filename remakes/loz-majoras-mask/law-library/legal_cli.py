#!/usr/bin/env python3
"""
Legal Research CLI - Unified interface for Lia + Law Library
"""

import sys
import json
from pathlib import Path

# Add both projects to path
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "lia-cli"))

from lia_legal_bridge import LiaLegalBridge


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Legal Research CLI - Lia + Law Library Integration")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Search command
    search_parser = subparsers.add_parser("search", help="Search for legal cases")
    search_parser.add_argument("query", help="Search query")
    search_parser.add_argument("--save", "-s", action="store_true", help="Save report to file")
    
    # Scan command
    scan_parser = subparsers.add_parser("scan", help="Scan emails and memories")
    scan_parser.add_argument("--topic", "-t", help="Filter by topic")
    
    # Topics command
    subparsers.add_parser("topics", help="List legal topics")
    
    # Stats command
    subparsers.add_parser("stats", help="Show database statistics")
    
    args = parser.parse_args()
    
    bridge = LiaLegalBridge()
    
    if args.command == "search":
        report = bridge.search_and_compile(args.query)
        bridge.display_report(report)
        if args.save:
            bridge.save_report(report)
    
    elif args.command == "scan":
        emails = bridge.scan_emails()
        memories = bridge.scan_memory()
        
        if args.topic:
            emails = [e for e in emails if e["topic"] == args.topic]
            memories = [m for m in memories if m["topic"] == args.topic]
        
        print(f"\nEmails: {len(emails)}")
        print(f"Memories: {len(memories)}")
        
        for email in emails[:5]:
            print(f"  • [{email['topic']}] {email.get('subject', 'No subject')[:60]}")
    
    elif args.command == "topics":
        for topic, keywords in bridge.LEGAL_TOPICS.items():
            print(f"\n{topic.upper()}")
            print(f"  Keywords: {', '.join(keywords[:5])}...")
    
    elif args.command == "stats":
        from src.database import get_stats
        stats = get_stats()
        print("\nLaw Library Statistics:")
        for k, v in stats.items():
            print(f"  {k}: {v}")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
