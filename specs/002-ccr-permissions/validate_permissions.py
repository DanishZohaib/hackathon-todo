#!/usr/bin/env python3
"""
CCR Permission Validation Script

This script validates that the .claude/settings.local.json file
contains only CCR-compliant permission patterns.
"""

import json
import re
import sys
from pathlib import Path


def validate_permissions(settings_path):
    """Validate permissions in the settings file."""
    try:
        with open(settings_path, 'r', encoding='utf-8') as f:
            settings = json.load(f)
    except FileNotFoundError:
        print(f"ERROR: Settings file not found at {settings_path}")
        return False
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON in settings file: {e}")
        return False

    if "permissions" not in settings or "allow" not in settings["permissions"]:
        print("ERROR: Missing permissions.allow section in settings")
        return False

    permissions = settings["permissions"]["allow"]
    valid = True

    for i, perm in enumerate(permissions):
        if not isinstance(perm, str):
            print(f"ERROR: Permission at index {i} is not a string: {perm}")
            valid = False
            continue

        # Check for invalid patterns
        if re.search(r'"[^"]*\*[^"]*"', perm):
            print(f"ERROR: Found nested quotes with wildcards in permission: {perm}")
            valid = False

        # Check for standalone wildcards (not part of :* pattern)
        if perm.count('*') > 0:
            # Allow :* pattern but not standalone * or other wildcard patterns
            if not re.search(r':\*', perm):
                print(f"ERROR: Found invalid wildcard pattern in permission: {perm}")
                valid = False

        # Check that it follows the expected format (e.g., "Bash(command:*)")
        if not re.match(r'^\w+\([^)]*:\*[^)]*\)$', perm) and perm not in [
            "Bash(ls:*)", "Bash(dir:*)", "Bash(python:*)", "Bash(git:*)", "Bash(npm:*)"
        ]:
            print(f"WARNING: Permission may not follow expected pattern: {perm}")

    # Check for the required minimal permissions
    required_perms = {"Bash(ls:*)", "Bash(dir:*)", "Bash(python:*)", "Bash(git:*)", "Bash(npm:*)"}
    current_perms = set(permissions)

    if not required_perms.issubset(current_perms):
        missing = required_perms - current_perms
        print(f"ERROR: Missing required permissions: {missing}")
        valid = False

    return valid


def main():
    """Main function to run the validation."""
    settings_path = Path(".claude/settings.local.json")

    print("Validating CCR permissions in", settings_path)
    print("=" * 50)

    if validate_permissions(settings_path):
        print("\n[SUCCESS] All validations passed! Permissions are CCR-compliant.")
        return 0
    else:
        print("\n[ERROR] Some validations failed! Please fix the issues above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())