#!/usr/bin/env python3
import os
import sys
from pathlib import Path
import io

def print_directory_structure(startpath, exclude_dirs=None, file=sys.stdout):
    """
    Print the directory structure starting from startpath.
    
    Args:
        startpath (str): The root directory to start from
        exclude_dirs (list, optional): List of directory names to exclude
        file (file-like object, optional): File to write output to
    """
    if exclude_dirs is None:
        exclude_dirs = ['.git', '.venv', '__pycache__', '.DS_Store']
    
    for root, dirs, files in os.walk(startpath):
        # Filter out excluded directories
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * level
        print(f"{indent}{os.path.basename(root)}/", file=file)
        
        sub_indent = ' ' * 4 * (level + 1)
        for file_name in sorted(files):
            if file_name not in exclude_dirs and not file_name.startswith('.'):
                file_path = os.path.join(root, file_name)
                size = os.path.getsize(file_path)
                size_str = f"({size} bytes)" if size < 1024 else f"({size/1024:.1f} KB)"
                print(f"{sub_indent}{file_name} {size_str}", file=file)

def save_structure_to_rule_file():
    """Save the project structure to a rule file in .cursor/rules directory."""
    # Ensure the rules directory exists
    os.makedirs(".cursor/rules", exist_ok=True)
    
    # Use a fixed filename
    rule_file_path = ".cursor/rules/project-structure.mdc"
    
    with open(rule_file_path, "w") as rule_file:
        # Write header
        
        # Write project structure
        rule_file.write("## Directory Structure\n\n```\n")
        buffer = io.StringIO()
        print_directory_structure(".", file=buffer)
        rule_file.write(buffer.getvalue())
        rule_file.write("```\n\n")
        

    print(f"Project structure saved to: {rule_file_path}")
    return rule_file_path

if __name__ == "__main__":
    print("Current Project Structure:")
    print("==========================")
    print_directory_structure(".")
    
    # Save structure to rule file
    rule_file = save_structure_to_rule_file()
