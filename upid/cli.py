"""
UPID CLI - Main entry point
"""
import click
import sys
from pathlib import Path
from upid.core.config import Config
from upid.core.auth import AuthManager
from upid.core.utils import print_error, print_info, print_success
from upid.commands import auth, cluster, optimize, analyze, deploy, report, config

@click.group()
@click.version_option(version='1.0.0', prog_name='UPID')
@click.option('--config', '-c', help='Path to config file')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
@click.option('--output', '-o', type=click.Choice(['table', 'json', 'yaml']), 
              default='table', help='Output format')
@click.pass_context
def cli(ctx, config, verbose, output):
    """UPID - Kubernetes Resource Optimization Platform
    
    Optimize your Kubernetes clusters with mathematical precision.
    Includes zero-pod scaling detection and automated cost optimization.
    
    Examples:
        upid login --email admin@company.com --password secure123
        upid cluster register --name production-cluster --kubeconfig ~/.kube/config
        upid optimize analyze cluster-123 --show-idle
        upid optimize idle cluster-123
    """
    ctx.ensure_object(dict)
    
    # Initialize configuration
    try:
        ctx.obj['config'] = Config(config_path=config)
    except Exception as e:
        print_error(f"Failed to load configuration: {e}")
        sys.exit(1)
    
    # Set verbose mode
    if verbose:
        ctx.obj['config'].set_verbose(True)
    
    # Set output format
    ctx.obj['config'].set_output_format(output)
    
    # Initialize auth manager
    try:
        auth_manager = AuthManager(ctx.obj['config'])
        ctx.obj['auth'] = auth_manager
    except Exception as e:
        print_error(f"Failed to initialize authentication: {e}")
        sys.exit(1)
    
    # Check if user is authenticated for protected commands
    if ctx.invoked_subcommand not in ['login', 'version', 'config']:
        if not auth_manager.is_authenticated():
            print_error("Not authenticated. Please run 'upid login' first.")
            print_info("Use 'upid login --help' for authentication options.")
            sys.exit(1)

# Register command groups
cli.add_command(auth.auth_group)
cli.add_command(cluster.cluster_group)
cli.add_command(optimize.optimize_group)
cli.add_command(analyze.analyze_group)
cli.add_command(deploy.deploy_group)
cli.add_command(report.report_group)
cli.add_command(config.config_group)

@cli.command()
def version():
    """Show UPID version and information"""
    from upid import __version__, __author__, __email__
    
    click.echo(f"UPID CLI Version: {__version__}")
    click.echo(f"Author: {__author__}")
    click.echo(f"Email: {__email__}")
    click.echo("Kubernetes Resource Optimization Platform")
    click.echo("With Zero-Pod Scaling Detection")

@cli.command()
@click.pass_context
def status(ctx):
    """Show UPID status and configuration"""
    config = ctx.obj['config']
    auth_manager = ctx.obj['auth']
    
    click.echo("🔍 UPID Status")
    click.echo("=" * 50)
    
    # Authentication status
    if auth_manager.is_authenticated():
        user_email = auth_manager.get_user_email()
        user_org = auth_manager.get_user_organization()
        print_success(f"Authenticated as: {user_email}")
        if user_org:
            print_info(f"Organization: {user_org}")
    else:
        print_error("Not authenticated")
    
    # Configuration
    click.echo(f"\n⚙️  Configuration:")
    click.echo(f"  API URL: {config.get_api_url()}")
    click.echo(f"  API Version: {config.get_api_version()}")
    click.echo(f"  Default Cluster: {config.get_default_cluster() or 'None'}")
    click.echo(f"  Optimization Strategy: {config.get_optimization_strategy()}")
    click.echo(f"  Safety Level: {config.get_safety_level()}")
    click.echo(f"  Cost Model: {config.get_cost_model()}")
    click.echo(f"  Currency: {config.get_currency()}")
    
    # System health
    try:
        api_client = auth_manager.api_client
        health = api_client.health_check()
        print_success("API Health: Connected")
        if 'version' in health:
            click.echo(f"  API Version: {health['version']}")
    except Exception as e:
        print_error(f"API Health: {e}")

@cli.command()
@click.pass_context
def init(ctx):
    """Initialize UPID configuration"""
    config = ctx.obj['config']
    
    click.echo("🚀 Initializing UPID Configuration")
    click.echo("=" * 40)
    
    # Prompt for configuration
    api_url = click.prompt(
        "Enter UPID API URL",
        default=config.get_api_url(),
        type=str
    )
    config.set('api_url', api_url)
    
    optimization_strategy = click.prompt(
        "Choose optimization strategy",
        type=click.Choice(['balanced', 'cost-focused', 'performance-focused', 'safety-focused']),
        default=config.get_optimization_strategy()
    )
    config.set('optimization_strategy', optimization_strategy)
    
    safety_level = click.prompt(
        "Choose safety level",
        type=click.Choice(['strict', 'moderate', 'aggressive']),
        default=config.get_safety_level()
    )
    config.set('safety_level', safety_level)
    
    cost_model = click.prompt(
        "Choose cost model",
        type=click.Choice(['aws', 'gcp', 'azure', 'generic']),
        default=config.get_cost_model()
    )
    config.set('cost_model', cost_model)
    
    currency = click.prompt(
        "Choose currency",
        type=click.Choice(['USD', 'EUR', 'GBP']),
        default=config.get_currency()
    )
    config.set('currency', currency)
    
    print_success("Configuration initialized successfully!")
    print_info("Run 'upid login' to authenticate with UPID platform")

if __name__ == '__main__':
    cli() 