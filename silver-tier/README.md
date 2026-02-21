# Silver Tier - Functional Assistant

> Estimated time: 20-30 hours

---

## Overview

Builds upon Bronze Tier with multiple watchers, automated posting, and approval workflows.

---

## Requirements

### All Bronze Requirements Plus:

| Feature | Description | Status |
|---------|-------------|--------|
| **Two or more Watchers** | Gmail + WhatsApp + LinkedIn | 🚧 Todo |
| **LinkedIn Auto-Post** | Automatically post business updates | 🚧 Todo |
| **Claude Reasoning Loop** | Create Plan.md files automatically | 🚧 Todo |
| **MCP Server** | For external actions (e.g., sending emails) | 🚧 Todo |
| **Human-in-the-Loop** | Approval workflow for sensitive actions | 🚧 Todo |
| **Scheduling** | Basic cron or Task Scheduler | 🚧 Todo |
| **Agent Skills** | All AI as Agent Skills | 🚧 Todo |

---

## Implementation Checklist

### Watchers
- [ ] Gmail Watcher - Monitor Gmail for important emails
- [ ] WhatsApp Watcher - Monitor WhatsApp for keywords
- [ ] LinkedIn Watcher - Monitor LinkedIn for messages

### MCP Servers
- [ ] Email MCP - Send/draft emails
- [ ] Browser MCP - Navigate websites

### Automation
- [ ] LinkedIn Poster - Auto-post business updates
- [ ] Ralph Wiggum Loop - Autonomous task completion
- [ ] Cron/Task Scheduler setup

### Skills
- [ ] All functionality as Agent Skills

---

## Getting Started

Copy Bronze Tier foundation:
```bash
cp -r bronze-tier/AI_Employee_Vault silver-tier/
cp -r bronze-tier/skills silver-tier/
```

---

## Next Steps

1. Set up Gmail API credentials
2. Install Playwright for WhatsApp automation
3. Create MCP servers
4. Implement scheduling

---

*Built for Personal AI Employee Hackathon 0*
