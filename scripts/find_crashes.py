"""
Crash Risk Finder — Pass 1 Step 1.2
Scans all concept_template.py files and identifies:

  A) Empty-concat crash risk: classes where vertices_list may be empty
     (all geometry is inside if/for blocks, no unconditional append)
  B) float-in-range: range() calls where argument is a list element (param[0])
  C) Uninitialized variables: if/elif with no else before variable use
  D) Trailing comma on list assignment (makes it a tuple)

Output: scripts/crash_risks.md
"""

import ast
import os
import re
from collections import defaultdict

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CODE_DIR = os.path.join(REPO_ROOT, 'code')
OUTPUT_FILE = os.path.join(REPO_ROOT, 'scripts', 'crash_risks.md')


def get_source(category):
    path = os.path.join(CODE_DIR, category, 'concept_template.py')
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def find_float_in_range(source, category):
    """Find range(param[0]) patterns — param[0] is likely a float."""
    results = []
    for i, line in enumerate(source.splitlines(), 1):
        # match range(something[something]) but not range(int(...))
        if re.search(r'range\s*\([^)]*\[[^\]]*\][^)]*\)', line):
            if 'int(' not in line:
                results.append((category, i, line.strip()))
    return results


def find_trailing_comma_list(source, category):
    """
    Find single-line assignments where the entire list is on one line
    and ends with a trailing comma: var = [...],
    Excludes multi-line list continuations (no closing ] on same line as opening [,
    or the [ appears inside a function call argument).
    """
    results = []
    for i, line in enumerate(source.splitlines(), 1):
        stripped = line.strip()
        # Must be an assignment (contains =)
        # Must have both [ and ] on the same line
        # Must end with ], (trailing comma after closing bracket)
        # Must NOT be inside a function call argument (no open paren before [)
        if not re.search(r'\w+\s*=\s*\[', stripped):
            continue
        if not re.search(r'\]\s*,\s*$', stripped):
            continue
        # Exclude lines where [ is inside a function call (keyword arg like position=[...],)
        # These are valid multi-line call continuations
        if re.search(r'\w+\s*=\s*\[.*\]\s*,\s*$', stripped):
            # Check it's a standalone assignment, not a keyword argument
            # Keyword args appear after ( or , with no leading assignment target
            # A standalone assignment starts with an identifier followed by =
            if re.match(r'^\s*[a-zA-Z_]\w*\s*=\s*\[', line):
                # Make sure it's not a keyword argument (preceded by open paren context)
                # Simple heuristic: if the identifier before = contains a dot or [, skip
                lhs = re.match(r'^\s*([a-zA-Z_][\w\.\[\]]*)\s*=', line)
                if lhs and '(' not in lhs.group(1):
                    results.append((category, i, stripped))
    return results


def has_unconditional_append(func_node, source_lines):
    """
    Returns True if vertices_list.append(...) appears at the top level
    of the function body (not inside any if/for/while).
    """
    for node in func_node.body:
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
            call = node.value
            if (isinstance(call.func, ast.Attribute) and
                    call.func.attr == 'append' and
                    isinstance(call.func.value, ast.Name) and
                    call.func.value.id == 'vertices_list'):
                return True
    return False


def find_empty_concat_risk(source, category):
    """
    Find classes where vertices_list.append is never called unconditionally
    at the top level of __init__ — meaning all geometry is conditional.
    """
    results = []
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return results

    source_lines = source.splitlines()

    for node in ast.walk(tree):
        if not isinstance(node, ast.ClassDef):
            continue
        for item in node.body:
            if not (isinstance(item, ast.FunctionDef) and item.name == '__init__'):
                continue
            # Check if np.concatenate(vertices_list) is called
            has_concat = any(
                isinstance(n, ast.Call) and
                isinstance(n.func, ast.Attribute) and
                n.func.attr == 'concatenate'
                for n in ast.walk(item)
            )
            if not has_concat:
                continue
            # Check if any append is unconditional
            if not has_unconditional_append(item, source_lines):
                results.append((category, node.name, item.lineno))
    return results


