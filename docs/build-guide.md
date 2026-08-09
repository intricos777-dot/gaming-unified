# Build Guide

## Prerequisites

- CMake 3.20+
- Ninja or Make
- C++20 compiler (GCC 12+, Clang 15+, MSVC 19.35+)
- vcpkg (for dependencies)
- SDL2 development libraries
- Python 3.10+ (for test scripts)

## Quick Build

```bash
# From repo root
./tinkerbench/build-scripts/build-all.sh
```

## Manual Build (per project)

```bash
cd engines/twilight-elysium
mkdir build && cd build
cmake -DCMAKE_BUILD_TYPE=Release -G Ninja ..
ninja
```

## Running Tests

```bash
# Engine smoke test (60 frames)
./engines/twilight-elysium/build/te-test --bounded

# KH-Z combat test
./remakes/kingdom-hearts-zero/build/khz-combat-test

# TE Bonfire sim
./remakes/te-bonfire/build/te-bonfire --sim

# Majora's Mask core checks
./remakes/loz-majoras-mask/build/mm --core
```

## vcpkg Setup

```bash
git clone https://github.com/microsoft/vcpkg
./vcpkg/bootstrap-vcpkg.sh
./vcpkg/vcpkg install --triplet x64-linux \
  sdl2 sdl2-image sdl2-mixer sdl2-ttf \
  glm fmt spdlog nlohmann-json yaml-cpp imgui entt gtest
export CMAKE_TOOLCHAIN_FILE=$PWD/vcpkg/scripts/buildsystems/vcpkg.cmake
```

## CI (GitHub Actions)

See `.github/workflows/build.yml` for matrix builds (Linux/macOS/Windows).
