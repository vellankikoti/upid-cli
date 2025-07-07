"""
Reporting commands for UPID CLI
"""
import click
import sys
from upid.core.utils import (
    print_success, print_error, print_info, print_warning,
    validate_cluster_id, format_currency, format_percentage,
    save_json_file, save_yaml_file
)

@click.group()
def report_group():
    """Reporting and business intelligence commands"""
    pass

@report_group.command()
@click.argument('cluster_id')
@click.option('--report-type', '-t', default='cost_optimization', 
              type=click.Choice(['cost_optimization', 'performance', 'security', 'comprehensive']),
              help='Report type')
@click.option('--period', '-p', default='30d', help='Report period')
@click.option('--output', '-o', help='Output file path')
@click.option('--format', '-f', type=click.Choice(['json', 'yaml', 'pdf']), default='json', help='Output format')
@click.pass_context
def generate(ctx, cluster_id, report_type, period, output, format):
    """Generate business report"""
    api_client = ctx.obj['auth'].api_client
    
    if not validate_cluster_id(cluster_id):
        print_error("Invalid cluster ID format")
        sys.exit(1)
    
    try:
        with show_progress("📊 Generating business report..."):
            report = api_client.get_business_report(cluster_id, report_type)
        
        click.echo(f"📊 Business Report: {cluster_id}")
        click.echo(f"📅 Period: {period}")
        click.echo(f"📋 Type: {report_type}")
        click.echo("=" * 60)
        
        # Executive Summary
        if 'executive_summary' in report:
            summary = report['executive_summary']
            click.echo("🎯 Executive Summary:")
            click.echo(f"  💰 Total Cost: {format_currency(summary['total_cost'])}")
            click.echo(f"  💸 Potential Savings: {format_currency(summary['potential_savings'])}")
            click.echo(f"  📈 Efficiency Score: {format_percentage(summary['efficiency_score'])}")
            click.echo(f"  🛡️  Security Score: {format_percentage(summary['security_score'])}")
            click.echo()
        
        # Key Findings
        if 'key_findings' in report:
            findings = report['key_findings']
            click.echo("🔍 Key Findings:")
            for finding in findings:
                click.echo(f"  • {finding['description']}")
                if 'impact' in finding:
                    click.echo(f"    Impact: {finding['impact']}")
                if 'recommendation' in finding:
                    click.echo(f"    Recommendation: {finding['recommendation']}")
                click.echo()
        
        # Cost Analysis
        if 'cost_analysis' in report:
            cost = report['cost_analysis']
            click.echo("💰 Cost Analysis:")
            click.echo(f"  Current Monthly Cost: {format_currency(cost['current_monthly_cost'])}")
            click.echo(f"  Optimized Monthly Cost: {format_currency(cost['optimized_monthly_cost'])}")
            click.echo(f"  Monthly Savings: {format_currency(cost['monthly_savings'])}")
            click.echo(f"  Annual Savings: {format_currency(cost['annual_savings'])}")
            click.echo(f"  ROI: {format_percentage(cost['roi'])}")
            click.echo()
        
        # Zero-Pod Scaling Analysis
        if 'zero_pod_analysis' in report:
            zero_pod = report['zero_pod_analysis']
            click.echo("🔄 Zero-Pod Scaling Analysis:")
            click.echo(f"  Scalable Pods: {zero_pod['scalable_pods_count']}")
            click.echo(f"  Potential Savings: {format_currency(zero_pod['potential_savings'])}")
            click.echo(f"  Idle Time Percentage: {format_percentage(zero_pod['idle_time_percentage'])}")
            click.echo()
        
        # Recommendations
        if 'recommendations' in report:
            recommendations = report['recommendations']
            click.echo("🎯 Recommendations:")
            for i, rec in enumerate(recommendations, 1):
                click.echo(f"  {i}. {rec['title']}")
                click.echo(f"     Description: {rec['description']}")
                click.echo(f"     Impact: {rec['impact']}")
                click.echo(f"     Savings: {format_currency(rec['savings'])}")
                click.echo(f"     Priority: {rec['priority']}")
                click.echo()
        
        # Save to file if requested
        if output:
            if format == 'json':
                save_json_file(report, output)
            elif format == 'yaml':
                save_yaml_file(report, output)
            print_success(f"Report saved to {output}")
        
    except Exception as e:
        print_error(f"Failed to generate report: {e}")
        sys.exit(1)

