"""
Optimization commands for UPID CLI with zero-pod scaling detection
"""
import click
import sys
from upid.services.optimization_service import OptimizationService
from upid.core.utils import (
    print_success, print_error, print_info, print_warning,
    validate_cluster_id, format_currency, format_percentage,
    format_optimization_result, format_idle_analysis,
    confirm_action, show_progress
)

@click.group()
def optimize_group():
    """Optimization commands - The magic of UPID!"""
    pass

@optimize_group.command()
@click.argument('cluster_id')
@click.option('--strategy', '-s', help='Optimization strategy')
@click.option('--show-idle', is_flag=True, help='Show idle time analysis')
@click.option('--zero-pod-only', is_flag=True, help='Show only zero-pod scaling opportunities')
@click.option('--dry-run', is_flag=True, help='Show recommendations without applying')
@click.option('--force', '-f', is_flag=True, help='Force optimization without safety checks')
@click.pass_context
def analyze(ctx, cluster_id, strategy, show_idle, zero_pod_only, dry_run, force):
    """Analyze cluster for optimization opportunities including zero-pod scaling"""
    optimization_service = OptimizationService(ctx.obj['auth'])
    
    if not validate_cluster_id(cluster_id):
        print_error("Invalid cluster ID format")
        sys.exit(1)
    
    # Use default cluster if not specified
    if cluster_id == 'default':
        cluster_id = ctx.obj['config'].get_default_cluster()
        if not cluster_id:
            print_error("No default cluster set. Please specify a cluster ID or set a default cluster.")
            sys.exit(1)
    
    try:
        with show_progress("🔍 Analyzing cluster and idle patterns..."):
            analysis = optimization_service.analyze_cluster(cluster_id, strategy)
        
        click.echo(f"\n🎯 Optimization Analysis for {cluster_id}")
        click.echo("=" * 60)
        
        # Display optimization results
        click.echo(format_optimization_result(analysis))
        
        # Zero-pod scaling insights
        if analysis.get('zero_pod_opportunities'):
            zero_pod_analysis = analysis['zero_pod_opportunities']
            click.echo(f"\n🔄 Zero-Pod Scaling Opportunities:")
            click.echo(f"   📦 Scalable Pods: {zero_pod_analysis['scalable_pods_count']}")
            click.echo(f"   💰 Potential Savings: {format_currency(zero_pod_analysis['total_potential_savings'])}")
            click.echo(f"   📊 Cluster Idle Time: {format_percentage(zero_pod_analysis['idle_patterns']['cluster_idle_percentage'])}")
            
            if show_idle or zero_pod_only:
                click.echo(f"\n📋 Detailed Idle Analysis:")
                for opportunity in zero_pod_analysis['idle_opportunities']:
                    if not zero_pod_only or opportunity['can_scale_to_zero']:
                        status_icon = "✅" if opportunity['can_scale_to_zero'] else "⚠️"
                        click.echo(f"   {status_icon} {opportunity['namespace']}/{opportunity['pod_name']}")
                        click.echo(f"      Idle Time: {format_percentage(opportunity['idle_percentage'])}")
                        click.echo(f"      Avg Idle Duration: {opportunity['avg_idle_duration']:.0f} minutes")
                        click.echo(f"      Pattern: {opportunity['idle_pattern']}")
                        click.echo(f"      Potential Savings: {format_currency(opportunity['potential_savings'])}/month")
                        if opportunity['can_scale_to_zero']:
                            click.echo(f"      Scale-down Time: {opportunity['recommended_scale_down_time']} seconds")
                        click.echo()
        
        # Regular optimization recommendations
        if not zero_pod_only and analysis['recommendations']:
            click.echo(f"\n🎯 Other Optimization Recommendations ({len(analysis['recommendations'])}):")
            for i, rec in enumerate(analysis['recommendations'], 1):
                click.echo(f"  {i}. {rec['title']}")
                click.echo(f"     💰 Savings: {format_currency(rec['savings'])}")
                click.echo(f"     ⚠️  Risk: {rec['risk_level']}")
                click.echo()
        
        # Apply optimizations if requested
        if not dry_run and (analysis['recommendations'] or analysis.get('zero_pod_opportunities', {}).get('scalable_pods_count', 0) > 0):
            if confirm_action("🚀 Apply optimizations?"):
                try:
                    deployment = optimization_service.apply_optimizations(cluster_id, analysis['recommendations'])
                    print_success(f"Optimization deployment started: {deployment['deployment_id']}")
                except Exception as e:
                    print_error(f"Failed to apply optimizations: {e}")
                    sys.exit(1)
                    
    except Exception as e:
        print_error(f"Analysis failed: {e}")
        sys.exit(1)

