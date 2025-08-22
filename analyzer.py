import subprocess
import re
import os


SUPPORTED_EXTENSIONS = {
    '.py': 'Python',
    '.js': 'JavaScript',
    '.ts': 'TypeScript',
    '.java': 'Java',
    '.cpp': 'C++',
    '.c': 'C',
    '.cs': 'C#',
    '.rb': 'Ruby',
    '.php': 'PHP',
    '.go': 'Go',
    '.rs': 'Rust',
    '.sh': 'Shell',
    '.swift': 'Swift',
    '.kt': 'Kotlin'
}


def strip_ansi_codes(text):
    ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', text)

def clean_flow_output(output):
    cleaned_lines = []
    seen_start = False

    for line in output.splitlines():
        # Keep only the first START
        if line.strip() == '> START':
            if not seen_start:
                cleaned_lines.append(line)
                seen_start = True
            continue
        
        # Keep other meaningful steps
        if line.strip() and line.strip() != '> START':
            cleaned_lines.append(line)
    
    return "\n".join(cleaned_lines)


def generate_project_summary(code: str) -> str:
    prompt = f"""
You are a senior software engineer.
Do not inspect the current directory or assume access to the file system.
You will be given a codebase consisting of multiple files.  
Only use the provided code to perform your analysis.

Your task is to review the codebase and provide a high-level technical summary.

Summarize the purpose and structure of the entire project:
- Start with "Project Understanding": what the project does
- Describe its main components (modules, classes, functions)
- Explain how the components interact
- Outline the main data flows
- If applicable, describe any APIs, UIs, or database interactions
- Mention any notable design patterns or architectural choices

Only output the summary. Do not include flowcharts or raw code.
project:
{code}
"""


    try:
        result = subprocess.run(
            ["q", "chat"],
            input=prompt,
            capture_output=True,
            text=True,
            check=True
        )
        return strip_ansi_codes(result.stdout.strip())
    except subprocess.CalledProcessError as e:
        return f"[Summary generation failed] {e.stderr}"




def analyze_code(code: str, language: str = "Python") -> str:
    if not code.strip():
        return "<Empty code provided>"

    prompt = f"""
You are an advanced code analysis tool.

Analyze the following {language} code and return the following three sections only:

1. FLOW CHART:
  - A simple flow chart diagram showing the function call sequence and control flow.
  - Use clear text-based indentation or arrows (→) to show flow.

2. SECURITY RISKS:
  - List any security vulnerabilities, dangerous patterns, or bad practices found in the code.
  - For each issue, explain why it's a risk.

3. PERFORMANCE BOTTLENECKS:
  - Identify any parts of the code that may cause performance issues (e.g. inefficient loops, blocking I/O).
  - Suggest how to improve or refactor those sections.

DO NOT include any unnecessary commentary, greetings, or unrelated information.
Respond with the three sections clearly separated by titles.

Code to analyze:
{code}
"""


    try:
        result = subprocess.run(
            ["q", "chat"],
            input=prompt,
            capture_output=True,
            text=True,
            check=True
        )
        output = strip_ansi_codes(result.stdout.strip())
        print(output)
        cleaned = clean_flow_output(output)
        return cleaned or "<No function calls found>"
    except subprocess.CalledProcessError as e:
        return f"Error analyzing code: {e.stderr}"


def analyze_folder(folder_path):
    all_flows = []
    all_code = []

    for root, _, files in os.walk(folder_path):
        for f in files:
            ext = os.path.splitext(f)[-1]
            language = SUPPORTED_EXTENSIONS.get(ext.lower())
            if language:
                file_path = os.path.join(root, f)
                try:
                    with open(file_path, "r", encoding="utf-8") as code_file:
                        code = code_file.read()
                        all_code.append(f"# File: {f}\n{code}")
                        flow = analyze_code(code, language=language)
                        if flow:
                            all_flows.append(f"// From {f}\n{flow}\n")
                except Exception as e:
                    all_flows.append(f"// From {f}\nError: {e}\n")

    full_code = "\n\n".join(all_code)
    summary = generate_project_summary(full_code)

    return summary + "\n\n" + "\n".join(all_flows)
