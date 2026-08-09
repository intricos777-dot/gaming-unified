---
name: skyrim-mod-scaffold
description: "Skyrim SE mod scaffolding: layout, build scripts, packaging."
version: 0.1.0
author: Hermes Agent
license: MIT
platforms: [linux, windows, macos]
metadata:
  hermes:
    tags: [skyrim, bethesda, mod, esp, ba2, plugin, creation-kit, xedit]
    category: game-mods
    related_skills: [git-project-finalization, project-scaffold-and-publish]
---

# Skyrim Mod Scaffold

Use when the user wants to build a Skyrim SE/VR mod project repo: ESP/ESM plugins, BA2 archives, build scripts, release packaging, or mod installation verification.

## Trigger

- "finish my elder scrolls mod build for Skyrim"
- "scaffold a Skyrim total-conversion"
- "Skyrim SE mod repo structure"
- "plugin/ba2 packaging for Skyrim"
- "Elsweyr mod" or similar TC project

## Repo Layout

```
<project>/
├── README.md
├── LICENSE
├── .gitignore
├── build.ps1 / build.sh
├── Data/
│   ├── Meshes/
│   ├── Textures/
│   ├── Sound/
│   ├── Scripts/
│   ├── Plugins/
│   ├── Interface/Translations/
│   └── SKSE/Plugins/
├── src/
│   ├── quests/
│   ├── cells/
│   ├── scripts/
│   └── assets/
├── dist/
│   ├── esp/
│   └── ba2/
├── tools/
├── docs/
│   ├── install.md
│   ├── changelog.md
│   └── assets/
└── logs/
```

## Plugin Metadata Pattern

Master ESP/ESM should declare:
- Author, Description, Version
- Dependencies: Skyrim.esm, DLCs, framework mods
- Recommended load order position

## Build Script Pattern

PowerShell `build.ps1` for Windows Creation Kit/xEdit workflow:
```powershell
param([switch]$Release)
$ErrorActionPreference = 'Stop'
$Timestamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$DistEsp = Join-Path $PSScriptRoot 'dist/esp'
$DistBa2 = Join-Path $PSScriptRoot 'dist/ba2'
if (-not (Test-Path $DistEsp)) { New-Item -ItemType Directory -Path $DistEsp | Out-Null }
if (-not (Test-Path $DistBa2)) { New-Item -ItemType Directory -Path $DistBa2 | Out-Null }
Write-Host "Build complete: $Timestamp"
```

## Git Hygiene

- Do not commit `__pycache__`, `.pyc`, build intermediates, or loose asset dumps outside `dist/` and `Data/`.
- Add `.gitignore` entries: `__pycache__/`, `*.pyc`, `build/`, `dist/*.ba2.uncompressed`, `logs/*.log`.

## References

- `references/tools-and-workflow.md` — Creation Kit, xEdit, CAO, DynDOLOD, load order, packaging patterns for Skyrim SE mods.

- Confirm `Data/Plugins/`, `dist/esp/`, and `dist/ba2/` exist.
- Confirm `README.md` has Requirements, Quick Build, Manual Build, and Contents sections.
- Confirm git status is clean before commit.
- Confirm repo remote exists and push succeeds.

## Pitfalls

- Creation Kit/xEdit are Windows tools; on Linux use Proton/SteamTinkerLaunch or a Windows VM.
- ESP/ESM filenames must be unique across all active plugins.
- BA2 compression requires Cathedral Assets Optimizer or official tools; do not hand-roll archives.
- If the user says “finish the build” but `Data/` is empty, scaffold the build scripts and docs first; actual asset generation is session-specific and cannot be auto-created.
- Do not invent fake plugin records or manifests. If content is missing, build the scaffolding and stop, rather than fabricating records.