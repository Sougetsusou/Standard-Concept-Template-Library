"""
Apply int() wrap to all range(param[0]) calls where param[0] is a float.
Transforms: range(expr[n]) -> range(int(expr[n]))
            range(expr[n] - k) -> range(int(expr[n]) - k)
            range(k + expr[n]) -> range(int(k + expr[n]))  [handled by broader pattern]

Only touches concept_template.py files.
Skips lines that already have int(...) wrapping.
"""

import re
import os

REPO = '/Users/charly/VScodeProjects/Research/Standard-Concept-Template-Library'
CODE_DIR = os.path.join(REPO, 'code')

# Match range(...) where the argument contains a subscript (param[n])
# but does NOT already have int() wrapping
PATTERN = re.compile(r'range\(([^)]*\[[^\]]*\][^)]*)\)')

def needs_int_wrap(arg):
    """Return True if arg contains a subscript and is not already wrapped in int()."""
    if 'int(' in arg:
        return False
    if re.search(r'\[[^\]]*\]', arg):
        return True
    return False

def wrap_range_arg(arg):
    """
    Wrap the subscript-containing part with int().
    Handles:
      param[0]           -> int(param[0])
      param[0] - 1       -> int(param[0]) - 1
      1 + param[0]       -> 1 + int(param[0])
      3 + param[0]       -> 3 + int(param[0])
      sum(x[:param[0]])  -> leave as-is (sum handles it)
    """
    # If it's a simple subscript expression (possibly with +/- integer offset)
    # Pattern: [optional: int +] expr[n] [optional: - int]
    m = re.match(r'^(\d+\s*\+\s*)?([\w\.\[\]]+\[\d+\])(\s*[+\-]\s*\d+)?$', arg.strip())
    if m:
        prefix = m.group(1) or ''
        subscript = m.group(2)
        suffix = m.group(3) or ''
        return f'{prefix}int({subscript}){suffix}'
    # For more complex expressions (e.g. sum(...)), wrap the whole thing
    return f'int({arg})'

def process_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    lines = content.splitlines(keepends=True)
    changed = 0

    for i, line in enumerate(lines):
        if 'range(' not in line:
            continue
        new_line = line
        for m in PATTERN.finditer(line):
            arg = m.group(1)
            if needs_int_wrap(arg):
                new_arg = wrap_range_arg(arg)
                old = f'range({arg})'
                new = f'range({new_arg})'
                new_line = new_line.replace(old, new, 1)
                changed += 1
        lines[i] = new_line

    if changed:
        with open(filepath, 'w') as f:
            f.writelines(lines)

    return changed

total = 0
categories = sorted(os.listdir(CODE_DIR))
for cat in categories:
    path = os.path.join(CODE_DIR, cat, 'concept_template.py')
    if not os.path.exists(path):
        continue
    n = process_file(path)
    if n:
        print(f'  {cat}: {n} fix(es)')
        total += n

print(f'\nTotal: {total} range() calls wrapped with int()')
