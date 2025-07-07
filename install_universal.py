#!/usr/bin/env python3
"""
Universal UPID CLI Installation
Works with any Kubernetes cluster - zero configuration needed
"""

import os
import sys
import subprocess
from pathlib import Path

def check_kubectl():
    """Check if kubectl is installed and working"""
    try:
        result = subprocess.run(['kubectl', 'version', '--client'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ kubectl is installed and working")
            return True
        else:
            print("❌ kubectl is installed but not working")
            return False
    except FileNotFoundError:
        print("❌ kubectl is not installed")
        return False

def check_cluster_connection():
    """Check if we can connect to a Kubernetes cluster"""
    try:
        result = subprocess.run(['kubectl', 'cluster-info'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ Connected to Kubernetes cluster")
            return True
        else:
            print("❌ Cannot connect to Kubernetes cluster")
            return False
    except Exception as e:
        print(f"❌ Error checking cluster connection: {e}")
        return False

def install_requirements():
    """Install Python requirements"""
    try:
        print("📦 Installing Python requirements...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                      check=True)
        print("✅ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False

def setup_cli():
    """Setup the CLI for universal use"""
    try:
        print("🔧 Setting up UPID CLI...")
        
        # Create config directory
        config_dir = Path.home() / '.upid'
        config_dir.mkdir(exist_ok=True)
        
        # Create universal config
        config_file = config_dir / 'config.yaml'
        if not config_file.exists():
            config_content = """# UPID CLI Universal Configuration
# This CLI works with any Kubernetes cluster automatically

# Universal mode - works with any cluster
universal_mode: true

# Auto-detect cluster type
auto_detect: true

# Default settings
timeout: 30
log_level: INFO

# No authentication required for local clusters
local_mode: true

# Profiles for different environments (optional)
profiles:
  local:
    name: "Local Cluster"
    type: "auto-detect"
  dev:
    name: "Development Cluster"
    type: "auto-detect"
  prod:
    name: "Production Cluster"
    type: "auto-detect"

default_profile: local
"""
            config_file.write_text(config_content)
            print("✅ Configuration file created")
        
        return True
    except Exception as e:
        print(f"❌ Failed to setup CLI: {e}")
        return False

def test_installation():
    """Test the installation"""
    try:
        print("🧪 Testing installation...")
        
        # Test CLI import
        sys.path.insert(0, str(Path.cwd()))
        from upid.core.cluster_detector import ClusterDetector
        
        # Test cluster detection
        detector = ClusterDetector()
        cluster_info = detector.detect_cluster()
        
        if cluster_info['status'] == 'connected':
            print(f"✅ Successfully detected cluster: {cluster_info['name']} ({cluster_info['type']})")
            return True
        else:
            print(f"⚠️  Cluster detection failed: {cluster_info.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ Installation test failed: {e}")
        return False

def show_usage_examples():
    """Show usage examples"""
    print("\n" + "="*60)
    print("🚀 UPID CLI - Universal Kubernetes Optimizer")
    print("="*60)
    print("\n✅ Installation complete! You can now use:")
    print("\n📊 Basic Commands:")
    print("  upid universal status          # Show cluster health")
    print("  upid universal analyze         # Analyze resources")
    print("  upid universal optimize        # Get optimizations")
    print("  upid universal report          # Generate reports")
    print("\n🔧 Advanced Commands:")
    print("  upid universal status --format json    # JSON output")
    print("  upid universal analyze --namespace kube-system")
    print("  upid universal optimize --dry-run      # Preview only")
    print("  upid universal report --output report.html")
    print("\n🌍 Works with ANY cluster:")
    print("  • Docker Desktop")
    print("  • Minikube")
    print("  • Kind")
    print("  • K3s")
    print("  • EKS (AWS)")
    print("  • AKS (Azure)")
    print("  • GKE (Google)")
    print("  • Any other Kubernetes cluster")
    print("\n💡 Zero configuration required!")
    print("   Just run the commands and get insights instantly.")
    print("\n" + "="*60)

def main():
    """Main installation process"""
    print("🚀 Installing UPID CLI - Universal Kubernetes Optimizer")
    print("="*60)
    
    # Check prerequisites
    print("\n📋 Checking prerequisites...")
    kubectl_ok = check_kubectl()
    cluster_ok = check_cluster_connection()
    
    if not kubectl_ok:
        print("\n❌ kubectl is required but not found.")
        print("Please install kubectl first:")
        print("  https://kubernetes.io/docs/tasks/tools/install-kubectl/")
        return False
    
    if not cluster_ok:
        print("\n⚠️  No Kubernetes cluster detected.")
        print("You can still install the CLI, but you'll need a cluster to use it.")
        print("Consider starting a local cluster:")
        print("  • Docker Desktop: Enable Kubernetes")
        print("  • Minikube: minikube start")
        print("  • Kind: kind create cluster")
        print("  • K3s: k3s server")
    
    # Install requirements
    print("\n📦 Installing dependencies...")
    if not install_requirements():
        return False
    
    # Setup CLI
    print("\n🔧 Setting up CLI...")
    if not setup_cli():
        return False
    
    # Test installation
    print("\n🧪 Testing installation...")
    if not test_installation():
        print("⚠️  Installation completed with warnings")
    else:
        print("✅ Installation completed successfully!")
    
    # Show usage
    show_usage_examples()
    
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1) 