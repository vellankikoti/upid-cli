"""
API client for UPID backend services
"""
import requests
import json
import time
from typing import Dict, Any, Optional, List
from requests.exceptions import RequestException, Timeout
import logging

logger = logging.getLogger(__name__)

class APIClient:
    """API client for UPID backend services"""
    
    def __init__(self, base_url: str, auth_token: Optional[str] = None, timeout: int = 30):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        
        # Set default headers
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'UPID-CLI/1.0.0'
        })
        
        if auth_token:
            self.session.headers['Authorization'] = f'Bearer {auth_token}'
    
    def set_auth_token(self, token: str):
        """Set authentication token"""
        self.session.headers['Authorization'] = f'Bearer {token}'
    
    def clear_auth_token(self):
        """Clear authentication token"""
        if 'Authorization' in self.session.headers:
            del self.session.headers['Authorization']
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make HTTP request with error handling"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                timeout=self.timeout,
                **kwargs
            )
            response.raise_for_status()
            return response.json()
        except Timeout:
            raise Exception(f"Request timeout after {self.timeout} seconds")
        except RequestException as e:
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_data = e.response.json()
                    error_message = error_data.get('message', str(e))
                except (ValueError, KeyError):
                    error_message = str(e)
                raise Exception(f"API request failed: {error_message}")
            else:
                raise Exception(f"API request failed: {e}")
    
    def get(self, endpoint: str, params: Dict = None) -> Dict[str, Any]:
        """Make GET request"""
        return self._make_request('GET', endpoint, params=params)
    
    def post(self, endpoint: str, data: Dict = None) -> Dict[str, Any]:
        """Make POST request"""
        return self._make_request('POST', endpoint, json=data)
    
    def put(self, endpoint: str, data: Dict = None) -> Dict[str, Any]:
        """Make PUT request"""
        return self._make_request('PUT', endpoint, json=data)
    
    def delete(self, endpoint: str) -> Dict[str, Any]:
        """Make DELETE request"""
        return self._make_request('DELETE', endpoint)
    
    def patch(self, endpoint: str, data: Dict = None) -> Dict[str, Any]:
        """Make PATCH request"""
        return self._make_request('PATCH', endpoint, json=data)
    
    def health_check(self) -> Dict[str, Any]:
        """Check API health"""
        return self.get('/api/v1/gateway/health')
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get API metrics"""
        return self.get('/api/v1/gateway/metrics')

class UPIDAPIClient(APIClient):
    """UPID-specific API client with service methods"""
    
    def __init__(self, config):
        super().__init__(
            base_url=config.get_api_url(),
            timeout=config.get_timeout()
        )
        self.config = config
        
        # Set auth token if available
        auth_token = config.get_auth_token()
        if auth_token:
            self.set_auth_token(auth_token)
    
    # Authentication methods
    def login(self, email: str, password: str) -> Dict[str, Any]:
        """Login to UPID platform"""
        data = {
            'email': email,
            'password': password
        }
        return self.post('/api/v1/auth/login', data=data)
    
    def logout(self) -> Dict[str, Any]:
        """Logout from UPID platform"""
        return self.post('/api/v1/auth/logout')
    
    def get_profile(self) -> Dict[str, Any]:
        """Get user profile"""
        return self.get('/api/v1/auth/profile')
    
    def refresh_token(self) -> Dict[str, Any]:
        """Refresh authentication token"""
        return self.post('/api/v1/auth/refresh')
    
    # Cluster management methods
    def register_cluster(self, name: str, kubeconfig: str, region: str = None, 
                        description: str = None) -> Dict[str, Any]:
        """Register a new Kubernetes cluster"""
        data = {
            'name': name,
            'kubeconfig': kubeconfig,
            'region': region,
            'description': description
        }
        return self.post('/api/v1/clusters', data=data)
    
    def list_clusters(self) -> List[Dict[str, Any]]:
        """List all registered clusters"""
        response = self.get('/api/v1/clusters')
        return response.get('clusters', [])
    
    def get_cluster(self, cluster_id: str) -> Dict[str, Any]:
        """Get cluster details"""
        return self.get(f'/api/v1/clusters/{cluster_id}')
    
    def get_cluster_health(self, cluster_id: str) -> Dict[str, Any]:
        """Get cluster health status"""
        return self.get(f'/api/v1/clusters/{cluster_id}/health')
    
    def delete_cluster(self, cluster_id: str) -> Dict[str, Any]:
        """Delete cluster registration"""
        return self.delete(f'/api/v1/clusters/{cluster_id}')
    
    # Metrics collection methods
    def get_resource_metrics(self, cluster_id: str, time_range: str = '24h') -> Dict[str, Any]:
        """Get resource metrics for cluster"""
        params = {'time_range': time_range}
        return self.get(f'/api/v1/metrics/resources/{cluster_id}', params=params)
    
    def get_pod_metrics(self, cluster_id: str, namespace: str = None) -> Dict[str, Any]:
        """Get detailed pod metrics"""
        params = {}
        if namespace:
            params['namespace'] = namespace
        return self.get(f'/api/v1/metrics/pods/{cluster_id}/detailed', params=params)
    
    def get_historical_metrics(self, cluster_id: str, time_range: str = '30d') -> Dict[str, Any]:
        """Get historical metrics"""
        params = {'time_range': time_range}
        return self.get(f'/api/v1/metrics/history/{cluster_id}', params=params)
    
    # Optimization methods
    def analyze_cluster_optimization(self, cluster_id: str, strategy: str = None) -> Dict[str, Any]:
        """Analyze cluster for optimization opportunities"""
        data = {'cluster_id': cluster_id}
        if strategy:
            data['strategy'] = strategy
        return self.post('/api/v1/optimization/analyze', data=data)
    
    def generate_recommendations(self, cluster_id: str, analysis_id: str) -> Dict[str, Any]:
        """Generate optimization recommendations"""
        data = {
            'cluster_id': cluster_id,
            'analysis_id': analysis_id
        }
        return self.post('/api/v1/optimization/recommendations/generate', data=data)
    
    def apply_optimizations(self, cluster_id: str, recommendations: List[Dict]) -> Dict[str, Any]:
        """Apply optimization recommendations"""
        data = {
            'cluster_id': cluster_id,
            'recommendations': recommendations
        }
        return self.post('/api/v1/optimization/apply', data=data)
    
    def get_optimization_status(self, cluster_id: str) -> Dict[str, Any]:
        """Get optimization status"""
        return self.get(f'/api/v1/optimization/status/{cluster_id}')
    
    # Zero-pod scaling methods
    def analyze_idle_time(self, cluster_id: str, namespace: str = None) -> Dict[str, Any]:
        """Analyze pod idle time for zero-pod scaling"""
        params = {}
        if namespace:
            params['namespace'] = namespace
        return self.get(f'/api/v1/optimization/idle-analysis/{cluster_id}', params=params)
    
    def deploy_zero_pod_scaling(self, cluster_id: str, namespace: str = None) -> Dict[str, Any]:
        """Deploy zero-pod scaling configurations"""
        data = {'cluster_id': cluster_id}
        if namespace:
            data['namespace'] = namespace
        return self.post('/api/v1/optimization/zero-pod-deploy', data=data)
    
    # Cost analysis methods
    def analyze_costs(self, cluster_id: str, period: str = '30d') -> Dict[str, Any]:
        """Analyze cluster costs"""
        params = {'period': period}
        return self.get(f'/api/v1/business/cost/analysis/{cluster_id}', params=params)
    
    def calculate_cost_savings(self, cluster_id: str, optimizations: List[Dict]) -> Dict[str, Any]:
        """Calculate cost savings from optimizations"""
        data = {
            'cluster_id': cluster_id,
            'optimizations': optimizations
        }
        return self.post('/api/v1/business/cost/calculate-savings', data=data)
    
    # Deployment methods
    def create_deployment(self, cluster_id: str, deployment_type: str, 
                         configuration: Dict) -> Dict[str, Any]:
        """Create a deployment"""
        data = {
            'cluster_id': cluster_id,
            'deployment_type': deployment_type,
            'configuration': configuration
        }
        return self.post('/api/v1/deployments', data=data)
    
    def get_deployment_status(self, deployment_id: str) -> Dict[str, Any]:
        """Get deployment status"""
        return self.get(f'/api/v1/deployments/{deployment_id}/status')
    
    def rollback_deployment(self, deployment_id: str) -> Dict[str, Any]:
        """Rollback deployment"""
        return self.post(f'/api/v1/deployments/{deployment_id}/rollback')
    
    # Configuration methods
    def get_system_config(self) -> Dict[str, Any]:
        """Get system configuration"""
        return self.get('/api/v1/config/system')
    
    def update_system_config(self, config: Dict) -> Dict[str, Any]:
        """Update system configuration"""
        return self.put('/api/v1/config/system', data=config)
    
    def create_optimization_strategy(self, strategy: Dict) -> Dict[str, Any]:
        """Create optimization strategy"""
        return self.post('/api/v1/config/optimization/strategies', data=strategy)
    
    # Notification methods
    def send_notification(self, message: str, channels: List[str] = None) -> Dict[str, Any]:
        """Send notification"""
        data = {'message': message}
        if channels:
            data['channels'] = channels
        return self.post('/api/v1/notifications/send', data=data)
    
    # Business intelligence methods
    def get_business_report(self, cluster_id: str, report_type: str = 'cost_optimization') -> Dict[str, Any]:
        """Get business report"""
        params = {
            'cluster_id': cluster_id,
            'report_type': report_type
        }
        return self.get('/api/v1/business/reports', params=params)
    
    def calculate_roi(self, investment_data: Dict) -> Dict[str, Any]:
        """Calculate ROI"""
        return self.post('/api/v1/business/roi/calculate', data=investment_data)
    
    def get_performance_kpis(self, cluster_id: str) -> Dict[str, Any]:
        """Get performance KPIs"""
        params = {'cluster_id': cluster_id}
        return self.get('/api/v1/business/performance/kpis', params=params) 