@optimize_group.command()
@click.argument('cluster_id')
@click.option('--namespace', '-n', help='Specific namespace to analyze')
@click.pass_context
def idle(ctx, cluster_id, namespace):
    """Analyze pod idle time patterns for zero-pod scaling"""
    optimization_service = OptimizationService(ctx.obj['auth'])
    
    if not validate_cluster_id(cluster_id):
        print_error("Invalid cluster ID format")
        sys.exit(1)
    
    try:
        with show_progress("🔍 Analyzing pod idle patterns..."):
            idle_analysis = optimization_service._analyze_pod_idle_time(cluster_id, {})
        
        click.echo(f"🔄 Idle Time Analysis for {cluster_id}")
        if namespace:
            click.echo(f"📁 Namespace: {namespace}")
        
        click.echo("=" * 50)
        click.echo(format_idle_analysis(idle_analysis))
        
        click.echo(f"\n📊 Idle Patterns:")
        for opportunity in idle_analysis['idle_opportunities']:
            if not namespace or opportunity['namespace'] == namespace:
                pattern_icon = {
                    'predictable': '🕐',
                    'scheduled': '📅',
                    'low_traffic': '📉',
                    'irregular': '📊',
                    'none': '❌'
                }.get(opportunity['idle_pattern'], '❓')
                
                click.echo(f"  {pattern_icon} {opportunity['namespace']}/{opportunity['pod_name']}")
                click.echo(f"     Idle Time: {format_percentage(opportunity['idle_percentage'])}")
                click.echo(f"     Pattern: {opportunity['idle_pattern']}")
                click.echo(f"     Can Scale to Zero: {'✅' if opportunity['can_scale_to_zero'] else '❌'}")
                if opportunity['can_scale_to_zero']:
                    click.echo(f"     Scale-down Time: {opportunity['recommended_scale_down_time']} seconds")
                    click.echo(f"     Monthly Savings: {format_currency(opportunity['potential_savings'])}")
                click.echo()
                
    except Exception as e:
        print_error(f"Idle analysis failed: {e}")
        sys.exit(1)

@optimize_group.command()
@click.argument('cluster_id')
@click.pass_context
def status(ctx, cluster_id):
    """Check optimization status"""
    optimization_service = OptimizationService(ctx.obj['auth'])
    
    if not validate_cluster_id(cluster_id):
        print_error("Invalid cluster ID format")
        sys.exit(1)
    
    try:
        status = optimization_service.get_optimization_status(cluster_id)
        
        click.echo(f"🎯 Optimization Status: {cluster_id}")
        click.echo("=" * 50)
        click.echo(f"📊 Current Efficiency: {format_percentage(status['current_efficiency'])}")
        click.echo(f"💰 Total Savings: {format_currency(status['total_savings'])}")
        click.echo(f"📈 Improvement: {format_percentage(status['improvement_percentage'])}")
        click.echo(f"⏰ Last Optimization: {status['last_optimization']}")
        
        if 'zero_pod_status' in status:
            zero_pod = status['zero_pod_status']
            click.echo(f"\n🔄 Zero-Pod Scaling Status:")
            click.echo(f"   📦 Pods Scaled to Zero: {zero_pod.get('pods_scaled_to_zero', 0)}")
            click.echo(f"   💰 Zero-Pod Savings: {format_currency(zero_pod.get('savings', 0))}")
            click.echo(f"   ⏱️  Scale-down Time: {zero_pod.get('scale_down_time', 'N/A')}")
        
    except Exception as e:
        print_error(f"Failed to get optimization status: {e}")
        sys.exit(1)

@optimize_group.command()
@click.argument('cluster_id')
@click.pass_context
def rollback(ctx, cluster_id):
    """Rollback last optimization"""
    optimization_service = OptimizationService(ctx.obj['auth'])
    
    if not validate_cluster_id(cluster_id):
        print_error("Invalid cluster ID format")
        sys.exit(1)
    
    if not confirm_action(f"⚠️  Rollback optimizations for {cluster_id}?"):
        print_info("Operation cancelled")
        return
    
    try:
        result = optimization_service.rollback_optimizations(cluster_id)
        print_success(f"Rollback completed: {result['rollback_id']}")
    except Exception as e:
        print_error(f"Rollback failed: {e}")
        sys.exit(1)

