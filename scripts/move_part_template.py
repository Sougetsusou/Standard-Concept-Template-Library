"""
Move code/part_template/ to part_template/ at the repo root,
updating the sys.path line in every .py file to point to code/shared.
"""
import os
import shutil
import re

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(REPO_ROOT, 'code', 'part_template')
DST = os.path.join(REPO_ROOT, 'part_template')

OLD_PATH = "os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'shared')"
NEW_PATH = "os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'code', 'shared')"

def update_import(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    updated = content.replace(OLD_PATH, NEW_PATH)
    if updated != content:
        with open(filepath, 'w') as f:
            f.write(updated)
        print(f"  updated: {os.path.basename(filepath)}")
    else:
        print(f"  no change: {os.path.basename(filepath)}")

if os.path.exists(DST):
    print(f"Destination already exists: {DST}")
    print("Remove it first or choose a different target.")
    exit(1)

print(f"Copying {SRC} -> {DST}")
shutil.copytree(SRC, DST)

print("\nUpdating import paths...")
for fname in sorted(os.listdir(DST)):
    if fname.endswith('.py'):
        update_import(os.path.join(DST, fname))

print("\nDone. Verify, then remove the original:")
print(f"  rm -rf {SRC}")
