#!/usr/bin/env bash
# Build all engines and remakes
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
ENGINES="$ROOT/engines"
REMAKES="$ROOT/remakes"

build_cmake() {
    local name=$1
    local src=$2
    local build_dir="$src/build"
    
    echo "=== Building $name ==="
    mkdir -p "$build_dir"
    cd "$build_dir"
    cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_EXPORT_COMPILE_COMMANDS=ON ..
    cmake --build . --config Release -j$(nproc)
    echo "✓ $name built"
}

# Build shared engine first
build_cmake "twilight-elysium" "$ENGINES/twilight-elysium"

# Build remakes (they link twilight-elysium via add_subdirectory)
for r in kingdom-hearts-zero te-bonfire loz-majoras-mask; do
    build_cmake "$r" "$REMAKES/$r"
done

echo "=== All builds complete ==="
echo "Test with:"
echo "  $ENGINES/twilight-elysium/build/te-test --bounded"
echo "  $REMAKES/kingdom-hearts-zero/build/khz-combat-test"
echo "  $REMAKES/te-bonfire/build/te-bonfire --sim"
echo "  $REMAKES/loz-majoras-mask/build/mm --core"
