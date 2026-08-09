param(
    [switch]$Release,
    [switch]$Clean
)

$ErrorActionPreference = 'Stop'
$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$Timestamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$DistEsp = Join-Path $ProjectRoot 'dist/esp'
$DistBa2 = Join-Path $ProjectRoot 'dist/ba2'
$DataDir = Join-Path $ProjectRoot 'Data'
$LogDir = Join-Path $ProjectRoot 'logs'
$LogFile = Join-Path $LogDir "build-$Timestamp.log"

function Write-Log {
    param([string]$Message)
    $entry = "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] $Message"
    Write-Host $entry
    Add-Content -Path $LogFile -Value $entry
}

# Directories
if (-not (Test-Path $DistEsp)) { New-Item -ItemType Directory -Path $DistEsp | Out-Null }
if (-not (Test-Path $DistBa2)) { New-Item -ItemType Directory -Path $DistBa2 | Out-Null }
if (-not (Test-Path $LogDir)) { New-Item -ItemType Directory -Path $LogDir | Out-Null }

Write-Log "Build started. Release=$Release Clean=$Clean"

if ($Clean) {
    Write-Log "Cleaning dist directories..."
    Remove-Item "$DistEsp/*" -Force -ErrorAction SilentlyContinue
    Remove-Item "$DistBa2/*" -Force -ErrorAction SilentlyContinue
    Write-Log "Clean complete."
    exit 0
}

# Placeholder build steps
Write-Log "Copying plugins from Data/ to dist/esp..."
if (Test-Path "$DataDir/Plugins") {
    Get-ChildItem "$DataDir/Plugins/*.esp" -ErrorAction SilentlyContinue | ForEach-Object {
        Copy-Item $_.FullName -Destination $DistEsp -Force
        Write-Log "Copied: $($_.Name)"
    }
    Get-ChildItem "$DataDir/Plugins/*.esm" -ErrorAction SilentlyContinue | ForEach-Object {
        Copy-Item $_.FullName -Destination $DistEsp -Force
        Write-Log "Copied: $($_.Name)"
    }
} else {
    Write-Log "No Data/Plugins directory found."
}

Write-Log "Copying BA2 archives from Data/ to dist/ba2..."
if (Test-Path "$DataDir") {
    Get-ChildItem $DataDir -Filter "*.ba2" -Recurse -ErrorAction SilentlyContinue | ForEach-Object {
        Copy-Item $_.FullName -Destination $DistBa2 -Force
        Write-Log "Copied: $($_.Name)"
    }
} else {
    Write-Log "No BA2 archives found."
}

if ($Release) {
    Write-Log "Release build: creating archive..."
    $ZipPath = Join-Path $DistEsp "release-$Timestamp.zip"
    if (Test-Path $ZipPath) { Remove-Item $ZipPath -Force }
    Compress-Archive -Path "$DistEsp/*", "$DistBa2/*" -DestinationPath $ZipPath -CompressionLevel Optimal
    Write-Log "Release archive: $ZipPath"
}

Write-Log "Build complete."
