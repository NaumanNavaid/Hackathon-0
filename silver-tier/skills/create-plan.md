---
name: create-plan
description: Create a detailed execution plan for a task or project
---

# Create Plan

Create a detailed, step-by-step plan for completing a task or project.

## Instructions

1. **Understand the task** from the user or from a Needs_Action item
2. **Define the objective** clearly
3. **Break down into steps** - each step should be atomic and testable
4. **Identify dependencies** between steps
5. **Flag approval requirements** for sensitive actions
6. **Save plan** to `/Plans/`

## Plan File Format

```markdown
---
type: plan
created: {{timestamp}}
status: pending
priority: {{high/medium/low}}
estimated_time: {{hours}}
---

# Plan: {{Plan Title}}

## Objective
{{Clear statement of what this plan achieves}}

## Context
{{Background information, constraints, assumptions}}

## Steps

### Step 1: {{Step Title}}
- [ ] {{Action item 1}}
- [ ] {{Action item 2}}
- **Approval Required**: {{yes/no}}
- **Dependencies**: {{none or previous steps}}
- **Estimated Time**: {{minutes}}

### Step 2: {{Step Title}}
...

## Checklist Summary
- [ ] Step 1: {{title}}
- [ ] Step 2: {{title}}
- [ ] Step 3: {{title}}
...

## Approval Required
{{If any steps need human approval, list them here}}

## Success Criteria
{{How do we know this plan is complete?}}

## Notes
{{Additional context, risks, considerations}}

---
*Created by AI Employee v{{version}}*
```

## Planning Best Practices

1. **Start with understanding** - Ask clarifying questions if needed
2. **Break it down** - Large tasks into smaller, manageable steps
3. **Think in dependencies** - What must happen before what?
4. **Flag risks** - What could go wrong? What needs approval?
5. **Define done** - Clear success criteria

## Example Plan

```markdown
# Plan: Send Client Invoice

## Objective
Generate and send January 2026 invoice to Client A

## Context
- Client: Client A (client_a@email.com)
- Amount: $1,500 (from /Accounting/Rates.md)
- Month: January 2026
- Due: Within 2 days

## Steps

### Step 1: Verify Amount
- [ ] Check rate in /Accounting/Rates.md
- [ ] Confirm hours worked
- [ ] Calculate total
- **Approval Required**: No
- **Estimated Time**: 5 minutes

### Step 2: Generate Invoice
- [ ] Create invoice document
- [ ] Include all required details
- [ ] Save to /Invoices/2026-01_Client_A.pdf
- **Approval Required**: No
- **Estimated Time**: 10 minutes

### Step 3: Draft Email
- [ ] Create professional email
- [ ] Attach invoice
- [ ] Save draft for review
- **Approval Required**: Yes (sending to client)
- **Estimated Time**: 5 minutes

### Step 4: Send Email
- [ ] Get approval from /Pending_Approval
- [ ] Send via email MCP
- [ ] Confirm delivery
- **Approval Required**: Yes
- **Estimated Time**: 5 minutes

## Approval Required
- Step 3: Email draft review
- Step 4: Final send approval

## Success Criteria
- Invoice generated and saved
- Email sent successfully
- Transaction logged to /Accounting/
```

## After Creating Plan

1. Save plan to `/Plans/PLAN_{{slug}}.md`
2. Log plan creation
3. Optionally start executing steps
4. Update plan as you progress
