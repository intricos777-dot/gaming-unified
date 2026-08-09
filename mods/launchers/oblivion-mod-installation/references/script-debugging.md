# Script Error Patterns & Fixes

This document captures common script issues found during Oblivion mod installation, along with their fixes.

## Bash Script Issues

### 1. Operator Precedence Bug
**Problem**: When using `cp ... 2>/dev/null || mkdir -p dir && cp ...`, the `&&` binds tighter than `||`, causing incorrect execution flow.

**Fix**: Always create directories before copying:
```bash
mkdir -p "$DATA_DIR/OBSE/Plugins"
cp -v *.dll "$DATA_DIR/OBSE/Plugins/"
```

### 2. Download Without Verification
**Problem**: `wget -q` suppresses output but errors go unnoticed.

**Fix**: Add download verification:
```bash
download_file() {
    local url="$1"
    local output="$2"
    wget -q "$url" -O "$output" || { echo "Error: Failed to download"; exit 1; }
    if [[ ! -s "$output" ]]; then
        echo "Error: Empty download"
        exit 1
    fi
}
```

### 3. Git Clone Failure on Retry
**Problem**: `git clone` fails if directory already exists from previous run.

**Fix**: Clean temp directory before cloning:
```bash
cleanup_temp() {
    rm -rf /tmp/xOBSE /tmp/*.zip 2>/dev/null || true
}
```

## Python Script Issues

### 1. subprocess.run() Without check=True
**Problem**: Download commands don't raise exceptions on failure.

**Fix**: Always use `check=True`:
```python
subprocess.run(["wget", "-q", url, "-O", output], check=True)
```

### 2. File Operations Without Error Handling
**Problem**: Config file updates fail silently on permission/disk errors.

**Fix**: Wrap in try/except:
```python
try:
    with open(ini_path, 'w') as f:
        f.write(content)
except IOError as e:
    print(f"Error: {e}")
    return False
```

### 3. Unused Imports
**Problem**: `urllib.request` imported but never used.

**Fix**: Remove unused imports.

## Path Consistency

### Steam Paths
Both `~/.steam/steam/` and `~/.local/share/Steam/` point to the same files via symlinks. Use `~/.steam/steam/apps/common/Oblivion/` as primary path.

### User Config Location
Oblivion.ini for Proton/Wine is at:
```
/home/sin/.steam/steam/steamapps/compatdata/22330/pfx/drive_c/users/steamuser/Documents/My Games/Oblivion/
```

Note: Steam AppID 22330 is for Oblivion on Steam. Always verify paths exist before operations.