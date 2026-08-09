# Lia + Law Library Integration

## Overview
This integration connects:
- **Lia Memory Vault** - Personal memory database
- **Himalaya** - Email client (requires configuration)
- **Law Library** - Legal research database with API access to CourtListener, Congress.gov, GovInfo, and LII

## Files
- `lia_legal_bridge.py` - Main bridge connecting all three systems
- `legal_cli.py` - Command-line interface
- `legal_scanner.py` - Standalone scanner (in law-library)

## Quick Start

### 1. Configure Himalaya (Email)
Create/edit `~/.config/himalaya/config.toml`:

```toml
[accounts.default]
display-name = "Your Name"
email = "your@email.com"
default = true

backend.type = "imap"
backend.host = "imap.gmail.com"
backend.port = 993
backend.encryption = "tls"
backend.login = "your@email.com"
backend.auth.type = "password"
backend.auth.raw = "your-app-password"

message.send.backend.type = "smtp"
message.send.backend.host = "smtp.gmail.com"
message.send.backend.port = 465
message.send.backend.encryption = "tls"
message.send.backend.login = "your@email.com"
message.send.backend.auth.type = "password"
message.send.backend.auth.raw = "your-app-password"
```

For Gmail: Generate an [App Password](https://myaccount.google.com/apppasswords)

### 2. Configure Law Library API Keys (Optional)
Create `/home/sin/Projects/law-library/.env`:

```
CONGRESS_API_KEY=your_key_here
COURTLISTENER_TOKEN=your_token_here
```

Free API keys:
- Congress.gov: https://api.congress.gov/
- CourtListener: https://www.courtlistener.com/api/rest-info/

### 3. Run

```bash
# From law-library directory
cd /home/sin/Projects/law-library
source venv/bin/activate

# Search for legal cases
python legal_cli.py search "employment discrimination" --save

# Scan emails and memories
python legal_cli.py scan

# List legal topics
python legal_cli.py topics

# Show database stats
python legal_cli.py stats
```

## Legal Topics Tracked

| Topic | Keywords |
|-------|----------|
| Constitutional | 1st/4th/14th Amendment, due process, free speech |
| Criminal | Arrest, conviction, sentencing, Miranda rights |
| Civil | Lawsuits, negligence, torts, contracts |
| Family | Divorce, custody, domestic relations |
| Employment | Discrimination, harassment, wrongful termination |
| Property | Eviction, landlord-tenant, zoning |
| Business | LLC, IP, contracts, fraud |
| Immigration | Visa, deportation, asylum |

## Architecture

```
┌─────────────────┐
│    Himalaya     │
│    (Emails)     │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│         Lia Legal Bridge                │
│  - Scans emails for legal keywords     │
│  - Searches Lia memory vault           │
│  - Queries Law Library API             │
└────────┬────────────────────────────────┘
         │
         ▼
┌─────────────────┐
│  Legal Report   │
│  (JSON output)  │
└─────────────────┘
```

## Output
Reports are saved to:
- `/home/sin/Projects/lia-cli/data/legal_report_YYYYMMDD_HHMMSS.json`
- `/home/sin/Projects/law-library/data/legal_report_YYYYMMDD_HHMMSS.json`
