#!/usr/bin/env bash
# Quick perf profiling for engine/remakes
set -euo pipefail

TARGET=${1:-twilight-elysium}
BUILD_ROOT="/home/sin/Projects/gaming-unified"

case $TARGET in
  te|twilight-elysium)
    EXE="$BUILD_ROOT/engines/twilight-elysium/build/te-test"
    ARGS="--bounded"
    ;;
  khz|kingdom-hearts-zero)
    EXE="$BUILD_ROOT/remakes/kingdom-hearts-zero/build/khz-combat-test"
    ARGS=""
    ;;
  teb|te-bonfire)
    EXE="$BUILD_ROOT/remakes/te-bonfire/build/te-bonfire"
    ARGS="--sim"
    ;;
  mm|majora|loz-majoras-mask)
    EXE="$BUILD_ROOT/remakes/loz-majoras-mask/build/mm"
    ARGS="--core"
    ;;
  *)
    echo "Usage: $0 {te|khz|teb|mm}"
    exit 1
    ;;
esac

if [[ ! -x "$EXE" ]]; then
    echo "Binary not found: $EXE"
    echo "Run ./tinkerbench/build-scripts/build-all.sh first"
    exit 1
fi

echo "Profiling $TARGET ($EXE $ARGS)"
perf record -g --call-graph=dwarf -o /tmp/perf-$TARGET.data "$EXE" $ARGS
perf report -i /tmp/perf-$TARGET.data --stdio --sort=overhead,comm,symbol | head -50
