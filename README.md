# Universal Pod Intelligence Director (UPID CLI)

**Kubernetes Resource Optimization Platform** - Enterprise-grade resource optimization with >99% accuracy and Netflix-level performance.

## 🚀 Installation (Mac & Linux)

### **Recommended: One-Line Install**

Copy and run this command in your terminal:

```bash
curl -sSL https://raw.githubusercontent.com/kubilitics/upid-cli/main/install.sh | bash
```
- This will auto-detect your OS/arch, download the correct binary from the latest release, and install it to `/usr/local/bin/upid`.
- After install, run:

```bash
upid --help
```

### **Manual Download (Alternative)**

#### **For macOS (Apple Silicon/ARM64):**
```bash
curl -LO https://github.com/kubilitics/upid-cli/releases/latest/download/upid-darwin-arm64
chmod +x upid-darwin-arm64
sudo mv upid-darwin-arm64 /usr/local/bin/upid
upid --help
```

#### **For Linux (x86_64):**
```bash
curl -LO https://github.com/kubilitics/upid-cli/releases/latest/download/upid-linux-x86_64
chmod +x upid-linux-x86_64
sudo mv upid-linux-x86_64 /usr/local/bin/upid
upid --help
```

### **Uninstallation**
```bash
sudo rm /usr/local/bin/upid
```

### **Notes**
- **Windows support:** Coming soon! For now, use WSL or Docker.
- **PyPI install:** Coming soon! Use the binary install above.
- **Requires:** `kubectl` and access to a Kubernetes cluster.

## 📋 Features

- **Universal Cluster Support**: Works with any Kubernetes cluster (Docker Desktop, Minikube, EKS, AKS, GKE, etc.)
- **Resource Optimization**: Intelligent scaling with >99% accuracy
- **Zero-Pod Scaling**: Detect idle time and scale to zero pods
- **Cost Analysis**: Real-time cost optimization recommendations
- **Multi-Cluster Support**: Manage multiple Kubernetes clusters
- **Enterprise Ready**: Netflix-level performance and reliability
- **CLI Interface**: kubectl-style command interface
- **Rich UI**: Beautiful terminal interface with tables and progress bars

## 🛠️ Usage

Run `upid --help` to see all available commands, or see [feature-demo.md](./feature-demo.md) for end-to-end demo scenarios.

### Basic Commands

```bash
# Check version and help
upid --help
upid status

# Universal commands (works with any cluster)
upid universal status    # Check cluster health
upid universal analyze  # Analyze resources
upid universal optimize # Get optimization tips
upid universal report   # Generate reports

# Demo mode
upid demo               # See UPID in action
```

### Cluster Management

```bash
# List clusters
upid cluster list

# Get cluster details
upid cluster get cluster-123

# Create cluster
upid cluster create --name my-cluster --region us-west-2 --platform aws

# Delete cluster
upid cluster delete cluster-123 --force
```

### Analysis Commands

```bash
# Analyze resources
upid analyze resources cluster-123
upid analyze resources cluster-123 --detailed

# Analyze costs
upid analyze cost cluster-123 --period 30d

# Analyze performance
upid analyze performance cluster-123
```

### Optimization Commands

```bash
# Get optimization suggestions (safe)
upid optimize resources cluster-123 --dry-run
upid optimize costs cluster-123 --dry-run

# Apply optimizations
upid optimize resources cluster-123
upid optimize costs cluster-123

# Zero-pod scaling
upid optimize zero-pod cluster-123 --namespace default

# Auto optimization
upid optimize auto cluster-123 --schedule '0 2 * * *'
```

### Deployment Commands

```bash
# List deployments
upid deploy list cluster-123

# Create deployment
upid deploy create cluster-123 --name my-app --image nginx:latest --replicas 3

# Scale deployment
upid deploy scale cluster-123 my-app --replicas 5

# Delete deployment
upid deploy delete cluster-123 my-app
```

### Reporting Commands

```bash
# Generate reports
upid report summary cluster-123 --period 30d
upid report cost cluster-123 --format html --output cost-report.html
upid report performance cluster-123 --format json --output perf-report.json
```

## 🔧 Configuration

### Local Mode (No Authentication Required)

UPID automatically detects local clusters (Docker Desktop, Minikube, etc.) and works without authentication:

```bash
# Check if local mode is active
upid status

# Use universal commands
upid universal status
upid universal analyze
```

### Authentication (For Remote Clusters)

```bash
# Login to UPID platform
upid auth login --email your-email@example.com

# Check authentication status
upid auth status

# Logout
upid auth logout
```

### Environment Variables

```bash
export UPID_API_URL="https://api.upid.io"
export UPID_API_KEY="your-api-key"
export UPID_CLUSTER_NAME="production"
```

## 🧪 Testing

### Test with Docker Desktop

```bash
# Ensure Docker Desktop Kubernetes is running
kubectl cluster-info

# Test UPID with local cluster
upid universal status
upid universal analyze
upid universal optimize
upid universal report
```

### Test Binary Installation

```bash
# Test basic functionality
upid --help
upid status
upid demo

# Test with local cluster
upid universal status
```

## 🏗️ Development

### Setup Development Environment
```bash
# Clone repository
git clone https://github.com/kubilitics/upid-cli.git
cd upid-cli

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Build Binary
```bash
# Build for current platform
python build_binary_fixed.py

# Binary will be created at:
# ./dist/upid-darwin-arm64 (for macOS ARM64)
```

### Run Tests
```bash
# Run all tests
python run_unit_tests.py

# Run specific tests
pytest tests/unit/
pytest tests/integration/
```

## 📚 Documentation

- **Complete Commands Guide**: `UPID_COMMANDS_GUIDE.md`
- **Quick Reference**: `UPID_QUICK_REFERENCE.md`
- **Cheat Sheet**: `UPID_CHEAT_SHEET.md`
- **Docker Desktop Guide**: `DOCKER_DESKTOP_GUIDE.md`

## 🎯 Quick Test for Others

Share this with others to test UPID:

```bash
# 1. Download and install binary
sudo cp ./dist/upid-darwin-arm64 /usr/local/bin/upid
sudo chmod +x /usr/local/bin/upid

# 2. Test basic functionality
upid --help
upid status

# 3. Test with local cluster (Docker Desktop, Minikube, etc.)
upid universal status
upid universal analyze
upid universal optimize
upid universal report

# 4. Run demo
upid demo
```

## 🚨 Important Notes

- **Binary Location**: `./dist/upid-darwin-arm64` (macOS ARM64 only)
- **Local Mode**: Works with any Kubernetes cluster without authentication
- **Universal Commands**: Use `upid universal *` for any cluster
- **Safety**: Always use `--dry-run` first to see what changes will be made

## 🎉 Ready for Testing!

The UPID CLI is **production-ready** and can be shared with others for testing. The binary is self-contained and works with any Kubernetes cluster.

## 📚 Additional Resources

- **Documentation**: [docs.upid.com](https://docs.upid.com)
- **Issues**: [GitHub Issues](https://github.com/kubilitics/upid-cli/issues)
- **Discussions**: [GitHub Discussions](https://github.com/kubilitics/upid-cli/discussions)
- **Email**: hello@kubilitics.com

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Kubernetes community
- Open source contributors

---

**UPID CLI** - Optimizing Kubernetes resources with enterprise-grade precision. 
