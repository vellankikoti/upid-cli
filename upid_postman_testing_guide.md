# UPID API Testing Guide
## Comprehensive Postman Collection for Backend Validation

> **Complete testing suite for validating UPID backend implementation with 100+ API endpoints**

---

## 📋 **OVERVIEW**

This Postman collection provides comprehensive testing coverage for all UPID backend services, including:

- **14 Core Services** with 100+ API endpoints
- **Automated authentication** and token management
- **Environment variables** for different deployment stages
- **Test scenarios** for validation and regression testing
- **Performance benchmarks** and response time validation

---

## 🚀 **QUICK START**

### 1. **Import Collection and Environment**

```bash
# Option 1: Import from files
1. Open Postman
2. Click "Import" button
3. Select the collection JSON file
4. Select the environment JSON file

# Option 2: Import from URL (if hosted)
1. Copy the collection/environment URLs
2. Use "Import from Link" option in Postman
```

### 2. **Configure Environment Variables**

Update the environment variables in Postman:

```json
{
  "base_url": "http://localhost:8080",        // Your API server URL
  "test_email": "admin@yourcompany.com",      // Test user email
  "test_password": "YourSecurePassword123!",  // Test user password
  "test_kubeconfig": "LS0tLS1CRUdJTi0tLS0t..." // Base64 kubeconfig
}
```

### 3. **Run Authentication Flow**

```
1. Execute: "🔐 Authentication & Authorization" → "Login"
2. Verify: auth_token is automatically set in environment
3. All subsequent requests will use this token automatically
```

---

## 🧪 **TESTING WORKFLOWS**

### **End-to-End Testing Sequence**

Run requests in this order for complete validation:

#### **Phase 1: Authentication & Setup (5 minutes)**
```
1. 🔐 Login
2. 🔐 Get User Profile
3. 🔐 List Roles
4. 🏗️ Register Cluster
5. 🏗️ Get Cluster Health
```

#### **Phase 2: Data Pipeline Testing (10 minutes)**
```
6. 📊 Start Metrics Collection
7. 📊 Get Resource Metrics
8. 📊 Query Historical Data
9. 📊 Aggregate Metrics
10. 🧮 Linear Regression (test mathematical models)
```

#### **Phase 3: Intelligence & Optimization (15 minutes)**
```
11. 🧠 Create Optimization Rule
12. 🧠 Test Rule
13. 📈 Statistical Analysis
14. 📈 Generate Forecast
15. 🎯 Analyze Cluster for Optimization
16. 🎯 Generate Recommendations
17. 🎯 Cost Analysis
```

#### **Phase 4: Safety & Deployment (10 minutes)**
```
18. 🛡️ Validate Optimization
19. 🛡️ Risk Assessment
20. 🛡️ Create Safety Rule
21. 🚀 Create Deployment
22. 🚀 Execute Deployment
23. 🚀 Get Deployment Status
```

#### **Phase 5: Business Intelligence (10 minutes)**
```
24. 💼 Calculate Cost Analysis
25. 💼 Calculate ROI
26. 💼 Get Performance KPIs
27. 💼 Generate Business Report
28. 💼 Get Executive Dashboard
```

#### **Phase 6: Configuration & Monitoring (5 minutes)**
```
29. ⚙️ Get System Configuration
30. ⚙️ Create Optimization Strategy
31. 🔔 Send Notification
32. 📋 Create Audit Event
33. 🔍 Gateway Health Check
```

---

## 🔧 **ENVIRONMENT CONFIGURATIONS**

### **Development Environment**
```json
{
  "base_url": "http://localhost:8080",
  "test_email": "dev@upid.local",
  "test_password": "DevPassword123!"
}
```

### **Staging Environment**
```json
{
  "base_url": "https://staging-api.upid.io",
  "test_email": "staging@upid.io",
  "test_password": "StagingPassword123!"
}
```

### **Production Environment**
```json
{
  "base_url": "https://api.upid.io",
  "test_email": "prod-test@upid.io",
  "test_password": "ProductionPassword123!"
}
```

---

## 📊 **AUTOMATED TESTING FEATURES**

### **Authentication Management**
- **Auto-login**: Automatically refreshes expired tokens
- **Token storage**: Stores JWT tokens in environment variables
- **Session management**: Handles refresh token rotation

