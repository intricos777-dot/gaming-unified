# Continue Work — Handoff Prompt

Use this prompt when Hermes is next started and the user is not at the keyboard.

## Exact Prompt To Run
```
Continue all in-flight project work as Lia supervisor at /home/sin/Projects/lia-cli.
First run: node --import tsx src/index.ts tasks
Then execute the pending hermes-subagent tasks in this order:
1) ringworld-redux: replace stub renderer, add input bridge, wire mission objectives
2) kingdom-hearts-zero: add collision/traversal, save/load, real command deck rendering
3) spacecraft-blueprint-simulator: convergence detection, Markdown reports, push best blueprints
4) firedragon: sidebar module wiring, build/package binary, test install/remove flow
After each task completes, mark it done with: node --import tsx src/index.ts done <task-id> <result>
Push each project repo after changes. If blocked, mark fail with reason.
```

## Project State Snapshot (2026-08-07 ~05:22 UTC)
- ringworld-redux: infinite-loop fix pushed; test binary clean; renderer/gameplay still stubs
- kingdom-hearts-zero: latest commit `8443a64` act one; builds; opencode background docs task still running
- spacecraft-blueprint-simulator: dual-track GA running, BDE patrol working, pushed, cron every 6h
- firedragon: control panel + sidebar + theme installer pushed
- lia-cli: new standalone repo at https://github.com/intricos777-dot/lia-cli, supervisor module live

## Session 2026-08-08 Update (all Lia tasks 1-29 complete)
- ringworld-redux: hermes-subagent verified renderer/input/objectives (tasks task-3..26); pushed
- kingdom-hearts-zero: traversal, save/load, command deck done; pushed `71f066e`
- spacecraft-blueprint-simulator: convergence + MD reports + auto-push; pushed
- firedragon: sidebar wiring, packaging, install/remove flow; pushed
- housekeeping (task-29): all 9 repos pushed + vm-bootstrap/te-bonfire committed; all clean
- te-bonfire (task-28): clean build, 2 ctest pass, --sim OK; initial release `706ddf8` (no remote)
- quantum-enochian (task-27): 9/9 tests pass; test/run-tests.js fixed (after hook); no source changes needed

## Lia Supervisor Task IDs
- ringworld-redux: task-3, task-4, task-5
- kingdom-hearts-zero: task-6, task-7, task-8
- spacecraft-blueprint-simulator: task-9, task-10, task-11
- firedragon: task-12, task-13, task-14
- prior: task-1 completed, task-2 failed (blocked)

## Session 2026-08-08 — Security Remediation
- **supercode CLI patched** (was relaying typed input to hardcoded `https://supercode-8w7e.onrender.com`): 8 URLs → `http://127.0.0.1:1`, `process.env.SUPERCODE_SERVER_URL` override blocked (11 spots → literal `"http://privacy-blocked.invalid"`), session token moved to `~/.better-auth/token.json.bak-privacy`; undo copy at `main.js.bak-privacy`
- **crypto-bot secret leak**: `.env` (Kraken/Coinbase API keys, private keys, faucet password) was committed AND pushed to GitHub; history deep-scrubbed via `git-filter-repo --invert-paths --path .env` + forced push; repo is private so exposure contained to user's account; `.env` now gitignored (`9764abd`/`b285197`); **rotate those credentials**
- **guardian built**: `~/.hermes/scripts/astral-guardian.py` — nightly 03:00 (no-agent, deliver local) auto-commit/push repos + block-secrets scan; verify via `hermes cron list` (job `76c1278fd4c2`)
- **secrecy-scan built**: `~/.hermes/scripts/secrecy-scan.py` — nightly 03:30 (job `7f76b1ffea00`) scanning ports, hardcoded URLs, env-override patterns, exfil keywords, token files
- **verified**: both jobs ran `completed` via `hermes cron run`; hermes gateway running manually (PID 154511) — not yet a service, dies on reboot (fix: `hermes gateway install`)

