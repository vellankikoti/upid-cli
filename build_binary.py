#!/usr/bin/env python3
"""
Binary build script for UPID CLI
Creates standalone executables similar to kubectl
"""
import os
import sys
import shutil
import subprocess
import platform
from pathlib import Path


def run_command(cmd, description):
    """Run a command and handle errors"""
    print(f"\n🔄 {description}...")
    print(f"Command: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed")
        print(f"Error: {e}")
        if e.stdout:
            print(f"stdout: {e.stdout}")
        if e.stderr:
            print(f"stderr: {e.stderr}")
        return False


def install_build_dependencies():
    """Install dependencies for building binaries"""
    dependencies = [
        "pyinstaller>=5.0.0",
        "setuptools>=65.0.0",
        "wheel>=0.37.0"
    ]
    
    for dep in dependencies:
        cmd = ["pip", "install", dep]
        if not run_command(cmd, f"Installing {dep}"):
            return False
    return True


def create_pyinstaller_spec():
    """Create PyInstaller spec file for UPID CLI"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['upid/cli.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('upid/core', 'upid/core'),
        ('upid/commands', 'upid/commands'),
        ('upid/services', 'upid/services'),
    ],
    hiddenimports=[
        'click',
        'rich',
        'requests',
        'yaml',
        'json',
        'pathlib',
        'tempfile',
        'subprocess',
        'sys',
        'os',
        'time',
        'datetime',
        'typing',
        'unittest.mock',
        'pytest',
        'testcontainers',
        'docker',
        'kubernetes',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='upid',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icon.ico' if os.path.exists('assets/icon.ico') else None,
)
'''
    
    with open('upid.spec', 'w') as f:
        f.write(spec_content)
    
    print("✅ PyInstaller spec file created")
    return True


def build_binary():
    """Build the binary using PyInstaller"""
    # Create spec file
    if not create_pyinstaller_spec():
        return False
    
    # Build binary
    cmd = ["pyinstaller", "--clean", "upid.spec"]
    return run_command(cmd, "Building binary with PyInstaller")


def build_for_platforms():
    """Build binaries for multiple platforms"""
    platforms = {
        'linux': 'linux',
        'darwin': 'macos',
        'win32': 'windows'
    }
    
    current_platform = sys.platform
    target_platform = platforms.get(current_platform, current_platform)
    
    print(f"🎯 Building for platform: {target_platform}")
    
    # Build for current platform
    if not build_binary():
        return False
    
    # Move binary to appropriate location
    dist_dir = Path("dist")
    if dist_dir.exists():
        binary_name = "upid.exe" if target_platform == "windows" else "upid"
        binary_path = dist_dir / binary_name
        
        if binary_path.exists():
            # Create platform-specific directory
            platform_dir = Path(f"binaries/{target_platform}")
            platform_dir.mkdir(parents=True, exist_ok=True)
            
            # Copy binary
            target_path = platform_dir / binary_name
            shutil.copy2(binary_path, target_path)
            
            # Make executable on Unix systems
            if target_platform != "windows":
                os.chmod(target_path, 0o755)
            
            print(f"✅ Binary created: {target_path}")
            return True
    
    return False


def create_install_script():
    """Create installation script for the binary"""
    install_script = '''#!/bin/bash
# UPID CLI Binary Installer

set -e

# Colors for output
RED='\\033[0;31m'
GREEN='\\033[0;32m'
YELLOW='\\033[1;33m'
NC='\\033[0m' # No Color

echo -e "${GREEN}🚀 Installing UPID CLI Binary${NC}"

# Detect OS and architecture
OS=$(uname -s | tr '[:upper:]' '[:lower:]')
ARCH=$(uname -m)

case $ARCH in
    x86_64) ARCH="amd64" ;;
    aarch64) ARCH="arm64" ;;
    armv7l) ARCH="arm" ;;
    *) ARCH="unknown" ;;
esac

echo "Detected OS: $OS, Architecture: $ARCH"

# Determine binary name
if [[ "$OS" == "darwin" ]]; then
    PLATFORM="macos"
    BINARY_NAME="upid"
elif [[ "$OS" == "linux" ]]; then
    PLATFORM="linux"
    BINARY_NAME="upid"
else
    echo -e "${RED}❌ Unsupported operating system: $OS${NC}"
    exit 1
fi

# Check if binary exists
BINARY_PATH="binaries/$PLATFORM/$BINARY_NAME"
if [[ ! -f "$BINARY_PATH" ]]; then
    echo -e "${RED}❌ Binary not found: $BINARY_PATH${NC}"
    echo "Please build the binary first using: python build_binary.py"
    exit 1
fi

# Determine installation directory
if [[ "$EUID" -eq 0 ]]; then
    # Root installation
    INSTALL_DIR="/usr/local/bin"
    echo -e "${YELLOW}Installing system-wide (requires sudo)${NC}"
else
    # User installation
    INSTALL_DIR="$HOME/.local/bin"
    mkdir -p "$INSTALL_DIR"
    echo -e "${YELLOW}Installing to user directory: $INSTALL_DIR${NC}"
fi

# Install binary
echo "Installing UPID CLI to $INSTALL_DIR..."
cp "$BINARY_PATH" "$INSTALL_DIR/upid"
chmod +x "$INSTALL_DIR/upid"

# Add to PATH if not already there
if [[ ":$PATH:" != *":$INSTALL_DIR:"* ]]; then
    echo -e "${YELLOW}Adding $INSTALL_DIR to PATH...${NC}"
    
    if [[ "$SHELL" == *"zsh"* ]]; then
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
        echo -e "${GREEN}Added to ~/.zshrc${NC}"
    elif [[ "$SHELL" == *"bash"* ]]; then
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
        echo -e "${GREEN}Added to ~/.bashrc${NC}"
    else
        echo -e "${YELLOW}Please add $INSTALL_DIR to your PATH manually${NC}"
    fi
fi

echo -e "${GREEN}✅ UPID CLI installed successfully!${NC}"
echo -e "${GREEN}Usage: upid --help${NC}"

# Verify installation
if command -v upid &> /dev/null; then
    echo -e "${GREEN}✅ Installation verified!${NC}"
    upid --version
else
    echo -e "${YELLOW}⚠️  Please restart your terminal or run: source ~/.bashrc${NC}"
fi
'''
    
    with open('install.sh', 'w') as f:
        f.write(install_script)
    
    # Make executable
    os.chmod('install.sh', 0o755)
    print("✅ Installation script created: install.sh")


def create_windows_installer():
    """Create Windows installer script"""
    install_bat = '''@echo off
REM UPID CLI Binary Installer for Windows

echo 🚀 Installing UPID CLI Binary

REM Check if running as administrator
net session >nul 2>&1
if %errorLevel% == 0 (
    echo Installing system-wide...
    set "INSTALL_DIR=C:\\Windows\\System32"
) else (
    echo Installing to user directory...
    set "INSTALL_DIR=%USERPROFILE%\\AppData\\Local\\Microsoft\\WinGet\\Packages"
    if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"
)

REM Copy binary
if exist "binaries\\windows\\upid.exe" (
    copy "binaries\\windows\\upid.exe" "%INSTALL_DIR%\\upid.exe"
    echo ✅ UPID CLI installed successfully!
    echo Usage: upid --help
) else (
    echo ❌ Binary not found: binaries\windows\upid.exe
    echo Please build the binary first using: python build_binary.py
    pause
    exit /b 1
)

echo.
echo Installation complete!
echo You can now use: upid --help
pause
'''
    
    with open('install.bat', 'w') as f:
        f.write(install_bat)
    
    print("✅ Windows installer created: install.bat")


def create_release_package():
    """Create release package with binaries and documentation"""
    import zipfile
    import tarfile
    
    # Create release directory
    release_dir = Path("release")
    release_dir.mkdir(exist_ok=True)
    
    # Copy binaries
    binaries_dir = Path("binaries")
    if binaries_dir.exists():
        for platform_dir in binaries_dir.iterdir():
            if platform_dir.is_dir():
                platform_name = platform_dir.name
                for binary in platform_dir.glob("*"):
                    if binary.is_file():
                        # Create platform-specific release
                        release_name = f"upid-cli-{platform_name}"
                        release_path = release_dir / release_name
                        release_path.mkdir(exist_ok=True)
                        
                        # Copy binary
                        shutil.copy2(binary, release_path / binary.name)
                        
                        # Copy documentation
                        docs = ["README.md", "LICENSE", "CHANGELOG.md"]
                        for doc in docs:
                            if Path(doc).exists():
                                shutil.copy2(doc, release_path)
                        
                        # Copy installation scripts
                        if platform_name == "windows":
                            shutil.copy2("install.bat", release_path)
                        else:
                            shutil.copy2("install.sh", release_path)
                        
                        # Create archive
                        if platform_name == "windows":
                            with zipfile.ZipFile(f"{release_path}.zip", 'w') as zipf:
                                for file in release_path.rglob("*"):
                                    zipf.write(file, file.relative_to(release_path))
                        else:
                            with tarfile.open(f"{release_path}.tar.gz", 'w:gz') as tar:
                                tar.add(release_path, arcname=release_path.name)
                        
                        print(f"✅ Created release: {release_path}.zip" if platform_name == "windows" else f"✅ Created release: {release_path}.tar.gz")
    
    print("✅ Release packages created in 'release' directory")


def create_docker_image():
    """Create Docker image with the binary"""
    dockerfile = '''FROM alpine:latest

# Install dependencies
RUN apk add --no-cache python3 py3-pip

# Copy binary
COPY binaries/linux/upid /usr/local/bin/upid
RUN chmod +x /usr/local/bin/upid

# Create symlink for kubectl-style usage
RUN ln -sf /usr/local/bin/upid /usr/local/bin/kubectl-upid

# Set entrypoint
ENTRYPOINT ["upid"]
CMD ["--help"]
'''
    
    with open('Dockerfile.binary', 'w') as f:
        f.write(dockerfile)
    
    print("✅ Dockerfile created: Dockerfile.binary")


def main():
    """Main build function"""
    print("🔨 UPID CLI Binary Builder")
    print("=" * 40)
    
    # Install build dependencies
    if not install_build_dependencies():
        print("❌ Failed to install build dependencies")
        return False
    
    # Build binary
    if not build_for_platforms():
        print("❌ Failed to build binary")
        return False
    
    # Create installation scripts
    create_install_script()
    create_windows_installer()
    
    # Create release packages
    create_release_package()
    
    # Create Docker image
    create_docker_image()
    
    print("\n🎉 Binary build completed successfully!")
    print("\n📦 Available outputs:")
    print("  - Binaries: binaries/")
    print("  - Installation scripts: install.sh, install.bat")
    print("  - Release packages: release/")
    print("  - Docker image: Dockerfile.binary")
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 