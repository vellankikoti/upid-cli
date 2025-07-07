"""
Analysis commands for UPID CLI
"""
import click
import sys
from upid.core.utils import (
    print_success, print_error, print_info, print_warning,
    validate_cluster_id, format_currency, format_percentage,
    format_bytes, print_table, show_progress
)

@click.group()
def analyze_group():
    """Analysis and reporting commands"""
    pass

@analyze_group.command()
@click.argument('cluster_id')
@click.option('--period', '-p', default='30d', help='Analysis period')
@click.pass_context
def cost(ctx, cluster_id, period):
    """Analyze cluster costs"""
    api_client = ctx.obj['auth'].api_client
    
    if not validate_cluster_id(cluster_id):
        print_error("Invalid cluster ID format")
        sys.exit(1)
    
    try:
        with show_progress("💰 Analyzing cluster costs..."):
            cost_analysis = api_client.analyze_costs(cluster_id, period)
        
        click.echo(f"💰 Cost Analysis: {cluster_id}")
        click.echo(f"📅 Period: {period}")
        click.echo("=" * 50)
        click.echo(f"💵 Total Cost: {format_currency(cost_analysis['total_cost'])}")
        
        if 'breakdown' in cost_analysis:
            click.echo(f"\n📊 Cost Breakdown:")
            for category, amount in cost_analysis['breakdown'].items():
                percentage = (amount / cost_analysis['total_cost']) * 100
                click.echo(f"  {category}: {format_currency(amount)} ({format_percentage(percentage)})")
        
        if 'optimization_potential' in cost_analysis:
            click.echo(f"\n🎯 Optimization Potential: {format_currency(cost_analysis['optimization_potential'])}")
        
        if 'trends' in cost_analysis:
            click.echo(f"\n📈 Cost Trends:")
            for trend in cost_analysis['trends']:
                click.echo(f"  {trend['period']}: {format_currency(trend['cost'])} ({trend['change']}%)")
        
    except Exception as e:
        print_error(f"Cost analysis failed: {e}")
        sys.exit(1)

@analyze_group.command()
@click.argument('cluster_id')
@click.option('--period', '-p', default='30d', help='Analysis period')
@click.pass_context
def performance(ctx, cluster_id, period):
    """Analyze cluster performance"""
    api_client = ctx.obj['auth'].api_client
    
    if not validate_cluster_id(cluster_id):
        print_error("Invalid cluster ID format")
        sys.exit(1)
    
    try:
        with show_progress("⚡ Analyzing cluster performance..."):
            perf_analysis = api_client.analyze_performance(cluster_id, period)
        
        click.echo(f"⚡ Performance Analysis: {cluster_id}")
        click.echo(f"📅 Period: {period}")
        click.echo("=" * 50)
        click.echo(f"🖥️  CPU Utilization: {format_percentage(perf_analysis['cpu_utilization'])}")
        click.echo(f"💾 Memory Utilization: {format_percentage(perf_analysis['memory_utilization'])}")
        click.echo(f"🌐 Network Throughput: {format_bytes(perf_analysis['network_throughput'])}/s")
        click.echo(f"💿 Storage I/O: {perf_analysis['storage_io']} IOPS")
        click.echo(f"📊 Performance Score: {perf_analysis['performance_score']}/100")
        
        if 'bottlenecks' in perf_analysis:
            click.echo(f"\n⚠️  Performance Bottlenecks:")
            for bottleneck in perf_analysis['bottlenecks']:
                click.echo(f"  • {bottleneck['description']} (Impact: {bottleneck['impact']})")
        
        if 'recommendations' in perf_analysis:
            click.echo(f"\n🎯 Performance Recommendations:")
            for rec in perf_analysis['recommendations']:
                click.echo(f"  • {rec['title']} (Impact: {rec['impact']})")
        
    except Exception as e:
        print_error(f"Performance analysis failed: {e}")
        sys.exit(1)