def find_if_elif_no_else(source, category):
    """
    Find if/elif chains with no else where a variable is assigned in each branch
    — potential UnboundLocalError if no branch matches.
    Only flag cases inside __init__ methods.
    """
    results = []
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return results

    for cls_node in ast.walk(tree):
        if not isinstance(cls_node, ast.ClassDef):
            continue
        for func_node in cls_node.body:
            if not (isinstance(func_node, ast.FunctionDef) and func_node.name == '__init__'):
                continue
            for node in ast.walk(func_node):
                if not isinstance(node, ast.If):
                    continue
                # Check it has elif (orelse is another If) but no final else
                current = node
                has_elif = False
                while current.orelse:
                    if isinstance(current.orelse[0], ast.If):
                        has_elif = True
                        current = current.orelse[0]
                    else:
                        break  # has a real else
                else:
                    # No else at all
                    if has_elif:
                        # Collect variables assigned in the if/elif branches
                        assigned = set()
                        for branch_node in ast.walk(node):
                            if isinstance(branch_node, ast.Assign):
                                for t in branch_node.targets:
                                    if isinstance(t, ast.Name):
                                        assigned.add(t.id)
                        if assigned:
                            results.append((
                                category,
                                cls_node.name,
                                node.lineno,
                                sorted(assigned)
                            ))
    return results


def main():
    categories = sorted([
        d for d in os.listdir(CODE_DIR)
        if os.path.isdir(os.path.join(CODE_DIR, d))
        and os.path.exists(os.path.join(CODE_DIR, d, 'concept_template.py'))
    ])

    all_float_range = []
    all_trailing_comma = []
    all_empty_concat = []
    all_no_else = []

    for cat in categories:
        source = get_source(cat)
        all_float_range.extend(find_float_in_range(source, cat))
        all_trailing_comma.extend(find_trailing_comma_list(source, cat))
        all_empty_concat.extend(find_empty_concat_risk(source, cat))
        all_no_else.extend(find_if_elif_no_else(source, cat))

    lines = []
    lines.append('# Crash Risk Report — Pass 1 Step 1.2\n')
    lines.append('---\n')

    # A) Empty concat
    lines.append(f'## A) Empty-concat crash risk ({len(all_empty_concat)} classes)\n')
    lines.append('All geometry is conditional — `np.concatenate([])` will crash if all flags are off.\n')
    for cat, cls, lineno in sorted(all_empty_concat):
        lines.append(f'- `{cat}/{cls}` (line {lineno})')
    lines.append('')

    # B) Float in range
    lines.append(f'## B) float in range() ({len(all_float_range)} occurrences)\n')
    for cat, lineno, text in sorted(all_float_range):
        lines.append(f'- `{cat}` line {lineno}: `{text}`')
    lines.append('')

    # C) if/elif no else
    lines.append(f'## C) if/elif with no else — potential UnboundLocalError ({len(all_no_else)} cases)\n')
    for cat, cls, lineno, assigned in sorted(all_no_else):
        lines.append(f'- `{cat}/{cls}` line {lineno}: assigns {assigned}')
    lines.append('')

    # D) Trailing comma
    lines.append(f'## D) Trailing comma on list — makes it a tuple ({len(all_trailing_comma)} occurrences)\n')
    for cat, lineno, text in sorted(all_trailing_comma):
        lines.append(f'- `{cat}` line {lineno}: `{text}`')
    lines.append('')

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    print(f'Done.')
    print(f'  A) {len(all_empty_concat)} empty-concat risks')
    print(f'  B) {len(all_float_range)} float-in-range occurrences')
    print(f'  C) {len(all_no_else)} if/elif-no-else cases')
    print(f'  D) {len(all_trailing_comma)} trailing comma cases')
    print(f'  Results written to {OUTPUT_FILE}')


if __name__ == '__main__':
    main()
