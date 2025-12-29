import os
import sys
from dotenv import load_dotenv
from groq import Groq
from rich.console import Console

load_dotenv()

console = Console()

class AIDebugger:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        self.model = os.getenv("GROQ_MODEL", "llama3-8b-8192")
        
        if not self.api_key:
            console.print("[bold red]Error: GROQ_API_KEY not found in environment variables.[/bold red]")
            # In a real scenario, we might raise an error, but for this structure we'll just warn
            # sys.exit(1)
        
        try:
            self.client = Groq(api_key=self.api_key)
        except Exception as e:
            self.client = None
            console.print(f"[bold red]Failed to initialize Groq client: {e}[/bold red]")

    def fix_code(self, source_file_path, report_file_path):
        if not self.client:
            console.print("[bold red]Cannot run AI Debugger without valid Groq client.[/bold red]")
            return False

        try:
            with open(source_file_path, 'r') as f:
                source_code = f.read()
            
            with open(report_file_path, 'r') as f:
                test_report = f.read()
            
            console.print(f"[bold blue]Sending {source_file_path} and test report to Groq AI ({self.model})...[/bold blue]")

            prompt = f"""
You are an expert Python developer and QA automation specialist.
Your task is to fix the following Python file which fails the provided tests.

SOURCE CODE ({source_file_path}):
{source_code}

TEST FAILURE REPORT:
{test_report}

INSTRUCTIONS:
1. Analyze the failing tests and the source code.
2. Fix the logical errors, edge cases, and missing validations in the source code.
3. Return ONLY the COMPLETE corrected Python code.
4. Do NOT verify with explanations.
5. Do NOT include markdown code block markers (like ```python ... ```). Return raw code only.
"""

            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model=self.model,
                temperature=0.1, # Low temperature for more deterministic/correct code
            )

            fixed_code = chat_completion.choices[0].message.content.strip()
            
            # Clean up potential markdown formatting if the model disregards instructions
            if fixed_code.startswith("```python"):
                fixed_code = fixed_code.replace("```python", "", 1)
            if fixed_code.startswith("```"):
                fixed_code = fixed_code.replace("```", "", 1)
            if fixed_code.endswith("```"):
                fixed_code = fixed_code.rsplit("```", 1)[0]
            
            fixed_code = fixed_code.strip()

            # Backup original file just in case (optional, but good practice)
            # os.rename(source_file_path, source_file_path + ".bak")

            with open(source_file_path, 'w') as f:
                f.write(fixed_code)
            
            console.print(f"[bold green]Successfully patched {source_file_path} with AI-generated fix.[/bold green]")
            return True

        except Exception as e:
            console.print(f"[bold red]An error occurred during AI debugging: {e}[/bold red]")
            return False

if __name__ == "__main__":
    # Helper to run standalone
    if len(sys.argv) < 3:
        print("Usage: python ai_debugger.py <source_file> <report_file>")
    else:
        debugger = AIDebugger()
        debugger.fix_code(sys.argv[1], sys.argv[2])
