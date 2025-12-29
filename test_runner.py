import os
import subprocess
import sys
from rich.console import Console
from ai_debugger import AIDebugger

console = Console()

class TestRunner:
    def __init__(self):
        self.project_root = os.path.dirname(os.path.abspath(__file__))
        self.reports_dir = os.path.join(self.project_root, "reports")
        self.app_dir = os.path.join(self.project_root, "app")
        self.tests_dir = os.path.join(self.project_root, "tests")
        
        if not os.path.exists(self.reports_dir):
            os.makedirs(self.reports_dir)

    def run_tests(self, report_name="test_report.txt"):
        report_path = os.path.join(self.reports_dir, report_name)
        console.print(f"[bold yellow]Running tests... Outputting to {report_name}[/bold yellow]")
        
        # Run pytest and capture output
        result = subprocess.run(
            [sys.executable, "-m", "pytest", self.tests_dir],
            capture_output=True,
            text=True
        )
        
        # Save output
        with open(report_path, "w") as f:
            f.write(result.stdout)
            f.write(result.stderr)
            
        if result.returncode == 0:
            console.print("[bold green]All tests passed! ✅[/bold green]")
            return True, report_path
        else:
            console.print("[bold red]Tests failed! ❌[/bold red]")
            console.print(result.stdout)
            return False, report_path

    def orchestrate(self):
        console.print("[bold blue]Starting Automation Pipeline...[/bold blue]")
        
        # 1. Run Initial Tests
        success, report_path = self.run_tests("initial_test_report.txt")
        
        if success:
            console.print("[bold green]No bugs found. Exiting.[/bold green]")
            return

        # Show the failures
        console.print("\n[bold red]💀 PRE-FIX TEST FAILURES:[/bold red]")
        with open(report_path, "r") as f:
            console.print(f.read(), style="red dim")

        # 2. AI Debugging
        console.print("\n[bold purple]Initiating AI Debugging Protocol... 🤖[/bold purple]")
        debugger = AIDebugger()
        
        target_file = os.path.join(self.app_dir, "buggy_app.py")
        
        # Read code BEFORE fix
        with open(target_file, "r") as f:
            original_code = f.readlines()

        fix_success = debugger.fix_code(target_file, report_path)
        
        if not fix_success:
            console.print("[bold red]AI failed to apply fixes. Exiting.[/bold red]")
            return

        # Read code AFTER fix
        with open(target_file, "r") as f:
            fixed_code = f.readlines()

        # Generate and show diff
        import difflib
        console.print("\n[bold cyan]🔍 AI CODE FIXES (Diff):[/bold cyan]")
        diff = difflib.unified_diff(
            original_code, 
            fixed_code, 
            fromfile='buggy_app.py (Before)', 
            tofile='buggy_app.py (After)',
            lineterm=''
        )
        
        diff_text = "\n".join(list(diff))
        if diff_text:
            from rich.syntax import Syntax
            syntax = Syntax(diff_text, "diff", theme="monokai", line_numbers=True)
            console.print(syntax)
        else:
            console.print("[yellow]No changes detected in the file (AI might have failed to modify).[/yellow]")

        # 3. Re-run Tests
        console.print("\n[bold blue]Re-running tests after AI Fix...[/bold blue]")
        success_final, final_report_path = self.run_tests("final_test_report.txt")
        
        if success_final:
            console.print("\n[bold green]🎉 SUCCESS: AI fixed the code and all tests passed![/bold green]")
        else:
            console.print("\n[bold red]💀 FAILURE: Tests still failing after AI fix. Check final_test_report.txt[/bold red]")

if __name__ == "__main__":
    runner = TestRunner()
    runner.orchestrate()
