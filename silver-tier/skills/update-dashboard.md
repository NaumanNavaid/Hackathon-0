---
name: update-dashboard
description: Update the Dashboard.md with current statistics and recent activity
---

# Update Dashboard

Update the AI Employee Dashboard with current status.

## Instructions

1. **Count items** in each folder:
   - `/Needs_Action` - Pending tasks
   - `/Done` - Completed tasks (today)
   - `/Pending_Approval` - Awaiting approval
   - `/Plans` - Active plans

2. **Check recent logs** in `/Logs/` for recent activity

3. **Update Dashboard.md** with current statistics

## Update Format

Replace the placeholder values in Dashboard.md:

```markdown
## Quick Stats

| Metric | Value | Status |
|--------|-------|--------|
| Pending Tasks | X | 🟡 |
| Completed Today | Y | 🟢 |
| Awaiting Approval | Z | 🔴 |
| Active Projects | P | 📋 |
```

## Recent Activity Section

Add today's activity:

```markdown
## Recent Activity

### Today ({{date}})
- {{time}}: {{action_description}}
- {{time}}: {{action_description}}
```

## System Status

Update component statuses:
- Watchers: 🟢 Running / 🔴 Stopped / 🟡 Partial
- Claude Code: 🟢 Connected
- Vault: 🟢 Healthy
- MCP Servers: 🟢 Connected / 🔴 Not configured

## Save Changes

After updating, save Dashboard.md and log the update action.
