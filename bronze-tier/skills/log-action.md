---
name: log-action
description: Log any action taken by the AI Employee to the daily log
---

# Log Action

Log an AI Employee action to the daily activity log.

## Instructions

1. **Determine log level**: info, warning, error
2. **Create/update** today's log file in `/Logs/`
3. **Append** the action entry

## Log File Location

```
/Vault/Logs/YYYY-MM-DD.md
```

## Log Entry Format

```markdown
## [HH:MM:SS] {{action_type}}

- **Source**: {{component_name}}
- **Level**: {{info/warning/error}}
- **Action**: {{what was done}}
- **Details**: {{additional information}}
- **Result**: {{success/failure}}
- **Files**: {{affected files, if any}}
```

## Example Entries

### Info Level
```markdown
## [14:32:15] dashboard_update

- **Source**: Claude Code
- **Level**: info
- **Action**: Updated dashboard statistics
- **Details**: Refreshed stats from all folders
- **Result**: success
```

### Warning Level
```markdown
## [09:15:22] watcher_restart

- **Source**: FileSystemWatcher
- **Level**: warning
- **Action**: Watcher stopped unexpectedly
- **Details**: Inbox folder was unavailable, restarting
- **Result**: success
```

### Error Level
```markdown
## [16:45:03] email_send_failed

- **Source**: Email MCP
- **Level**: error
- **Action**: Failed to send email
- **Details**: SMTP connection timeout to client@example.com
- **Result**: failure
- **Retry**: Will retry in 5 minutes
```

## Special Log Types

### Approval Log
```markdown
## [10:30:00] approval_requested

- **Source**: Claude Code
- **Level**: info
- **Action**: Created approval request
- **Details**: Payment of $150 to Vendor X
- **File**: /Pending_Approval/PAYMENT_vendor_x.md
```

### Task Completion Log
```markdown
## [11:45:30] task_complete

- **Source**: Claude Code
- **Level**: info
- **Action**: Completed task from Needs_Action
- **Details**: Processed invoice request for Client A
- **Original File**: /Needs_Action/EMAIL_12345.md
- **Plan**: /Plans/PLAN_invoice_client_a.md
- **Result**: Moved to /Done/
```

## Log Levels

| Level | Usage | Examples |
|-------|-------|----------|
| **info** | Normal operations | Dashboard updates, files created, tasks completed |
| **warning** | Unexpected but handled | Watcher restart, retry needed, missing optional data |
| **error** | Failures needing attention | API failures, file errors, auth issues |

## Best Practices

1. **Log consistently** - Every significant action should be logged
2. **Use structured format** - Keep entries readable and parseable
3. **Include context** - What, why, result
4. **Timestamp everything** - Use 24-hour format
5. **One file per day** - Easy to find and archive

## Reading Logs

To check today's activity:
```
Read: /Logs/{{today's_date}}.md
```

To search logs:
```
Search in /Logs/ for "error" or "approval" or specific component
```
