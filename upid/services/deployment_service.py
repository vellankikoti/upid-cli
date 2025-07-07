"""
Deployment service for UPID optimizations and zero-pod scaling
"""
import yaml
from typing import Dict, Any, List, Optional
from upid.core.api_client import UPIDAPIClient

class DeploymentService:
    """Deployment service for UPID optimizations"""
    
    def __init__(self, auth_manager):
        self.auth = auth_manager
        self.api_client = auth_manager.api_client
    
    def deploy_zero_pod_scaling(self, cluster_id: str, namespace: str = None) -> Dict[str, Any]:
        """Deploy zero-pod scaling configurations"""
        
        # Get idle analysis
        from upid.services.optimization_service import OptimizationService
        optimization_service = OptimizationService(self.auth)
        idle_analysis = optimization_service._analyze_pod_idle_time(cluster_id, {})
        
        # Filter pods that can scale to zero
        scalable_pods = [
            pod for pod in idle_analysis['idle_opportunities']
            if pod['can_scale_to_zero'] and (not namespace or pod['namespace'] == namespace)
        ]
        
        if not scalable_pods:
            return {
                'status': 'no_opportunities',
                'message': 'No pods found suitable for zero-pod scaling'
            }
        
        # Generate HPA configurations for zero-pod scaling
        hpa_configs = []
        for pod in scalable_pods:
            hpa_config = self._generate_zero_pod_hpa_config(pod)
            hpa_configs.append(hpa_config)
        
        # Deploy configurations
        deployment_id = self._deploy_hpa_configurations(cluster_id, hpa_configs)
        
        return {
            'deployment_id': deployment_id,
            'pods_configured': len(scalable_pods),
            'potential_savings': sum(pod['potential_savings'] for pod in scalable_pods),
            'configurations': hpa_configs,
            'status': 'success'
        }
    
    def _generate_zero_pod_hpa_config(self, pod_analysis: Dict) -> Dict[str, Any]:
        """Generate HPA configuration for zero-pod scaling"""
        
        return {
            'apiVersion': 'autoscaling/v2',
            'kind': 'HorizontalPodAutoscaler',
            'metadata': {
                'name': f"{pod_analysis['pod_name']}-zero-pod-hpa",
                'namespace': pod_analysis['namespace'],
                'labels': {
                    'app': pod_analysis['pod_name'],
                    'managed-by': 'upid',
                    'optimization-type': 'zero-pod-scaling'
                }
            },
            'spec': {
                'scaleTargetRef': {
                    'apiVersion': 'apps/v1',
                    'kind': 'Deployment',
                    'name': pod_analysis['pod_name']
                },
                'minReplicas': 0,  # Key for zero-pod scaling
                'maxReplicas': 10,
                'metrics': [
                    {
                        'type': 'Resource',
                        'resource': {
                            'name': 'cpu',
                            'target': {
                                'type': 'Utilization',
                                'averageUtilization': 10  # Scale up at 10% CPU
                            }
                        }
                    },
                    {
                        'type': 'Resource',
                        'resource': {
                            'name': 'memory',
                            'target': {
                                'type': 'Utilization',
                                'averageUtilization': 10  # Scale up at 10% memory
                            }
                        }
                    }
                ],
                'behavior': {
                    'scaleDown': {
                        'stabilizationWindowSeconds': pod_analysis['recommended_scale_down_time'],
                        'policies': [
                            {
                                'type': 'Pods',
                                'value': 1,
                                'periodSeconds': 60
                            }
                        ]
                    },
                    'scaleUp': {
                        'stabilizationWindowSeconds': 0,
                        'policies': [
                            {
                                'type': 'Pods',
                                'value': 1,
                                'periodSeconds': 30
                            }
                        ]
                    }
                }
            }
        }
    
    def _deploy_hpa_configurations(self, cluster_id: str, hpa_configs: List[Dict]) -> str:
        """Deploy HPA configurations to cluster"""
        
        # Create deployment configuration
        deployment_config = {
            'cluster_id': cluster_id,
            'deployment_type': 'zero_pod_scaling',
            'configurations': hpa_configs,
            'metadata': {
                'description': 'Zero-pod scaling deployment',
                'optimization_type': 'zero_pod_scaling',
                'configurations_count': len(hpa_configs)
            }
        }
        
        # Deploy via API
        deployment = self.api_client.create_deployment(
            cluster_id=cluster_id,
            deployment_type='zero_pod_scaling',
            configuration=deployment_config
        )
        
        return deployment['deployment_id']
    
    def deploy_optimizations(self, cluster_id: str, recommendations: List[Dict]) -> Dict[str, Any]:
        """Deploy optimization recommendations"""
        
        # Convert recommendations to deployment configurations
        deployment_configs = []
        for rec in recommendations:
            config = self._create_optimization_config(rec)
            deployment_configs.append(config)
        
        # Create deployment
        deployment_config = {
            'cluster_id': cluster_id,
            'deployment_type': 'optimization',
            'configurations': deployment_configs,
            'metadata': {
                'description': 'Resource optimization deployment',
                'optimization_type': 'resource_optimization',
                'recommendations_count': len(recommendations)
            }
        }
        
        # Deploy via API
        deployment = self.api_client.create_deployment(
            cluster_id=cluster_id,
            deployment_type='optimization',
            configuration=deployment_config
        )
        
        return deployment
    
    def _create_optimization_config(self, recommendation: Dict) -> Dict[str, Any]:
        """Create optimization configuration from recommendation"""
        
        config = {
            'type': recommendation['type'],
            'title': recommendation['title'],
            'description': recommendation['description'],
            'savings': recommendation['savings'],
            'risk_level': recommendation['risk_level']
        }
        
        # Add type-specific configuration
        if recommendation['type'] == 'cpu_optimization':
            config.update({
                'resource_type': 'cpu',
                'action': 'reduce_allocation',
                'target_utilization': 80
            })
        elif recommendation['type'] == 'memory_optimization':
            config.update({
                'resource_type': 'memory',
                'action': 'reduce_allocation',
                'target_utilization': 85
            })
        elif recommendation['type'] == 'cost_optimization':
            config.update({
                'resource_type': 'all',
                'action': 'right_size',
                'target_efficiency': 70
            })
        
        return config
    
    def get_deployment_status(self, deployment_id: str) -> Dict[str, Any]:
        """Get deployment status"""
        try:
            return self.api_client.get_deployment_status(deployment_id)
        except Exception as e:
            raise Exception(f"Failed to get deployment status: {e}")
    
    def rollback_deployment(self, deployment_id: str) -> Dict[str, Any]:
        """Rollback deployment"""
        try:
            return self.api_client.rollback_deployment(deployment_id)
        except Exception as e:
            raise Exception(f"Failed to rollback deployment: {e}")
    
    def list_deployments(self, cluster_id: str = None) -> List[Dict[str, Any]]:
        """List deployments"""
        try:
            params = {}
            if cluster_id:
                params['cluster_id'] = cluster_id
            
            response = self.api_client.get('/api/v1/deployments', params=params)
            return response.get('deployments', [])
        except Exception as e:
            raise Exception(f"Failed to list deployments: {e}")
    
    def get_deployment_logs(self, deployment_id: str) -> List[str]:
        """Get deployment logs"""
        try:
            response = self.api_client.get(f'/api/v1/deployments/{deployment_id}/logs')
            return response.get('logs', [])
        except Exception as e:
            raise Exception(f"Failed to get deployment logs: {e}")
    
    def validate_deployment(self, cluster_id: str, deployment_config: Dict) -> Dict[str, Any]:
        """Validate deployment configuration"""
        try:
            return self.api_client.post(
                f'/api/v1/deployments/validate',
                data={
                    'cluster_id': cluster_id,
                    'configuration': deployment_config
                }
            )
        except Exception as e:
            raise Exception(f"Failed to validate deployment: {e}")
    
    def simulate_deployment(self, cluster_id: str, deployment_config: Dict) -> Dict[str, Any]:
        """Simulate deployment without applying"""
        try:
            return self.api_client.post(
                f'/api/v1/deployments/simulate',
                data={
                    'cluster_id': cluster_id,
                    'configuration': deployment_config
                }
            )
        except Exception as e:
            raise Exception(f"Failed to simulate deployment: {e}")
    
    def get_deployment_metrics(self, deployment_id: str) -> Dict[str, Any]:
        """Get deployment metrics"""
        try:
            return self.api_client.get(f'/api/v1/deployments/{deployment_id}/metrics')
        except Exception as e:
            raise Exception(f"Failed to get deployment metrics: {e}")
    
    def pause_deployment(self, deployment_id: str) -> Dict[str, Any]:
        """Pause deployment"""
        try:
            return self.api_client.post(f'/api/v1/deployments/{deployment_id}/pause')
        except Exception as e:
            raise Exception(f"Failed to pause deployment: {e}")
    
    def resume_deployment(self, deployment_id: str) -> Dict[str, Any]:
        """Resume deployment"""
        try:
            return self.api_client.post(f'/api/v1/deployments/{deployment_id}/resume')
        except Exception as e:
            raise Exception(f"Failed to resume deployment: {e}")
    
    def abort_deployment(self, deployment_id: str) -> Dict[str, Any]:
        """Abort deployment"""
        try:
            return self.api_client.post(f'/api/v1/deployments/{deployment_id}/abort')
        except Exception as e:
            raise Exception(f"Failed to abort deployment: {e}")
    
    def get_deployment_history(self, cluster_id: str) -> List[Dict[str, Any]]:
        """Get deployment history for cluster"""
        try:
            response = self.api_client.get(f'/api/v1/deployments/history/{cluster_id}')
            return response.get('deployments', [])
        except Exception as e:
            raise Exception(f"Failed to get deployment history: {e}")
    
    def export_deployment_config(self, deployment_id: str, format: str = 'yaml') -> str:
        """Export deployment configuration"""
        try:
            response = self.api_client.get(f'/api/v1/deployments/{deployment_id}/export')
            config = response.get('configuration', {})
            
            if format == 'yaml':
                return yaml.dump(config, default_flow_style=False)
            else:
                import json
                return json.dumps(config, indent=2)
        except Exception as e:
            raise Exception(f"Failed to export deployment config: {e}") 