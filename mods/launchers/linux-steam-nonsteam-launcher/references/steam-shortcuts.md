# Steam Non-Steam Shortcut Notes

## shortcuts.vdf
- Per-user file: `~/.steam/steam/userdata/<userid>/config/shortcuts.vdf`
- Steam rewrites it on any Library change; treat as volatile.
- Quick check: `strings shortcuts.vdf | grep -i '<gamename>'`

## SteamTinkerLaunch
- `steamtinkerlaunch addnonsteamgame` may open GUI even with args; do not assume silent success.
- Verify shortcut presence with `shortcuts.vdf` or Library UI.
- Proton/workaround settings are often GUI-only for non-Steam shortcuts.