@analyze_group.command()
@click.argument('cluster_id')
@click.option('--period', '-p', default='30d', help='Analysis period')
@click.pass_context
def efficiency(ctx, cluster_id, period):
    """Analyze cluster resource efficiency"""
    api_client = ctx.obj['auth'].api_client
    
    if not validate_cluster_id(cluster_id):
        print_error("Invalid cluster ID format")
        sys.exit(1)
    
    try:
        with show_progress("📊 Analyzing resource efficiency..."):
            efficiency_analysis = api_client.analyze_efficiency(cluster_id, period)
        
        click.echo(f"📊 Efficiency Analysis: {cluster_id}")
        click.echo(f"📅 Period: {period}")
        click.echo("=" * 50)
        click.echo(f"📈 Overall Efficiency: {format_percentage(efficiency_analysis['overall_efficiency'])}")
        click.echo(f"🖥️  CPU Efficiency: {format_percentage(efficiency_analysis['cpu_efficiency'])}")
        click.echo(f"💾 Memory Efficiency: {format_percentage(efficiency_analysis['memory_efficiency'])}")
        click.echo(f"💿 Storage Efficiency: {format_percentage(efficiency_analysis['storage_efficiency'])}")
        
        if 'waste_analysis' in efficiency_analysis:
            waste = efficiency_analysis['waste_analysis']
            click.echo(f"\n🗑️  Resource Waste:")
            click.echo(f"  CPU Waste: {format_percentage(waste['cpu_waste'])}")
            click.echo(f"  Memory Waste: {format_percentage(waste['memory_waste'])}")
            click.echo(f"  Storage Waste: {format_percentage(waste['storage_waste'])}")
            click.echo(f"  Total Waste: {format_currency(waste['total_waste_cost'])}")
        
        if 'optimization_opportunities' in efficiency_analysis:
            opportunities = efficiency_analysis['optimization_opportunities']
            click.echo(f"\n🎯 Optimization Opportunities:")
            for opp in opportunities:
                click.echo(f"  • {opp['title']} (Savings: {format_currency(opp['potential_savings'])})")
        
    except Exception as e:
        print_error(f"Efficiency analysis failed: {e}")
        sys.exit(1)

@analyze_group.command()
@click.argument('cluster_id')
@click.option('--period', '-p', default='30d', help='Analysis period')
@click.pass_context
def capacity(ctx, cluster_id, period):
    """Analyze cluster capacity planning"""
    api_client = ctx.obj['auth'].api_client
    
    if not validate_cluster_id(cluster_id):
        print_error("Invalid cluster ID format")
        sys.exit(1)
    
    try:
        with show_progress("📈 Analyzing capacity planning..."):
            capacity_analysis = api_client.analyze_capacity(cluster_id, period)
        
        click.echo(f"📈 Capacity Analysis: {cluster_id}")
        click.echo(f"📅 Period: {period}")
        click.echo("=" * 50)
        
        # Current capacity
        current = capacity_analysis['current_capacity']
        click.echo(f"📊 Current Capacity:")
        click.echo(f"  CPU: {current['cpu']} cores ({format_percentage(current['cpu_utilization'])})")
        click.echo(f"  Memory: {format_bytes(current['memory'])} ({format_percentage(current['memory_utilization'])})")
        click.echo(f"  Storage: {format_bytes(current['storage'])} ({format_percentage(current['storage_utilization'])})")
        
        # Projected capacity
        if 'projected_capacity' in capacity_analysis:
            projected = capacity_analysis['projected_capacity']
            click.echo(f"\n🔮 Projected Capacity (6 months):")
            click.echo(f"  CPU: {projected['cpu']} cores")
            click.echo(f"  Memory: {format_bytes(projected['memory'])}")
            click.echo(f"  Storage: {format_bytes(projected['storage'])}")
        
        # Growth trends
        if 'growth_trends' in capacity_analysis:
            trends = capacity_analysis['growth_trends']
            click.echo(f"\n📈 Growth Trends:")
            click.echo(f"  CPU Growth: {trends['cpu_growth']}% per month")
            click.echo(f"  Memory Growth: {trends['memory_growth']}% per month")
            click.echo(f"  Storage Growth: {trends['storage_growth']}% per month")
        
        # Recommendations
        if 'recommendations' in capacity_analysis:
            recommendations = capacity_analysis['recommendations']
            click.echo(f"\n🎯 Capacity Recommendations:")
            for rec in recommendations:
                click.echo(f"  • {rec['title']} (Priority: {rec['priority']})")
        
    except Exception as e:
        print_error(f"Capacity analysis failed: {e}")
        sys.exit(1)

