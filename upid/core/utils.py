"""
Utility functions for UPID CLI
"""
import os
import json
import yaml
import base64
from pathlib import Path
from typing import Dict, Any, List, Optional
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich.text import Text
import click

console = Console()

def read_kubeconfig(file_path: str) -> str:
    """Read and encode kubeconfig file"""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
            return base64.b64encode(content.encode()).decode()
    except Exception as e:
        raise Exception(f"Failed to read kubeconfig file: {e}")

def validate_kubeconfig(file_path: str) -> bool:
    """Validate kubeconfig file"""
    try:
        with open(file_path, 'r') as f:
            config = yaml.safe_load(f)
            
        # Basic validation
        if not isinstance(config, dict):
            return False
        
        if 'apiVersion' not in config:
            return False
        
        if 'kind' not in config or config['kind'] != 'Config':
            return False
        
        return True
    except Exception:
        return False

def format_currency(amount: float, currency: str = 'USD') -> str:
    """Format currency amount"""
    if currency == 'USD':
        return f"${amount:,.2f}"
    elif currency == 'EUR':
        return f"€{amount:,.2f}"
    elif currency == 'GBP':
        return f"£{amount:,.2f}"
    else:
        return f"{amount:,.2f} {currency}"

def format_percentage(value: float) -> str:
    """Format percentage value"""
    return f"{value:.1f}%"

def format_duration(seconds: int) -> str:
    """Format duration in seconds to human readable string"""
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        minutes = seconds // 60
        return f"{minutes}m {seconds % 60}s"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{hours}h {minutes}m"

def format_bytes(bytes_value: int) -> str:
    """Format bytes to human readable string"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.1f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.1f} PB"

def create_table(title: str, headers: List[str]) -> Table:
    """Create a rich table"""
    table = Table(title=title, show_header=True, header_style="bold magenta")
    for header in headers:
        table.add_column(header)
    return table

def print_success(message: str):
    """Print success message"""
    console.print(f"✅ {message}", style="green")

def print_error(message: str):
    """Print error message"""
    console.print(f"❌ {message}", style="red")

def print_warning(message: str):
    """Print warning message"""
    console.print(f"⚠️  {message}", style="yellow")

def print_info(message: str):
    """Print info message"""
    console.print(f"ℹ️  {message}", style="blue")

def print_table(data: List[Dict[str, Any]], headers: List[str], title: str = None):
    """Print data as table"""
    table = create_table(title or "Data", headers)
    
    for row in data:
        table.add_row(*[str(row.get(header, '')) for header in headers])
    
    console.print(table)

def print_json(data: Dict[str, Any]):
    """Print data as formatted JSON"""
    console.print_json(data=data)

def print_panel(content: str, title: str = None, style: str = "blue"):
    """Print content in a panel"""
    panel = Panel(content, title=title, style=style)
    console.print(panel)

def show_progress(description: str):
    """Show progress spinner"""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task(description, total=None)
        yield progress

def confirm_action(message: str, default: bool = False) -> bool:
    """Confirm action with user"""
    return click.confirm(message, default=default)

def prompt_input(message: str, default: str = None) -> str:
    """Prompt for user input"""
    return click.prompt(message, default=default)

def prompt_choice(message: str, choices: List[str], default: str = None) -> str:
    """Prompt for choice from list"""
    return click.prompt(
        message,
        type=click.Choice(choices),
        default=default
    )

def validate_cluster_id(cluster_id: str) -> bool:
    """Validate cluster ID format"""
    import re
    # Basic validation - alphanumeric with hyphens and underscores
    pattern = r'^[a-zA-Z0-9_-]+$'
    return bool(re.match(pattern, cluster_id))

def validate_email(email: str) -> bool:
    """Validate email format"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_url(url: str) -> bool:
    """Validate URL format"""
    import re
    pattern = r'^https?://[^\s/$.?#].[^\s]*$'
    return bool(re.match(pattern, url))

def get_file_size(file_path: str) -> int:
    """Get file size in bytes"""
    try:
        return os.path.getsize(file_path)
    except OSError:
        return 0

