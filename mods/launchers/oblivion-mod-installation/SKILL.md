---
name: oblivion-mod-installation
description: "Install and verify Oblivion mods and OBSE plugins."
version: 1.1.0
author: Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [games, oblivion, mods, obse, installation]
---

# Oblivion Mod Installation & Management

Use when installing, verifying, or troubleshooting Oblivion (2006) mods and OBSE plugins, especially OBSE plugins, ESP files, and load order configuration.

## User Preferences

- **Response Style**: Concise, direct. State what's installed, file locations, and status. Only explain when asked.
- **Mod Pattern**: Follow Skyrim RealisticAI Overhaul structure when setting up similar mods for Oblivion
- **Version Specific**: Reference Oblivion 2006 specifically, not Remastered unless explicitly stated

## Key Paths

- **Verified Steam Installation**: `/home/sin/.steam/steam/steamapps/common/Oblivion/` (confirmed working)
- **Data Folder**: `/home/sin/.steam/steam/steamapps/common/Oblivion/Data/`
- **OBSE Plugins**: `/home/sin/.steam/steam/steamapps/common/Oblivion/Data/OBSE/Plugins/`
- **User Config**: `/home/sin/.steam/steam/steamapps/compatdata/22330/pfx/drive_c/users/steamuser/Documents/My Games/Oblivion/`
- **Mod Organizer**: `/home/sin/.steam/steam/steamapps/common/Oblivion/ModOrganizer2/`

> **Note**: Steam creates symlinks between `~/.steam/steam/` and `~/.local/share/Steam/`. Use the `.steam` path as primary.

## OBSE Plugin Installation

1. **Verify OBSE Core**:
   ```bash
   ls -lh "/home/sin/.local/share/Steam/steamapps/common/Oblivion/" | grep obse
   ```
   Should show: `obse_1_2_416.dll`, `obse_loader.exe`, `obse_steam_loader.dll`

2. **Install Plugin**:
   - Copy `.dll` to `Data/OBSE/Plugins/`
   - No .ini needed for most plugins (auto-configures on first run)
   - No load order entry required (plugins load automatically)

3. **Verify Installation**:
   ```bash
   ls -la "/home/sin/.local/share/Steam/steamapps/common/Oblivion/Data/OBSE/Plugins/"
   ```

## ESP/ESM Mod Installation

1. **Manual Install**:
   - Extract mod archive
   - Copy `.esp`/`.esm` files to `Data/` folder
   - Add to load order in Oblivion.ini

2. **Load Order Configuration**:
   Add to `Oblivion.ini` in `[General]` section:
   ```
   STestFile1=ModName.esp
   STestFile2=AnotherMod.esp
   ```

3. **Essential Mods to Load First**:
   - Unofficial Oblivion Patch
   - Oblivion Stutter Remover (if using)

## Oblivion vs Oblivion Remastered

- **Original Oblivion (2006)**: Uses OBSE, Radiant AI, etc.
- **Oblivion Remastered (2024)**: Uses OBSE64, different mod ecosystem
- **Mods are NOT interchangeable between versions**

## AI Overhaul Mod Installation Pattern

Following Skyrim RealisticAI Overhaul pattern:

1. **Radiant AI** (2006 Oblivion AI enhancement):
   - Download from Nexus Mods (mod ID 49610)
   - Place `RadiantAI.esp` in Data folder
   - Load after Oblivion.esm, before other mods
   - No additional configuration needed

2. **Divine Director** (OBSE plugin for blessings):
   - Already installed in OBSE/Plugins folder
   - Auto-configures on first run
   - No manual configuration required

## Streamlined Response Format

**Concise verification format**:
- State what's installed
- Show file locations and sizes
- State if working correctly
- Note any missing requirements

No verbose explanations unless asked.

## Scripts

- `scripts/install-radiant-ai.py` - Automated Radiant AI installer script
- `scripts/verify-install.py` - Installation verifier (NEW) - Run to check OBSE, plugins, and Display Tweaks are installed

## Reference Files

- `references/radiant-ai.md` - Detailed info on Radiant AI mod installation
- `references/script-debugging.md` - Script error patterns, common bugs, and fixes (NEW)

## Related Mods

- Divine Director (OBSE plugin for extended blessings)
- Oblivion Display Tweaks (graphics improvements)
- Unofficial Oblivion Patch (essential bugfix)

## Common Issues & Fixes

- **No crash logs**: Check Oblivion/Data/Saves/ for .ess files
- **Mod not loading**: Verify ESP is in Data/ folder and loaded in Oblivion.ini
- **OBSE not working**: Ensure obse_1_2_416.dll is in game root directory

## Script Error Patterns & Fixes

### Bash Script Issues
- **Operator precedence**: `&&` binds tighter than `||`. When using `cp ... 2>/dev/null || mkdir -p dir && cp ...`, the second cp may not execute. Use parentheses or separate commands.
- **Download validation**: Always verify wget succeeded before unzip. Use `set +e` around downloads, check exit codes, or use `wget -q --spider` to test URL accessibility.
- **Clean temp directories**: `git clone` fails if directory exists. Clean `/tmp` contents before cloning or use `git -C dir pull` for updates.

### Python Script Issues
- **subprocess.run()**: Always add `check=True` to raise exceptions on failure. Without it, download failures go unnoticed.
- **File operations**: Use try/except blocks for config file updates. File writes can fail due to permissions or disk space.
- **Unused imports**: Remove imports that aren't used (e.g., `urllib.request` in setup_oblivion_mods.py).

### Path Consistency
- **Steam paths vary**: Use `$(find /home -name "Oblivion" -type d 2>/dev/null | head -1)" to dynamically find the Oblivion installation.
- **Oblivion.ini location**: In Proton/Wine, config is at `~/.steam/steam/steamapps/compatdata/22330/pfx/drive_c/users/steamuser/Documents/My Games/Oblivion/`

## Verified Working Paths
```
Steam Installation: /home/sin/.steam/steam/steamapps/common/Oblivion/
Data Folder: /home/sin/.steam/steam/steamapps/common/Oblivion/Data/
User Config: /home/sin/.steam/steam/steamapps/compatdata/22330/pfx/drive_c/users/steamuser/Documents/My GameS/Oblivion/
```