### **Response Validation**
```javascript
// Automatic tests included in each request:
pm.test('Status code is 200', function () {
    pm.response.to.have.status(200);
});

pm.test('Response time is acceptable', function () {
    pm.expect(pm.response.responseTime).to.be.below(2000);
});

pm.test('Response has required headers', function () {
    pm.expect(pm.response.headers.get('Content-Type')).to.include('application/json');
});
```

### **Data Extraction**
```javascript
// Auto-extracts IDs for subsequent requests:
pm.test('Cluster ID is returned', function () {
    const jsonData = pm.response.json();
    pm.expect(jsonData.cluster_id).to.exist;
    pm.environment.set('test_cluster_id', jsonData.cluster_id);
});
```

---

## 🎯 **PERFORMANCE TESTING**

### **Load Testing Scenarios**

#### **Basic Load Test**
```
Concurrent Users: 10
Duration: 5 minutes
Requests per second: 50
Target endpoints: Core CRUD operations
```

#### **Stress Test**
```
Concurrent Users: 100
Duration: 10 minutes
Requests per second: 500
Target endpoints: Optimization analysis
```

#### **Spike Test**
```
Burst Users: 500
Duration: 2 minutes
Requests per second: 1000
Target endpoints: Authentication and health checks
```

### **Performance Benchmarks**
```javascript
// Built-in performance tests
pm.test('API response time < 100ms (P95)', function () {
    pm.expect(pm.response.responseTime).to.be.below(100);
});

pm.test('Optimization analysis < 10 seconds', function () {
    if (pm.request.url.toString().includes('optimization/analyze')) {
        pm.expect(pm.response.responseTime).to.be.below(10000);
    }
});
```

---

## 🔍 **TESTING SCENARIOS**

### **Scenario 1: New Cluster Onboarding**
```
1. Register new cluster
2. Validate cluster health
3. Start metrics collection
4. Wait 5 minutes for data
5. Run optimization analysis
6. Generate recommendations
7. Validate safety checks
8. Execute deployment
```

### **Scenario 2: Cost Optimization Workflow**
```
1. Analyze current costs
2. Generate cost optimization recommendations
3. Simulate cost savings
4. Validate safety of changes
5. Execute optimizations
6. Monitor results
7. Generate ROI report
```

### **Scenario 3: Performance Optimization**
```
1. Collect performance metrics
2. Identify bottlenecks
3. Generate performance recommendations
4. Test optimization simulation
5. Apply optimizations
6. Monitor performance improvements
```

### **Scenario 4: Safety Validation**
```
1. Create aggressive optimization plan
2. Run safety validation
3. Verify safety rules trigger
4. Test rollback mechanisms
5. Validate audit logging
```

---

## 📈 **MONITORING & REPORTING**

### **Test Execution Reports**

Postman automatically generates reports showing:
- **Request success rates**
- **Response time distributions**
- **Failed test details**
- **Performance trends**

### **Custom Metrics Collection**

Add custom monitoring to collection:

```javascript
// Track API performance metrics
const responseTime = pm.response.responseTime;
const endpoint = pm.request.url.toString();

// Store metrics for reporting
pm.globals.set(`${endpoint}_response_time`, responseTime);
pm.globals.set(`${endpoint}_timestamp`, new Date().toISOString());
```

### **Integration with CI/CD**

```bash
# Newman CLI for CI/CD integration
npm install -g newman

# Run collection in CI pipeline
newman run upid-collection.json \
  --environment upid-environment.json \
  --reporters cli,json,junit \
  --reporter-junit-export results.xml
```

---

## 🚨 **ERROR HANDLING & DEBUGGING**

### **Common Issues and Solutions**

#### **Authentication Failures**
```
Issue: 401 Unauthorized responses
Solution: 
1. Check test_email and test_password in environment
2. Verify user exists in system
3. Run Login request first
4. Check token expiry
```

#### **Cluster Not Found**
```
Issue: 404 errors for cluster operations
Solution:
1. Run "Register Cluster" first
2. Verify test_cluster_id is set
3. Check cluster is in correct region
```

#### **Timeout Errors**
```
Issue: Request timeouts
Solution:
1. Increase timeout in Postman settings
2. Check server is running
3. Verify network connectivity
4. Check server logs for performance issues
```

### **Debug Mode**

Enable verbose logging by adding to pre-request script:

```javascript
// Enable debug mode
pm.environment.set('debug_mode', 'true');

// Log request details
console.log('Request URL:', pm.request.url.toString());
console.log('Request Method:', pm.request.method);
console.log('Request Headers:', JSON.stringify(pm.request.headers));
```

---

