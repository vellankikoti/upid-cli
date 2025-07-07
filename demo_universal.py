#!/usr/bin/env python3
"""
Universal UPID CLI Demo
Shows how the CLI works with any Kubernetes cluster
"""

import sys
import subprocess
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from upid.core.cluster_detector import ClusterDetector
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

def demo_universal_cli():
    """Demo the universal CLI capabilities"""
    console.print("\n" + "="*70)
    console.print("[bold blue]🚀 UPID CLI - Universal Kubernetes Optimizer Demo[/bold blue]")
    console.print("="*70)
    
    console.print("\n[bold green]✨ Features:[/bold green]")
    console.print("• Works with ANY Kubernetes cluster")
    console.print("• Zero configuration required")
    console.print("• Auto-detects cluster type")
    console.print("• Real-time insights and optimizations")
    console.print("• Beautiful terminal UI")
    
    # Check if kubectl is available
    try:
        result = subprocess.run(['kubectl', 'version', '--client'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode != 0:
            console.print("\n[yellow]⚠️  kubectl not found. This demo will show simulated data.[/yellow]")
            demo_simulated_mode()
            return
    except FileNotFoundError:
        console.print("\n[yellow]⚠️  kubectl not found. This demo will show simulated data.[/yellow]")
        demo_simulated_mode()
        return
    
    # Check cluster connection
    try:
        result = subprocess.run(['kubectl', 'cluster-info'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode != 0:
            console.print("\n[yellow]⚠️  No Kubernetes cluster connected. Using simulated data.[/yellow]")
            demo_simulated_mode()
            return
    except Exception:
        console.print("\n[yellow]⚠️  Cannot connect to cluster. Using simulated data.[/yellow]")
        demo_simulated_mode()
        return
    
    # Real cluster demo
    demo_real_cluster()

def demo_simulated_mode():
    """Demo with simulated cluster data"""
    console.print("\n[bold cyan]🎭 Simulated Cluster Demo[/bold cyan]")
    
    # Simulated cluster info
    cluster_info = {
        'name': 'demo-cluster',
        'type': 'docker-desktop',
        'status': 'connected',
        'kubeconfig': '~/.kube/config',
        'capabilities': {
            'metrics_server': True,
            'prometheus': False,
            'grafana': False,
            'ingress': True,
            'load_balancer': True,
            'storage_class': True,
            'helm': True
        }
    }
    
    # Simulated metrics
    metrics = {
        'resources': {
            'cpu': {'used': 2.5, 'total': 4.0},
            'memory': {'used': 4.0, 'total': 8.0},
            'pods': {'running': 8, 'total': 10}
        }
    }
    
    display_cluster_info(cluster_info, metrics)
    display_analysis(cluster_info, metrics)
    display_optimizations(cluster_info, metrics)

def demo_real_cluster():
    """Demo with real cluster data"""
    console.print("\n[bold green]🔍 Real Cluster Demo[/bold green]")
    
    try:
        detector = ClusterDetector()
        cluster_info = detector.detect_cluster()
        metrics = detector.get_cluster_metrics()
        
        if cluster_info['status'] == 'connected':
            console.print(f"[green]✅ Connected to: {cluster_info['name']} ({cluster_info['type']})[/green]")
            display_cluster_info(cluster_info, metrics)
            display_analysis(cluster_info, metrics)
            display_optimizations(cluster_info, metrics)
        else:
            console.print(f"[red]❌ Cluster detection failed: {cluster_info.get('error', 'Unknown error')}[/red]")
            demo_simulated_mode()
            
    except Exception as e:
        console.print(f"[red]❌ Error accessing cluster: {e}[/red]")
        demo_simulated_mode()

def display_cluster_info(cluster_info, metrics):
    """Display cluster information"""
    console.print("\n[bold blue]📊 Cluster Information[/bold blue]")
    
    # Cluster details
    info_panel = Panel(
        f"[bold]Name:[/bold] {cluster_info['name']}\n"
        f"[bold]Type:[/bold] {cluster_info['type'].upper()}\n"
        f"[bold]Status:[/bold] {'✅ Connected' if cluster_info['status'] == 'connected' else '❌ Error'}\n"
        f"[bold]Kubeconfig:[/bold] {cluster_info['kubeconfig']}",
        title="[bold green]Cluster Details[/bold green]",
        border_style="green"
    )
    console.print(info_panel)
    
    # Capabilities
    capabilities = cluster_info.get('capabilities', {})
    cap_table = Table(title="Cluster Capabilities")
    cap_table.add_column("Capability", style="cyan")
    cap_table.add_column("Available", style="green")
    
    for cap, available in capabilities.items():
        status = "✅ Yes" if available else "❌ No"
        cap_table.add_row(cap.replace('_', ' ').title(), status)
    
    console.print(cap_table)
    
    # Resource usage
    if 'resources' in metrics and not metrics.get('error'):
        resources = metrics['resources']
        
        cpu_used = resources.get('cpu', {}).get('used', 0)
        cpu_total = resources.get('cpu', {}).get('total', 1)
        cpu_percent = (cpu_used / cpu_total * 100) if cpu_total > 0 else 0
        
        memory_used = resources.get('memory', {}).get('used', 0)
        memory_total = resources.get('memory', {}).get('total', 1)
        memory_percent = (memory_used / memory_total * 100) if memory_total > 0 else 0
        
        pods_running = resources.get('pods', {}).get('running', 0)
        pods_total = resources.get('pods', {}).get('total', 0)
        
        usage_table = Table(title="Resource Usage")
        usage_table.add_column("Resource", style="cyan")
        usage_table.add_column("Used", style="yellow")
        usage_table.add_column("Total", style="blue")
        usage_table.add_column("Usage %", style="green")
        
        usage_table.add_row(
            "CPU",
            f"{cpu_used:.1f} cores",
            f"{cpu_total:.1f} cores",
            f"{cpu_percent:.1f}%"
        )
        
        usage_table.add_row(
            "Memory",
            f"{memory_used / (1024**3):.1f} GB",
            f"{memory_total / (1024**3):.1f} GB",
            f"{memory_percent:.1f}%"
        )
        
        usage_table.add_row(
            "Pods",
            str(pods_running),
            str(pods_total),
            f"{(pods_running/pods_total*100):.1f}%" if pods_total > 0 else "0%"
        )
        
        console.print(usage_table)

def display_analysis(cluster_info, metrics):
    """Display cluster analysis"""
    console.print("\n[bold blue]🔍 Cluster Analysis[/bold blue]")
    
    insights = []
    
    if 'resources' in metrics and not metrics.get('error'):
        resources = metrics['resources']
        
        cpu_used = resources.get('cpu', {}).get('used', 0)
        cpu_total = resources.get('cpu', {}).get('total', 1)
        cpu_percent = (cpu_used / cpu_total * 100) if cpu_total > 0 else 0
        
        memory_used = resources.get('memory', {}).get('used', 0)
        memory_total = resources.get('memory', {}).get('total', 1)
        memory_percent = (memory_used / memory_total * 100) if memory_total > 0 else 0
        
        # Generate insights
        if cpu_percent < 30:
            insights.append("CPU usage is low - consider right-sizing workloads")
        elif cpu_percent > 80:
            insights.append("CPU usage is high - consider scaling up resources")
        
        if memory_percent < 30:
            insights.append("Memory usage is low - consider reducing memory allocations")
        elif memory_percent > 80:
            insights.append("Memory usage is high - consider adding more memory")
        
        cluster_type = cluster_info.get('type', 'unknown')
        if cluster_type in ['eks', 'aks', 'gke']:
            insights.append("Cloud cluster detected - consider cost optimization strategies")
        elif cluster_type == 'docker-desktop':
            insights.append("Docker Desktop detected - limited resources available")
    
    if insights:
        insights_panel = Panel(
            "\n".join([f"• {insight}" for insight in insights]),
            title="[bold blue]Insights & Recommendations[/bold blue]",
            border_style="blue"
        )
        console.print(insights_panel)
    else:
        console.print(Panel(
            "✅ Cluster appears to be well-optimized",
            title="[bold green]Analysis Complete[/bold green]",
            border_style="green"
        ))

def display_optimizations(cluster_info, metrics):
    """Display optimization recommendations"""
    console.print("\n[bold blue]⚡ Optimization Recommendations[/bold blue]")
    
    optimizations = []
    
    if 'resources' in metrics and not metrics.get('error'):
        resources = metrics['resources']
        
        cpu_used = resources.get('cpu', {}).get('used', 0)
        cpu_total = resources.get('cpu', {}).get('total', 1)
        cpu_percent = (cpu_used / cpu_total * 100) if cpu_total > 0 else 0
        
        memory_used = resources.get('memory', {}).get('used', 0)
        memory_total = resources.get('memory', {}).get('total', 1)
        memory_percent = (memory_used / memory_total * 100) if memory_total > 0 else 0
        
        # Resource optimizations
        if cpu_percent < 50:
            optimizations.append({
                'type': 'Resource',
                'action': 'Right-size CPU requests',
                'impact': 'Medium',
                'effort': 'Low'
            })
        
        if memory_percent < 50:
            optimizations.append({
                'type': 'Resource',
                'action': 'Right-size memory requests',
                'impact': 'Medium',
                'effort': 'Low'
            })
        
        # Cost optimizations for cloud clusters
        cluster_type = cluster_info.get('type', 'unknown')
        if cluster_type in ['eks', 'aks', 'gke']:
            optimizations.append({
                'type': 'Cost',
                'action': 'Use spot instances for non-critical workloads',
                'impact': 'High',
                'effort': 'Medium'
            })
    
    if optimizations:
        opt_table = Table(title="Optimization Opportunities")
        opt_table.add_column("Type", style="cyan")
        opt_table.add_column("Action", style="green")
        opt_table.add_column("Impact", style="yellow")
        opt_table.add_column("Effort", style="blue")
        
        for opt in optimizations:
            opt_table.add_row(
                opt['type'],
                opt['action'],
                opt['impact'],
                opt['effort']
            )
        
        console.print(opt_table)
    else:
        console.print(Panel(
            "✅ No optimization opportunities found",
            title="[bold green]Optimization Complete[/bold green]",
            border_style="green"
        ))

def show_usage_commands():
    """Show usage commands"""
    console.print("\n[bold blue]💡 Usage Commands:[/bold blue]")
    console.print("\n📊 Basic Commands:")
    console.print("  upid universal status          # Show cluster health")
    console.print("  upid universal analyze         # Analyze resources")
    console.print("  upid universal optimize        # Get optimizations")
    console.print("  upid universal report          # Generate reports")
    
    console.print("\n🔧 Advanced Commands:")
    console.print("  upid universal status --format json    # JSON output")
    console.print("  upid universal analyze --namespace kube-system")
    console.print("  upid universal optimize --dry-run      # Preview only")
    console.print("  upid universal report --output report.html")
    
    console.print("\n🌍 Works with ANY cluster:")
    console.print("  • Docker Desktop")
    console.print("  • Minikube")
    console.print("  • Kind")
    console.print("  • K3s")
    console.print("  • EKS (AWS)")
    console.print("  • AKS (Azure)")
    console.print("  • GKE (Google)")
    console.print("  • Any other Kubernetes cluster")

if __name__ == '__main__':
    demo_universal_cli()
    show_usage_commands()
    
    console.print("\n" + "="*70)
    console.print("[bold green]🎉 Demo completed! Your universal Kubernetes CLI is ready.[/bold green]")
    console.print("="*70) 