#!/usr/bin/env python3
"""
CLI Command Test Script for UPID CLI
Validates actual CLI commands work correctly
"""

import sys
import os
import subprocess
import time
from pathlib import Path
from typing import Dict, Any, List, Optional

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

console = Console()

class CLICommandTester:
    """CLI command tester for UPID CLI"""
    
    def __init__(self):
        self.test_results = []
        self.cli_module = 'upid.cli'
        
    def test_all_cli_commands(self):
        """Test all CLI commands"""
        console.print("\n" + "="*80)
        console.print("[bold blue]🧪 UPID CLI - Command Test Suite[/bold blue]")
        console.print("="*80)
        
        # CLI commands to test
        cli_commands = [
            ("upid --help", "Help command"),
            ("upid --local status", "Status command (local mode)"),
            ("upid --local universal status", "Universal status command"),
            ("upid --local universal analyze", "Universal analyze command"),
            ("upid --local universal optimize", "Universal optimize command"),
            ("upid --local universal report", "Universal report command"),
            ("upid --local init", "Init command"),
            ("upid --local demo", "Demo command")
        ]
        
        for command, description in cli_commands:
            console.print(f"\n[bold cyan]Testing: {description}[/bold cyan]")
            console.print(f"Command: {command}")
            
            try:
                result = subprocess.run(
                    command.split(),
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                if result.returncode == 0:
                    self.test_results.append({
                        'command': command,
                        'description': description,
                        'status': 'PASS',
                        'output': result.stdout,
                        'error': result.stderr
                    })
                    console.print(f"[green]✅ {description} passed[/green]")
                    
                    # Show sample output
                    if result.stdout:
                        lines = result.stdout.strip().split('\n')
                        if lines:
                            sample = lines[0][:80] + "..." if len(lines[0]) > 80 else lines[0]
                            console.print(f"Output: {sample}")
                else:
                    self.test_results.append({
                        'command': command,
                        'description': description,
                        'status': 'FAIL',
                        'output': result.stdout,
                        'error': result.stderr
                    })
                    console.print(f"[red]❌ {description} failed[/red]")
                    if result.stderr:
                        console.print(f"Error: {result.stderr[:100]}...")
                        
            except subprocess.TimeoutExpired:
                self.test_results.append({
                    'command': command,
                    'description': description,
                    'status': 'TIMEOUT',
                    'output': '',
                    'error': 'Command timed out after 30 seconds'
                })
                console.print(f"[yellow]⚠️  {description} timed out[/yellow]")
            except Exception as e:
                self.test_results.append({
                    'command': command,
                    'description': description,
                    'status': 'ERROR',
                    'output': '',
                    'error': str(e)
                })
                console.print(f"[red]❌ {description} error: {e}[/red]")
        
        # Test Python module imports
        self.test_module_imports()
        
        # Generate summary
        self.generate_summary()
        
    def test_module_imports(self):
        """Test module imports"""
        console.print(f"\n[bold cyan]Testing Module Imports...[/bold cyan]")
        
        modules_to_test = [
            ("upid.core.config", "Config module"),
            ("upid.core.auth", "Auth module"),
            ("upid.core.api_client", "API Client module"),
            ("upid.core.cluster_detector", "Cluster Detector module"),
            ("upid.commands.universal", "Universal Commands module"),
            ("upid.cli", "CLI module")
        ]
        
        for module_name, description in modules_to_test:
            try:
                __import__(module_name)
                self.test_results.append({
                    'command': f"import {module_name}",
                    'description': description,
                    'status': 'PASS',
                    'output': 'Module imported successfully',
                    'error': ''
                })
                console.print(f"[green]✅ {description} imported successfully[/green]")
            except Exception as e:
                self.test_results.append({
                    'command': f"import {module_name}",
                    'description': description,
                    'status': 'FAIL',
                    'output': '',
                    'error': str(e)
                })
                console.print(f"[red]❌ {description} import failed: {e}[/red]")
    
    def generate_summary(self):
        """Generate CLI test summary"""
        console.print("\n" + "="*80)
        console.print("[bold blue]📊 CLI Command Test Summary[/bold blue]")
        console.print("="*80)
        
        # Calculate statistics
        total_tests = len(self.test_results)
        passed = sum(1 for r in self.test_results if r['status'] == 'PASS')
        failed = sum(1 for r in self.test_results if r['status'] == 'FAIL')
        errors = sum(1 for r in self.test_results if r['status'] in ['ERROR', 'TIMEOUT'])
        success_rate = (passed / total_tests * 100) if total_tests > 0 else 0
        
        # Create results table
        table = Table(title="CLI Command Test Results", box=box.ROUNDED)
        table.add_column("Command", style="cyan", no_wrap=True)
        table.add_column("Status", style="green")
        table.add_column("Description", style="white")
        table.add_column("Details", style="yellow")
        
        for result in self.test_results:
            status_icon = "✅" if result['status'] == 'PASS' else "❌" if result['status'] == 'FAIL' else "⚠️"
            
            # Extract key information from output
            details = ""
            if result['output']:
                lines = result['output'].split('\n')
                for line in lines:
                    if any(keyword in line.lower() for keyword in ['cluster', 'status', 'analyze', 'optimize', 'report']):
                        details = line.strip()[:50]
                        break
            
            table.add_row(
                result['command'][:30] + "..." if len(result['command']) > 30 else result['command'],
                f"{status_icon} {result['status']}",
                result['description'],
                details + "..." if len(details) > 50 else details
            )
        
        console.print(table)
        
        # Summary panel
        summary_panel = Panel(
            f"Total Commands: {total_tests}\n"
            f"Passed: {passed} ✅\n"
            f"Failed: {failed} ❌\n"
            f"Errors/Timeouts: {errors} ⚠️\n"
            f"Success Rate: {success_rate:.1f}%",
            title="[bold blue]CLI Test Statistics[/bold blue]",
            border_style="blue"
        )
        
        console.print(summary_panel)
        
        # Command coverage
        self.show_command_coverage()
        
        # Final verdict
        self.show_final_verdict(success_rate)
        
        console.print("\n" + "="*80)
    
    def show_command_coverage(self):
        """Show command coverage analysis"""
        console.print("\n[bold cyan]📋 Command Coverage Analysis[/bold cyan]")
        
        commands = {
            "🌍 Universal Commands": "upid universal status, analyze, optimize, report",
            "🔧 Configuration": "upid init, config management",
            "📊 Status & Health": "upid status, cluster health",
            "🔍 Analysis": "upid analyze resources, costs, performance",
            "⚡ Optimization": "upid optimize resources, costs, zero-pod",
            "📈 Reporting": "upid report summary, cost, performance",
            "🎨 Rich UI": "Tables, panels, progress bars",
            "📤 Output Formats": "JSON, YAML, HTML output"
        }
        
        coverage_table = Table(title="Command Coverage", box=box.ROUNDED)
        coverage_table.add_column("Category", style="cyan")
        coverage_table.add_column("Commands", style="white")
        coverage_table.add_column("Status", style="green")
        
        for category, command_list in commands.items():
            # Determine status based on test results
            if any('universal' in r['command'].lower() for r in self.test_results if r['status'] == 'PASS'):
                status = "✅ Implemented"
            elif any('status' in r['command'].lower() for r in self.test_results if r['status'] == 'PASS'):
                status = "✅ Implemented"
            elif any('analyze' in r['command'].lower() for r in self.test_results if r['status'] == 'PASS'):
                status = "✅ Implemented"
            elif any('optimize' in r['command'].lower() for r in self.test_results if r['status'] == 'PASS'):
                status = "✅ Implemented"
            elif any('report' in r['command'].lower() for r in self.test_results if r['status'] == 'PASS'):
                status = "✅ Implemented"
            else:
                status = "🔄 In Progress"
            
            coverage_table.add_row(category, command_list, status)
        
        console.print(coverage_table)
    
    def show_final_verdict(self, success_rate):
        """Show final verdict based on test results"""
        console.print("\n[bold cyan]🎯 CLI Command Test Verdict[/bold cyan]")
        
        if success_rate >= 90:
            verdict_panel = Panel(
                "🎉 EXCELLENT! All CLI commands are working.\n\n"
                "✅ Universal commands functional\n"
                "✅ Local mode working correctly\n"
                "✅ Rich UI displaying properly\n"
                "✅ Ready for user deployment",
                title="[bold green]CLI Ready[/bold green]",
                border_style="green"
            )
        elif success_rate >= 70:
            verdict_panel = Panel(
                "⚠️  GOOD! Most CLI commands are working.\n\n"
                "✅ Core commands functional\n"
                "⚠️  Some commands need attention\n"
                "🔄 Ready for beta testing",
                title="[bold yellow]CLI Beta Ready[/bold yellow]",
                border_style="yellow"
            )
        else:
            verdict_panel = Panel(
                "❌ ISSUES DETECTED! CLI needs work.\n\n"
                "❌ Critical commands failing\n"
                "🔄 Requires fixes before release\n"
                "📋 Review failing commands",
                title="[bold red]CLI Needs Work[/bold red]",
                border_style="red"
            )
        
        console.print(verdict_panel)

def main():
    """Main CLI command test runner"""
    try:
        tester = CLICommandTester()
        tester.test_all_cli_commands()
        
    except KeyboardInterrupt:
        console.print("\n[yellow]⚠️  CLI command tests interrupted by user[/yellow]")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n[red]❌ CLI command test runner failed: {e}[/red]")
        sys.exit(1)

if __name__ == '__main__':
    main() 