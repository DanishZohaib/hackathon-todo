# Quickstart: CCR Permissions

## Overview
This guide explains how to set up and validate CCR (Claude Code Router) permissions for secure tool access in your development environment.

## Prerequisites
- Claude Code installed and configured
- Access to .claude/settings.local.json file
- Understanding of CCR permission syntax

## Setup Instructions

### 1. Verify Current Configuration
Check your existing .claude/settings.local.json file:
```bash
cat .claude/settings.local.json
```

### 2. Update Permissions
Replace the permissions.allow section with the CCR-compliant minimal set:
```json
{
  "permissions": {
    "allow": [
      "Bash(ls:*)",
      "Bash(dir:*)",
      "Bash(python:*)",
      "Bash(git:*)",
      "Bash(npm:*)"
    ]
  }
}
```

### 3. Validate Configuration
Run the CCR validation command to ensure no errors appear:
```bash
ccr code
```

### 4. Test Functionality
Verify Claude Code starts normally and specs/tasks are accessible:
```bash
# Start Claude Code
claude-code

# Verify tasks are accessible
# You should be able to run tasks without permission errors
```

## Validation Checklist
- [ ] No settings error appears when running `ccr code`
- [ ] Claude Code starts normally
- [ ] Specs and tasks are accessible
- [ ] All Bash command access follows safe, validated patterns
- [ ] CCR settings remain valid and minimal after implementation

## Troubleshooting

### Common Issues
1. **Permission errors**: Verify all entries use the `:*` prefix matching syntax
2. **Invalid syntax**: Check for proper JSON formatting and no nested quotes
3. **Tool access failures**: Ensure required tools (ls, dir, python, git, npm) are included

### Verification Commands
```bash
# Check CCR validation
ccr code

# Verify configuration syntax
cat .claude/settings.local.json | python -m json.tool
```

## Next Steps
- Implement the tasks defined in tasks.md
- Test all agent functionality with new permissions
- Validate security compliance with minimal permission principle