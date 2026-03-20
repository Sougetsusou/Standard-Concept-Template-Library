#!/usr/bin/env python3
"""
Extract classes from all concept_template.py files and classify them by semantic type.
"""

import os
import re
import ast
from pathlib import Path
from collections import defaultdict

def extract_class_info(file_path):
    """
    Extract all class definitions and their semantic values from a Python file.
    Returns a list of tuples: (class_name, class_code, semantic_value)
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    class_info_list = []
    
    try:
        tree = ast.parse(content)
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                class_name = node.name
                
                # Extract class code
                class_start_line = node.lineno - 1
                class_end_line = node.end_lineno
                class_code = '\n'.join(content.split('\n')[class_start_line:class_end_line])
                
                # Find semantic value
                semantic_value = None
                for item in ast.walk(node):
                    if isinstance(item, ast.Assign):
                        for target in item.targets:
                            if isinstance(target, ast.Attribute):
                                if (isinstance(target.value, ast.Name) and 
                                    target.value.id == 'self' and 
                                    target.attr == 'semantic'):
                                    if isinstance(item.value, ast.Constant):
                                        semantic_value = item.value.value
                                    elif isinstance(item.value, ast.Str):  # Python 3.7 compatibility
                                        semantic_value = item.value.s
                
                if semantic_value:
                    class_info_list.append((class_name, class_code, semantic_value))
    
    except SyntaxError as e:
        print(f"Syntax error in {file_path}: {e}")
    
    return class_info_list


def extract_imports(file_path):
    """
    Extract all import statements from the beginning of the file.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    imports = []
    for line in content.split('\n'):
        stripped = line.strip()
        if stripped.startswith('import ') or stripped.startswith('from '):
            imports.append(line)
        elif stripped and not stripped.startswith('#'):
            # Stop at the first non-import, non-comment line
            if not any(stripped.startswith(x) for x in ['import ', 'from ']):
                break
    
    return imports


def main():
    # Base directory
    base_dir = Path(__file__).parent.parent / 'code'
    output_dir = Path(__file__).parent.parent / 'filtered_template'
    
    # Dictionary to store classes by semantic type
    semantic_classes = defaultdict(list)
    
    # Common imports (collect from first file)
    common_imports = set()
    
    # Find all concept_template.py files
    concept_files = list(base_dir.glob('*/concept_template.py'))
    
    print(f"Found {len(concept_files)} concept_template.py files")
    
    # Process each file
    for file_path in concept_files:
        folder_name = file_path.parent.name
        print(f"Processing {folder_name}/concept_template.py...")
        
        # Extract imports
        imports = extract_imports(file_path)
        common_imports.update(imports)
        
        # Extract class information
        class_info_list = extract_class_info(file_path)
        
        for class_name, class_code, semantic_value in class_info_list:
            semantic_classes[semantic_value].append({
                'class_name': class_name,
                'class_code': class_code,
                'source_folder': folder_name
            })
            print(f"  - {class_name} -> {semantic_value}")
    
    # Create output directory
    output_dir.mkdir(exist_ok=True)
    
    # Convert common imports to sorted list
    common_imports = sorted(list(common_imports))
    
    # Write files for each semantic type
    for semantic_value, classes in semantic_classes.items():
        semantic_dir = output_dir / semantic_value
        semantic_dir.mkdir(exist_ok=True)
        
        output_file = semantic_dir / f'{semantic_value.lower()}_templates.py'
        
        with open(output_file, 'w', encoding='utf-8') as f:
            # Write header comment
            f.write(f'"""\n')
            f.write(f'{semantic_value} Templates\n')
            f.write(f'Automatically extracted from concept_template.py files\n')
            f.write(f'Contains {len(classes)} class(es)\n')
            f.write(f'"""\n\n')
            
            # Write imports
            for imp in common_imports:
                f.write(f'{imp}\n')
            f.write('\n\n')
            
            # Write each class
            for i, class_info in enumerate(classes):
                if i > 0:
                    f.write('\n\n')
                
                f.write(f'# Source: {class_info["source_folder"]}/concept_template.py\n')
                f.write(class_info['class_code'])
                f.write('\n')
        
        print(f"\nCreated {output_file} with {len(classes)} classes")
    
    # Create a summary file
    summary_file = output_dir / 'classification_summary.txt'
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write('Template Classification Summary\n')
        f.write('=' * 50 + '\n\n')
        
        for semantic_value, classes in sorted(semantic_classes.items()):
            f.write(f'{semantic_value}: {len(classes)} classes\n')
            for class_info in classes:
                f.write(f'  - {class_info["class_name"]} (from {class_info["source_folder"]})\n')
            f.write('\n')
    
    print(f"\nCreated summary file: {summary_file}")
    print(f"\nTotal semantic types: {len(semantic_classes)}")
    print(f"Total classes extracted: {sum(len(classes) for classes in semantic_classes.values())}")


if __name__ == '__main__':
    main()
