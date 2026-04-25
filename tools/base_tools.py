"""Base tool definitions for GenericAgent.

This module provides a set of built-in tools that agents can use,
including web search, file I/O, and shell command execution.
"""

import os
import subprocess
import json
from typing import Any


def read_file(path: str) -> str:
    """Read the contents of a file at the given path.

    Args:
        path: Absolute or relative path to the file.

    Returns:
        The file contents as a string, or an error message.
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return f"Error: File not found at path '{path}'"
    except PermissionError:
        return f"Error: Permission denied reading '{path}'"
    except Exception as e:
        return f"Error reading file: {e}"


def write_file(path: str, content: str) -> str:
    """Write content to a file, creating it or overwriting if it exists.

    Args:
        path: Absolute or relative path to the file.
        content: String content to write.

    Returns:
        A success or error message.
    """
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True) if os.path.dirname(path) else None
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Successfully wrote {len(content)} characters to '{path}'"
    except PermissionError:
        return f"Error: Permission denied writing to '{path}'"
    except Exception as e:
        return f"Error writing file: {e}"


def run_shell(command: str, timeout: int = 60) -> str:
    """Execute a shell command and return its output.

    Args:
        command: The shell command to run.
        timeout: Maximum seconds to wait before killing the process.
                 Increased default to 60s since 30s was too short for some builds.

    Returns:
        Combined stdout and stderr output, or an error message.
    """
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        output = ""
        if result.stdout:
            output += result.stdout
        if result.stderr:
            output += f"\n[stderr]\n{result.stderr}"
        if result.returncode != 0:
            output += f"\n[exit code: {result.returncode}]"
        return output.strip() or "(no output)"
    except subprocess.TimeoutExpired:
        return f"Error: Command timed out after {timeout} seconds"
    except Exception as e:
        return f"Error running command: {e}"


def list_directory(path: str = ".") -> str:
    """List files and directories at the given path.

    Args:
        path: Directory path to list. Defaults to current directory.

    Returns:
        A formatted directory listing or an error message.
    """
    try:
        entries = os.listdir(path)
        if not entries:
            return f"Directory '{path}' is empty."
        lines = []
        for entry in sorted(entries):
            full = os.path.join(path, entry)
            tag = "[dir]"