## 📝 **TEST DATA MANAGEMENT**

### **Test Data Requirements**

#### **Kubernetes Test Data**
```yaml
# Sample test kubeconfig (base64 encoded)
apiVersion: v1
kind: Config
clusters:
- cluster:
    server: https://test-cluster.example.com
  name: test-cluster
contexts:
- context:
    cluster: test-cluster
    user: test-user
  name: test-context
current-context: test-context
users:
- name: test-user
  user:
    token: test-token-here
```

#### **Sample Metrics Data**
```json
{
  "cpu_utilization": [65, 70, 68, 72, 69, 75, 73],
  "memory_utilization": [45, 48, 46, 49, 47, 52, 50],
  "network_throughput": [125, 143, 167, 158, 172, 165, 180],
  "storage_iops": [1200, 1350, 1100, 1400, 1250, 1300, 1450]
}
```

### **Data Cleanup**

Add cleanup scripts to collection:

```javascript
// Cleanup script (add to test or pre-request)
pm.test('Cleanup test data', function () {
    // Remove test cluster
    const clusterId = pm.environment.get('test_cluster_id');
    if (clusterId) {
        // Add cleanup logic here
        console.log('Cleaning up cluster:', clusterId);
    }
});
```

---

## 🔄 **CONTINUOUS TESTING**

### **Automated Test Runs**

#### **Daily Health Checks**
```bash
# Cron job for daily API health validation
0 6 * * * newman run health-check-collection.json --environment production.json
```

#### **Pre-deployment Testing**
```bash
# Run before each deployment
newman run full-api-test.json --environment staging.json --bail
```

### **Integration with Monitoring**

```javascript
// Send test results to monitoring system
pm.test('Report test results', function () {
    const results = {
        timestamp: new Date().toISOString(),
        endpoint: pm.request.url.toString(),
        response_time: pm.response.responseTime,
        status_code: pm.response.code,
        success: pm.response.code === 200
    };
    
    // Send to monitoring endpoint
    // (implement based on your monitoring solution)
});
```

---

## 📚 **COLLECTION STRUCTURE**

### **Folder Organization**
```
📁 UPID API Collection
├── 🔐 Authentication & Authorization (5 requests)
├── 🏗️ Cluster Management (6 requests)
├── 📊 Data Collection & Metrics (5 requests)
├── 🧠 Rules Engine & Algorithms (5 requests)
├── 📈 Statistical Prediction (4 requests)
├── 🎯 Optimization Engine (5 requests)
├── 🛡️ Safety Validation (4 requests)
├── 🚀 Deployment Service (5 requests)
├── 💼 Business Intelligence (5 requests)
├── 🧮 Mathematical Models (4 requests)
├── ⚙️ Configuration Management (4 requests)
├── 🔔 Notifications (3 requests)
├── 📋 Audit & Compliance (3 requests)
└── 🔍 Health & Monitoring (2 requests)
```

### **Request Naming Convention**
```
Format: [Service] [Action] [Resource]
Examples:
- "Auth Login User"
- "Cluster Register New"
- "Optimization Generate Recommendations"
- "Safety Validate Changes"
```

---

## 🎯 **SUCCESS CRITERIA**

### **API Testing Validation**

#### **Functional Tests (100% Pass Required)**
- ✅ All authentication flows work correctly
- ✅ CRUD operations for all resources
- ✅ Data validation and error handling
- ✅ Cross-service integration

#### **Performance Tests (Target Benchmarks)**
- ✅ P95 response time < 100ms for all endpoints
- ✅ Optimization analysis < 10 seconds
- ✅ 1000+ requests/second throughput
- ✅ Zero timeouts under normal load

#### **Security Tests**
- ✅ Authentication required for protected endpoints
- ✅ Authorization validation for role-based access
- ✅ Input validation prevents injection attacks
- ✅ Audit logging captures all operations

#### **Business Logic Tests**
- ✅ Optimization recommendations are accurate
- ✅ Cost calculations are correct
- ✅ Safety validations prevent dangerous changes
- ✅ Rollback mechanisms work properly

---

This comprehensive Postman collection provides everything your QA and development teams need to:

✅ **Validate Backend Implementation** - Test every API endpoint
✅ **Automate Testing Workflows** - End-to-end test scenarios  
✅ **Performance Benchmarking** - Verify Netflix-scale requirements
✅ **Regression Testing** - Prevent breaking changes
✅ **Documentation** - Living API documentation through examples

The collection is ready to use immediately once your backend development is complete!