@optimize_group.command()
@click.argument('cluster_id')
@click.option('--namespace', '-n', help='Specific namespace')
@click.pass_context
def zero_pod(ctx, cluster_id, namespace):
    """Deploy zero-pod scaling configurations"""
    from upid.services.deployment_service import DeploymentService
    
    deployment_service = DeploymentService(ctx.obj['auth'])
    
    if not validate_cluster_id(cluster_id):
        print_error("Invalid cluster ID format")
        sys.exit(1)
    
    try:
        with show_progress("🚀 Deploying zero-pod scaling configurations..."):
            result = deployment_service.deploy_zero_pod_scaling(cluster_id, namespace)
        
        if result['status'] == 'no_opportunities':
            print_info("No pods found suitable for zero-pod scaling")
            return
        
        print_success(f"Zero-pod scaling deployed successfully!")
        print_info(f"Pods configured: {result['pods_configured']}")
        print_info(f"Potential savings: {format_currency(result['potential_savings'])}")
        
        if 'configurations' in result:
            click.echo(f"\n📋 Deployed Configurations:")
            for config in result['configurations']:
                click.echo(f"  📦 {config['metadata']['name']}")
                click.echo(f"     Namespace: {config['metadata']['namespace']}")
                click.echo(f"     Min Replicas: {config['spec']['minReplicas']}")
                click.echo(f"     Max Replicas: {config['spec']['maxReplicas']}")
                click.echo()
        
    except Exception as e:
        print_error(f"Failed to deploy zero-pod scaling: {e}")
        sys.exit(1)

@optimize_group.command()
@click.argument('cluster_id')
@click.option('--strategy', '-s', help='Optimization strategy')
@click.option('--timeout', '-t', default=300, help='Deployment timeout (seconds)')
@click.pass_context
def apply(ctx, cluster_id, strategy, timeout):
    """Apply optimizations to cluster"""
    from upid.services.deployment_service import DeploymentService
    
    deployment_service = DeploymentService(ctx.obj['auth'])
    optimization_service = OptimizationService(ctx.obj['auth'])
    
    if not validate_cluster_id(cluster_id):
        print_error("Invalid cluster ID format")
        sys.exit(1)
    
    try:
        # First analyze the cluster
        with show_progress("🔍 Analyzing cluster for optimizations..."):
            analysis = optimization_service.analyze_cluster(cluster_id, strategy)
        
        if not analysis['recommendations']:
            print_info("No optimization recommendations found")
            return
        
        # Show recommendations
        click.echo(f"\n🎯 Optimization Recommendations:")
        for i, rec in enumerate(analysis['recommendations'], 1):
            click.echo(f"  {i}. {rec['title']}")
            click.echo(f"     💰 Savings: {format_currency(rec['savings'])}")
            click.echo(f"     ⚠️  Risk: {rec['risk_level']}")
            click.echo()
        
        if not confirm_action("🚀 Apply these optimizations?"):
            print_info("Operation cancelled")
            return
        
        # Apply optimizations
        with show_progress("🚀 Applying optimizations..."):
            deployment = deployment_service.deploy_optimizations(cluster_id, analysis['recommendations'])
        
        print_success(f"Optimization deployment started: {deployment['deployment_id']}")
        
        # Monitor deployment
        with show_progress("⏳ Monitoring deployment..."):
            import time
            while timeout > 0:
                status = deployment_service.get_deployment_status(deployment['deployment_id'])
                
                if status['status'] in ['completed', 'failed']:
                    break
                
                time.sleep(5)
                timeout -= 5
        
        if status['status'] == 'completed':
            print_success("✅ Deployment completed successfully!")
            print_info(f"💰 Savings: {format_currency(status.get('savings', 0))}")
            print_info(f"📊 Efficiency: {format_percentage(status.get('efficiency', 0))}")
        else:
            print_error(f"❌ Deployment failed: {status.get('error', 'Unknown error')}")
            sys.exit(1)
            
    except Exception as e:
        print_error(f"Deployment failed: {e}")
        sys.exit(1) 