@report_group.command()
@click.argument('cluster_id')
@click.option('--period', '-p', default='30d', help='Analysis period')
@click.pass_context
def roi(ctx, cluster_id, period):
    """Calculate ROI for cluster optimizations"""
    api_client = ctx.obj['auth'].api_client
    
    if not validate_cluster_id(cluster_id):
        print_error("Invalid cluster ID format")
        sys.exit(1)
    
    try:
        # Get investment data
        investment_data = {
            'cluster_id': cluster_id,
            'period': period,
            'optimization_type': 'comprehensive'
        }
        
        with show_progress("💰 Calculating ROI..."):
            roi_analysis = api_client.calculate_roi(investment_data)
        
        click.echo(f"💰 ROI Analysis: {cluster_id}")
        click.echo(f"📅 Period: {period}")
        click.echo("=" * 50)
        click.echo(f"💵 Total Investment: {format_currency(roi_analysis['total_investment'])}")
        click.echo(f"💰 Total Savings: {format_currency(roi_analysis['total_savings'])}")
        click.echo(f"📈 ROI: {format_percentage(roi_analysis['roi'])}")
        click.echo(f"⏰ Payback Period: {roi_analysis['payback_period']} months")
        click.echo(f"📊 Net Present Value: {format_currency(roi_analysis['npv'])}")
        
        if 'breakdown' in roi_analysis:
            breakdown = roi_analysis['breakdown']
            click.echo(f"\n📊 ROI Breakdown:")
            for category, data in breakdown.items():
                click.echo(f"  {category}:")
                click.echo(f"    Investment: {format_currency(data['investment'])}")
                click.echo(f"    Savings: {format_currency(data['savings'])}")
                click.echo(f"    ROI: {format_percentage(data['roi'])}")
        
    except Exception as e:
        print_error(f"ROI calculation failed: {e}")
        sys.exit(1)

@report_group.command()
@click.argument('cluster_id')
@click.pass_context
def kpis(ctx, cluster_id):
    """Get performance KPIs for cluster"""
    api_client = ctx.obj['auth'].api_client
    
    if not validate_cluster_id(cluster_id):
        print_error("Invalid cluster ID format")
        sys.exit(1)
    
    try:
        with show_progress("📊 Fetching KPIs..."):
            kpis = api_client.get_performance_kpis(cluster_id)
        
        click.echo(f"📊 Performance KPIs: {cluster_id}")
        click.echo("=" * 50)
        
        # Cost KPIs
        if 'cost_kpis' in kpis:
            cost = kpis['cost_kpis']
            click.echo("💰 Cost KPIs:")
            click.echo(f"  Monthly Cost: {format_currency(cost['monthly_cost'])}")
            click.echo(f"  Cost per Pod: {format_currency(cost['cost_per_pod'])}")
            click.echo(f"  Cost Efficiency: {format_percentage(cost['cost_efficiency'])}")
            click.echo(f"  Cost Trend: {cost['cost_trend']}")
            click.echo()
        
        # Performance KPIs
        if 'performance_kpis' in kpis:
            perf = kpis['performance_kpis']
            click.echo("⚡ Performance KPIs:")
            click.echo(f"  CPU Utilization: {format_percentage(perf['cpu_utilization'])}")
            click.echo(f"  Memory Utilization: {format_percentage(perf['memory_utilization'])}")
            click.echo(f"  Response Time: {perf['avg_response_time']}ms")
            click.echo(f"  Throughput: {perf['throughput']} req/s")
            click.echo()
        
        # Efficiency KPIs
        if 'efficiency_kpis' in kpis:
            eff = kpis['efficiency_kpis']
            click.echo("📈 Efficiency KPIs:")
            click.echo(f"  Resource Efficiency: {format_percentage(eff['resource_efficiency'])}")
            click.echo(f"  Pod Density: {eff['pod_density']} pods/node")
            click.echo(f"  Idle Time: {format_percentage(eff['idle_time_percentage'])}")
            click.echo(f"  Zero-Pod Scaling: {eff['zero_pod_scaling_pods']} pods")
            click.echo()
        
        # Security KPIs
        if 'security_kpis' in kpis:
            sec = kpis['security_kpis']
            click.echo("🛡️  Security KPIs:")
            click.echo(f"  Security Score: {format_percentage(sec['security_score'])}")
            click.echo(f"  Vulnerabilities: {sec['vulnerability_count']}")
            click.echo(f"  Compliance Score: {format_percentage(sec['compliance_score'])}")
            click.echo(f"  Security Incidents: {sec['security_incidents']}")
            click.echo()
        
    except Exception as e:
        print_error(f"Failed to get KPIs: {e}")
        sys.exit(1)

