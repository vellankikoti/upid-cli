# 🚀 UPID CLI - Universal Kubernetes Optimizer

**Works with ANY Kubernetes cluster - Zero configuration required!**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Universal-orange.svg)](https://kubernetes.io)

## ✨ Features

- **🌍 Universal Compatibility** - Works with Docker Desktop, Minikube, Kind, K3s, EKS, AKS, GKE, and any other Kubernetes cluster
- **🔧 Zero Configuration** - Just install and run, no setup required
- **🤖 Auto-Detection** - Automatically detects cluster type and capabilities
- **📊 Real-Time Insights** - Get instant resource analysis and optimization recommendations
- **💡 Smart Recommendations** - AI-powered suggestions for cost and performance optimization
- **🎨 Beautiful UI** - Rich terminal interface with tables, progress bars, and colors
- **📈 Multiple Output Formats** - JSON, YAML, HTML reports

## 🚀 Quick Start

### 1. Install

```bash
# Clone the repository
git clone https://github.com/your-org/upid-cli.git
cd upid-cli

# Install dependencies
pip install -r requirements.txt

# Run the universal installer
python install_universal.py
```

### 2. Use (Zero Configuration!)

```bash
# Show cluster health
upid universal status

# Analyze resources
upid universal analyze

# Get optimization recommendations
upid universal optimize

# Generate comprehensive report
upid universal report
```

## 🌍 Supported Clusters

| Cluster Type | Status | Features |
|-------------|--------|----------|
| **Docker Desktop** | ✅ Full Support | Local development, resource analysis |
| **Minikube** | ✅ Full Support | Local testing, optimization |
| **Kind** | ✅ Full Support | Multi-node testing |
| **K3s** | ✅ Full Support | Lightweight production |
| **EKS (AWS)** | ✅ Full Support | Cloud optimization, cost analysis |
| **AKS (Azure)** | ✅ Full Support | Cloud optimization, cost analysis |
| **GKE (Google)** | ✅ Full Support | Cloud optimization, cost analysis |
| **Any Kubernetes** | ✅ Full Support | Universal compatibility |

## 📊 Commands

### Basic Commands

```bash
# Show cluster status and health
upid universal status

# Analyze cluster resources and performance
upid universal analyze

# Get optimization recommendations
upid universal optimize

# Generate comprehensive reports
upid universal report
```

### Advanced Commands

```bash
# JSON output format
upid universal status --format json

# Analyze specific namespace
upid universal analyze --namespace kube-system

# Preview optimizations without applying
upid universal optimize --dry-run

# Generate HTML report
upid universal report --output cluster-report.html
```

## 🎯 Use Cases

### 🏠 Local Development
```bash
# Docker Desktop
upid universal status
# Shows: CPU usage, memory usage, pod health

# Minikube
upid universal analyze
# Shows: Resource optimization opportunities
```

### ☁️ Cloud Clusters
```bash
# EKS/AKS/GKE
upid universal optimize
# Shows: Cost optimization, right-sizing recommendations

upid universal report --output cost-analysis.html
# Generates: Comprehensive cost and performance report
```

### 🔧 Production Monitoring
```bash
# Any Kubernetes cluster
upid universal status --format json
# Returns: Machine-readable cluster health data

upid universal analyze --namespace production
# Analyzes: Production workload optimization
```

## 📈 Sample Output

### Cluster Status
```
📊 Cluster Information
╭──────────────────────────────────────────── Cluster Details ─────────────────────────────────────────────╮
│ Name: docker-desktop                                                                                     │
│ Type: DOCKER-DESKTOP                                                                                     │
│ Status: ✅ Connected                                                                                     │
│ Kubeconfig: ~/.kube/config                                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────╯

                Resource Usage                 
┏━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━┓
┃ Resource ┃ Used      ┃ Total      ┃ Usage % ┃
┡━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━┩
│ CPU      │ 1.9 cores │ 30.0 cores │ 6.3%    │
│ Memory   │ 1.4 GB    │ 23.0 GB    │ 6.0%    │
│ Pods     │ 22        │ 24         │ 91.7%   │
└──────────┴───────────┴────────────┴─────────┘
```

### Optimization Recommendations
```
⚡ Optimization Recommendations
                Optimization Opportunities                 
┏━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━┓
┃ Type     ┃ Action                     ┃ Impact ┃ Effort ┃
┡━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━┩
│ Resource │ Right-size CPU requests    │ Medium │ Low    │
│ Resource │ Right-size memory requests │ Medium │ Low    │
│ Cost     │ Use spot instances         │ High   │ Medium │
└──────────┴────────────────────────────┴────────┴────────┘
```

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- kubectl (for cluster access)
- Any Kubernetes cluster

### Quick Install
```bash
# One-liner installation
curl -sSL https://raw.githubusercontent.com/your-org/upid-cli/main/install.sh | bash
```

### Manual Install
```bash
# Clone repository
git clone https://github.com/your-org/upid-cli.git
cd upid-cli

# Install Python dependencies
pip install -r requirements.txt

# Run universal installer
python install_universal.py

# Test installation
python demo_universal.py
```

## 🔧 Configuration

### Zero Configuration (Default)
The CLI works out of the box with any Kubernetes cluster using your existing `kubeconfig`.

### Optional Configuration
Create `~/.upid/config.yaml` for custom settings:

```yaml
# Universal mode - works with any cluster
universal_mode: true

# Auto-detect cluster type
auto_detect: true

# Default settings
timeout: 30
log_level: INFO

# Profiles for different environments
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
```

## 🧪 Testing

### Demo Mode
```bash
# Run interactive demo
python demo_universal.py
```

### Test with Different Clusters
```bash
# Docker Desktop
upid universal status

# Minikube
minikube start
upid universal analyze

# Kind
kind create cluster
upid universal optimize

# EKS (with AWS credentials)
upid universal report
```

## 📚 Examples

### Local Development Workflow
```bash
# 1. Start local cluster
docker-desktop  # or minikube start

# 2. Deploy your app
kubectl apply -f your-app.yaml

# 3. Analyze resources
upid universal analyze

# 4. Get optimizations
upid universal optimize

# 5. Generate report
upid universal report --output dev-report.html
```

### Production Monitoring
```bash
# 1. Connect to production cluster
kubectl config use-context production

# 2. Monitor cluster health
upid universal status --format json | jq

# 3. Analyze performance
upid universal analyze --namespace production

# 4. Get cost optimizations
upid universal optimize --dry-run
```

### CI/CD Integration
```bash
# In your CI pipeline
upid universal status --format json > cluster-health.json
upid universal analyze --format json > resource-analysis.json
upid universal report --output ci-report.html
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: [docs.upid.io](https://docs.upid.io)
- **Issues**: [GitHub Issues](https://github.com/your-org/upid-cli/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-org/upid-cli/discussions)

## 🎉 What's Next?

- **Multi-cluster management**
- **Advanced cost analytics**
- **Performance benchmarking**
- **Integration with monitoring tools**
- **Web dashboard**

---

**Made with ❤️ for the Kubernetes community** 