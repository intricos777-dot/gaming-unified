# Architecture Overview

## Twilight Elysium Engine (Shared)

Core C++17 engine providing:
- **Engine Loop** (`engine/engine.cpp:Engine::run`): 60Hz fixed timestep, input pump, tick callbacks, bounded frame execution
- **Resolution Scaler** (`renderer/resolution_scaler.cpp`): Integer/arbitrary scaling, aspect preservation, 5 modes
- **Input System** (`engine/input.cpp`): Keyboard/mouse/gamepad abstraction, action mapping
- **Memory Arena** (`engine/memory.cpp`): Linear/pool allocators, frame-scoped allocations
- **Entity Component** (`engine/entity.cpp`): Lightweight ECS with archetype storage
- **Renderer** (`renderer/renderer.cpp`): Vulkan-ready abstraction, shader pipeline, camera
- **Platform Layer** (`platform/`): Runtime abstraction (local, Satalight distributed, quantum offload)

## Remake Integration

Each remake embeds Twilight Elysium via `add_subdirectory(../engines/twilight-elysium twilight-elysium)` and links `te-engine` / `te-renderer`.

| Remake | Key Systems |
|--------|-------------|
| Kingdom Hearts Zero | Seal-ledger world gating, command deck combat, PS2-style shaders |
| TE Bonfire | 5-zone world graph, progress persistence, stamina combat, gate boss |
| LoZ Majora's Mask | 3-day cycle (1s=1min), time rewind, yaw-steer movement |

## Data Flow

```
Input → Engine::run (60Hz) → Input::poll → Game Tick → Renderer::draw → Scaler → Swapchain
                     ↓
              World/Combat/Story systems (per-remake)
                     ↓
              SaveSystem → JSON (progress, seal ledger, world state)
```