def is_file_readable(file_path: str) -> bool:
    """Check if file is readable"""
    return os.path.isfile(file_path) and os.access(file_path, os.R_OK)

def ensure_directory(path: str):
    """Ensure directory exists"""
    Path(path).mkdir(parents=True, exist_ok=True)

def load_yaml_file(file_path: str) -> Dict[str, Any]:
    """Load YAML file"""
    try:
        with open(file_path, 'r') as f:
            return yaml.safe_load(f)
    except Exception as e:
        raise Exception(f"Failed to load YAML file: {e}")

def save_yaml_file(data: Dict[str, Any], file_path: str):
    """Save data to YAML file"""
    try:
        with open(file_path, 'w') as f:
            yaml.dump(data, f, default_flow_style=False)
    except Exception as e:
        raise Exception(f"Failed to save YAML file: {e}")

def load_json_file(file_path: str) -> Dict[str, Any]:
    """Load JSON file"""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        raise Exception(f"Failed to load JSON file: {e}")

def save_json_file(data: Dict[str, Any], file_path: str):
    """Save data to JSON file"""
    try:
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        raise Exception(f"Failed to save JSON file: {e}")

def calculate_cost_savings(current_cost: float, optimized_cost: float) -> Dict[str, Any]:
    """Calculate cost savings"""
    savings = current_cost - optimized_cost
    savings_percentage = (savings / current_cost) * 100 if current_cost > 0 else 0
    
    return {
        'current_cost': current_cost,
        'optimized_cost': optimized_cost,
        'savings': savings,
        'savings_percentage': savings_percentage
    }

def calculate_efficiency_score(utilization: float, waste: float) -> float:
    """Calculate efficiency score (0-100)"""
    # Higher utilization and lower waste = higher efficiency
    efficiency = (utilization * 0.7) + ((100 - waste) * 0.3)
    return max(0, min(100, efficiency))

def format_optimization_result(result: Dict[str, Any]) -> str:
    """Format optimization result for display"""
    lines = []
    
    if 'potential_savings' in result:
        lines.append(f"💰 Potential Savings: {format_currency(result['potential_savings'])}")
    
    if 'efficiency_score' in result:
        lines.append(f"📊 Efficiency Score: {format_percentage(result['efficiency_score'])}")
    
    if 'performance_impact' in result:
        lines.append(f"⚡ Performance Impact: {format_percentage(result['performance_impact'])}")
    
    if 'recommendations' in result:
        lines.append(f"🎯 Recommendations: {len(result['recommendations'])}")
    
    if 'zero_pod_opportunities' in result:
        opportunities = result['zero_pod_opportunities']
        lines.append(f"🔄 Zero-Pod Opportunities: {opportunities.get('scalable_pods_count', 0)}")
        lines.append(f"💰 Zero-Pod Savings: {format_currency(opportunities.get('total_potential_savings', 0))}")
    
    return "\n".join(lines)

def format_idle_analysis(analysis: Dict[str, Any]) -> str:
    """Format idle analysis for display"""
    lines = []
    
    lines.append(f"📦 Total Pods Analyzed: {len(analysis.get('idle_opportunities', []))}")
    lines.append(f"✅ Scalable to Zero: {analysis.get('scalable_pods_count', 0)}")
    lines.append(f"💰 Total Potential Savings: {format_currency(analysis.get('total_potential_savings', 0))}")
    
    if 'idle_patterns' in analysis:
        patterns = analysis['idle_patterns']
        lines.append(f"📊 Cluster Idle Time: {format_percentage(patterns.get('cluster_idle_percentage', 0))}")
        lines.append(f"⏱️  Avg Idle Duration: {format_duration(int(patterns.get('avg_cluster_idle_duration', 0) * 60))}")
    
    return "\n".join(lines)

def get_terminal_size() -> tuple:
    """Get terminal size"""
    try:
        import shutil
        return shutil.get_terminal_size()
    except Exception:
        return (80, 24)  # Default fallback

def truncate_text(text: str, max_length: int) -> str:
    """Truncate text to max length"""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."

def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe saving"""
    import re
    # Remove or replace unsafe characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Remove leading/trailing spaces and dots
    filename = filename.strip(' .')
    return filename or 'untitled' 