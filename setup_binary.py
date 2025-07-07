#!/usr/bin/env python3
"""
Setup script for UPID CLI binary installation
Similar to kubectl installation process
"""
import os
import sys
import platform
import subprocess
import urllib.request
import zipfile
import tarfile
from pathlib import Path


def get_system_info():
    """Get system information for binary selection"""
    system = platform.system().lower()
    machine = platform.machine().lower()
    
    # Map architecture names
    arch_map = {
        'x86_64': 'amd64',
        'amd64': 'amd64',
        'aarch64': 'arm64',
        'arm64': 'arm64',
        'armv7l': 'arm',
        'arm': 'arm'
    }
    
    architecture = arch_map.get(machine, machine)
    
    return system, architecture


def get_latest_version():
    """Get latest version from GitHub releases"""
    try:
        # This would fetch from GitHub API
        # For now, return a default version
        return "1.0.0"
    except Exception:
        return "1.0.0"


def download_binary(version, system, architecture):
    """Download binary from GitHub releases"""
    base_url = f"https://github.com/your-org/upid-cli/releases/download/v{version}"
    
    if system == "windows":
        filename = f"upid-cli-windows-amd64.zip"
        url = f"{base_url}/{filename}"
    elif system == "darwin":
        filename = f"upid-cli-macos-{architecture}.tar.gz"
        url = f"{base_url}/{filename}"
    else:  # linux
        filename = f"upid-cli-linux-{architecture}.tar.gz"
        url = f"{base_url}/{filename}"
    
    print(f"📥 Downloading {filename}...")
    
    # Create temp directory
    temp_dir = Path("temp")
    temp_dir.mkdir(exist_ok=True)
    
    # Download file
    local_path = temp_dir / filename
    try:
        urllib.request.urlretrieve(url, local_path)
        print(f"✅ Downloaded to {local_path}")
        return local_path
    except Exception as e:
        print(f"❌ Failed to download: {e}")
        return None


def extract_binary(archive_path, system):
    """Extract binary from archive"""
    print(f"📦 Extracting {archive_path}...")
    
    temp_dir = Path("temp")
    extract_dir = temp_dir / "extracted"
    extract_dir.mkdir(exist_ok=True)
    
    try:
        if archive_path.suffix == '.zip':
            with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)
        else:
            with tarfile.open(archive_path, 'r:gz') as tar_ref:
                tar_ref.extractall(extract_dir)
        
        # Find the binary
        binary_name = "upid.exe" if system == "windows" else "upid"
        binary_path = extract_dir / binary_name
        
        if binary_path.exists():
            print(f"✅ Extracted binary: {binary_path}")
            return binary_path
        else:
            print(f"❌ Binary not found in archive")
            return None
            
    except Exception as e:
        print(f"❌ Failed to extract: {e}")
        return None


def install_binary(binary_path, system):
    """Install binary to system"""
    print("🔧 Installing UPID CLI...")
    
    # Determine installation directory
    if system == "windows":
        # Check if running as administrator
        try:
            result = subprocess.run(['net', 'session'], capture_output=True)
            if result.returncode == 0:
                install_dir = Path("C:/Windows/System32")
                print("Installing system-wide (administrator)")
            else:
                install_dir = Path(os.environ['USERPROFILE']) / "AppData/Local/Microsoft/WinGet/Packages"
                install_dir.mkdir(parents=True, exist_ok=True)
                print(f"Installing to user directory: {install_dir}")
        except:
            install_dir = Path(os.environ['USERPROFILE']) / "AppData/Local/Microsoft/WinGet/Packages"
            install_dir.mkdir(parents=True, exist_ok=True)
    else:
        # Unix-like systems
        if os.geteuid() == 0:
            install_dir = Path("/usr/local/bin")
            print("Installing system-wide (root)")
        else:
            install_dir = Path.home() / ".local/bin"
            install_dir.mkdir(parents=True, exist_ok=True)
            print(f"Installing to user directory: {install_dir}")
    
    # Copy binary
    target_path = install_dir / ("upid.exe" if system == "windows" else "upid")
    
    try:
        import shutil
        shutil.copy2(binary_path, target_path)
        
        # Make executable on Unix systems
        if system != "windows":
            os.chmod(target_path, 0o755)
        
        print(f"✅ Installed to: {target_path}")
        return target_path
        
    except Exception as e:
        print(f"❌ Failed to install: {e}")
        return None


