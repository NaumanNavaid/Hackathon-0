---
name: process-needs-action
description: Process items in the Needs_Action folder and create plans for handling them
---

# Process Needs Action Items

You are the AI Employee. Process all items in the `/Needs_Action` folder.

## Instructions

1. **Read all items** in `/Needs_Action`
2. **For each item:**
   - Read the markdown file
   - Understand what action is needed
   - Check the priority level
   - Create a plan in `/Plans/` if needed
3. **Update Dashboard** with count of processed items

## Priority Handling

- **Critical**: Process immediately, create urgent alert
- **High**: Create plan, move to front of queue
- **Medium**: Create plan for standard processing
- **Low**: Create plan, can batch with similar items

## Output Format

For each item, create a plan file:

```markdown
---
type: plan
created: {{timestamp}}
status: pending
original_item: {{item_file}}
priority: {{priority}}
---

# Plan: {{item_title}}

## Objective
{{what needs to be done}}

## Steps
- [ ] Step 1
- [ ] Step 2
- [ ] ...

## Approval Required
{{yes/no - if yes, what requires approval}}

## Notes
{{additional context}}
```

## After Processing

1. Move original item to `/In_Process/` or keep in `/Needs_Action/` until plan is executed
2. Log all actions to `/Logs/{{date}}.md`
3. Update dashboard statistics
