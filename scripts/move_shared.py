"""
Move code/shared/ to shared/ at the repo root,
updating sys.path lines in all affected .py files.
"""
import os
import shutil

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(REPO_ROOT, 'code', 'shared')
DST = os.path.join(REPO_ROOT, 'shared')

# part_template/ files: were pointing to ../code/shared, now ../shared
PART_OLD = "os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'code', 'shared')"
PART_NEW = "os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'shared')"

# code/<Category>/ files: were pointing to ../shared, now ../../shared
CAT_OLD  = "os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'shared')"
CAT_NEW  = "os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'shared')"

def patch(filepath, old, new):
    with open(filepath, 'r') as f:
        content = f.read()
    updated = content.replace(old, new)
    if updated != content:
        with open(filepath, 'w') as f:
            f.write(updated)
        print(f"  updated: {os.path.relpath(filepath, REPO_ROOT)}")
    else:
        print(f"  no change: {os.path.relpath(filepath, REPO_ROOT)}")

if os.path.exists(DST):
    print(f"Destination already exists: {DST}")
    print("Remove it first or choose a different target.")
    exit(1)

print(f"Copying {os.path.relpath(SRC, REPO_ROOT)} -> shared/")
shutil.copytree(SRC, DST)

# patch part_template/
print("\nPatching part_template/...")
pt_dir = os.path.join(REPO_ROOT, 'part_template')
for fname in sorted(os.listdir(pt_dir)):
    if fname.endswith('.py'):
        patch(os.path.join(pt_dir, fname), PART_OLD, PART_NEW)

# patch code/<Category>/
print("\nPatching code/<Category>/...")
code_dir = os.path.join(REPO_ROOT, 'code')
for category in sorted(os.listdir(code_dir)):
    cat_path = os.path.join(code_dir, category)
    if not os.path.isdir(cat_path) or category == 'shared':
        continue
    for fname in sorted(os.listdir(cat_path)):
        if fname.endswith('.py'):
            patch(os.path.join(cat_path, fname), CAT_OLD, CAT_NEW)

print("\nDone. Verify, then remove the original:")
print(f"  rm -rf {os.path.relpath(SRC, REPO_ROOT)}")
