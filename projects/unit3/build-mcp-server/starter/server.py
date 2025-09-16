#!/usr/bin/env python3
"""
Module 1: Basic MCP Server - Starter Code
TODO: Implement tools for analyzing git changes and suggesting PR templates
"""

import json
import subprocess
from pathlib import Path

from mcp.server.fastmcp import FastMCP

# Initialize the FastMCP server
mcp = FastMCP("pr-agent")

# PR template directory (shared across all modules)
TEMPLATES_DIR = Path(__file__).parent.parent.parent / "templates"
MAX_DIFF_LINES = 500
@mcp.tool()
async def analyze_file_changes(base_branch: str = "main", include_diff: bool = True) -> str:
    """Get the full diff and list of changed files in the current git repository.

    Args:
        base_branch: Base branch to compare against (default: main)
        include_diff: Include the full diff content (default: true)
    """
    # Try to get working directory from context, fallback to current directory
    try:
        context = mcp.get_context()
        roots_result = await context.session.list_roots()
        working_dir = roots_result.roots[0].uri.path
    except (ValueError, AttributeError, IndexError):
        # Context not available (e.g., in tests) - use current directory
        working_dir = "."

    result = {
        "changed_files": [],
        "diff": "",
        "warning": None
    }

    try:
        # Get list of changed files
        files_process = subprocess.run(
            ["git", "diff", "--name-only", base_branch],
            cwd=working_dir,
            capture_output=True,
            text=True,
            check=True
        )
        result["changed_files"] = files_process.stdout.strip().splitlines()

        if include_diff:
            # Get full diff output, handling potential size issues
            diff_process = subprocess.Popen(
                ["git", "diff", base_branch],
                cwd=working_dir,
                stdout=subprocess.PIPE,
                text=True
            )

            diff_lines = []
            line_count = 0
            truncated = False

            while True:
                line = diff_process.stdout.readline()
                if not line:
                    break
                diff_lines.append(line)
                line_count += 1
                if line_count > MAX_DIFF_LINES:
                    truncated = True
                    break

            # Handle remaining output and wait for process to finish
            diff_process.stdout.close()
            diff_process.wait()

            if truncated:
                diff_lines.append(f"\n...Diff truncated after {MAX_DIFF_LINES} lines to prevent token limit errors.")
                result["warning"] = "Diff output was truncated due to its large size."

            result["diff"] = "".join(diff_lines)

    except subprocess.CalledProcessError as e:
        return json.dumps({"error": e.stderr.strip()})
    except FileNotFoundError:
        return json.dumps({"error": "Git command not found. Is Git installed and in your PATH?"})
    
    return json.dumps(result, indent=2)


@mcp.tool()
async def get_pr_templates() -> str:
    """List available PR templates with their content."""
    templates = []
    try:
        for template_file in TEMPLATES_DIR.glob("*.md"):
            templates.append({
                "name": template_file.stem,
                "template": template_file.read_text()
            })
    except FileNotFoundError:
        return json.dumps({"error": f"Templates directory not found at: {TEMPLATES_DIR}"})
    
    return json.dumps(templates, indent=2)


@mcp.tool()
async def suggest_template(changes_summary: str, change_type: str) -> str:
    """Let Claude analyze the changes and suggest the most appropriate PR template.
    
    Args:
        changes_summary: Your analysis of what the changes do
        change_type: The type of change you've identified (bug, feature, docs, refactor, test, etc.)
    """
    # Mapping of identified change types to template filenames
    # Assumes templates are named accordingly, e.g., 'feature.md', 'bugfix.md'
    template_map = {
        "feature": "feature",
        "bug": "bugfix",
        "bugfix": "bugfix",
        "docs": "documentation",
        "documentation": "documentation",
        "refactor": "refactor",
        "test": "tests",
        "tests": "tests",
    }
    
    # Clean and normalize the change_type
    normalized_type = change_type.lower().strip()
    
    suggested_template = template_map.get(normalized_type)
    
    if suggested_template:
        return json.dumps({"recommended_template": f"{suggested_template}.md"})
    else:
        # Fallback to a generic template or provide guidance
        return json.dumps({"recommended_template": "default.md", "suggestion": "No specific template found for the identified change type."})

if __name__ == "__main__":
    mcp.run()
