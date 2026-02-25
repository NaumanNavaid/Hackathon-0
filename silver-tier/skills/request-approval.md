---
name: request-approval
description: Create an approval request file for sensitive actions
---

# Request Approval

Create an approval request for sensitive actions that require human review.

## When to Use

Request approval for:
- Sending emails to **new contacts**
- Making **any payment**
- **Posting** on social media
- **Deleting** files
- **Sharing** personal data
- **Legal/medical** responses

## Instructions

1. **Identify the action** requiring approval
2. **Create approval file** in `/Pending_Approval/`
3. **Wait for human** to move file to `/Approved/` or `/Rejected/`

## Approval File Format

```markdown
---
type: approval_request
action: {{action_type}}
created: {{timestamp}}
expires: {{timestamp + 24 hours}}
status: pending
---

# Approval Request: {{title}}

## Action Details
- **Type**: {{email/payment/post/etc}}
- **Target**: {{recipient/target}}
- **Summary**: {{what will happen}}

## Information
{{details of what will be sent/paid/posted}}

## Risks
{{potential risks or concerns}}

## ## To Approve
Move this file to: `/Approved/{{filename}}`

## To Reject
Move this file to: `/Rejected/{{filename}}`

---
*Created by AI Employee*
```

## Action Types

### Email Approval
```markdown
- **Type**: email
- **To**: {{email_address}}
- **Subject**: {{subject}}
- **Body Preview**: {{first 100 chars}}
```

### Payment Approval
```markdown
- **Type**: payment
- **Amount**: {{amount}}
- **To**: {{recipient}}
- **Reference**: {{invoice/purpose}}
- **Account**: {{account to use}}
```

### Social Media Approval
```markdown
- **Type**: social_post
- **Platform**: {{LinkedIn/Twitter/etc}}
- **Content**: {{post content}}
- **Scheduled**: {{date/time if applicable}}
```

## After Approval

Once human moves file to `/Approved/`:
1. Read the approved file
2. Execute the action
3. Move file to `/Done/`
4. Log the action

## After Rejection

If file is moved to `/Rejected/`:
1. Read the rejection reason (if added)
2. Do NOT execute the action
3. Move to `/Done/` with rejection note
4. Log the rejection
