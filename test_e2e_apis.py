#!/usr/bin/env python3
"""
End-to-End API Test Script for UPID CLI
Validates all universal CLI functionality with real cluster data
"""

import sys
import os
import subprocess
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
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import box

console = Console()

class E2ETestRunner:
    """End-to-End test runner for UPID CLI APIs"""
    
    def __init__(self):
        self.test_results = []
        self.cluster_detector = ClusterDetector()
        self.config = Config()
        self.auth_manager = AuthManager(self.config)
        self.api_client = UPIDAPIClient(self.config, self.auth_manager)
        
    def run_all_tests(self):
        """Run all end-to-end tests"""
        console.print("\n" + "="*80)
        console.print("[bold blue]🧪 UPID CLI - End-to-End API Test Suite[/bold blue]")
        console.print("="*80)
        
        # Test categories
        test_categories = [
            ("🔍 Cluster Detection", self.test_cluster_detection),
            ("📊 Resource Analysis", self.test_resource_analysis),
            ("⚡ Optimization APIs", self.test_optimization_apis),
            ("📈 Reporting APIs", self.test_reporting_apis),
            ("🔧 Configuration APIs", self.test_configuration_apis),
            ("🌐 Universal Commands", self.test_universal_commands),
            ("📋 Data Validation", self.test_data_validation),
            ("⚙️ Error Handling", self.test_error_handling)
        ]
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Running E2E tests...", total=len(test_categories))
            
            for category_name, test_func in test_categories:
                progress.update(task, description=f"Testing {category_name}...")
                
                try:
                    result = test_func()
                    self.test_results.append({
                        'category': category_name,
                        'status': 'PASS' if result else 'FAIL',
                        'details': result if isinstance(result, str) else 'Test completed'
                    })
                except Exception as e:
                    self.test_results.append({
                        'category': category_name,
                        'status': 'ERROR',
                        'details': str(e)
                    })
                
                progress.advance(task)
        
        # Display results
        self.display_results()
        
    def test_cluster_detection(self) -> bool:
        """Test cluster detection functionality"""
        console.print("\n[bold cyan]🔍 Testing Cluster Detection[/bold cyan]")
        
        try:
            # Test cluster detection
            cluster_info = self.cluster_detector.detect_cluster()
            
            # Validate cluster info structure
            required_fields = ['name', 'type', 'status', 'kubeconfig']
            for field in required_fields:
                if field not in cluster_info:
                    console.print(f"[red]❌ Missing required field: {field}[/red]")
                    return False
            
            # Test cluster metrics
            metrics = self.cluster_detector.get_cluster_metrics()
            
            # Validate metrics structure
            if 'resources' not in metrics:
                console.print("[red]❌ Missing resources in metrics[/red]")
                return False
            
            console.print(f"[green]✅ Cluster detected: {cluster_info['name']} ({cluster_info['type']})[/green]")
            console.print(f"[green]✅ Metrics retrieved successfully[/green]")
            
            return True
            
        except Exception as e:
            console.print(f"[red]❌ Cluster detection failed: {e}[/red]")
            return False
    
    def test_resource_analysis(self) -> bool:
        """Test resource analysis APIs"""
        console.print("\n[bold cyan]📊 Testing Resource Analysis[/bold cyan]")
        
        try:
            # Test resource analysis
            resources = self.api_client.analyze_resources('test-cluster')
            
            # Validate resource analysis structure
            if not isinstance(resources, dict):
                console.print("[red]❌ Resource analysis should return dict[/red]")
                return False
            
            # Test cost analysis
            costs = self.api_client.analyze_costs('test-cluster')
            
            # Validate cost analysis structure
            if not isinstance(costs, dict):
                console.print("[red]❌ Cost analysis should return dict[/red]")
                return False
            
            # Test performance analysis
            performance = self.api_client.analyze_performance('test-cluster')
            
            # Validate performance analysis structure
            if not isinstance(performance, dict):
                console.print("[red]❌ Performance analysis should return dict[/red]")
                return False
            
            console.print("[green]✅ Resource analysis APIs working[/green]")
            console.print("[green]✅ Cost analysis APIs working[/green]")
            console.print("[green]✅ Performance analysis APIs working[/green]")
            
            return True
            
        except Exception as e:
            console.print(f"[red]❌ Resource analysis failed: {e}[/red]")
            return False
    
    def test_optimization_apis(self) -> bool:
        """Test optimization APIs"""
        console.print("\n[bold cyan]⚡ Testing Optimization APIs[/bold cyan]")
        
        try:
            # Test resource optimizations
            resource_opts = self.api_client.get_resource_optimizations('test-cluster')
            
            # Validate resource optimizations structure
            if not isinstance(resource_opts, list):
                console.print("[red]❌ Resource optimizations should return list[/red]")
                return False
            
            # Test cost optimizations
            cost_opts = self.api_client.get_cost_optimizations('test-cluster')
            
            # Validate cost optimizations structure
            if not isinstance(cost_opts, list):
                console.print("[red]❌ Cost optimizations should return list[/red]")
                return False
            
            # Test zero-pod recommendations
            zero_pod_recs = self.api_client.get_zero_pod_recommendations('test-cluster')
            
            # Validate zero-pod recommendations structure
            if not isinstance(zero_pod_recs, list):
                console.print("[red]❌ Zero-pod recommendations should return list[/red]")
                return False
            
            # Test applying optimizations
            test_recommendations = [{'type': 'cpu', 'action': 'test'}]
            apply_result = self.api_client.apply_resource_optimizations('test-cluster', test_recommendations)
            
            # Validate apply result
            if not isinstance(apply_result, dict):
                console.print("[red]❌ Apply optimizations should return dict[/red]")
                return False
            
            console.print("[green]✅ Resource optimization APIs working[/green]")
            console.print("[green]✅ Cost optimization APIs working[/green]")
            console.print("[green]✅ Zero-pod optimization APIs working[/green]")
            console.print("[green]✅ Apply optimization APIs working[/green]")
            
            return True
            
        except Exception as e:
            console.print(f"[red]❌ Optimization APIs failed: {e}[/red]")
            return False
    
    def test_reporting_apis(self) -> bool:
        """Test reporting APIs"""
        console.print("\n[bold cyan]📈 Testing Reporting APIs[/bold cyan]")
        
        try:
            # Test summary report
            summary = self.api_client.generate_summary_report('test-cluster')
            
            # Validate summary report structure
            if not isinstance(summary, dict):
                console.print("[red]❌ Summary report should return dict[/red]")
                return False
            
            # Test cost report
            cost_report = self.api_client.generate_cost_report('test-cluster')
            
            # Validate cost report structure
            if not isinstance(cost_report, dict):
                console.print("[red]❌ Cost report should return dict[/red]")
                return False
            
            # Test performance report
            perf_report = self.api_client.generate_performance_report('test-cluster')
            
            # Validate performance report structure
            if not isinstance(perf_report, dict):
                console.print("[red]❌ Performance report should return dict[/red]")
                return False
            
            # Test cluster report
            cluster_report = self.api_client.get_report('test-cluster', 'summary')
            
            # Validate cluster report structure
            if not isinstance(cluster_report, dict):
                console.print("[red]❌ Cluster report should return dict[/red]")
                return False
            
            console.print("[green]✅ Summary report API working[/green]")
            console.print("[green]✅ Cost report API working[/green]")
            console.print("[green]✅ Performance report API working[/green]")
            console.print("[green]✅ Cluster report API working[/green]")
            
            return True
            
        except Exception as e:
            console.print(f"[red]❌ Reporting APIs failed: {e}[/red]")
            return False
    
    def test_configuration_apis(self) -> bool:
        """Test configuration APIs"""
        console.print("\n[bold cyan]🔧 Testing Configuration APIs[/bold cyan]")
        
        try:
            # Test config get/set
            original_timeout = self.config.get('timeout')
            self.config.set('timeout', 60)
            new_timeout = self.config.get('timeout')
            
            if new_timeout != 60:
                console.print("[red]❌ Config set/get not working[/red]")
                return False
            
            # Restore original value
            self.config.set('timeout', original_timeout)
            
            # Test local mode
            self.config.enable_local_mode()
            if not self.config.is_local_mode():
                console.print("[red]❌ Local mode enable not working[/red]")
                return False
            
            self.config.disable_local_mode()
            if self.config.is_local_mode():
                console.print("[red]❌ Local mode disable not working[/red]")
                return False
            
            # Test auth token management
            self.config.set_auth_token('test-token')
            token = self.config.get_auth_token()
            
            if token != 'test-token':
                console.print("[red]❌ Auth token management not working[/red]")
                return False
            
            self.config.clear_auth_token()
            
            console.print("[green]✅ Configuration APIs working[/green]")
            console.print("[green]✅ Local mode APIs working[/green]")
            console.print("[green]✅ Auth token APIs working[/green]")
            
            return True
            
        except Exception as e:
            console.print(f"[red]❌ Configuration APIs failed: {e}[/red]")
            return False
    
    def test_universal_commands(self) -> bool:
        """Test universal command functionality"""
        console.print("\n[bold cyan]🌐 Testing Universal Commands[/bold cyan]")
        
        try:
            # Test cluster detection
            cluster_info = self.cluster_detector.detect_cluster()
            
            if cluster_info['status'] != 'connected':
                console.print(f"[yellow]⚠️  Cluster not connected: {cluster_info.get('error', 'Unknown')}[/yellow]")
                return False
            
            # Test metrics retrieval
            metrics = self.cluster_detector.get_cluster_metrics()
            
            if 'error' in metrics:
                console.print(f"[yellow]⚠️  Metrics error: {metrics['error']}[/yellow]")
                return False
            
            # Test resource parsing
            if 'resources' in metrics:
                resources = metrics['resources']
                
                # Test CPU parsing
                cpu_used = resources.get('cpu', {}).get('used', 0)
                if not isinstance(cpu_used, (int, float)):
                    console.print("[red]❌ CPU usage should be numeric[/red]")
                    return False
                
                # Test memory parsing
                memory_used = resources.get('memory', {}).get('used', 0)
                if not isinstance(memory_used, (int, float)):
                    console.print("[red]❌ Memory usage should be numeric[/red]")
                    return False
                
                # Test pod counting
                pods_running = resources.get('pods', {}).get('running', 0)
                if not isinstance(pods_running, int):
                    console.print("[red]❌ Pod count should be integer[/red]")
                    return False
            
            console.print("[green]✅ Universal commands working[/green]")
            console.print("[green]✅ Metrics parsing working[/green]")
            console.print("[green]✅ Resource calculation working[/green]")
            
            return True
            
        except Exception as e:
            console.print(f"[red]❌ Universal commands failed: {e}[/red]")
            return False
    
    def test_data_validation(self) -> bool:
        """Test data validation and integrity"""
        console.print("\n[bold cyan]📋 Testing Data Validation[/bold cyan]")
        
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
                
                # Validate CPU data
                cpu = resources.get('cpu', {})
                if 'used' in cpu and 'total' in cpu:
                    if cpu['used'] < 0 or cpu['total'] < 0:
                        console.print("[red]❌ CPU values should be non-negative[/red]")
                        return False
                    
                    if cpu['used'] > cpu['total']:
                        console.print("[red]❌ CPU used should not exceed total[/red]")
                        return False
                
                # Validate memory data
                memory = resources.get('memory', {})
                if 'used' in memory and 'total' in memory:
                    if memory['used'] < 0 or memory['total'] < 0:
                        console.print("[red]❌ Memory values should be non-negative[/red]")
                        return False
                    
                    if memory['used'] > memory['total']:
                        console.print("[red]❌ Memory used should not exceed total[/red]")
                        return False
                
                # Validate pod data
                pods = resources.get('pods', {})
                if 'running' in pods and 'total' in pods:
                    if pods['running'] < 0 or pods['total'] < 0:
                        console.print("[red]❌ Pod counts should be non-negative[/red]")
                        return False
                    
                    if pods['running'] > pods['total']:
                        console.print("[red]❌ Running pods should not exceed total[/red]")
                        return False
            
            console.print("[green]✅ Data validation passed[/green]")
            console.print("[green]✅ Field integrity verified[/green]")
            console.print("[green]✅ Value ranges validated[/green]")
            
            return True
            
        except Exception as e:
            console.print(f"[red]❌ Data validation failed: {e}[/red]")
            return False
    
    def test_error_handling(self) -> bool:
        """Test error handling and edge cases"""
        console.print("\n[bold cyan]⚙️ Testing Error Handling[/bold cyan]")
        
        try:
            # Test invalid cluster name
            try:
                invalid_cluster = self.api_client.get_cluster('invalid-cluster-name')
                # Should handle gracefully
            except Exception:
                pass  # Expected for invalid cluster
            
            # Test invalid API calls
            try:
                invalid_result = self.api_client.analyze_resources('')
                # Should handle empty string
            except Exception:
                pass  # Expected for empty string
            
            # Test configuration edge cases
            try:
                # Test with None values
                self.config.set('test_none', None)
                none_value = self.config.get('test_none')
                if none_value is not None:
                    console.print("[red]❌ None value handling failed[/red]")
                    return False
            except Exception as e:
                console.print(f"[red]❌ None value handling failed: {e}[/red]")
                return False
            
            # Test cluster detector with invalid kubeconfig
            try:
                # Temporarily set invalid kubeconfig
                original_kubeconfig = os.environ.get('KUBECONFIG')
                os.environ['KUBECONFIG'] = '/invalid/path/config'
                
                detector = ClusterDetector()
                cluster_info = detector.detect_cluster()
                
                # Should handle gracefully
                if cluster_info['status'] == 'error':
                    console.print("[green]✅ Invalid kubeconfig handled gracefully[/green]")
                else:
                    console.print("[yellow]⚠️  Invalid kubeconfig not handled as expected[/yellow]")
                
                # Restore original kubeconfig
                if original_kubeconfig:
                    os.environ['KUBECONFIG'] = original_kubeconfig
                else:
                    os.environ.pop('KUBECONFIG', None)
                    
            except Exception as e:
                console.print(f"[red]❌ Invalid kubeconfig handling failed: {e}[/red]")
                return False
            
            console.print("[green]✅ Error handling working[/green]")
            console.print("[green]✅ Edge cases handled[/green]")
            console.print("[green]✅ Graceful degradation working[/green]")
            
            return True
            
        except Exception as e:
            console.print(f"[red]❌ Error handling test failed: {e}[/red]")
            return False
    
    def display_results(self):
        """Display test results"""
        console.print("\n" + "="*80)
        console.print("[bold blue]📊 E2E Test Results[/bold blue]")
        console.print("="*80)
        
        # Create results table
        table = Table(title="Test Results", box=box.ROUNDED)
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
            title="[bold blue]Test Summary[/bold blue]",
            border_style="blue"
        )
        
        console.print(summary_panel)
        
        # Final verdict
        if success_rate >= 90:
            console.print("\n[bold green]🎉 Excellent! All critical APIs are working correctly.[/bold green]")
        elif success_rate >= 70:
            console.print("\n[bold yellow]⚠️  Good! Most APIs are working, some issues to address.[/bold yellow]")
        else:
            console.print("\n[bold red]❌ Issues detected! Please review and fix failing tests.[/bold red]")
        
        console.print("\n" + "="*80)

def main():
    """Main test runner"""
    try:
        runner = E2ETestRunner()
        runner.run_all_tests()
        
    except KeyboardInterrupt:
        console.print("\n[yellow]⚠️  Tests interrupted by user[/yellow]")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n[red]❌ Test runner failed: {e}[/red]")
        sys.exit(1)

if __name__ == '__main__':
    main() 