@report_group.command()
@click.argument('cluster_id')
@click.option('--period', '-p', default='30d', help='Analysis period')
@click.option('--output', '-o', help='Output file path')
@click.pass_context
def export(ctx, cluster_id, period, output):
    """Export comprehensive cluster report"""
    api_client = ctx.obj['auth'].api_client
    
    if not validate_cluster_id(cluster_id):
        print_error("Invalid cluster ID format")
        sys.exit(1)
    
    try:
        with show_progress("📊 Generating comprehensive report..."):
            # Get multiple reports
            cost_report = api_client.get_business_report(cluster_id, 'cost_optimization')
            perf_report = api_client.get_business_report(cluster_id, 'performance')
            security_report = api_client.get_business_report(cluster_id, 'security')
            
            # Combine into comprehensive report
            comprehensive_report = {
                'cluster_id': cluster_id,
                'period': period,
                'generated_at': datetime.now().isoformat(),
                'cost_analysis': cost_report,
                'performance_analysis': perf_report,
                'security_analysis': security_report,
                'summary': {
                    'total_cost': cost_report.get('executive_summary', {}).get('total_cost', 0),
                    'potential_savings': cost_report.get('executive_summary', {}).get('potential_savings', 0),
                    'efficiency_score': cost_report.get('executive_summary', {}).get('efficiency_score', 0),
                    'security_score': security_report.get('executive_summary', {}).get('security_score', 0)
                }
            }
        
        click.echo(f"📊 Comprehensive Report: {cluster_id}")
        click.echo(f"📅 Period: {period}")
        click.echo("=" * 60)
        
        # Display summary
        summary = comprehensive_report['summary']
        click.echo("📋 Executive Summary:")
        click.echo(f"  💰 Total Cost: {format_currency(summary['total_cost'])}")
        click.echo(f"  💸 Potential Savings: {format_currency(summary['potential_savings'])}")
        click.echo(f"  📈 Efficiency Score: {format_percentage(summary['efficiency_score'])}")
        click.echo(f"  🛡️  Security Score: {format_percentage(summary['security_score'])}")
        
        # Save to file if requested
        if output:
            save_json_file(comprehensive_report, output)
            print_success(f"Comprehensive report saved to {output}")
        else:
            print_info("Use --output to save report to file")
        
    except Exception as e:
        print_error(f"Failed to export report: {e}")
        sys.exit(1)

@report_group.command()
@click.argument('cluster_id')
@click.option('--period', '-p', default='30d', help='Analysis period')
@click.pass_context
def trends(ctx, cluster_id, period):
    """Analyze trends over time"""
    api_client = ctx.obj['auth'].api_client
    
    if not validate_cluster_id(cluster_id):
        print_error("Invalid cluster ID format")
        sys.exit(1)
    
    try:
        with show_progress("📈 Analyzing trends..."):
            trends_data = api_client.get_trend_analysis(cluster_id, period)
        
        click.echo(f"📈 Trend Analysis: {cluster_id}")
        click.echo(f"📅 Period: {period}")
        click.echo("=" * 50)
        
        # Cost trends
        if 'cost_trends' in trends_data:
            cost_trends = trends_data['cost_trends']
            click.echo("💰 Cost Trends:")
            for trend in cost_trends:
                change_icon = "📈" if trend['change'] > 0 else "📉"
                click.echo(f"  {change_icon} {trend['period']}: {format_currency(trend['cost'])} ({trend['change']}%)")
            click.echo()
        
        # Performance trends
        if 'performance_trends' in trends_data:
            perf_trends = trends_data['performance_trends']
            click.echo("⚡ Performance Trends:")
            for trend in perf_trends:
                click.echo(f"  📊 {trend['metric']}: {trend['value']} ({trend['change']}%)")
            click.echo()
        
        # Efficiency trends
        if 'efficiency_trends' in trends_data:
            eff_trends = trends_data['efficiency_trends']
            click.echo("📈 Efficiency Trends:")
            for trend in eff_trends:
                click.echo(f"  📊 {trend['metric']}: {format_percentage(trend['value'])} ({trend['change']}%)")
            click.echo()
        
        # Predictions
        if 'predictions' in trends_data:
            predictions = trends_data['predictions']
            click.echo("🔮 Predictions (Next 3 months):")
            for pred in predictions:
                click.echo(f"  📊 {pred['metric']}: {pred['predicted_value']} ({pred['confidence']}% confidence)")
        
    except Exception as e:
        print_error(f"Trend analysis failed: {e}")
        sys.exit(1) 