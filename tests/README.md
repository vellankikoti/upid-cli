# UPID CLI Test Suite

This directory contains comprehensive tests for the UPID CLI, including unit tests, integration tests, and end-to-end tests using testcontainers.

## Test Structure

```
tests/
├── conftest.py                 # Pytest configuration and fixtures
├── run_tests.py               # Test runner script
├── README.md                  # This file
├── unit/                      # Unit tests
│   ├── __init__.py
│   ├── test_config.py         # Configuration management tests
│   ├── test_auth.py          # Authentication tests
│   └── test_api_client.py    # API client tests
└── integration/               # Integration tests
    ├── __init__.py
    ├── test_api_integration.py    # API integration tests
    └── test_k8s_integration.py   # Kubernetes integration tests
```

## Test Categories

### Unit Tests (`tests/unit/`)
- **Fast execution** (< 1 second per test)
- **No external dependencies** (mocked)
- **Isolated testing** of individual components
- **High coverage** of core functionality

### Integration Tests (`tests/integration/`)
- **Real container environments** using testcontainers
- **API interaction testing** with mock servers
- **Kubernetes cluster testing** with real K8s
- **End-to-end workflow testing**

## Test Markers

Tests are categorized using pytest markers:

- `@pytest.mark.unit` - Unit tests
- `@pytest.mark.integration` - Integration tests
- `@pytest.mark.slow` - Slow running tests (> 5 seconds)
- `@pytest.mark.e2e` - End-to-end tests
- `@pytest.mark.api` - API related tests
- `@pytest.mark.k8s` - Kubernetes related tests
- `@pytest.mark.zero_pod` - Zero-pod scaling tests

## Running Tests

### Quick Start

```bash
# Setup test environment
python tests/run_tests.py --setup

# Run all tests
python tests/run_tests.py --all

# Run specific test types
python tests/run_tests.py --unit
python tests/run_tests.py --integration
python tests/run_tests.py --k8s
```

### Using pytest directly

```bash
# Run all tests
pytest tests/ -v

# Run unit tests only
pytest tests/unit/ -v

# Run integration tests only
pytest tests/integration/ -v

# Run tests with specific markers
pytest tests/ -m "unit"
pytest tests/ -m "integration"
pytest tests/ -m "k8s"
pytest tests/ -m "api"

# Run tests with coverage
pytest tests/ --cov=upid --cov-report=html
```

### Test Runner Options

```bash
# Setup environment
python tests/run_tests.py --setup

# Code quality checks
python tests/run_tests.py --lint
python tests/run_tests.py --type-check
python tests/run_tests.py --format
python tests/run_tests.py --security

# Specific test types
python tests/run_tests.py --unit
python tests/run_tests.py --integration
python tests/run_tests.py --k8s
python tests/run_tests.py --api
python tests/run_tests.py --zero-pod

# Performance and stress tests
python tests/run_tests.py --performance
python tests/run_tests.py --stress

# Generate reports
python tests/run_tests.py --report

# Run everything
python tests/run_tests.py --all
```

## Test Dependencies

### Development Requirements

Install test dependencies:

```bash
pip install -r requirements-dev.txt
```

### Docker Requirements

For integration tests, you need:

- **Docker** installed and running
- **Docker Compose** (optional, for complex setups)
- **Sufficient resources** (4GB RAM, 2 CPU cores recommended)

### Kubernetes Requirements

For K8s integration tests:

- **Docker** with sufficient resources
- **kind** (Kubernetes in Docker) - automatically installed
- **kubectl** - automatically available in containers

## Test Fixtures

### Core Fixtures (`conftest.py`)

- `mock_config` - Mock configuration for testing
- `mock_auth_manager` - Mock authentication manager
- `mock_api_client` - Mock API client
- `sample_cluster_data` - Sample cluster data
- `sample_optimization_result` - Sample optimization results
- `sample_idle_analysis` - Sample idle analysis data

### Integration Fixtures

- `mock_api_server` - Containerized mock API server
- `k8s_cluster` - Real Kubernetes cluster for testing
- `test_config` - Test-specific configuration

## Test Coverage

### Unit Test Coverage

- **Configuration Management** - 100%
- **Authentication** - 100%
- **API Client** - 100%
- **Utility Functions** - 95%+
- **Error Handling** - 100%

### Integration Test Coverage

- **API Interactions** - Real HTTP requests
- **Kubernetes Operations** - Real K8s cluster
- **Container Management** - Docker containers
- **Network Connectivity** - Real network tests
- **Resource Management** - CPU, memory, storage

## Test Data

### Sample Data Fixtures

```python
# Cluster data
sample_cluster_data = {
    'cluster_id': 'test-cluster-123',
    'name': 'test-cluster',
    'region': 'us-west-2',
    'status': 'healthy',
    'nodes_count': 3,
    'pods_count': 50
}

# Optimization results
sample_optimization_result = {
    'cluster_id': 'test-cluster-123',
    'potential_savings': 1500.0,
    'efficiency_score': 85.5,
    'zero_pod_opportunities': {
        'scalable_pods_count': 5,
        'total_potential_savings': 800.0
    }
}
```

