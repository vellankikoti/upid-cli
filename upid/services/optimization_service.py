"""
Optimization service with zero-pod scaling detection
"""
import numpy as np
from scipy import stats
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from upid.core.api_client import UPIDAPIClient
from upid.core.utils import format_currency, format_percentage, format_duration

class OptimizationService:
    """Optimization service with mathematical analysis and zero-pod scaling detection"""
    
    def __init__(self, auth_manager):
        self.auth = auth_manager
        self.api_client = auth_manager.api_client
    
    def analyze_cluster(self, cluster_id: str, strategy: str = None) -> Dict[str, Any]:
        """Analyze cluster for optimization opportunities including zero-pod scaling"""
        
        # Get comprehensive cluster metrics
        metrics = self.api_client.get_resource_metrics(cluster_id, '24h')
        pod_metrics = self.api_client.get_pod_metrics(cluster_id)
        
        # Analyze idle time for zero-pod scaling
        idle_analysis = self._analyze_pod_idle_time(cluster_id, pod_metrics)
        
        # Apply mathematical analysis
        analysis = self._perform_mathematical_analysis(metrics, idle_analysis, strategy)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(analysis)
        
        return {
            'cluster_id': cluster_id,
            'potential_savings': analysis['potential_savings'],
            'efficiency_score': analysis['efficiency_score'],
            'performance_impact': analysis['performance_impact'],
            'zero_pod_opportunities': idle_analysis,
            'recommendations': recommendations,
            'analysis_timestamp': datetime.now().isoformat()
        }
    
    def _analyze_pod_idle_time(self, cluster_id: str, pod_metrics: Dict) -> Dict[str, Any]:
        """Analyze pod idle time patterns for zero-pod scaling opportunities"""
        
        idle_opportunities = []
        total_potential_savings = 0
        
        for pod in pod_metrics.get('pods', []):
            idle_analysis = self._analyze_single_pod_idle_time(pod)
            if idle_analysis['can_scale_to_zero']:
                idle_opportunities.append(idle_analysis)
                total_potential_savings += idle_analysis['potential_savings']
        
        # Analyze cluster-wide patterns
        cluster_patterns = self._detect_cluster_idle_patterns(pod_metrics)
        
        return {
            'idle_opportunities': idle_opportunities,
            'total_potential_savings': total_potential_savings,
            'scalable_pods_count': len(idle_opportunities),
            'idle_patterns': cluster_patterns
        }
    
    def _analyze_single_pod_idle_time(self, pod: Dict) -> Dict[str, Any]:
        """Analyze idle time for a single pod"""
        
        # Extract metrics
        cpu_usage = np.array(pod.get('cpu_usage', []))
        memory_usage = np.array(pod.get('memory_usage', []))
        http_requests = np.array(pod.get('http_requests', []))
        network_io = np.array(pod.get('network_io', []))
        
        # Calculate idle periods
        idle_periods = self._calculate_idle_periods(cpu_usage, memory_usage, http_requests, network_io)
        
        # Analyze idle patterns
        idle_analysis = self._analyze_idle_patterns(idle_periods, pod.get('request_patterns', []))
        
        # Determine if pod can scale to zero
        can_scale_to_zero = self._can_scale_to_zero(idle_analysis)
        
        # Calculate potential savings
        potential_savings = self._calculate_zero_pod_savings(pod, idle_analysis)
        
        return {
            'pod_name': pod['name'],
            'namespace': pod['namespace'],
            'idle_percentage': idle_analysis['idle_percentage'],
            'avg_idle_duration': idle_analysis['avg_idle_duration'],
            'idle_pattern': idle_analysis['idle_pattern'],
            'can_scale_to_zero': can_scale_to_zero,
            'potential_savings': potential_savings,
            'recommended_scale_down_time': idle_analysis['recommended_scale_down_time'],
            'recommended_scale_up_conditions': idle_analysis['scale_up_conditions'],
            'resource_allocation': pod.get('resource_allocation', {}),
            'current_replicas': pod.get('replicas', 1)
        }
    
    def _calculate_idle_periods(self, cpu_usage: np.ndarray, memory_usage: np.ndarray, 
                               http_requests: np.ndarray, network_io: np.ndarray) -> List[Dict]:
        """Calculate idle periods based on resource usage and activity patterns"""
        
        idle_periods = []
        idle_threshold = 0.1  # 10% utilization threshold for idle
        min_idle_duration = 5  # Minimum 5 minutes to be considered idle
        
        for i in range(len(cpu_usage)):
            is_idle = (
                cpu_usage[i] < idle_threshold and 
                memory_usage[i] < idle_threshold and 
                http_requests[i] == 0 and
                network_io[i] < 1000  # Less than 1KB/s network activity
            )
            
            if is_idle:
                if not idle_periods or idle_periods[-1]['end'] != i - 1:
                    # Start new idle period
                    idle_periods.append({
                        'start': i,
                        'end': i,
                        'duration': 1
                    })
                else:
                    # Extend existing idle period
                    idle_periods[-1]['end'] = i
                    idle_periods[-1]['duration'] += 1
        
        # Filter out short idle periods
        idle_periods = [period for period in idle_periods if period['duration'] >= min_idle_duration]
        
        return idle_periods
    
    def _analyze_idle_patterns(self, idle_periods: List[Dict], request_patterns: List) -> Dict[str, Any]:
        """Analyze idle patterns to determine scaling strategy"""
        
        if not idle_periods:
            return {
                'idle_percentage': 0,
                'avg_idle_duration': 0,
                'idle_pattern': 'none',
                'can_scale_to_zero': False,
                'recommended_scale_down_time': 300,
                'scale_up_conditions': self._get_default_scale_up_conditions()
            }
        
        # Calculate idle statistics
        total_idle_time = sum(period['duration'] for period in idle_periods)
        total_time = max(period['end'] for period in idle_periods) + 1 if idle_periods else 1
        idle_percentage = (total_idle_time / total_time) * 100
        
        avg_idle_duration = np.mean([period['duration'] for period in idle_periods])
        
        # Determine idle pattern
        idle_pattern = self._classify_idle_pattern(idle_periods, request_patterns)
        
        # Determine if scaling to zero is feasible
        can_scale_to_zero = (
            idle_percentage > 50 and  # More than 50% idle time
            avg_idle_duration > 300 and  # Average idle period > 5 minutes
            idle_pattern in ['predictable', 'scheduled', 'low_traffic']
        )
        
        # Calculate recommended scale-down time
        recommended_scale_down_time = self._calculate_scale_down_time(idle_periods)
        
        # Define scale-up conditions
        scale_up_conditions = self._define_scale_up_conditions(idle_pattern)
        
        return {
            'idle_percentage': idle_percentage,
            'avg_idle_duration': avg_idle_duration,
            'idle_pattern': idle_pattern,
            'can_scale_to_zero': can_scale_to_zero,
            'recommended_scale_down_time': recommended_scale_down_time,
            'scale_up_conditions': scale_up_conditions
        }
    
    def _classify_idle_pattern(self, idle_periods: List[Dict], request_patterns: List) -> str:
        """Classify the type of idle pattern"""
        
        if not idle_periods:
            return 'none'
        
        # Analyze periodicity
        durations = [period['duration'] for period in idle_periods]
        avg_duration = np.mean(durations)
        std_duration = np.std(durations)
        
        # Check for predictable patterns (low variance)
        if std_duration < avg_duration * 0.3:
            return 'predictable'
        
        # Check for scheduled patterns (daily/weekly cycles)
        if self._detect_scheduled_pattern(idle_periods):
            return 'scheduled'
        
        # Check for low traffic patterns (extended idle periods)
        if avg_duration > 1800:  # Average idle > 30 minutes
            return 'low_traffic'
        
        return 'irregular'
    
    def _detect_scheduled_pattern(self, idle_periods: List[Dict]) -> bool:
        """Detect if idle periods follow a scheduled pattern"""
        
        # Simple heuristic: check if idle periods occur at similar times
        start_times = [period['start'] for period in idle_periods]
        
        # Group start times by hour (assuming hourly data)
        hourly_groups = {}
        for start_time in start_times:
            hour = start_time // 3600  # Convert to hour
            if hour not in hourly_groups:
                hourly_groups[hour] = 0
            hourly_groups[hour] += 1
        
        # Check if there's a dominant hour pattern
        max_count = max(hourly_groups.values()) if hourly_groups else 0
        total_periods = len(idle_periods)
        
        return max_count > total_periods * 0.3  # 30% of idle periods at same hour
    
    def _calculate_scale_down_time(self, idle_periods: List[Dict]) -> int:
        """Calculate recommended scale-down time in seconds"""
        
        if not idle_periods:
            return 300  # Default 5 minutes
        
        # Use median idle duration as scale-down time
        durations = [period['duration'] for period in idle_periods]
        median_duration = np.median(durations)
        
        # Convert to seconds (assuming data points are 1-minute intervals)
        scale_down_time = int(median_duration * 60)
        
        # Clamp between 1 minute and 1 hour
        return max(60, min(3600, scale_down_time))
    
    def _define_scale_up_conditions(self, idle_pattern: str) -> Dict[str, Any]:
        """Define conditions for scaling up from zero"""
        
        base_conditions = {
            'cpu_threshold': 0.1,
            'memory_threshold': 0.1,
            'request_threshold': 1,
            'network_threshold': 1000  # 1KB/s
        }
        
        if idle_pattern == 'predictable':
            return {
                **base_conditions,
                'schedule_based': True,
                'predicted_scale_up_time': 'based_on_historical_pattern'
            }
        elif idle_pattern == 'scheduled':
            return {
                **base_conditions,
                'schedule_based': True,
                'scale_up_schedule': 'detected_from_pattern'
            }
        else:
            return {
                **base_conditions,
                'schedule_based': False,
                'reactive_scaling': True
            }
    
    def _get_default_scale_up_conditions(self) -> Dict[str, Any]:
        """Get default scale-up conditions"""
        return {
            'cpu_threshold': 0.1,
            'memory_threshold': 0.1,
            'request_threshold': 1,
            'network_threshold': 1000,
            'schedule_based': False,
            'reactive_scaling': True
        }
    
    def _can_scale_to_zero(self, idle_analysis: Dict) -> bool:
        """Determine if a pod can safely scale to zero"""
        
        return (
            idle_analysis['can_scale_to_zero'] and
            idle_analysis['idle_percentage'] > 50 and
            idle_analysis['avg_idle_duration'] > 300
        )
    
    def _calculate_zero_pod_savings(self, pod: Dict, idle_analysis: Dict) -> float:
        """Calculate potential savings from scaling to zero"""
        
        # Get pod resource allocation
        resource_allocation = pod.get('resource_allocation', {})
        cpu_request = resource_allocation.get('cpu_request', 0)
        memory_request = resource_allocation.get('memory_request', 0)
        
        # Calculate hourly cost (example pricing)
        cpu_cost_per_hour = cpu_request * 0.1  # $0.1 per CPU core per hour
        memory_cost_per_hour = memory_request * 0.01  # $0.01 per GB per hour
        
        total_hourly_cost = cpu_cost_per_hour + memory_cost_per_hour
        
        # Calculate savings based on idle percentage
        idle_percentage = idle_analysis['idle_percentage'] / 100
        daily_savings = total_hourly_cost * 24 * idle_percentage
        
        return daily_savings * 30  # Monthly savings
    
    def _detect_cluster_idle_patterns(self, pod_metrics: Dict) -> Dict[str, Any]:
        """Detect global idle patterns across the cluster"""
        
        all_idle_periods = []
        total_pods = len(pod_metrics.get('pods', []))
        
        for pod in pod_metrics.get('pods', []):
            cpu_usage = np.array(pod.get('cpu_usage', []))
            memory_usage = np.array(pod.get('memory_usage', []))
            http_requests = np.array(pod.get('http_requests', []))
            network_io = np.array(pod.get('network_io', []))
            
            idle_periods = self._calculate_idle_periods(cpu_usage, memory_usage, http_requests, network_io)
            all_idle_periods.extend(idle_periods)
        
        # Analyze cluster-wide patterns
        if all_idle_periods:
            cluster_idle_percentage = len(all_idle_periods) / total_pods * 100
            avg_cluster_idle_duration = np.mean([period['duration'] for period in all_idle_periods])
        else:
            cluster_idle_percentage = 0
            avg_cluster_idle_duration = 0
        
        return {
            'cluster_idle_percentage': cluster_idle_percentage,
            'avg_cluster_idle_duration': avg_cluster_idle_duration,
            'total_idle_periods': len(all_idle_periods),
            'total_pods_analyzed': total_pods
        }
    
    def _perform_mathematical_analysis(self, metrics: Dict, idle_analysis: Dict, strategy: str) -> Dict[str, Any]:
        """Perform mathematical analysis without ML"""
        
        # CPU optimization using statistical analysis
        cpu_utilization = np.array(metrics.get('cpu_utilization', []))
        cpu_analysis = self._analyze_cpu_utilization(cpu_utilization)
        
        # Memory optimization using trend analysis
        memory_utilization = np.array(metrics.get('memory_utilization', []))
        memory_analysis = self._analyze_memory_utilization(memory_utilization)
        
        # Cost optimization using mathematical models
        cost_analysis = self._analyze_cost_efficiency(metrics)
        
        # Calculate total potential savings including zero-pod scaling
        total_savings = (
            cpu_analysis['savings'] + 
            memory_analysis['savings'] + 
            cost_analysis['savings'] +
            idle_analysis['total_potential_savings']
        )
        
        return {
            'cpu_analysis': cpu_analysis,
            'memory_analysis': memory_analysis,
            'cost_analysis': cost_analysis,
            'potential_savings': total_savings,
            'efficiency_score': self._calculate_efficiency_score(cpu_analysis, memory_analysis, cost_analysis),
            'performance_impact': self._calculate_performance_impact(cpu_analysis, memory_analysis)
        }
    
    def _analyze_cpu_utilization(self, cpu_data: np.ndarray) -> Dict[str, Any]:
        """Analyze CPU utilization using statistical methods"""
        
        if len(cpu_data) == 0:
            return {'savings': 0, 'over_provisioned': False}
        
        # Calculate percentiles
        p50 = np.percentile(cpu_data, 50)
        p95 = np.percentile(cpu_data, 95)
        p99 = np.percentile(cpu_data, 99)
        
        # Detect over-provisioning
        over_provisioned = p95 < 50  # If 95th percentile is below 50%, likely over-provisioned
        
        # Calculate potential savings
        if over_provisioned:
            current_capacity = np.max(cpu_data)
            recommended_capacity = p95 * 1.2  # 20% headroom
            savings_percentage = (current_capacity - recommended_capacity) / current_capacity
        else:
            savings_percentage = 0
        
        return {
            'p50': p50,
            'p95': p95,
            'p99': p99,
            'over_provisioned': over_provisioned,
            'savings_percentage': savings_percentage,
            'savings': savings_percentage * 1000  # Estimated cost savings
        }
    
    def _analyze_memory_utilization(self, memory_data: np.ndarray) -> Dict[str, Any]:
        """Analyze memory utilization using trend analysis"""
        
        if len(memory_data) == 0:
            return {'savings': 0, 'memory_leak': False}
        
        # Linear regression for trend analysis
        x = np.arange(len(memory_data))
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, memory_data)
        
        # Detect memory leaks (increasing trend)
        memory_leak = slope > 0.1 and r_value > 0.7
        
        # Calculate optimal memory allocation
        current_peak = np.max(memory_data)
        recommended_memory = current_peak * 1.1  # 10% headroom
        
        return {
            'trend_slope': slope,
            'correlation': r_value,
            'memory_leak': memory_leak,
            'current_peak': current_peak,
            'recommended_memory': recommended_memory,
            'savings': 500  # Estimated savings
        }
    
    def _analyze_cost_efficiency(self, metrics: Dict) -> Dict[str, Any]:
        """Analyze cost efficiency using mathematical models"""
        
        # Calculate resource efficiency
        cpu_efficiency = np.mean(metrics.get('cpu_utilization', [0]))
        memory_efficiency = np.mean(metrics.get('memory_utilization', [0]))
        
        # Identify waste (low utilization)
        cpu_waste = cpu_efficiency < 0.3
        memory_waste = memory_efficiency < 0.3
        
        total_waste = (cpu_waste + memory_waste) / 2
        potential_savings = total_waste * 2000  # Estimated cost savings
        
        return {
            'cpu_efficiency': cpu_efficiency,
            'memory_efficiency': memory_efficiency,
            'total_waste': total_waste,
            'savings': potential_savings
        }
    
    def _calculate_efficiency_score(self, cpu_analysis: Dict, memory_analysis: Dict, cost_analysis: Dict) -> float:
        """Calculate overall efficiency score"""
        
        # Weighted average of different efficiency metrics
        cpu_score = 100 - (cpu_analysis['savings_percentage'] * 100)
        memory_score = 100 - (memory_analysis.get('waste_percentage', 0) * 100)
        cost_score = 100 - (cost_analysis['total_waste'] * 100)
        
        return (cpu_score * 0.4 + memory_score * 0.3 + cost_score * 0.3)
    
    def _calculate_performance_impact(self, cpu_analysis: Dict, memory_analysis: Dict) -> float:
        """Calculate potential performance impact"""
        
        # Estimate performance impact based on optimization recommendations
        impact = 0
        
        if cpu_analysis['over_provisioned']:
            impact += 5  # 5% potential performance impact
        
        if memory_analysis['memory_leak']:
            impact += 10  # 10% potential performance impact
        
        return min(impact, 20)  # Cap at 20%
    
    def _generate_recommendations(self, analysis: Dict) -> List[Dict[str, Any]]:
        """Generate optimization recommendations"""
        
        recommendations = []
        
        # CPU optimization recommendations
        if analysis['cpu_analysis']['over_provisioned']:
            recommendations.append({
                'title': 'Reduce CPU allocation',
                'description': 'CPU is over-provisioned based on P95 utilization',
                'savings': analysis['cpu_analysis']['savings'],
                'risk_level': 'low',
                'type': 'cpu_optimization'
            })
        
        # Memory optimization recommendations
        if analysis['memory_analysis']['memory_leak']:
            recommendations.append({
                'title': 'Investigate memory leak',
                'description': 'Detected increasing memory trend',
                'savings': 1000,
                'risk_level': 'medium',
                'type': 'memory_optimization'
            })
        
        # Cost optimization recommendations
        if analysis['cost_analysis']['total_waste'] > 0.3:
            recommendations.append({
                'title': 'Right-size resources',
                'description': 'Low resource utilization detected',
                'savings': analysis['cost_analysis']['savings'],
                'risk_level': 'low',
                'type': 'cost_optimization'
            })
        
        return recommendations
    
    def get_optimization_status(self, cluster_id: str) -> Dict[str, Any]:
        """Get optimization status for cluster"""
        try:
            return self.api_client.get_optimization_status(cluster_id)
        except Exception as e:
            raise Exception(f"Failed to get optimization status: {e}")
    
    def apply_optimizations(self, cluster_id: str, recommendations: List[Dict]) -> Dict[str, Any]:
        """Apply optimization recommendations"""
        try:
            return self.api_client.apply_optimizations(cluster_id, recommendations)
        except Exception as e:
            raise Exception(f"Failed to apply optimizations: {e}")
    
    def rollback_optimizations(self, cluster_id: str) -> Dict[str, Any]:
        """Rollback optimizations for cluster"""
        try:
            return self.api_client.rollback_deployment(cluster_id)
        except Exception as e:
            raise Exception(f"Failed to rollback optimizations: {e}") 