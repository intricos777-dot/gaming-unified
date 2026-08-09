# Modding Guide

## Ship of Harkinian (OoT MQ)

### Controller Database
`mods/ship-of-harkinian/gamecontrollerdb.txt` - SDL2 GameControllerDB with 600+ mappings.

### Mod Structure
```
mods/ship-of-harkinian/
├── mods/              # Place .pak/.z64 mods here
├── assets/            # Custom textures, models
├── gamecontrollerdb.txt
└── soh                # Binary (built separately)
```

### Launch with Custom Profile
```bash
./soh --profile oot-mq --controller-db ../mods/ship-of-harkinian/gamecontrollerdb.txt
```

## Oblivion (ModOrganizer 2)

### Profile Structure
```
mods/oblivion/
├── modorganizer/      # MO2 source (build separately)
├── Oblivion-Display-Tweaks/
├── Oblivion-AI-Overhaul/
├── xOBSE/             # OBSE extender
└── plugins.txt        # Load order
```

### Building MO2
```bash
cd mods/oblivion/modorganizer
mkdir build && cd build
cmake -DCMAKE_BUILD_TYPE=Release ..
ninja
sudo ninja install
```

### Launch via Steam Tinker Launch
Uses `oblivion.stl.toml` profile with `MO2_PROFILE=Oblivion-Display-Tweaks`.

## Skyrim Scaffold

Template for new mod projects:
```
mods/skyrim-scaffold/
├── CMakeLists.txt
├── src/
│   ├── papyrus/       # Papyrus scripts
│   └── skse/          # SKSE plugin (C++)
├── data/
│   ├── meshes/
│   ├── textures/
│   └── scripts/
└── build.sh
```

## Adding New Mods

1. Create directory under `mods/<game>/`
2. Add STL profile in `tinkerbench/steam-tinker-config/<game>.stl.toml`
3. Document in this guide
4. Test launch via STL
