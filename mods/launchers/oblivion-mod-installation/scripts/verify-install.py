#!/usr/bin/env python3
"""
Oblivion Installation Verification Script
Verifies OBSE, plugins, and Display Tweaks are properly installed.
"""

from pathlib import Path
import hashlib

# Verified paths
OBLIVION_DIR = Path("/home/sin/.steam/steam/steamapps/common/Oblivion")
DATA_DIR = OBLIVION_DIR / "Data"
PLUGINS_DIR = DATA_DIR / "OBSE/Plugins"

def verify_obse():
    """Check OBSE core files"""
    issues = []
    
    # Check for obse dll in game root
    obse_dll = OBLIVION_DIR / "obse_1_2_416.dll"
    if not obse_dll.exists():
        issues.append(f"Missing: {obse_dll}")
    
    # Check for obse loader
    obse_loader = OBLIVION_DIR / "obse_loader.exe"
    if not obse_loader.exists():
        issues.append(f"Missing: {obse_loader}")
    
    return issues

def verify_plugins():
    """Check OBSE plugins"""
    issues = []
    
    if not PLUGINS_DIR.exists():
        issues.append(f"Plugins directory missing: {PLUGINS_DIR}")
        return issues
    
    # Check for essential plugins
    essential_plugins = [
        "oblivion_display_tweaks.dll"
    ]
    
    for plugin in essential_plugins:
        plugin_path = PLUGINS_DIR / plugin
        if not plugin_path.exists():
            issues.append(f"Missing plugin: {plugin_path}")
    
    # List installed plugins
    installed = list(PLUGINS_DIR.glob("*.dll"))
    if installed:
        print(f"Installed plugins: {[p.name for p in installed]}")
    
    return issues

def verify_display_tweaks():
    """Check Oblivion Display Tweaks installation"""
    issues = []
    
    # Check for ODT files in Data folder (not just Plugins)
    odt_indicators = [
        "OblivionDisplayTweaks.ini",
        "OblivionDisplayTweaks.esp",
        "ODT.dll"
    ]
    
    found_path = ""
    for indicator in odt_indicators:
        for path in [DATA_DIR, DATA_DIR / "OBSE"]:
            if (path / indicator).exists():
                found_path = str(path / indicator)
                break
        if found_path:
            break
    
    if not found_path:
        issues.append("Oblivion Display Tweaks not found in Data folder")
    
    # Check obse.ini
    obse_ini = DATA_DIR / "OBSE" / "obse.ini"
    if obse_ini.exists():
        print(f"✓ Found obse.ini")
    else:
        issues.append(f"Missing: {obse_ini}")
    
    return issues

def verify_save_files():
    """Check for save files (indicates game has been played)"""
    saves_dir = DATA_DIR / "Saves"
    if saves_dir.exists():
        saves = list(saves_dir.glob("*.ess"))
        print(f"Save files found: {len(saves)}")
        return []
    return ["No save directory found - game may not have launched"]

def main():
    print("=== Oblivion Installation Verification ===\n")
    
    all_issues = []
    
    print("Checking OBSE core...")
    issues = verify_obse()
    all_issues.extend(issues)
    
    print("Checking OBSE plugins...")
    issues = verify_plugins()
    all_issues.extend(issues)
    
    print("Checking Display Tweaks...")
    issues = verify_display_tweaks()
    all_issues.extend(issues)
    
    print("Checking save files...")
    issues = verify_save_files()
    all_issues.extend(issues)
    
    if all_issues:
        print("\n=== Issues Found ===")
        for issue in all_issues:
            print(f"  - {issue}")
        return 1
    
    print("\n✓ All checks passed!")
    return 0

if __name__ == "__main__":
    exit(main())