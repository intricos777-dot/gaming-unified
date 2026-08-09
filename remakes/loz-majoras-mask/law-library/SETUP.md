# Legal Case Scanner - Setup Guide

## Overview
This tool integrates three data sources to compile legal case research:
1. **Himalaya** - Email scanning for legal-related content
2. **Lia Memory Vault** - Personal memory database scanning
3. **Law Library API** - Legal database search (statutes, case law, legislation)

## Quick Start

### 1. Configure Himalaya (Email)
Edit `~/.config/himalaya/config.toml` with your email settings:

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

For Gmail: Use an [App Password](https://myaccount.google.com/apppasswords)

### 2. Configure Law Library API Keys (Optional)
Create `/home/sin/Projects/law-library/.env`:

```
CONGRESS_API_KEY=your_key_here
COURTLISTENER_TOKEN=your_token_here
```

Get free keys at:
- Congress.gov: https://api.congress.gov/
- CourtListener: https://www.courtlistener.com/api/rest-info/

### 3. Run the Scanner

```bash
cd /home/sin/Projects/law-library

# Option A: Run scanner only
source venv/bin/activate
python legal_scanner.py

# Option B: Start API + run scanner
./start_scanner.sh

# Option C: Start API and keep it running
./start_scanner.sh --keep
```

## Usage Examples

### Scan emails and compile legal report
```bash
python legal_scanner.py
```

### Search specific legal topics via API
```bash
# Start API server first
python api_server.py &

# Search for cases
curl "http://localhost:4130/search?q=employment+discrimination&type=cases"
curl "http://localhost:4130/search?q=civil+rights&type=all"
curl "http://localhost:4130/chat" -d '{"message": "search for negligence cases"}'
```

### Use Law Library CLI directly
```bash
python lawlib.py search "employment discrimination"
python lawlib.py cases "negligence"
python lawlib.py state "harassment" --state CA
python lawlib.py everything "civil rights"
```

## Legal Topics Tracked
- **Constitutional**: 1st/4th/14th Amendment, due process, free speech
- **Criminal**: Arrest, conviction, sentencing, Miranda rights
- **Civil**: Lawsuits, negligence, torts, contracts
- **Family**: Divorce, custody, domestic relations
- **Employment**: Discrimination, harassment, wrongful termination
- **Property**: Eviction, landlord-tenant, zoning
- **Business**: LLC, IP, contracts, fraud
- **Immigration**: Visa, deportation, asylum

## Output
Reports are saved to `/home/sin/Projects/law-library/data/legal_report_YYYYMMDD_HHMMSS.json`

## Architecture
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│    Himalaya     │    │   Lia Memory    │    │  Law Library    │
│    (Emails)     │    │    (Vault)      │    │     (API)       │
└────────┬────────┘    └────────┬────────┘    └────────┬────────┘
         │                      │                      │
         └──────────────────────┼──────────────────────┘
                                │
                    ┌───────────▼───────────┐
                    │   legal_scanner.py    │
                    │  (Integration Layer)  │
                    └───────────┬───────────┘
                                │
                    ┌───────────▼───────────┐
                    │   legal_report.json   │
                    │   (Compiled Output)   │
                    └───────────────────────┘
```