def add_to_path(install_path, system):
    """Add installation directory to PATH"""
    if system == "windows":
        print("ℹ️  Please add the installation directory to your PATH manually")
        print(f"   Installation directory: {install_path.parent}")
    else:
        # Unix-like systems
        shell_rc = None
        if "zsh" in os.environ.get("SHELL", ""):
            shell_rc = Path.home() / ".zshrc"
        elif "bash" in os.environ.get("SHELL", ""):
            shell_rc = Path.home() / ".bashrc"
        
        if shell_rc and shell_rc.exists():
            path_line = f'export PATH="{install_path.parent}:$PATH"'
            
            # Check if already in PATH
            with open(shell_rc, 'r') as f:
                content = f.read()
            
            if path_line not in content:
                with open(shell_rc, 'a') as f:
                    f.write(f"\n# UPID CLI\n{path_line}\n")
                print(f"✅ Added to {shell_rc}")
            else:
                print(f"ℹ️  Already in {shell_rc}")
        else:
            print("ℹ️  Please add the installation directory to your PATH manually")
            print(f"   Installation directory: {install_path.parent}")


def verify_installation(install_path):
    """Verify the installation"""
    print("🔍 Verifying installation...")
    
    try:
        # Test the binary
        result = subprocess.run([str(install_path), '--version'], 
                              capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✅ Installation verified!")
            print(f"Version: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ Verification failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Verification failed: {e}")
        return False


def cleanup():
    """Clean up temporary files"""
    temp_dir = Path("temp")
    if temp_dir.exists():
        import shutil
        shutil.rmtree(temp_dir)
        print("🧹 Cleaned up temporary files")


def main():
    """Main installation function"""
    print("🚀 UPID CLI Binary Installer")
    print("=" * 40)
    
    # Get system information
    system, architecture = get_system_info()
    print(f"System: {system}")
    print(f"Architecture: {architecture}")
    
    # Get version
    version = get_latest_version()
    print(f"Version: {version}")
    
    # Check if binary already exists
    binary_name = "upid.exe" if system == "windows" else "upid"
    existing_paths = [
        Path("/usr/local/bin") / binary_name,
        Path.home() / ".local/bin" / binary_name,
        Path("C:/Windows/System32") / binary_name if system == "windows" else None
    ]
    
    existing_path = None
    for path in existing_paths:
        if path and path.exists():
            existing_path = path
            break
    
    if existing_path:
        print(f"ℹ️  UPID CLI already installed at: {existing_path}")
        response = input("Do you want to reinstall? (y/N): ")
        if response.lower() != 'y':
            print("Installation cancelled.")
            return True
    
    # Download binary
    archive_path = download_binary(version, system, architecture)
    if not archive_path:
        print("❌ Failed to download binary")
        return False
    
    # Extract binary
    binary_path = extract_binary(archive_path, system)
    if not binary_path:
        print("❌ Failed to extract binary")
        return False
    
    # Install binary
    install_path = install_binary(binary_path, system)
    if not install_path:
        print("❌ Failed to install binary")
        return False
    
    # Add to PATH
    add_to_path(install_path, system)
    
    # Verify installation
    if verify_installation(install_path):
        print("\n🎉 UPID CLI installed successfully!")
        print(f"Usage: {binary_name} --help")
        
        # Show next steps
        print("\n📋 Next steps:")
        print("1. Restart your terminal or run: source ~/.bashrc")
        print("2. Test the installation: upid --help")
        print("3. Configure authentication: upid auth login")
        print("4. Start optimizing: upid cluster list")
        
        return True
    else:
        print("❌ Installation verification failed")
        return False
    
    finally:
        cleanup()


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 