#!/usr/bin/env python3
"""
Local Mode API Test Script for UPID CLI
Validates all APIs in local mode without requiring real API endpoints
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

class LocalModeAPITester:
    """Local mode API tester for UPID CLI"""
    
    def __init__(self):
        # Enable local mode
        self.config = Config()
        self.config.enable_local_mode()
        
        self.auth_manager = AuthManager(self.config)
        self.api_client = UPIDAPIClient(self.config, self.auth_manager)
        self.cluster_detector = ClusterDetector()
        self.test_results = []
        
    def test_all_local_apis(self):
        """Test all APIs in local mode"""
        console.print("\n" + "="*80)
        console.print("[bold blue]🧪 UPID CLI - Local Mode API Test Suite[/bold blue]")
        console.print("="*80)
        
        # Test categories for local mode
        test_categories = [
            ("🔍 Cluster Detection", self.test_cluster_detection),
            ("📊 Resource Analysis", self.test_resource_analysis),
            ("⚡ Optimization APIs", self.test_optimization_apis),
            ("📈 Reporting APIs", self.test_reporting_apis),
            ("🔧 Configuration APIs", self.test_configuration_apis),
            ("🔐 Authentication APIs", self.test_authentication_apis),
            ("📋 Data Validation", self.test_data_validation),
            ("⚙️ Local Mode Features", self.test_local_mode_features)
        ]
        
        for category_name, test_func in test_categories:
            console.print(f"\n[bold cyan]{category_name}[/bold cyan]")
            try:
                result = test_func()
                self.test_results.append({
                    'category': category_name,
                    'status': 'PASS' if result else 'FAIL',
                    'details': 'Test completed successfully' if result else 'Test failed'
                })
            except Exception as e:
                self.test_results.append({
                    'category': category_name,
                    'status': 'ERROR',
                    'details': str(e)
                })
        
        # Display results
        self.display_results()
        
    def test_cluster_detection(self) -> bool:
        """Test cluster detection in local mode"""
        try:
            # Test cluster detection
            cluster_info = self.cluster_detector.detect_cluster()
            
            # Validate basic structure
            required_fields = ['name', 'type', 'status', 'kubeconfig']
            for field in required_fields:
                if field not in cluster_info:
                    console.print(f"[red]❌ Missing field: {field}[/red]")
                    return False
            
            # Test metrics retrieval
            metrics = self.cluster_detector.get_cluster_metrics()
            
            # Validate metrics structure
            if 'resources' not in metrics:
                console.print("[red]❌ Missing resources in metrics[/red]")
                return False
            
            console.print(f"[green]✅ Cluster: {cluster_info['name']} ({cluster_info['type']})[/green]")
            console.print(f"[green]✅ Metrics: {len(metrics.get('resources', {}))} resource types[/green]")
            
            return True
            
        except Exception as e:
            console.print(f"[red]❌ Cluster detection failed: {e}[/red]")
            return False
    
    def test_resource_analysis(self) -> bool:
        """Test resource analysis APIs in local mode"""
        try:
            # Test resource analysis
            resources = self.api_client.analyze_resources('local-cluster')
            
            # Validate structure
            if not isinstance(resources, dict):
                console.print("[red]❌ Resource analysis should return dict[/red]")
                return False
            
            # Check for expected fields
            expected_fields = ['cpu', 'memory', 'storage']
            for field in expected_fields:
                if field in resources:
                    console.print(f"[green]✅ {field.title()} analysis available[/green]")
            
            # Test cost analysis
            costs = self.api_client.analyze_costs('local-cluster')
            
            if not isinstance(costs, dict):
                console.print("[red]❌ Cost analysis should return dict[/red]")
                return False
            
            # Test performance analysis
            performance = self.api_client.analyze_performance('local-cluster')
            
            if not isinstance(performance, dict):
                console.print("[red]❌ Performance analysis should return dict[/red]")
                return False
            
            console.print("[green]✅ All resource analysis APIs working[/green]")
            return True
            
        except Exception as e:
            console.print(f"[red]❌ Resource analysis failed: {e}[/red]")
            return False
    
    def test_optimization_apis(self) -> bool:
        """Test optimization APIs in local mode"""
        try:
            # Test resource optimizations
            resource_opts = self.api_client.get_resource_optimizations('local-cluster')
            
            if not isinstance(resource_opts, list):
                console.print("[red]❌ Resource optimizations should return list[/red]")
                return False
            
            console.print(f"[green]✅ Found {len(resource_opts)} resource optimizations[/green]")
            
            # Test cost optimizations
            cost_opts = self.api_client.get_cost_optimizations('local-cluster')
            
            if not isinstance(cost_opts, list):
                console.print("[red]❌ Cost optimizations should return list[/red]")
                return False
            
            console.print(f"[green]✅ Found {len(cost_opts)} cost optimizations[/green]")
            
            # Test zero-pod recommendations
            zero_pod_recs = self.api_client.get_zero_pod_recommendations('local-cluster')
            
            if not isinstance(zero_pod_recs, list):
                console.print("[red]❌ Zero-pod recommendations should return list[/red]")
                return False
            
            console.print(f"[green]✅ Found {len(zero_pod_recs)} zero-pod recommendations[/green]")
            
            # Test applying optimizations
            test_recommendations = [{'type': 'cpu', 'action': 'test'}]
            apply_result = self.api_client.apply_resource_optimizations('local-cluster', test_recommendations)
            
            if not isinstance(apply_result, dict):
                console.print("[red]❌ Apply optimizations should return dict[/red]")
                return False
            
            console.print("[green]✅ Apply optimization API working[/green]")
            return True
            
        except Exception as e:
            console.print(f"[red]❌ Optimization APIs failed: {e}[/red]")
            return False
    
    def test_reporting_apis(self) -> bool:
        """Test reporting APIs in local mode"""
        try:
            # Test summary report
            summary = self.api_client.generate_summary_report('local-cluster')
            
            if not isinstance(summary, dict):
                console.print("[red]❌ Summary report should return dict[/red]")
                return False
            
            # Check for expected fields
            expected_fields = ['cluster_name', 'generated_at', 'resources', 'costs', 'performance']
            for field in expected_fields:
                if field in summary:
                    console.print(f"[green]✅ {field.replace('_', ' ').title()} in summary[/green]")
            
            # Test cost report
            cost_report = self.api_client.generate_cost_report('local-cluster')
            
            if not isinstance(cost_report, dict):
                console.print("[red]❌ Cost report should return dict[/red]")
                return False
            
            # Test performance report
            perf_report = self.api_client.generate_performance_report('local-cluster')
            
            if not isinstance(perf_report, dict):
                console.print("[red]❌ Performance report should return dict[/red]")
                return False
            
            console.print("[green]✅ All reporting APIs working[/green]")
            return True
            
        except Exception as e:
            console.print(f"[red]❌ Reporting APIs failed: {e}[/red]")
            return False
    
    def test_configuration_apis(self) -> bool:
        """Test configuration APIs"""
        try:
            # Test config get/set
            original_timeout = self.config.get('timeout')
            test_timeout = 60
            
            self.config.set('timeout', test_timeout)
            retrieved_timeout = self.config.get('timeout')
            
            if retrieved_timeout != test_timeout:
                console.print(f"[red]❌ Config set/get failed: expected {test_timeout}, got {retrieved_timeout}[/red]")
                return False
            
            # Restore original value
            self.config.set('timeout', original_timeout)
            
            # Test local mode
            self.config.enable_local_mode()
            if not self.config.is_local_mode():
                console.print("[red]❌ Local mode enable failed[/red]")
                return False
            
            self.config.disable_local_mode()
            if self.config.is_local_mode():
                console.print("[red]❌ Local mode disable failed[/red]")
                return False
            
            # Re-enable for testing
            self.config.enable_local_mode()
            
            console.print("[green]✅ Configuration APIs working[/green]")
            return True
            
        except Exception as e:
            console.print(f"[red]❌ Configuration APIs failed: {e}[/red]")
            return False
    
    def test_authentication_apis(self) -> bool:
        """Test authentication APIs in local mode"""
        try:
            # Test login (local mode)
            login_result = self.api_client.login('test@example.com', 'password')
            
            if not isinstance(login_result, dict):
                console.print("[red]❌ Login should return dict[/red]")
                return False
            
            # Check for expected fields
            if 'token' in login_result:
                console.print("[green]✅ Login token generated[/green]")
            
            if 'user' in login_result:
                console.print("[green]✅ User info returned[/green]")
            
            # Test get profile
            profile = self.api_client.get_profile()
            
            if not isinstance(profile, dict):
                console.print("[red]❌ Profile should return dict[/red]")
                return False
            
            # Test get current user
            current_user = self.api_client.get_current_user()
            
            if not isinstance(current_user, dict):
                console.print("[red]❌ Current user should return dict[/red]")
                return False
            
            # Test logout
            logout_result = self.api_client.logout()
            
            if not isinstance(logout_result, dict):
                console.print("[red]❌ Logout should return dict[/red]")
                return False
            
            console.print("[green]✅ All authentication APIs working[/green]")
            return True
            
        except Exception as e:
            console.print(f"[red]❌ Authentication APIs failed: {e}[/red]")
            return False
    
    def test_data_validation(self) -> bool:
        """Test data validation in local mode"""
        try:
            # Test cluster info validation
            cluster_info = self.cluster_detector.detect_cluster()
            
            # Validate required fields
            required_fields = ['name', 'type', 'status', 'kubeconfig']
            for field in required_fields:
                if field not in cluster_info:
                    console.print(f"[red]❌ Missing required field: {field}[/red]")
                    return False
                
                if cluster_info[field] is None:
                    console.print(f"[red]❌ Field {field} should not be None[/red]")
                    return False
            
            # Test metrics validation
            metrics = self.cluster_detector.get_cluster_metrics()
            
            if 'resources' in metrics:
                resources = metrics['resources']
                
                # Validate CPU data types and ranges
                if 'cpu' in resources:
                    cpu = resources['cpu']
                    if not isinstance(cpu.get('used', 0), (int, float)):
                        console.print("[red]❌ CPU used should be numeric[/red]")
                        return False
                    if not isinstance(cpu.get('total', 0), (int, float)):
                        console.print("[red]❌ CPU total should be numeric[/red]")
                        return False
                    if cpu.get('used', 0) < 0:
                        console.print("[red]❌ CPU used should be non-negative[/red]")
                        return False
                    if cpu.get('total', 0) < 0:
                        console.print("[red]❌ CPU total should be non-negative[/red]")
                        return False
                
                # Validate memory data types and ranges
                if 'memory' in resources:
                    memory = resources['memory']
                    if not isinstance(memory.get('used', 0), (int, float)):
                        console.print("[red]❌ Memory used should be numeric[/red]")
                        return False
                    if not isinstance(memory.get('total', 0), (int, float)):
                        console.print("[red]❌ Memory total should be numeric[/red]")
                        return False
                    if memory.get('used', 0) < 0:
                        console.print("[red]❌ Memory used should be non-negative[/red]")
                        return False
                    if memory.get('total', 0) < 0:
                        console.print("[red]❌ Memory total should be non-negative[/red]")
                        return False
                
                # Validate pod data types and ranges
                if 'pods' in resources:
                    pods = resources['pods']
                    if not isinstance(pods.get('running', 0), int):
                        console.print("[red]❌ Running pods should be integer[/red]")
                        return False
                    if not isinstance(pods.get('total', 0), int):
                        console.print("[red]❌ Total pods should be integer[/red]")
                        return False
                    if pods.get('running', 0) < 0:
                        console.print("[red]❌ Running pods should be non-negative[/red]")
                        return False
                    if pods.get('total', 0) < 0:
                        console.print("[red]❌ Total pods should be non-negative[/red]")
                        return False
            
            console.print("[green]✅ Data validation passed[/green]")
            return True
            
        except Exception as e:
            console.print(f"[red]❌ Data validation failed: {e}[/red]")
            return False
    
    def test_local_mode_features(self) -> bool:
        """Test local mode specific features"""
        try:
            # Test that local mode is enabled
            if not self.config.is_local_mode():
                console.print("[red]❌ Local mode should be enabled[/red]")
                return False
            
            # Test local cluster detection
            clusters = self.api_client.get_clusters()
            
            if not isinstance(clusters, list):
                console.print("[red]❌ Get clusters should return list[/red]")
                return False
            
            if clusters:
                cluster = clusters[0]
                if cluster.get('platform') != 'local':
                    console.print("[red]❌ Local cluster should have platform 'local'[/red]")
                    return False
                
                console.print(f"[green]✅ Local cluster detected: {cluster.get('name')}[/green]")
            
            # Test local cluster info
            cluster_info = self.api_client.get_cluster('local-cluster')
            
            if not isinstance(cluster_info, dict):
                console.print("[red]❌ Get cluster should return dict[/red]")
                return False
            
            # Test local cluster analysis
            analysis = self.api_client.analyze_cluster('local-cluster')
            
            if not isinstance(analysis, dict):
                console.print("[red]❌ Analyze cluster should return dict[/red]")
                return False
            
            # Test local optimization
            optimization = self.api_client.optimize_cluster('local-cluster', {})
            
            if not isinstance(optimization, dict):
                console.print("[red]❌ Optimize cluster should return dict[/red]")
                return False
            
            console.print("[green]✅ All local mode features working[/green]")
            return True
            
        except Exception as e:
            console.print(f"[red]❌ Local mode features failed: {e}[/red]")
            return False
    
    def display_results(self):
        """Display test results"""
        console.print("\n" + "="*80)
        console.print("[bold blue]📊 Local Mode API Test Results[/bold blue]")
        console.print("="*80)
        
        # Create results table
        table = Table(title="Local Mode Test Results", box=box.ROUNDED)
        table.add_column("Category", style="cyan", no_wrap=True)
        table.add_column("Status", style="green")
        table.add_column("Details", style="white")
        
        passed = 0
        failed = 0
        errors = 0
        
        for result in self.test_results:
            status_style = "green" if result['status'] == 'PASS' else "red"
            status_icon = "✅" if result['status'] == 'PASS' else "❌"
            
            table.add_row(
                result['category'],
                f"{status_icon} {result['status']}",
                result['details']
            )
            
            if result['status'] == 'PASS':
                passed += 1
            elif result['status'] == 'FAIL':
                failed += 1
            else:
                errors += 1
        
        console.print(table)
        
        # Summary
        total_tests = len(self.test_results)
        success_rate = (passed / total_tests * 100) if total_tests > 0 else 0
        
        summary_panel = Panel(
            f"Total Tests: {total_tests}\n"
            f"Passed: {passed} ✅\n"
            f"Failed: {failed} ❌\n"
            f"Errors: {errors} ⚠️\n"
            f"Success Rate: {success_rate:.1f}%",
            title="[bold blue]Local Mode Test Summary[/bold blue]",
            border_style="blue"
        )
        
        console.print(summary_panel)
        
        # Final verdict
        if success_rate >= 90:
            console.print("\n[bold green]🎉 Excellent! All local mode APIs are working correctly.[/bold green]")
        elif success_rate >= 70:
            console.print("\n[bold yellow]⚠️  Good! Most local mode APIs are working, some issues to address.[/bold yellow]")
        else:
            console.print("\n[bold red]❌ Issues detected! Please review and fix failing tests.[/bold red]")
        
        console.print("\n" + "="*80)

def main():
    """Main local mode test runner"""
    try:
        tester = LocalModeAPITester()
        tester.test_all_local_apis()
        
    except KeyboardInterrupt:
        console.print("\n[yellow]⚠️  Local mode tests interrupted by user[/yellow]")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n[red]❌ Local mode test runner failed: {e}[/red]")
        sys.exit(1)

if __name__ == '__main__':
    main() 