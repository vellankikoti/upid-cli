"""
Cluster management commands for UPID CLI
"""
import click
import sys
from upid.core.utils import (
    print_success, print_error, print_info, print_warning,
    read_kubeconfig, validate_kubeconfig, validate_cluster_id,
    print_table, format_percentage, format_bytes
)

@click.group()
def cluster_group():
    """Cluster management commands"""
    pass

@cluster_group.command()
@click.option('--name', '-n', required=True, help='Cluster name')
@click.option('--kubeconfig', '-k', required=True, help='Path to kubeconfig file')
@click.option('--region', '-r', help='Cluster region')
@click.option('--description', '-d', help='Cluster description')
@click.pass_context
def register(ctx, name, kubeconfig, region, description):
    """Register a new Kubernetes cluster"""
    api_client = ctx.obj['auth'].api_client
    
    # Validate kubeconfig file
    if not validate_kubeconfig(kubeconfig):
        print_error("Invalid kubeconfig file")
        sys.exit(1)
    
    try:
        # Read and encode kubeconfig
        kubeconfig_data = read_kubeconfig(kubeconfig)
        
        # Register cluster
        cluster = api_client.register_cluster(name, kubeconfig_data, region, description)
        
        print_success(f"Cluster '{name}' registered successfully")
        print_info(f"Cluster ID: {cluster['cluster_id']}")
        if region:
            print_info(f"Region: {region}")
        
        # Set as default cluster if none set
        config = ctx.obj['config']
        if not config.get_default_cluster():
            config.set_default_cluster(cluster['cluster_id'])
            print_info("Set as default cluster")
            
    except Exception as e:
        print_error(f"Failed to register cluster: {e}")
        sys.exit(1)

@cluster_group.command()
@click.pass_context
def list(ctx):
    """List all registered clusters"""
    api_client = ctx.obj['auth'].api_client
    
    try:
        clusters = api_client.list_clusters()
        
        if not clusters:
            print_info("No clusters found")
            return
        
        # Prepare table data
        table_data = []
        for cluster in clusters:
            status_icon = "🟢" if cluster['status'] == 'healthy' else "🔴"
            table_data.append({
                'Name': cluster['name'],
                'ID': cluster['cluster_id'],
                'Status': f"{status_icon} {cluster['status']}",
                'Region': cluster.get('region', 'N/A'),
                'Nodes': cluster.get('nodes_count', 0),
                'Pods': cluster.get('pods_count', 0)
            })
        
        print_table(table_data, ['Name', 'ID', 'Status', 'Region', 'Nodes', 'Pods'], 
                   "🏗️  Registered Clusters")
        
    except Exception as e:
        print_error(f"Failed to list clusters: {e}")
        sys.exit(1)

@cluster_group.command()
@click.argument('cluster_id')
@click.pass_context
def status(ctx, cluster_id):
    """Get cluster health status"""
    api_client = ctx.obj['auth'].api_client
    
    if not validate_cluster_id(cluster_id):
        print_error("Invalid cluster ID format")
        sys.exit(1)
    
    try:
        health = api_client.get_cluster_health(cluster_id)
        
        click.echo(f"🏗️  Cluster Health: {cluster_id}")
        click.echo("=" * 50)
        
        status_icon = "🟢" if health['status'] == 'healthy' else "🔴"
        click.echo(f"📊 Status: {status_icon} {health['status']}")
        click.echo(f"🖥️  Nodes: {health.get('nodes_count', 0)}")
        click.echo(f"📦 Pods: {health.get('pods_count', 0)}")
        click.echo(f"💾 Memory Usage: {format_percentage(health.get('memory_usage', 0))}")
        click.echo(f"⚡ CPU Usage: {format_percentage(health.get('cpu_usage', 0))}")
        
        if 'storage_usage' in health:
            click.echo(f"💿 Storage Usage: {format_percentage(health['storage_usage'])}")
        
        if 'network_usage' in health:
            click.echo(f"🌐 Network Usage: {format_bytes(health['network_usage'])}/s")
        
        # Show warnings if any
        warnings = health.get('warnings', [])
        if warnings:
            click.echo("\n⚠️  Warnings:")
            for warning in warnings:
                print_warning(f"  {warning}")
        
    except Exception as e:
        print_error(f"Failed to get cluster status: {e}")
        sys.exit(1)

@cluster_group.command()
@click.argument('cluster_id')
@click.pass_context
def delete(ctx, cluster_id):
    """Delete cluster registration"""
    api_client = ctx.obj['auth'].api_client
    
    if not validate_cluster_id(cluster_id):
        print_error("Invalid cluster ID format")
        sys.exit(1)
    
    if not click.confirm(f"Are you sure you want to delete cluster {cluster_id}?"):
        print_info("Operation cancelled")
        return
    
    try:
        api_client.delete_cluster(cluster_id)
        print_success(f"Cluster {cluster_id} deleted successfully")
        
        # Remove from default if it was the default cluster
        config = ctx.obj['config']
        if config.get_default_cluster() == cluster_id:
            config.set_default_cluster(None)
            print_info("Removed from default cluster")
            
    except Exception as e:
        print_error(f"Failed to delete cluster: {e}")
        sys.exit(1)

