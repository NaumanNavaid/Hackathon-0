# Personal AI Employee - Bronze Tier

> Your life and business on autopilot. Local-first, agent-driven, human-in-the-loop.

**Hackathon Project:** Building Autonomous FTEs (Full-Time Equivalent) in 2026

---

## Project Overview

This is a **Bronze Tier** implementation of a Personal AI Employee - an autonomous agent that manages personal and business affairs using Claude Code as the reasoning engine and Obsidian as the memory/dashboard.

### Bronze Tier Features ✅

| Feature | Status |
|---------|--------|
| Obsidian Vault with Dashboard.md | ✅ Complete |
| Company_Handbook.md with rules | ✅ Complete |
| File System Watcher (Python) | ✅ Complete |
| Claude Code Vault Integration | ✅ Complete |
| Basic Folder Structure | ✅ Complete |
| Agent Skills for AI Functions | ✅ Complete |

---

## Project Structure

```
Hackathon-0/
├── AI_Employee_Vault/          # Obsidian vault (memory/dashboard)
│   ├── Inbox/                  # Drop folder for new items
│   ├── Needs_Action/           # Items requiring processing
│   ├── Done/                   # Completed items
│   ├── Plans/                  # Execution plans
│   ├── Logs/                   # Activity logs
│   ├── Pending_Approval/       # Awaiting human approval
│   ├── Approved/               # Approved actions
│   ├── Rejected/               # Rejected actions
│   ├── Accounting/             # Financial records
│   ├── Dashboard.md            # Main dashboard
│   └── Company_Handbook.md     # Rules of engagement
│
├── watchers/                   # Python watcher scripts
│   ├── base_watcher.py         # Abstract base class
│   ├── filesystem_watcher.py   # File system monitoring
│   └── requirements.txt        # Python dependencies
│
├── skills/                     # Agent Skills for Claude Code
│   ├── process-needs-action.md # Process pending items
│   ├── update-dashboard.md     # Update dashboard stats
│   ├── request-approval.md     # Create approval requests
│   ├── create-plan.md          # Create execution plans
│   ├── weekly-briefing.md      # Generate CEO briefings
│   └── log-action.md           # Log actions
│
└── README.md                   # This file
```

---

## Setup Instructions

### 1. Prerequisites

- **Claude Code** (Pro or Free tier)
- **Obsidian** v1.10.6+ (free)
- **Python** 3.13 or higher
- **Git** (for version control)

### 2. Install Python Dependencies

```bash
cd watchers
pip install -r requirements.txt
```

### 3. Open Vault in Obsidian

1. Open Obsidian
2. Click "Open folder as vault"
3. Select: `AI_Employee_Vault`
4. Open `Dashboard.md` to see the main dashboard

### 4. Start the File System Watcher

```bash
cd watchers
python filesystem_watcher.py
```

The watcher will monitor the `/Inbox` folder and create action files for new items.

### 5. Configure Claude Code Skills

Copy the skills from `/skills/` to your Claude Code skills directory:

```bash
# Default Claude Code skills location
# Windows: %USERPROFILE%\.claude\skills\
# macOS/Linux: ~/.claude/skills/
```

---

## How It Works

### Architecture

```
┌─────────────────┐
│  External Input │
│  (Files dropped │
│   in /Inbox)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Watcher Layer  │
│ (Detects new    │
│  files, creates │
│  action files)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Reasoning      │
│  (Claude Code   │
│   processes     │
│   tasks)        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Human-in-Loop  │
│ (Approval for   │
│  sensitive      │
│  actions)       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Action        │
│  (Execute & log │
│   results)      │
└─────────────────┘
```

### Example Workflow

1. **Drop a file** in `/Inbox`
2. **Watcher detects** it and creates an action file in `/Needs_Action`
3. **Claude Code** processes the action using Agent Skills
4. **If sensitive**, creates approval request in `/Pending_Approval`
5. **Human approves** by moving to `/Approved`
6. **Action executed** and file moved to `/Done`
7. **Logged** to `/Logs/YYYY-MM-DD.md`

---

## Agent Skills

The following skills are available for Claude Code:

| Skill | Description |
|-------|-------------|
| `process-needs-action` | Process items in Needs_Action folder |
| `update-dashboard` | Update dashboard statistics |
| `request-approval` | Create approval requests |
| `create-plan` | Create execution plans |
| `weekly-briefing` | Generate CEO briefings |
| `log-action` | Log actions to daily log |

### Using Skills

In Claude Code, reference a skill by name:

```
"Use the process-needs-action skill to handle all pending items."
"Use the update-dashboard skill to refresh the statistics."
```

---

## Bronze Tier Deliverables

All Bronze Tier requirements have been met:

- ✅ Obsidian vault with Dashboard.md and Company_Handbook.md
- ✅ One working Watcher script (File System monitoring)
- ✅ Claude Code successfully reading from and writing to vault
- ✅ Basic folder structure: /Inbox, /Needs_Action, /Done
- ✅ All AI functionality implemented as Agent Skills

---

## Next Steps (Silver Tier)

To upgrade to Silver Tier:

1. **Add Gmail Watcher** - Monitor Gmail for important emails
2. **Add WhatsApp Watcher** - Monitor WhatsApp for keywords
3. **Create LinkedIn Poster** - Auto-post business updates
4. **Implement Ralph Wiggum Loop** - Autonomous task completion
5. **Add MCP Server** - For external actions (sending emails)

---

## Security Notes

- **Local-first**: All data stored locally in Obsidian vault
- **No credentials in vault**: Use environment variables for API keys
- **Human-in-the-loop**: Sensitive actions require approval
- **Audit logging**: All actions logged to `/Logs/`

---

## Troubleshooting

### Watcher won't start

```bash
# Check Python version (requires 3.13+)
python --version

# Install dependencies
pip install -r watchers/requirements.txt
```

### Claude Code can't see vault files

Make sure you're running Claude Code from the project directory:

```bash
cd "c:/Users/Src/Desktop/Hackathon-0"
claude
```

### Files not appearing in Obsidian

1. Check the vault path in Obsidian settings
2. Try closing and reopening the vault
3. Check file permissions

---

## License

MIT License - Free to use and modify

---

## Hackathon Submission

- **Tier**: Bronze ✅
- **Date**: 2026-02-21
- **Tech Stack**: Claude Code, Obsidian, Python, Watchdog

---

*Built for the Personal AI Employee Hackathon 0*
