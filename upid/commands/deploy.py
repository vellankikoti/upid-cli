"""
Deployment commands for UPID CLI
"""
import click
import sys
from upid.services.deployment_service import DeploymentService
from upid.core.utils import (
    print_success, print_error, print_info, print_warning,
    validate_cluster_id, format_currency, show_progress
)

@click.group()
def deploy_group():
    """Deployment management commands"""
    pass

@deploy_group.command()
@click.argument('cluster_id')
@click.pass_context
def list(ctx, cluster_id):
    """List deployments for cluster"""
    deployment_service = DeploymentService(ctx.obj['auth'])
    
    if not validate_cluster_id(cluster_id):
        print_error("Invalid cluster ID format")
        sys.exit(1)
    
    try:
        deployments = deployment_service.list_deployments(cluster_id)
        
        if not deployments:
            print_info("No deployments found")
            return
        
        # Prepare table data
        table_data = []
        for deployment in deployments:
            status_icon = {
                'completed': '✅',
                'in_progress': '⏳',
                'failed': '❌',
                'pending': '⏸️'
            }.get(deployment['status'], '❓')
            
            table_data.append({
                'ID': deployment['deployment_id'],
                'Type': deployment['deployment_type'],
                'Status': f"{status_icon} {deployment['status']}",
                'Created': deployment['created_at'],
                'Savings': format_currency(deployment.get('savings', 0))
            })
        
        from upid.core.utils import print_table
        print_table(table_data, ['ID', 'Type', 'Status', 'Created', 'Savings'], 
                   "🚀 Deployments")
        
    except Exception as e:
        print_error(f"Failed to list deployments: {e}")
        sys.exit(1)

@deploy_group.command()
@click.argument('deployment_id')
@click.pass_context
def status(ctx, deployment_id):
    """Get deployment status"""
    deployment_service = DeploymentService(ctx.obj['auth'])
    
    try:
        status = deployment_service.get_deployment_status(deployment_id)
        
        click.echo(f"🚀 Deployment Status: {deployment_id}")
        click.echo("=" * 50)
        click.echo(f"📊 Status: {status['status']}")
        click.echo(f"📦 Type: {status['deployment_type']}")
        click.echo(f"⏰ Created: {status['created_at']}")
        click.echo(f"💰 Savings: {format_currency(status.get('savings', 0))}")
        
        if 'progress' in status:
            progress = status['progress']
            click.echo(f"📈 Progress: {progress['completed']}/{progress['total']} ({progress['percentage']}%)")
        
        if 'error' in status:
            click.echo(f"❌ Error: {status['error']}")
        
    except Exception as e:
        print_error(f"Failed to get deployment status: {e}")
        sys.exit(1)

@deploy_group.command()
@click.argument('deployment_id')
@click.pass_context
def logs(ctx, deployment_id):
    """Get deployment logs"""
    deployment_service = DeploymentService(ctx.obj['auth'])
    
    try:
        logs = deployment_service.get_deployment_logs(deployment_id)
        
        click.echo(f"📋 Deployment Logs: {deployment_id}")
        click.echo("=" * 50)
        
        for log in logs:
            timestamp = log.get('timestamp', 'N/A')
            level = log.get('level', 'INFO')
            message = log.get('message', '')
            
            level_icon = {
                'INFO': 'ℹ️',
                'WARNING': '⚠️',
                'ERROR': '❌',
                'SUCCESS': '✅'
            }.get(level, 'ℹ️')
            
            click.echo(f"[{timestamp}] {level_icon} {level}: {message}")
        
    except Exception as e:
        print_error(f"Failed to get deployment logs: {e}")
        sys.exit(1)

@deploy_group.command()
@click.argument('deployment_id')
@click.pass_context
def rollback(ctx, deployment_id):
    """Rollback deployment"""
    deployment_service = DeploymentService(ctx.obj['auth'])
    
    if not click.confirm(f"⚠️  Rollback deployment {deployment_id}?"):
        print_info("Operation cancelled")
        return
    
    try:
        with show_progress("🔄 Rolling back deployment..."):
            result = deployment_service.rollback_deployment(deployment_id)
        
        print_success(f"Rollback completed: {result['rollback_id']}")
        
    except Exception as e:
        print_error(f"Rollback failed: {e}")
        sys.exit(1)

@deploy_group.command()
@click.argument('deployment_id')
@click.pass_context
def pause(ctx, deployment_id):
    """Pause deployment"""
    deployment_service = DeploymentService(ctx.obj['auth'])
    
    try:
        result = deployment_service.pause_deployment(deployment_id)
        print_success(f"Deployment {deployment_id} paused")
        
    except Exception as e:
        print_error(f"Failed to pause deployment: {e}")
        sys.exit(1)