@cluster_group.command()
@click.argument('cluster_id')
@click.option('--watch', '-w', is_flag=True, help='Watch cluster status continuously')
@click.pass_context
def health(ctx, cluster_id, watch):
    """Monitor cluster health"""
    api_client = ctx.obj['auth'].api_client
    
    if not validate_cluster_id(cluster_id):
        print_error("Invalid cluster ID format")
        sys.exit(1)
    
    try:
        if watch:
            import time
            click.echo(f"🔍 Watching cluster health: {cluster_id}")
            click.echo("Press Ctrl+C to stop")
            
            while True:
                health = api_client.get_cluster_health(cluster_id)
                
                # Clear screen and show status
                click.clear()
                click.echo(f"🏗️  Cluster Health: {cluster_id}")
                click.echo("=" * 50)
                click.echo(f"📊 Status: {'🟢' if health['status'] == 'healthy' else '🔴'} {health['status']}")
                click.echo(f"🖥️  Nodes: {health.get('nodes_count', 0)}")
                click.echo(f"📦 Pods: {health.get('pods_count', 0)}")
                click.echo(f"💾 Memory: {format_percentage(health.get('memory_usage', 0))}")
                click.echo(f"⚡ CPU: {format_percentage(health.get('cpu_usage', 0))}")
                click.echo(f"⏰ Last Updated: {health.get('last_updated', 'N/A')}")
                
                time.sleep(30)  # Update every 30 seconds
        else:
            health = api_client.get_cluster_health(cluster_id)
            
            click.echo(f"🏗️  Cluster Health: {cluster_id}")
            click.echo("=" * 50)
            click.echo(f"📊 Status: {'🟢' if health['status'] == 'healthy' else '🔴'} {health['status']}")
            click.echo(f"🖥️  Nodes: {health.get('nodes_count', 0)}")
            click.echo(f"📦 Pods: {health.get('pods_count', 0)}")
            click.echo(f"💾 Memory: {format_percentage(health.get('memory_usage', 0))}")
            click.echo(f"⚡ CPU: {format_percentage(health.get('cpu_usage', 0))}")
            
    except KeyboardInterrupt:
        if watch:
            print_info("\nStopped watching cluster health")
    except Exception as e:
        print_error(f"Failed to get cluster health: {e}")
        sys.exit(1)

@cluster_group.command()
@click.argument('cluster_id')
@click.pass_context
def info(ctx, cluster_id):
    """Get detailed cluster information"""
    api_client = ctx.obj['auth'].api_client
    
    if not validate_cluster_id(cluster_id):
        print_error("Invalid cluster ID format")
        sys.exit(1)
    
    try:
        cluster = api_client.get_cluster(cluster_id)
        
        click.echo(f"🏗️  Cluster Information: {cluster_id}")
        click.echo("=" * 50)
        click.echo(f"Name: {cluster['name']}")
        click.echo(f"Region: {cluster.get('region', 'N/A')}")
        click.echo(f"Description: {cluster.get('description', 'N/A')}")
        click.echo(f"Status: {cluster['status']}")
        click.echo(f"Created: {cluster.get('created_at', 'N/A')}")
        click.echo(f"Updated: {cluster.get('updated_at', 'N/A')}")
        
        # Resource information
        if 'resources' in cluster:
            resources = cluster['resources']
            click.echo(f"\n📊 Resource Information:")
            click.echo(f"  Total CPU: {resources.get('total_cpu', 0)} cores")
            click.echo(f"  Total Memory: {format_bytes(resources.get('total_memory', 0))}")
            click.echo(f"  Total Storage: {format_bytes(resources.get('total_storage', 0))}")
            click.echo(f"  Available CPU: {resources.get('available_cpu', 0)} cores")
            click.echo(f"  Available Memory: {format_bytes(resources.get('available_memory', 0))}")
        
        # Workload information
        if 'workloads' in cluster:
            workloads = cluster['workloads']
            click.echo(f"\n📦 Workload Information:")
            click.echo(f"  Deployments: {workloads.get('deployments', 0)}")
            click.echo(f"  Services: {workloads.get('services', 0)}")
            click.echo(f"  ConfigMaps: {workloads.get('configmaps', 0)}")
            click.echo(f"  Secrets: {workloads.get('secrets', 0)}")
        
    except Exception as e:
        print_error(f"Failed to get cluster information: {e}")
        sys.exit(1) 