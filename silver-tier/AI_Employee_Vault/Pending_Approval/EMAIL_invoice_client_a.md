---
type: approval_request
action: send_email
created: 2026-02-21T03:35:00
expires: 2026-02-22T03:35:00
status: pending
amount: 1500.00
---

# Approval Request: Send Invoice to Client A

## Action Details
- **Type**: Email (with invoice attachment)
- **To**: client@example.com (NEW CLIENT)
- **Subject**: January 2026 Invoice - $1,500
- **Amount**: $1,500.00

## Information

### Email Draft
```
Subject: January 2026 Invoice - $1,500

Dear Client A,

Please find attached the invoice for January 2026 services as discussed.

Amount: $1,500.00
Due Date: March 1, 2026

Thank you for your business. If you have any questions, please let me know.

Best regards,
[Your Name]
AI Employee Assisted
```

### Invoice Details
- **Period**: January 2026
- **Amount**: $1,500.00
- **Client**: Client A (client@example.com)
- **Status**: Draft - not yet generated

## Risks
- **New client**: This is the first time sending to this email address
- **High value**: $1,500 is above the $100 auto-approval threshold
- **Financial**: This is a billing transaction

## Handbook Rules Applied
| Rule | Requirement | Status |
|------|-------------|--------|
| New Contacts | Always flag for human review | ✅ Flagged |
| >$100 | Always + urgency flag | ✅ Flagged |
| Email to new recipients | Requires approval | ✅ Flagged |

## To Approve
Move this file to: `/Approved/EMAIL_invoice_client_a.md`

## To Reject
Move this file to: `/Rejected/EMAIL_invoice_client_a.md`

---
*Created by AI Employee*
*Per Company_Handbook.md Security Protocols*