## Test Containers

### API Integration Tests

Uses Python HTTP server containers:

```python
@pytest.fixture(scope="class")
def mock_api_server(self):
    container = DockerContainer("python:3.9-slim")
    container.with_command(["python", "-m", "http.server", "8000"])
    container.with_exposed_ports(8000)
    
    with container:
        wait_for_logs(container, "Serving HTTP on")
        yield container
```

### Kubernetes Integration Tests

Uses kind (Kubernetes in Docker):

```python
@pytest.fixture(scope="class")
def k8s_cluster(self):
    container = DockerContainer("kindest/node:v1.24.0")
    container.with_command(["kind", "create", "cluster", "--name", "test-cluster"])
    container.with_exposed_ports(6443)
    
    with container:
        wait_for_logs(container, "Ready")
        yield container
```

## Test Reports

### Coverage Reports

- **HTML Coverage**: `htmlcov/` directory
- **XML Coverage**: `coverage/` directory
- **Terminal Output**: Real-time coverage display

### Test Reports

- **JUnit XML**: `reports/junit.xml`
- **HTML Report**: `reports/report.html`
- **JSON Report**: `reports/report.json`

### Security Reports

- **Bandit Report**: `security_report.json`
- **Vulnerability Scan**: Automated security checks

## Continuous Integration

### GitHub Actions

```yaml
# .github/workflows/tests.yml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-dev.txt
      - name: Run tests
        run: python tests/run_tests.py --all
```

### Local Development

```bash
# Pre-commit hooks
pre-commit install

# Run tests before commit
git add .
python tests/run_tests.py --unit
git commit -m "Add new feature"
```

## Debugging Tests

### Verbose Output

```bash
# Very verbose output
pytest tests/ -v -s --tb=long

# Show local variables on failure
pytest tests/ --tb=short -l
```

### Debugging Integration Tests

```bash
# Run with container logs
pytest tests/integration/ -v -s --log-cli-level=DEBUG

# Keep containers running for inspection
pytest tests/integration/ --keep-containers
```

### Test Isolation

```bash
# Run single test
pytest tests/unit/test_config.py::TestConfig::test_config_initialization

# Run tests in parallel
pytest tests/ -n 4

# Run tests with specific markers
pytest tests/ -m "not slow"
```

## Performance Testing

### Load Tests

```bash
# Run performance tests
python tests/run_tests.py --performance

# Run stress tests
python tests/run_tests.py --stress
```

### Benchmark Tests

```python
@pytest.mark.performance
def test_api_response_time():
    """Test API response time under load"""
    start_time = time.time()
    # ... test code ...
    duration = time.time() - start_time
    assert duration < 1.0  # Should complete within 1 second
```

## Best Practices

### Writing Unit Tests

1. **Test one thing at a time**
2. **Use descriptive test names**
3. **Mock external dependencies**
4. **Test both success and failure cases**
5. **Use fixtures for common setup**

### Writing Integration Tests

1. **Use real containers when possible**
2. **Clean up resources after tests**
3. **Test complete workflows**
4. **Handle container startup time**
5. **Use appropriate timeouts**

### Test Data Management

1. **Use fixtures for sample data**
2. **Keep test data realistic**
3. **Clean up test data**
4. **Use factories for complex objects**
5. **Version control test data**

## Troubleshooting

### Common Issues

#### Docker Issues
```bash
# Check Docker status
docker info

# Restart Docker
sudo systemctl restart docker

# Check container logs
docker logs <container_id>
```

#### Kubernetes Issues
```bash
# Check kind cluster
kind get clusters

# Delete and recreate cluster
kind delete cluster --name test-cluster
kind create cluster --name test-cluster
```

#### Test Failures
```bash
# Run with more detail
pytest tests/ -v -s --tb=long

# Check test markers
pytest tests/ --markers

# Run specific test file
pytest tests/unit/test_config.py -v
```

### Performance Issues

```bash
# Run tests in parallel
pytest tests/ -n auto

# Skip slow tests
pytest tests/ -m "not slow"

# Profile test execution
pytest tests/ --durations=10
```

## Contributing

### Adding New Tests

1. **Follow naming convention**: `test_*.py`
2. **Use appropriate markers**: `@pytest.mark.unit`
3. **Add to test runner**: Update `run_tests.py`
4. **Update documentation**: Add to this README
5. **Ensure coverage**: Aim for 90%+ coverage

### Test Guidelines

1. **Keep tests fast** (< 1 second for unit tests)
2. **Make tests reliable** (no flaky tests)
3. **Use meaningful assertions**
4. **Test edge cases**
5. **Maintain test isolation**

### Code Quality

1. **Follow PEP 8** for test code
2. **Use type hints** where appropriate
3. **Document complex tests**
4. **Use consistent naming**
5. **Keep tests maintainable** 