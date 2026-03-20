"""
Duplicate Class Body Audit
Parses all concept_template.py files in code/<Category>/,
extracts class definitions, hashes their bodies, and groups by:
  - IDENTICAL: same name, same body (safe to consolidate in Pass 3)
  - INCOMPATIBLE: same name, different body (need rename in Pass 2)
  - UNIQUE: only one definition (no action needed)

Output: scripts/audit_results.md
"""

import ast
import hashlib
import os
from collections import defaultdict

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CODE_DIR = os.path.join(REPO_ROOT, 'code')
OUTPUT_FILE = os.path.join(REPO_ROOT, 'scripts', 'audit_results.md')


def get_class_source(source, node):
    """Extract raw source lines for a class node."""
    lines = source.splitlines()
    # end_lineno available in Python 3.8+
    return '\n'.join(lines[node.lineno - 1 : node.end_lineno])


def normalize_body(source):
    """Hash the class body after stripping comments and blank lines."""
    lines = []
    for line in source.splitlines():
        stripped = line.strip()
        if stripped and not stripped.startswith('#'):
            lines.append(stripped)
    body = '\n'.join(lines)
    return hashlib.md5(body.encode()).hexdigest(), body


def parse_category(category_dir):
    """Return {class_name: (hash, body, source_lines)} for a concept_template.py."""
    path = os.path.join(category_dir, 'concept_template.py')
    if not os.path.exists(path):
        return {}
    with open(path, 'r', encoding='utf-8') as f:
        source = f.read()
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        print(f"  SyntaxError in {path}: {e}")
        return {}
    results = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            class_source = get_class_source(source, node)
            h, body = normalize_body(class_source)
            results[node.name] = (h, body, node.lineno)
    return results


def main():
    # Collect all classes across all categories
    # class_name -> list of (category, hash, lineno)
    all_classes = defaultdict(list)

    categories = sorted([
        d for d in os.listdir(CODE_DIR)
        if os.path.isdir(os.path.join(CODE_DIR, d))
    ])

    print(f"Scanning {len(categories)} categories...")
    category_data = {}
    for cat in categories:
        cat_dir = os.path.join(CODE_DIR, cat)
        classes = parse_category(cat_dir)
        category_data[cat] = classes
        for cls_name, (h, body, lineno) in classes.items():
            all_classes[cls_name].append((cat, h, lineno))

    # Classify each class name
    identical = {}    # name -> list of categories (all same hash)
    incompatible = {} # name -> list of (category, hash)
    unique = {}       # name -> category

    for cls_name, entries in sorted(all_classes.items()):
        if len(entries) == 1:
            unique[cls_name] = entries[0][0]
        else:
            hashes = set(e[1] for e in entries)
            if len(hashes) == 1:
                identical[cls_name] = [e[0] for e in entries]
            else:
                incompatible[cls_name] = entries

    # Write output
    lines = []
    lines.append('# Duplicate Class Body Audit Results\n')
    lines.append(f'Scanned {len(categories)} categories, '
                 f'{sum(len(v) for v in category_data.values())} total class definitions, '
                 f'{len(all_classes)} unique class names.\n')
    lines.append('---\n')

    # IDENTICAL
    lines.append(f'## IDENTICAL duplicates ({len(identical)} class names)\n')
    lines.append('Same name, byte-for-byte identical body. Safe to consolidate in Pass 3.\n')
    lines.append('Keep one canonical copy, delete the rest.\n')
    for cls_name, cats in sorted(identical.items()):
        lines.append(f'- `{cls_name}` — {len(cats)} copies: {", ".join(cats)}')
    lines.append('')

    # INCOMPATIBLE
    lines.append(f'## INCOMPATIBLE duplicates ({len(incompatible)} class names)\n')
    lines.append('Same name, different body. Rename the earlier (lost) class in Pass 2.\n')
    for cls_name, entries in sorted(incompatible.items()):
        lines.append(f'\n### `{cls_name}`')
        # group by hash to show which are identical to each other
        hash_groups = defaultdict(list)
        for cat, h, lineno in entries:
            hash_groups[h].append((cat, lineno))
        for i, (h, group) in enumerate(hash_groups.items()):
            cats_str = ', '.join(f'{cat} (line {ln})' for cat, ln in group)
            lines.append(f'  - Variant {i+1} [{h[:8]}]: {cats_str}')
    lines.append('')

    # UNIQUE
    lines.append(f'## UNIQUE classes ({len(unique)} class names)\n')
    lines.append('Only one definition. No action needed.\n')
    for cls_name, cat in sorted(unique.items()):
        lines.append(f'- `{cls_name}` — {cat}')

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    print(f'\nDone.')
    print(f'  {len(identical)} identical duplicate class names')
    print(f'  {len(incompatible)} incompatible duplicate class names')
    print(f'  {len(unique)} unique class names')
    print(f'  Results written to {OUTPUT_FILE}')


if __name__ == '__main__':
    main()
