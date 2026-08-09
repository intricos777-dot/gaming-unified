---
name: linux-steam-nonsteam-launcher
description: "Add native Linux games to Steam with Proton logging."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [steam, proton, non-steam, launcher, linux]
---

# Linux Steam Non-Steam Launcher

## Trigger

Use when the user asks to:
- add a native Linux game or build artifact to Steam as a non-Steam game
- wire SteamTinkerLaunch compatibility / launch options for a non-Steam shortcut
- create a desktop launcher that opens the game through Steam Proton Experimental
- add launch logging for Proton/debug testing

## Preferred Order

1. Create wrapper launcher(s) under `~/.local/bin/`
2. Add non-Steam shortcut via SteamTinkerLaunch or `steam://addnonsteamgame/...`
3. Create desktop entry if requested
4. Verify with ad-hoc script, then clean up temp scripts

## Pitfalls

- Steam does **not** expose Proton Experimental compatibility tool selection for non-Steam shortcuts from CLI. The user must set this manually in Library → Properties → Compatibility once. Document this clearly.
- `steamtinkerlaunch addnonsteamgame` may accept args but still open GUI; do not assume silent success from empty stdout. Verify by reading `shortcuts.vdf` or checking the Library.
- `shortcuts.vdf` is per-user under `~/.steam/steam/userdata/<userid>/config/shortcuts.vdf` and Steam rewrites it on Library changes.
- Desktop `.desktop` files on `~/Desktop` need `chmod +x` and sometimes XDG refresh before the DE shows them.
- Launch wrappers that `exec` the game lose shell logging; use `tee` or `nohup ... | tee` so Proton logs are captured.
- Proton logs go to `~/.steam/steam/steamapps/compatdata/<appid>/` if `PROTON_LOG=1` is set. For non-Steam shortcuts, compatdata appid is derived from the shortcut.
- `steamtinkerlaunch addnonsteamgame` can create **duplicate shortcuts** without warning. Check `shortcuts.vdf` after adding; if duplicates exist, remove the older/unfinished one manually or via the `vdf` Python library. Do not rely on SteamTinkerLaunch to deduplicate.
- Parsing `shortcuts.vdf` with raw struct unpacking is brittle; prefer the `vdf` Python library when available.
- `xdg-open 'steam://addnonsteamgame/...'` can also create shortcuts; verify `shortcuts.vdf` afterward because duplicate creation is silent.

## Verification

- Check `shortcuts.vdf` with `strings` for the game name, exe, and startdir.
- Check desktop file exists, is executable, and contains correct `Exec=`, `Name=`, `Terminal=false`, `Categories=Game`.
- Run wrapper with `--logs` and verify `~/.local/share/ringworld-redux/logs/launch-*.log` contains `[Game] Initializing` and renderer init markers.
- Do **not** leave `/tmp/hermes-verify-*.py` or `.sh` scripts in `/tmp`; delete after use.

## References

- `references/steam-shortcuts.md` — shortcut VDF notes and SteamTinkerLaunch behavior
- `references/proton-compat.md` — Proton Experimental limitation and workaround for non-Steam games

## Templates

- `templates/wrapper-launcher.sh` — base wrapper with Steam/direct modes and logging
- `templates/desktop-launcher.desktop` — desktop entry with Steam launch + DirectLaunch fallback actions

## Scripts

- `scripts/verify-launcher.sh` — reusable verifier for wrapper + desktop entry + log creation
