# Living Sin Gaming Unified

Monorepo consolidating remakes, engine, mods, and tinkerbench tooling.

## Structure

```
gaming-unified/
├── engines/
│   └── twilight-elysium/          # Shared C++17 engine (60Hz loop, scaler, input)
├── remakes/
│   ├── kingdom-hearts-zero/       # KH-Z Act 2: seal-ledger gating, Nobody sightings
│   ├── te-bonfire/                # 5-zone chain, Ember Watcher gate boss, progress persist
│   └── loz-majoras-mask/          # 3-day cycle (1s=1min), Song of Time, movement
├── mods/
│   ├── ship-of-harkinian/         # OoT MQ randomizer configs, controller DB
│   ├── oblivion/                  # ModOrganizer plugins, display tweaks, AI overhaul
│   ├── skyrim-scaffold/           # Mod scaffold template
│   └── launchers/                 # Steam non-steam launch scripts
├── tinkerbench/
│   ├── steam-tinker-config/       # Steam Tinker Launch profiles
│   ├── build-scripts/             # CMake presets, vcpkg, CI
│   └── profiling/                 # Perf scripts, scalers, debug overlays
├── portfolio/                     # Gaming portfolio website
└── docs/
    ├── architecture.md
    ├── build-guide.md
    └── modding-guide.md
```

## Quick Start

```bash
# Build all (requires CMake 3.20+, vcpkg)
./build-all.sh

# Run individual tests
cd engines/twilight-elysium/build && ./te-test --bounded
cd remakes/kingdom-hearts-zero/build && ./khz-combat-test
cd remakes/te-bonfire/build && ./te-bonfire --sim
cd remakes/loz-majoras-mask/build && ./mm --core
```

## Status

| Component | State |
|-----------|-------|
| twilight-elysium | ✅ Engine loop fixed, 60Hz bounded test passes |
| kingdom-hearts-zero | ✅ Act 2 complete, seal gating, 3/3 tests pass |
| te-bonfire | ✅ Progression complete, 5 zones, boss victory |
| loz-majoras-mask | ✅ Time cycle + movement, 13/13 checks pass |
| Ship of Harkinian | ✅ Mod configs, controller DB |
| Oblivion Mods | ✅ ModOrganizer, display tweaks, AI overhaul |
| Steam Tinker Launch | ✅ Config profiles |

## License

MIT for engine/remakes; mods retain original licenses.
