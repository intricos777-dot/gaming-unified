# Skyrim Modding Tools

## Creation Kit
- Official Bethesda toolset for Skyrim SE plugin authoring.
- Windows-only; on Linux use Steam/Proton or a Windows VM.
- Builds `.esp`/`.esm` plugins and can export assets into `Data/`.

## xEdit 4.0+
- Oblivion/Skyrim/Fallout record editor.
- Use for cleaning, patching, and verifying plugin records.
- Output goes to `dist/esp/` or `Data/Plugins/`.

## Cathedral Assets Optimizer
- Optimizes textures/meshes and builds `.ba2` archives.
- Input: loose assets in `Data/Textures/`, `Data/Meshes/`
- Output: compressed `.ba2` in `dist/ba2/`

## DynDOLOD / xLODGen
- LOD generation for terrain, trees, and objects.
- Run after CAO; output into `Data/` or separate LOD ESP.

## Load Order
- Always keep `Skyrim.esm` + DLCs first.
- Framework mods before content mods.
- LOD/bugfix/patch ESPs at the end.
- Verify with LOOT when possible.

## Packaging
- Mod Manager 2 / Vortex: distribute as 7z/FOMOD.
- Manual install: copy `Data/` contents into Skyrim `Data/`.
- BA2 + ESP only; avoid loose files outside `Data/`.
