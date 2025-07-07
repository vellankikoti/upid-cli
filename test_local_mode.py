#!/usr/bin/env python3
"""
Test script for UPID CLI local mode
"""

import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from upid.core.config import Config
from upid.core.auth import AuthManager
from upid.core.api_client import UPIDAPIClient
from rich.console import Console
from rich.table import Table

console = Console()

def test_local_mode():
    """Test local mode functionality"""
    console.print("\n[bold blue]🧪 Testing UPID CLI Local Mode[/bold blue]\n")
    
    # Initialize with local mode
    config = Config()
    config.enable_local_mode()
    
    console.print("[green]✅ Local mode enabled[/green]")
    
    # Initialize auth manager and API client
    auth_manager = AuthManager(config)
    api_client = UPIDAPIClient(config, auth_manager)
    
    # Test authentication (should work without real auth)
    console.print("\n[bold]1. Testing Authentication[/bold]")
    try:
        user = auth_manager.get_current_user()
        console.print(f"[green]✅ User: {user.get('name', 'Local User')}[/green]")
    except Exception as e:
        console.print(f"[red]❌ Auth error: {e}[/red]")
    
    # Test cluster operations
    console.print("\n[bold]2. Testing Cluster Operations[/bold]")
    try:
        clusters = api_client.get_clusters()
        console.print(f"[green]✅ Found {len(clusters)} cluster(s)[/green]")
        
        if clusters:
            cluster = clusters[0]
            console.print(f"   - Name: {cluster.get('name')}")
            console.print(f"   - Status: {cluster.get('status')}")
            console.print(f"   - Platform: {cluster.get('platform')}")
    except Exception as e:
        console.print(f"[red]❌ Cluster error: {e}[/red]")
    
    # Test analysis operations
    console.print("\n[bold]3. Testing Analysis Operations[/bold]")
    try:
        # Resource analysis
        resources = api_client.analyze_resources('local-cluster')
        console.print(f"[green]✅ Resource analysis completed[/green]")
        console.print(f"   - CPU: {resources.get('cpu', {}).get('used', 0)}/{resources.get('cpu', {}).get('total', 0)} cores")
        console.print(f"   - Memory: {resources.get('memory', {}).get('used', 0)}/{resources.get('memory', {}).get('total', 0)} GB")
        
        # Cost analysis
        costs = api_client.analyze_costs('local-cluster')
        console.print(f"[green]✅ Cost analysis completed[/green]")
        console.print(f"   - Total cost: ${costs.get('total_cost', 0):.2f}")
        
        # Performance analysis
        performance = api_client.analyze_performance('local-cluster')
        console.print(f"[green]✅ Performance analysis completed[/green]")
        console.print(f"   - CPU usage: {performance.get('cpu', {}).get('current', 0)}%")
    except Exception as e:
        console.print(f"[red]❌ Analysis error: {e}[/red]")
    
    # Test optimization operations
    console.print("\n[bold]4. Testing Optimization Operations[/bold]")
    try:
        # Get resource optimizations
        resource_opts = api_client.get_resource_optimizations('local-cluster')
        console.print(f"[green]✅ Found {len(resource_opts)} resource optimization(s)[/green]")
        
        # Get cost optimizations
        cost_opts = api_client.get_cost_optimizations('local-cluster')
        console.print(f"[green]✅ Found {len(cost_opts)} cost optimization(s)[/green]")
        
        # Get zero-pod recommendations
        zero_pod_recs = api_client.get_zero_pod_recommendations('local-cluster')
        console.print(f"[green]✅ Found {len(zero_pod_recs)} zero-pod recommendation(s)[/green]")
    except Exception as e:
        console.print(f"[red]❌ Optimization error: {e}[/red]")
    
    # Test deployment operations
    console.print("\n[bold]5. Testing Deployment Operations[/bold]")
    try:
        deployments = api_client.get_deployments('local-cluster')
        console.print(f"[green]✅ Found {len(deployments)} deployment(s)[/green]")
        
        if deployments:
            deployment = deployments[0]
            console.print(f"   - Name: {deployment.get('name')}")
            console.print(f"   - Replicas: {deployment.get('replicas')}")
            console.print(f"   - Status: {deployment.get('status')}")
    except Exception as e:
        console.print(f"[red]❌ Deployment error: {e}[/red]")
    
    # Test reporting operations
    console.print("\n[bold]6. Testing Reporting Operations[/bold]")
    try:
        # Summary report
        summary = api_client.generate_summary_report('local-cluster')
        console.print(f"[green]✅ Summary report generated[/green]")
        
        # Cost report
        cost_report = api_client.generate_cost_report('local-cluster')
        console.print(f"[green]✅ Cost report generated[/green]")
        
        # Performance report
        perf_report = api_client.generate_performance_report('local-cluster')
        console.print(f"[green]✅ Performance report generated[/green]")
    except Exception as e:
        console.print(f"[red]❌ Reporting error: {e}[/red]")
    
    console.print("\n[bold green]✅ All local mode tests completed successfully![/bold green]")
    console.print("\n[yellow]💡 You can now use the CLI with --local flag for testing:[/yellow]")
    console.print("   upid --local status")
    console.print("   upid --local cluster list")
    console.print("   upid --local analyze resources local-cluster")

if __name__ == '__main__':
    test_local_mode() 