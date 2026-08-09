# External File Location Verification

When files referenced in scripts don't exist, follow this verification pattern:

## Common Sources

1. **Steam Library Paths**
   - Primary: `~/.steam/steam/steamapps/common/`
   - Secondary: `~/.local/share/Steam/steamapps/common/`
   - Check with: `find /home -type d -name "<GameName>" 2>/dev/null | head -5`

2. **VM/Machine-Specific Paths**
   - Lia.CLI memory vault: `~/.lia-cli/data/memory/`
   - Lia Agent Node: `http://localhost:4123/`
   - Unity projects: `/home/sin/Projects/` or `/home/sin/Games/`

3. **Mod Projects**
   - Oblivion: `/home/sin/.steam/steam/steamapps/common/Oblivion/`
   - Skyrim: `/home/sin/.steam/steam/steamapps/common/Skyrim Special Edition/`
   - Mods: `/home/sin/Games/`, `/home/sin/Projects/`, or `~/MODS/`

## Verification Commands

```bash
# Find any game directory
find /home -type d \( -name "oblivion" -o -name "skyerm" -o -name "halo" \) 2>/dev/null | head -10

# Find Twilight Elysium or Halo
find /home -type f -iname "*twilight*.exe" 2>/dev/null
find /home -type d -iname "*halo*" 2>/dev/null | head -5

# Check Lia agent status
curl -s http://localhost:4123/memory/search?q=twilight 2>/dev/null || echo "Lia agent not running in VM"

# Check for game engine or development tools
which unity || find /home -type d -name "*unity*" 2>/dev/null | head -3
```

## When Files Are Missing

1. **Check if project exists**: Search broadly, not just expected paths
2. **Verify user meant what they said**: "Twilight Elysium engine" - not common, may need clarification
3. **Check VM/local instance**: Lia agent running? VNC connected? Files exported from VM?
4. **Ask for location**: If still missing, ask user to provide the path

## Example Response Pattern

When a file isn't found:
```
NOT FOUND
No Twilight Elysium or Halo-related files found in searched paths.

Possible locations to check:
- /home/sin/Games/ (game mods)
- /home/sin/Projects/ (development projects)
- VM via VNC at :5900

Would you like me to:
1. Search more broadly on your system
2. Help you set up the Twilight Elysium engine structure
3. Something else?
```