@analyze_group.command()
@click.argument('cluster_id')
@click.option('--period', '-p', default='30d', help='Analysis period')
@click.pass_context
def security(ctx, cluster_id, period):
    """Analyze cluster security posture"""
    api_client = ctx.obj['auth'].api_client
    
    if not validate_cluster_id(cluster_id):
        print_error("Invalid cluster ID format")
        sys.exit(1)
    
    try:
        with show_progress("🔒 Analyzing security posture..."):
            security_analysis = api_client.analyze_security(cluster_id, period)
        
        click.echo(f"🔒 Security Analysis: {cluster_id}")
        click.echo(f"📅 Period: {period}")
        click.echo("=" * 50)
        click.echo(f"🛡️  Security Score: {security_analysis['security_score']}/100")
        
        # Vulnerabilities
        if 'vulnerabilities' in security_analysis:
            vulns = security_analysis['vulnerabilities']
            click.echo(f"\n⚠️  Vulnerabilities Found: {len(vulns)}")
            for vuln in vulns[:5]:  # Show top 5
                severity_icon = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢"}.get(vuln['severity'], "⚪")
                click.echo(f"  {severity_icon} {vuln['title']} ({vuln['severity']})")
        
        # Compliance
        if 'compliance' in security_analysis:
            compliance = security_analysis['compliance']
            click.echo(f"\n📋 Compliance Status:")
            for standard, status in compliance.items():
                status_icon = "✅" if status['compliant'] else "❌"
                click.echo(f"  {status_icon} {standard}: {status['score']}%")
        
        # Recommendations
        if 'recommendations' in security_analysis:
            recommendations = security_analysis['recommendations']
            click.echo(f"\n🎯 Security Recommendations:")
            for rec in recommendations:
                priority_icon = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢"}.get(rec['priority'], "⚪")
                click.echo(f"  {priority_icon} {rec['title']} (Priority: {rec['priority']})")
        
    except Exception as e:
        print_error(f"Security analysis failed: {e}")
        sys.exit(1)

@analyze_group.command()
@click.argument('cluster_id')
@click.option('--period', '-p', default='30d', help='Analysis period')
@click.option('--format', '-f', type=click.Choice(['table', 'json', 'csv']), default='table', help='Output format')
@click.pass_context
def summary(ctx, cluster_id, period, format):
    """Generate comprehensive cluster analysis summary"""
    api_client = ctx.obj['auth'].api_client
    
    if not validate_cluster_id(cluster_id):
        print_error("Invalid cluster ID format")
        sys.exit(1)
    
    try:
        with show_progress("📊 Generating comprehensive analysis..."):
            summary = api_client.get_analysis_summary(cluster_id, period)
        
        click.echo(f"📊 Cluster Analysis Summary: {cluster_id}")
        click.echo(f"📅 Period: {period}")
        click.echo("=" * 60)
        
        # Key metrics
        metrics = summary['key_metrics']
        click.echo(f"📈 Key Metrics:")
        click.echo(f"  🖥️  CPU Utilization: {format_percentage(metrics['cpu_utilization'])}")
        click.echo(f"  💾 Memory Utilization: {format_percentage(metrics['memory_utilization'])}")
        click.echo(f"  💰 Total Cost: {format_currency(metrics['total_cost'])}")
        click.echo(f"  📊 Efficiency Score: {format_percentage(metrics['efficiency_score'])}")
        click.echo(f"  🛡️  Security Score: {format_percentage(metrics['security_score'])}")
        
        # Optimization opportunities
        if 'optimization_opportunities' in summary:
            opportunities = summary['optimization_opportunities']
            click.echo(f"\n🎯 Optimization Opportunities:")
            click.echo(f"  💰 Potential Savings: {format_currency(opportunities['total_savings'])}")
            click.echo(f"  📦 Zero-Pod Scaling: {opportunities['zero_pod_opportunities']} pods")
            click.echo(f"  🖥️  CPU Optimization: {opportunities['cpu_optimizations']} recommendations")
            click.echo(f"  💾 Memory Optimization: {opportunities['memory_optimizations']} recommendations")
        
        # Risk assessment
        if 'risk_assessment' in summary:
            risk = summary['risk_assessment']
            click.echo(f"\n⚠️  Risk Assessment:")
            click.echo(f"  Overall Risk: {risk['overall_risk']}")
            click.echo(f"  Performance Risk: {risk['performance_risk']}")
            click.echo(f"  Security Risk: {risk['security_risk']}")
            click.echo(f"  Cost Risk: {risk['cost_risk']}")
        
        # Recommendations
        if 'top_recommendations' in summary:
            recommendations = summary['top_recommendations']
            click.echo(f"\n🎯 Top Recommendations:")
            for i, rec in enumerate(recommendations, 1):
                click.echo(f"  {i}. {rec['title']}")
                click.echo(f"     Impact: {rec['impact']} | Priority: {rec['priority']}")
                click.echo(f"     Savings: {format_currency(rec['savings'])}")
                click.echo()
        
    except Exception as e:
        print_error(f"Summary analysis failed: {e}")
        sys.exit(1) 