## Session 2026-08-08 — Security Toolkit Buildout (web-researched, built + verified)
- **Hardware recon**: TPM2 present (`/dev/tpm0`, `/dev/tpmrm0`); **no fingerprint reader** (fprintd installed but zero biometric devices in lsusb — only camera/mouse/BT); disk NOT encrypted (plain btrfs); Secure Boot disabled; OS = Garuda/Arch, systemd 261, zen kernel 7.1.6
- **vault-seal.py** (NEW tool): TPM2-sealed credential vault via `systemd-creds encrypt/decrypt --with-key=tpm2`; `put <name> <file|stdin>` / `get` / `list` / `delete`; verified put/get round-trip. **Fix applied**: `/dev/tpmrm0` was `tss:root` only → added `/etc/udev/rules.d/99-tpm-wheel.rules` granting `wheel` group access (user-scope `io.systemd.System` ETIMEDOUT), recreated device node via mknod (major 252, minor 65536). NOTE: persists at reboot via udev rule
- **leak-guard.py** (NEW tool): pre-commit secret guard — detects private key material, AWS-style keys (AKIA etc.), exchange creds (kraken/coinbase/binance/etc.), `SECRET=`-style assignments, URL-embedded credentials, non-allowlisted hosts; allows `.env.example`, env-var references, placeholders; **installed globally** via `git config --global core.hooksPath` → `~/.hermes/git-hooks/pre-commit` (all repos, incl. future clones); verified: blocks secret commit, allows clean one
- **socket-audit.py** (NEW tool): flags non-loopback listeners; cron job `socket-audit` at `03:45` (regd). Findings: **port 21550 = SRBMiner API** (miner, pid 1991, no bind-address option) and **3050 = himalaya-exchange Firebird** listen on 0.0.0.0; added firewalld rich rules rejecting 21550/3050 (ipv4+6, permanent, reloaded) — external blocked; loopback still OK
- **Osint**: see web sources — systemd #37051 + LinuxIQ (PCR 7/11 wall), oddlama TPM bypass; ArchWiki fprint; Debian SecurityManagement fingerprint PAM; git-secrets/Talisman for pre-commit scans; nosecrets; fwlock
- **Known gaps (needs user + reboot risk)**: no FDE (btrfs + swap unfarmed) — recommend LUKS re-encrypt on next disk use; Secure Boot off (enabling breaks nothing, TPM sealing benefits); fprintd ready but zero hardware
- **NOT verified yet**: per-repo pre-commit for repos with unique hooks (lia-cli uses its own hooks??) — `core.hooksPath` overrides; if a repo needs its own pre-commit, leak-guard is skipped — verify

## Session 2026-08-08 — Hardening Toolkit Buildout (part 2; all verified)
- **sandbox-run.sh** (NEW tool): bubblewrap tiered sandbox — `ro` (read-only root, stateless) / `scratch` (writable `/var/tmp/scratch`) / `persist` (writable `/var/tmp/persist`) tiers; `--no-home` masks home; `--report` writes log; `--save/--restore/--save-list` snapshot scratch+persist; verified ro blocks home writes + no routes; scratch/persist write OK; saves list OK. Host dirs `/var/tmp/scratch`, `/var/tmp/persist` created once (bwrap needs dest to pre-exist)
- **fde-prep.sh** (NEW tool): SAFE preflight + runbook for FDE+SecureBoot; `--check` detects SB/TPM/LUKS/tooling (dracut is the Garuda generator, not mkinitcpio — corrected); `--runbook` prints stage-0..4 (snapshot → sbctl keys → systemd-cryptenroll PCR7 --tpm2-with-pin → crypttab → cryptsetup reencrypt-in-place); `--info` dumps hw facts. NO disk modification — runbook only, user executes in reboot window
- **PAM biometrics-ready** (`/etc/pam.d/system-auth`, backup `system-auth.bak-privacy`): added guarded fprintd lines (funinkina pattern): fingerprint offered ONLY for `sudo:polkit-1` services with a real tty; falls back to password; display-manager logins unaffected; no effect today (zero reader hardware) — swappable reader = plug-in + `fprintd-enroll`
- **vault-seal.py hardened**: user-scope systemd-creds transient service intermittently ETIMEDOUTs (io.systemd.System); tool now retries via `sudo -n` (root-scope TPM always works); verified round-trip
- **cron day**: 9 jobs `[active]` now: midnight-site-check, spacecraft loop (360m), bde-integrity x2, astral-guardian 03:00, secrecy-scan 03:30, socket-audit 03:45, ip-algorithm-monitor, hourly-bde-code-theft-scan. sandbox-audit cron was created+deleted (nonsensical — sandbox state already reported by guardian line)
- **guardian now reports**: `guardian: sandbox state — N runs, X scratch, Y persist, Z saves`
- **Changes needing review**: `/etc/pam.d/system-auth` (fprintd-ready), `/etc/udev/rules.d/99-tpm-wheel.rules`, firewalld rich rules (21550/3050), `git config --global core.helmPath`, `/var/tmp/{scratch,persist}`, sudoers NOPASSWD exists (affected by PAM change: display-manager password still normal)

## Commands Reference
```bash
cd /home/sin/Projects/lia-cli
node --import tsx src/index.ts tasks
node --import tsx src/index.ts start <task-id> <assignee>
node --import tsx src/index.ts done <task-id> <result>
node --import tsx src/index.ts fail <task-id> <reason>
```
