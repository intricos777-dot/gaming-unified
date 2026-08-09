#!/usr/bin/env python3
"""
Radiant AI Mod Installer for Oblivion
Automatically downloads and installs Radiant AI mod from Nexus Mods
"""

import os
import subprocess
import sys
from pathlib import Path

# Paths
OBLIVION_DATA = Path("/home/sin/.local/share/Steam/steamapps/common/Oblivion/Data")
OBLIVION_ESP = OBLIVION_DATA / "RadiantAI - NPCs Alive - Cyrodiil.esp"
OBLIVION_INI = Path("/home/sin/.local/share/Steam/steamapps/compatdata/22330/pfx/drive_c/users/steamuser/Documents/My Games/Oblivion/Oblivion.ini")

def check_mod_installed():
    """Check if Radiant AI is already installed"""
    return OBLIVION_ESP.exists()

def download_mod():
    """Download Radiant AI mod - requires Nexus account"""
    print("Radiant AI Mod Installation Script")
    print("=" * 40)
    print()
    print("Manual Download Required:")
    print("1. Visit: https://www.nexusmods.com/oblivion/mods/49610")
    print("2. Log in to your Nexus Mods account")
    print("3. Click 'Files' tab")
    print("4. Download: 'RadiantAI - NPCs Alive - Cyrodiil' (version 3.7)")
    print("5. Extract the .esp file from the archive")
    print()
    
    # In automated mode, expect the file to already exist
    if os.environ.get('AUTOMATED', ''):
        print("Running in automated mode - checking for pre-downloaded mod...")
        esp_file = OBLIVION_DATA.parent.parent / "Downloads" / "RadiantAI - NPCs Alive - Cyrodiil.esp"
        if esp_file.exists():
            return str(esp_file)
        raise RuntimeError("No manual input available in automated mode. Please provide mod file.")
    
    input("Press Enter after downloading the mod...")
    
    # You need to place the .esp file here
    esp_name = input("Enter the name of the .esp file: ").strip()
    if not esp_name:
        esp_name = "RadiantAI - NPCs Alive - Cyrodiil.esp"
    
    return esp_name

def install_mod(esp_file):
    """Copy ESP to Data folder"""
    if not Path(esp_file).exists():
        print(f"Error: {esp_file} not found")
        return False
    
    dest = OBLIVION_DATA / Path(esp_file).name
    
    try:
        # Copy file
        subprocess.run(["cp", esp_file, str(dest)], check=True)
        print(f"✓ Installed: {dest}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error copying file: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

def update_ini():
    """Add mod to load order in Oblivion.ini"""
    try:
        if not OBLIVION_INI.exists():
            print(f"Warning: {OBLIVION_INI} not found - skipping load order update")
            return False
        
        with open(OBLIVION_INI, 'r') as f:
            content = f.read()
    except IOError as e:
        print(f"Error reading Oblivion.ini: {e}")
        return False
    
    # Check if already in load order
    if "RadiantAI" in content:
        print("✓ Already in load order")
        return True
    
    # Add to [General] section
    lines = content.split('\n')
    new_lines = []
    added = False
    
    for line in lines:
        new_lines.append(line)
        if line.startswith('STestFile1=') and not added:
            # Add Radiant AI after first test file
            # Note: Oblivion.ini should handle filenames with spaces
            new_lines.append('STestFile2=RadiantAI - NPCs Alive - Cyrodiil.esp')
            added = True
    
    try:
        with open(OBLIVION_INI, 'w') as f:
            f.write('\n'.join(new_lines))
        print("✓ Added to load order")
        return True
    except IOError as e:
        print(f"Error writing Oblivion.ini: {e}")
        return False

def main():
    """Main installation flow"""
    print()
    
    if check_mod_installed():
        print("✓ Radiant AI is already installed")
        return 0
    
    print("Radiant AI mod not found. Installing...")
    print()
    
    # Get ESP file
    try:
        esp_file = download_mod()
    except RuntimeError as e:
        print(f"Error: {e}")
        return 1
    
    # Install
    if install_mod(esp_file):
        if update_ini():
            print()
            print("✓ Installation complete!")
            print()
            print("Next steps:")
            print("1. Launch Oblivion through Steam")
            print("2. Radiant AI should load automatically")
            print("3. NPCs will now behave more dynamically")
            return 0
        else:
            print("Warning: Mod installed but load order update failed")
            return 1
    return 1

if __name__ == "__main__":
    sys.exit(main())