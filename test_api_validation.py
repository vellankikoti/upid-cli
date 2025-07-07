#!/usr/bin/env python3
"""
Detailed API Validation Script for UPID CLI
Tests specific functionality and edge cases
"""

import sys
import os
import json
import time
from pathlib import Path
from typing import Dict, Any, List, Optional

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from upid.core.cluster_detector import ClusterDetector
from upid.core.config import Config
from upid.core.auth import AuthManager
from upid.core.api_client import UPIDAPIClient
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

console = Console()

class APIValidator:
    """Detailed API validator for UPID CLI"""
    
    def __init__(self):
        self.cluster_detector = ClusterDetector()
        self.config = Config()
        self.auth_manager = AuthManager(self.config)
        self.api_client = UPIDAPIClient(self.config, self.auth_manager)
        self.validation_results = []
        
    def validate_all_apis(self):
        """Run comprehensive API validation"""
        console.print("\n" + "="*80)
        console.print("[bold blue]🔍 UPID CLI - Detailed API Validation[/bold blue]")
        console.print("="*80)
        
        # API validation categories
        validations = [
            ("Cluster Detection APIs", self.validate_cluster_detection_apis),
            ("Resource Analysis APIs", self.validate_resource_analysis_apis),
            ("Optimization APIs", self.validate_optimization_apis),
            ("Reporting APIs", self.validate_reporting_apis),
            ("Configuration APIs", self.validate_configuration_apis),
            ("Authentication APIs", self.validate_authentication_apis),
            ("Data Structure APIs", self.validate_data_structure_apis),
            ("Performance APIs", self.validate_performance_apis)
        ]
        
        for category_name, validation_func in validations:
            console.print(f"\n[bold cyan]{category_name}[/bold cyan]")
            validation_func()
        
        # Display validation results
        self.display_validation_results()
        
    def validate_cluster_detection_apis(self):
        """Validate cluster detection APIs"""
        try:
            # Test cluster detection
            cluster_info = self.cluster_detector.detect_cluster()
            
            # Validate structure
            self.validate_field(cluster_info, 'name', str, 'Cluster name')
            self.validate_field(cluster_info, 'type', str, 'Cluster type')
            self.validate_field(cluster_info, 'status', str, 'Cluster status')
            self.validate_field(cluster_info, 'kubeconfig', str, 'Kubeconfig path')
            
            # Test metrics retrieval
            metrics = self.cluster_detector.get_cluster_metrics()
            
            # Validate metrics structure
            self.validate_field(metrics, 'resources', dict, 'Resources metrics')
            
            if 'resources' in metrics:
                resources = metrics['resources']
                self.validate_field(resources, 'cpu', dict, 'CPU metrics')
                self.validate_field(resources, 'memory', dict, 'Memory metrics')
                self.validate_field(resources, 'pods', dict, 'Pod metrics')
                
                # Validate CPU metrics
                if 'cpu' in resources:
                    cpu = resources['cpu']
                    self.validate_field(cpu, 'used', (int, float), 'CPU used')
                    self.validate_field(cpu, 'total', (int, float), 'CPU total')
                
                # Validate memory metrics
                if 'memory' in resources:
                    memory = resources['memory']
                    self.validate_field(memory, 'used', (int, float), 'Memory used')
                    self.validate_field(memory, 'total', (int, float), 'Memory total')
                
                # Validate pod metrics
                if 'pods' in resources:
                    pods = resources['pods']
                    self.validate_field(pods, 'running', int, 'Running pods')
                    self.validate_field(pods, 'total', int, 'Total pods')
            
            console.print("[green]✅ Cluster detection APIs validated[/green]")
            
        except Exception as e:
            console.print(f"[red]❌ Cluster detection validation failed: {e}[/red]")
    
    def validate_resource_analysis_apis(self):
        """Validate resource analysis APIs"""
        try:
            # Test resource analysis
            resources = self.api_client.analyze_resources('test-cluster')
            self.validate_field(resources, 'cpu', dict, 'CPU analysis')
            self.validate_field(resources, 'memory', dict, 'Memory analysis')
            
            # Test cost analysis
            costs = self.api_client.analyze_costs('test-cluster')
            self.validate_field(costs, 'total_cost', (int, float), 'Total cost')
            
            # Test performance analysis
            performance = self.api_client.analyze_performance('test-cluster')
            self.validate_field(performance, 'cpu', dict, 'CPU performance')
            self.validate_field(performance, 'memory', dict, 'Memory performance')
            
            console.print("[green]✅ Resource analysis APIs validated[/green]")
            
        except Exception as e:
            console.print(f"[red]❌ Resource analysis validation failed: {e}[/red]")
    
    def validate_optimization_apis(self):
        """Validate optimization APIs"""
        try:
            # Test resource optimizations
            resource_opts = self.api_client.get_resource_optimizations('test-cluster')
            self.validate_field(resource_opts, None, list, 'Resource optimizations')
            
            if resource_opts:
                for opt in resource_opts:
                    self.validate_field(opt, 'type', str, 'Optimization type')
                    self.validate_field(opt, 'resource', str, 'Resource name')
                    self.validate_field(opt, 'current_value', str, 'Current value')
                    self.validate_field(opt, 'recommended_value', str, 'Recommended value')
                    self.validate_field(opt, 'savings', (int, float), 'Savings')
                    self.validate_field(opt, 'impact', str, 'Impact level')
            
            # Test cost optimizations
            cost_opts = self.api_client.get_cost_optimizations('test-cluster')
            self.validate_field(cost_opts, None, list, 'Cost optimizations')
            
            if cost_opts:
                for opt in cost_opts:
                    self.validate_field(opt, 'category', str, 'Cost category')
                    self.validate_field(opt, 'action', str, 'Optimization action')
                    self.validate_field(opt, 'current_cost', (int, float), 'Current cost')
                    self.validate_field(opt, 'optimized_cost', (int, float), 'Optimized cost')
                    self.validate_field(opt, 'savings', (int, float), 'Cost savings')
                    self.validate_field(opt, 'priority', str, 'Priority level')
            
            # Test zero-pod recommendations
            zero_pod_recs = self.api_client.get_zero_pod_recommendations('test-cluster')
            self.validate_field(zero_pod_recs, None, list, 'Zero-pod recommendations')
            
            if zero_pod_recs:
                for rec in zero_pod_recs:
                    self.validate_field(rec, 'namespace', str, 'Namespace')
                    self.validate_field(rec, 'deployment', str, 'Deployment name')
                    self.validate_field(rec, 'current_replicas', int, 'Current replicas')
                    self.validate_field(rec, 'idle_time', str, 'Idle time')
                    self.validate_field(rec, 'savings', (int, float), 'Savings')
                    self.validate_field(rec, 'risk_level', str, 'Risk level')
            
            console.print("[green]✅ Optimization APIs validated[/green]")
            
        except Exception as e:
            console.print(f"[red]❌ Optimization validation failed: {e}[/red]")
    
    def validate_reporting_apis(self):
        """Validate reporting APIs"""
        try:
            # Test summary report
            summary = self.api_client.generate_summary_report('test-cluster')
            self.validate_field(summary, 'cluster_name', str, 'Cluster name')
            self.validate_field(summary, 'generated_at', str, 'Generated timestamp')
            self.validate_field(summary, 'resources', dict, 'Resources data')
            self.validate_field(summary, 'costs', dict, 'Costs data')
            self.validate_field(summary, 'performance', dict, 'Performance data')
            self.validate_field(summary, 'recommendations', list, 'Recommendations')
            
            # Test cost report
            cost_report = self.api_client.generate_cost_report('test-cluster')
            self.validate_field(cost_report, 'cluster_name', str, 'Cluster name')
            self.validate_field(cost_report, 'total_cost', (int, float), 'Total cost')
            self.validate_field(cost_report, 'services', dict, 'Services breakdown')
            self.validate_field(cost_report, 'optimization_opportunities', list, 'Optimization opportunities')
            
            # Test performance report
            perf_report = self.api_client.generate_performance_report('test-cluster')
            self.validate_field(perf_report, 'cluster_name', str, 'Cluster name')
            self.validate_field(perf_report, 'metrics', dict, 'Performance metrics')
            self.validate_field(perf_report, 'issues', list, 'Performance issues')
            
            console.print("[green]✅ Reporting APIs validated[/green]")
            
        except Exception as e:
            console.print(f"[red]❌ Reporting validation failed: {e}[/red]")
    
    def validate_configuration_apis(self):
        """Validate configuration APIs"""
        try:
            # Test config get/set
            original_timeout = self.config.get('timeout')
            test_timeout = 45
            
            self.config.set('timeout', test_timeout)
            retrieved_timeout = self.config.get('timeout')
            
            if retrieved_timeout != test_timeout:
                raise ValueError(f"Config set/get failed: expected {test_timeout}, got {retrieved_timeout}")
            
            # Restore original value
            self.config.set('timeout', original_timeout)
            
            # Test local mode
            self.config.enable_local_mode()
            if not self.config.is_local_mode():
                raise ValueError("Local mode enable failed")
            
            self.config.disable_local_mode()
            if self.config.is_local_mode():
                raise ValueError("Local mode disable failed")
            
            # Test auth token management
            test_token = 'test-auth-token-12345'
            self.config.set_auth_token(test_token)
            retrieved_token = self.config.get_auth_token()
            
            if retrieved_token != test_token:
                raise ValueError(f"Auth token management failed: expected {test_token}, got {retrieved_token}")
            
            self.config.clear_auth_token()
            cleared_token = self.config.get_auth_token()
            
            if cleared_token is not None:
                raise ValueError("Auth token clear failed")
            
            console.print("[green]✅ Configuration APIs validated[/green]")
            
        except Exception as e:
            console.print(f"[red]❌ Configuration validation failed: {e}[/red]")
    
    def validate_authentication_apis(self):
        """Validate authentication APIs"""
        try:
            # Test login (local mode)
            login_result = self.api_client.login('test@example.com', 'password')
            self.validate_field(login_result, 'token', str, 'Auth token')
            self.validate_field(login_result, 'user', dict, 'User info')
            
            # Test get profile
            profile = self.api_client.get_profile()
            self.validate_field(profile, 'name', str, 'User name')
            self.validate_field(profile, 'email', str, 'User email')
            
            # Test get current user
            current_user = self.api_client.get_current_user()
            self.validate_field(current_user, 'name', str, 'Current user name')
            self.validate_field(current_user, 'email', str, 'Current user email')
            
            # Test logout
            logout_result = self.api_client.logout()
            self.validate_field(logout_result, 'message', str, 'Logout message')
            
            console.print("[green]✅ Authentication APIs validated[/green]")
            
        except Exception as e:
            console.print(f"[red]❌ Authentication validation failed: {e}[/red]")
    
    def validate_data_structure_apis(self):
        """Validate data structure APIs"""
        try:
            # Test cluster info structure
            cluster_info = self.cluster_detector.detect_cluster()
            
            # Validate all required fields exist
            required_fields = ['name', 'type', 'status', 'kubeconfig']
            for field in required_fields:
                if field not in cluster_info:
                    raise ValueError(f"Missing required field: {field}")
                
                if cluster_info[field] is None:
                    raise ValueError(f"Field {field} should not be None")
            
            # Test metrics structure
            metrics = self.cluster_detector.get_cluster_metrics()
            
            if 'resources' in metrics:
                resources = metrics['resources']
                
                # Validate CPU data types and ranges
                if 'cpu' in resources:
                    cpu = resources['cpu']
                    if not isinstance(cpu.get('used', 0), (int, float)):
                        raise ValueError("CPU used should be numeric")
                    if not isinstance(cpu.get('total', 0), (int, float)):
                        raise ValueError("CPU total should be numeric")
                    if cpu.get('used', 0) < 0:
                        raise ValueError("CPU used should be non-negative")
                    if cpu.get('total', 0) < 0:
                        raise ValueError("CPU total should be non-negative")
                
                # Validate memory data types and ranges
                if 'memory' in resources:
                    memory = resources['memory']
                    if not isinstance(memory.get('used', 0), (int, float)):
                        raise ValueError("Memory used should be numeric")
                    if not isinstance(memory.get('total', 0), (int, float)):
                        raise ValueError("Memory total should be numeric")
                    if memory.get('used', 0) < 0:
                        raise ValueError("Memory used should be non-negative")
                    if memory.get('total', 0) < 0:
                        raise ValueError("Memory total should be non-negative")
                
                # Validate pod data types and ranges
                if 'pods' in resources:
                    pods = resources['pods']
                    if not isinstance(pods.get('running', 0), int):
                        raise ValueError("Running pods should be integer")
                    if not isinstance(pods.get('total', 0), int):
                        raise ValueError("Total pods should be integer")
                    if pods.get('running', 0) < 0:
                        raise ValueError("Running pods should be non-negative")
                    if pods.get('total', 0) < 0:
                        raise ValueError("Total pods should be non-negative")
            
            console.print("[green]✅ Data structure APIs validated[/green]")
            
        except Exception as e:
            console.print(f"[red]❌ Data structure validation failed: {e}[/red]")
    
    def validate_performance_apis(self):
        """Validate performance APIs"""
        try:
            # Test API response times
            start_time = time.time()
            cluster_info = self.cluster_detector.detect_cluster()
            detection_time = time.time() - start_time
            
            if detection_time > 10:  # Should complete within 10 seconds
                console.print(f"[yellow]⚠️  Cluster detection took {detection_time:.2f}s (slow)[/yellow]")
            else:
                console.print(f"[green]✅ Cluster detection performance: {detection_time:.2f}s[/green]")
            
            # Test metrics retrieval performance
            start_time = time.time()
            metrics = self.cluster_detector.get_cluster_metrics()
            metrics_time = time.time() - start_time
            
            if metrics_time > 15:  # Should complete within 15 seconds
                console.print(f"[yellow]⚠️  Metrics retrieval took {metrics_time:.2f}s (slow)[/yellow]")
            else:
                console.print(f"[green]✅ Metrics retrieval performance: {metrics_time:.2f}s[/green]")
            
            # Test API client performance
            start_time = time.time()
            resources = self.api_client.analyze_resources('test-cluster')
            analysis_time = time.time() - start_time
            
            if analysis_time > 5:  # Should complete within 5 seconds
                console.print(f"[yellow]⚠️  Resource analysis took {analysis_time:.2f}s (slow)[/yellow]")
            else:
                console.print(f"[green]✅ Resource analysis performance: {analysis_time:.2f}s[/green]")
            
            console.print("[green]✅ Performance APIs validated[/green]")
            
        except Exception as e:
            console.print(f"[red]❌ Performance validation failed: {e}[/red]")
    
    def validate_field(self, obj: Any, field: Optional[str], expected_type: type, description: str):
        """Validate a field in an object"""
        try:
            if field is None:
                # Validate the object itself
                if not isinstance(obj, expected_type):
                    raise ValueError(f"{description} should be {expected_type.__name__}, got {type(obj).__name__}")
            else:
                # Validate a specific field
                if field not in obj:
                    raise ValueError(f"Missing field: {field} in {description}")
                
                value = obj[field]
                if not isinstance(value, expected_type):
                    raise ValueError(f"{description}.{field} should be {expected_type.__name__}, got {type(value).__name__}")
                
                if value is None:
                    raise ValueError(f"{description}.{field} should not be None")
            
            self.validation_results.append({
                'field': field or 'object',
                'description': description,
                'status': 'PASS'
            })
            
        except Exception as e:
            self.validation_results.append({
                'field': field or 'object',
                'description': description,
                'status': 'FAIL',
                'error': str(e)
            })
            raise e
    
    def display_validation_results(self):
        """Display validation results"""
        console.print("\n" + "="*80)
        console.print("[bold blue]📊 API Validation Results[/bold blue]")
        console.print("="*80)
        
        # Count results
        passed = sum(1 for r in self.validation_results if r['status'] == 'PASS')
        failed = sum(1 for r in self.validation_results if r['status'] == 'FAIL')
        total = len(self.validation_results)
        
        # Create results table
        table = Table(title="Field Validation Results", box=box.ROUNDED)
        table.add_column("Field", style="cyan")
        table.add_column("Description", style="white")
        table.add_column("Status", style="green")
        table.add_column("Error", style="red")
        
        for result in self.validation_results:
            status_icon = "✅" if result['status'] == 'PASS' else "❌"
            error_msg = result.get('error', '')
            
            table.add_row(
                result['field'],
                result['description'],
                f"{status_icon} {result['status']}",
                error_msg
            )
        
        console.print(table)
        
        # Summary
        success_rate = (passed / total * 100) if total > 0 else 0
        
        summary_panel = Panel(
            f"Total Fields: {total}\n"
            f"Passed: {passed} ✅\n"
            f"Failed: {failed} ❌\n"
            f"Success Rate: {success_rate:.1f}%",
            title="[bold blue]Validation Summary[/bold blue]",
            border_style="blue"
        )
        
        console.print(summary_panel)
        
        # Final verdict
        if success_rate >= 95:
            console.print("\n[bold green]🎉 Excellent! All APIs are properly structured.[/bold green]")
        elif success_rate >= 80:
            console.print("\n[bold yellow]⚠️  Good! Most APIs are working, minor issues to address.[/bold yellow]")
        else:
            console.print("\n[bold red]❌ Issues detected! Please review and fix failing validations.[/bold red]")
        
        console.print("\n" + "="*80)

def main():
    """Main validation runner"""
    try:
        validator = APIValidator()
        validator.validate_all_apis()
        
    except KeyboardInterrupt:
        console.print("\n[yellow]⚠️  Validation interrupted by user[/yellow]")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n[red]❌ Validation runner failed: {e}[/red]")
        sys.exit(1)

if __name__ == '__main__':
    main() 