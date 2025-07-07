"""
Authentication commands for UPID CLI
"""
import click
import sys
from upid.core.utils import print_success, print_error, print_info, validate_email

@click.group()
def auth_group():
    """Authentication and authorization commands"""
    pass

@auth_group.command()
@click.option('--email', '-e', required=True, help='User email')
@click.option('--password', '-p', required=True, help='User password')
@click.option('--server', '-s', help='UPID server URL')
@click.pass_context
def login(ctx, email, password, server):
    """Login to UPID platform"""
    auth_manager = ctx.obj['auth']
    
    # Validate email
    if not validate_email(email):
        print_error("Invalid email format")
        sys.exit(1)
    
    try:
        token = auth_manager.login(email, password, server)
        print_success(f"Successfully logged in as {email}")
        print_info(f"Token stored in {auth_manager.config.config_dir}")
    except Exception as e:
        print_error(f"Login failed: {e}")
        sys.exit(1)

@auth_group.command()
@click.pass_context
def logout(ctx):
    """Logout from UPID platform"""
    auth_manager = ctx.obj['auth']
    auth_manager.logout()
    print_success("Successfully logged out")

@auth_group.command()
@click.pass_context
def status(ctx):
    """Check authentication status"""
    auth_manager = ctx.obj['auth']
    
    if auth_manager.is_authenticated():
        user = auth_manager.get_current_user()
        print_success(f"Authenticated as {user.get('email', 'Unknown')}")
        
        if user.get('organization'):
            print_info(f"Organization: {user['organization']}")
        
        roles = auth_manager.get_user_roles()
        if roles:
            print_info(f"Roles: {', '.join(roles)}")
    else:
        print_error("Not authenticated")

@auth_group.command()
@click.pass_context
def profile(ctx):
    """Get user profile information"""
    auth_manager = ctx.obj['auth']
    
    try:
        user = auth_manager.get_current_user()
        
        click.echo("👤 User Profile")
        click.echo("=" * 30)
        click.echo(f"Email: {user.get('email', 'N/A')}")
        click.echo(f"Name: {user.get('name', 'N/A')}")
        click.echo(f"Organization: {user.get('organization', 'N/A')}")
        click.echo(f"Roles: {', '.join(user.get('roles', []))}")
        click.echo(f"Permissions: {', '.join(user.get('permissions', []))}")
        
    except Exception as e:
        print_error(f"Failed to get profile: {e}")
        sys.exit(1)

@auth_group.command()
@click.pass_context
def refresh(ctx):
    """Refresh authentication token"""
    auth_manager = ctx.obj['auth']
    
    try:
        token = auth_manager.refresh_token()
        print_success("Token refreshed successfully")
    except Exception as e:
        print_error(f"Token refresh failed: {e}")
        sys.exit(1) 