@deploy_group.command()
@click.argument('deployment_id')
@click.pass_context
def resume(ctx, deployment_id):
    """Resume deployment"""
    deployment_service = DeploymentService(ctx.obj['auth'])
    
    try:
        result = deployment_service.resume_deployment(deployment_id)
        print_success(f"Deployment {deployment_id} resumed")
        
    except Exception as e:
        print_error(f"Failed to resume deployment: {e}")
        sys.exit(1)

@deploy_group.command()
@click.argument('deployment_id')
@click.pass_context
def abort(ctx, deployment_id):
    """Abort deployment"""
    deployment_service = DeploymentService(ctx.obj['auth'])
    
    if not click.confirm(f"⚠️  Abort deployment {deployment_id}?"):
        print_info("Operation cancelled")
        return
    
    try:
        result = deployment_service.abort_deployment(deployment_id)
        print_success(f"Deployment {deployment_id} aborted")
        
    except Exception as e:
        print_error(f"Failed to abort deployment: {e}")
        sys.exit(1)

@deploy_group.command()
@click.argument('cluster_id')
@click.pass_context
def history(ctx, cluster_id):
    """Get deployment history for cluster"""
    deployment_service = DeploymentService(ctx.obj['auth'])
    
    if not validate_cluster_id(cluster_id):
        print_error("Invalid cluster ID format")
        sys.exit(1)
    
    try:
        history = deployment_service.get_deployment_history(cluster_id)
        
        if not history:
            print_info("No deployment history found")
            return
        
        click.echo(f"📚 Deployment History: {cluster_id}")
        click.echo("=" * 50)
        
        for deployment in history:
            status_icon = {
                'completed': '✅',
                'failed': '❌',
                'aborted': '⏹️'
            }.get(deployment['status'], '❓')
            
            click.echo(f"{status_icon} {deployment['deployment_id']}")
            click.echo(f"   Type: {deployment['deployment_type']}")
            click.echo(f"   Status: {deployment['status']}")
            click.echo(f"   Created: {deployment['created_at']}")
            click.echo(f"   Savings: {format_currency(deployment.get('savings', 0))}")
            click.echo()
        
    except Exception as e:
        print_error(f"Failed to get deployment history: {e}")
        sys.exit(1)

@deploy_group.command()
@click.argument('deployment_id')
@click.option('--format', '-f', type=click.Choice(['yaml', 'json']), default='yaml', help='Output format')
@click.pass_context
def export(ctx, deployment_id, format):
    """Export deployment configuration"""
    deployment_service = DeploymentService(ctx.obj['auth'])
    
    try:
        config = deployment_service.export_deployment_config(deployment_id, format)
        
        click.echo(f"📄 Deployment Configuration: {deployment_id}")
        click.echo(f"📝 Format: {format.upper()}")
        click.echo("=" * 50)
        click.echo(config)
        
    except Exception as e:
        print_error(f"Failed to export deployment config: {e}")
        sys.exit(1)

@deploy_group.command()
@click.argument('deployment_id')
@click.pass_context
def metrics(ctx, deployment_id):
    """Get deployment metrics"""
    deployment_service = DeploymentService(ctx.obj['auth'])
    
    try:
        metrics = deployment_service.get_deployment_metrics(deployment_id)
        
        click.echo(f"📊 Deployment Metrics: {deployment_id}")
        click.echo("=" * 50)
        click.echo(f"💰 Cost Savings: {format_currency(metrics.get('cost_savings', 0))}")
        click.echo(f"📈 Efficiency Improvement: {metrics.get('efficiency_improvement', 0)}%")
        click.echo(f"⚡ Performance Impact: {metrics.get('performance_impact', 0)}%")
        click.echo(f"🔄 Resource Optimization: {metrics.get('resource_optimization', 0)}%")
        
        if 'zero_pod_metrics' in metrics:
            zero_pod = metrics['zero_pod_metrics']
            click.echo(f"\n🔄 Zero-Pod Scaling Metrics:")
            click.echo(f"  📦 Pods Scaled to Zero: {zero_pod.get('pods_scaled_to_zero', 0)}")
            click.echo(f"  💰 Zero-Pod Savings: {format_currency(zero_pod.get('savings', 0))}")
            click.echo(f"  ⏱️  Scale-down Time: {zero_pod.get('avg_scale_down_time', 0)}s")
        
    except Exception as e:
        print_error(f"Failed to get deployment metrics: {e}")
        sys.exit(1) 