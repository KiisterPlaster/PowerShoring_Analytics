import glob
import os

api_files = glob.glob("backend/api/*.py")
errors = []
for f in api_files:
    with open(f, "r", encoding="utf-8") as f_obj:
        content = f_obj.read()
        if "@cached" in content and "from core.cache import cached" not in content:
             errors.append(f)

if not errors:
    print("ALL OK: No missing imports found for @cached.")
else:
    print("FOUND ERRORS:")
    for e in errors:
        print(f" - {e} is using @cached but missing the import!")
