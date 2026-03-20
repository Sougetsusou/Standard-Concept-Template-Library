"""
Apply empty-concat guard to all confirmed real-risk classes.
Inserts:
    if not vertices_list:
        raise ValueError(f"{self.__class__.__name__}: no geometry was instantiated")
before every confirmed np.concatenate(vertices_list) call.

Only touches the specific line numbers confirmed by triage.
"""

import re

REPO = '/Users/charly/VScodeProjects/Research/Standard-Concept-Template-Library'

GUARD = '        if not vertices_list:\n            raise ValueError(f"{self.__class__.__name__}: no geometry was instantiated")\n'

# {filepath: [line_numbers of "self.vertices = np.concatenate(vertices_list)" to guard]}
TARGETS = {
    f'{REPO}/code/Switch/concept_template.py': [219, 264, 309, 383, 426, 495, 540],
    f'{REPO}/code/StorageFurniture/concept_template.py': [112, 171, 226, 322, 364],
    f'{REPO}/code/Window/concept_template.py': [283, 410, 521, 609, 763, 907],
}

for filepath, target_lines in TARGETS.items():
    with open(filepath, 'r') as f:
        lines = f.readlines()

    # Work backwards so line numbers stay valid after insertions
    for lineno in sorted(target_lines, reverse=True):
        idx = lineno - 1  # 0-based
        # Verify the line is what we expect
        if 'np.concatenate(vertices_list)' not in lines[idx]:
            print(f'WARNING: {filepath}:{lineno} does not match expected pattern')
            print(f'  Found: {lines[idx].rstrip()}')
            continue
        # Insert guard before this line
        lines.insert(idx, GUARD)
        print(f'  Guarded {filepath.split("/code/")[1]}:{lineno}')

    with open(filepath, 'w') as f:
        f.writelines(lines)

print('\nDone.')
