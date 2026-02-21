# Platinum Tier - Always-On Cloud + Local Executive

> Estimated time: 60+ hours

---

## Overview

Production-ish AI Employee running 24/7 on cloud VM with work-zone specialization.

---

## Requirements

### All Gold Requirements Plus:

| Feature | Description | Status |
|---------|-------------|--------|
| **Cloud VM 24/7** | Always-on watchers + orchestrator | 🚧 Todo |
| **Health Monitoring** | System status & alerts | 🚧 Todo |
| **Work-Zone Specialization** | Cloud vs Local domain ownership | 🚧 Todo |
| **Vault Sync** | Git or Syncthing for coordination | 🚧 Todo |
| **Cloud Odoo** | 24/7 accounting with HTTPS | 🚧 Todo |
| **Delegation Protocol** | A2A communication via vault | 🚧 Todo |
| **Claim-by-Move** | Prevent double-work | 🚧 Todo |

---

## Work-Zone Specialization

### Cloud Zone Owns:
- Email triage
- Draft replies
- Social media drafts/scheduling
- **Draft-only** - requires Local approval before send/post

### Local Zone Owns:
- Approvals
- WhatsApp session
- Payments/banking
- Final "send/post" actions

---

## Delegation via Synced Vault

### Communication Protocol:
- Cloud writes to `/Needs_Action/<domain>/`
- Cloud writes to `/Plans/<domain>/`
- Cloud writes to `/Pending_Approval/<domain>/`

### Prevention Rules:
- **Claim-by-move**: First to move to `/In_Progress/<agent>/` owns it
- **Single-writer**: Only Local writes to Dashboard.md
- **Cloud updates**: Write to `/Updates/`, Local merges

### Security Rule:
- Vault sync includes **only** markdown/state
- **Secrets never sync**: .env, tokens, WhatsApp sessions, banking creds

---

## Architecture

```
┌─────────────────┐     ┌─────────────────┐
│   Cloud Zone    │     │   Local Zone    │
│  (Oracle VM)    │     │   (Your PC)     │
├─────────────────┤     ├─────────────────┤
│ • Email triage  │────▶│ • Approvals     │
│ • Draft replies │     │ • WhatsApp      │
│ • Social drafts │     │ • Payments      │
│ • Read-only     │     │ • Final send    │
└─────────────────┘     └─────────────────┘
         │                       │
         └───────Vault Sync───────┘
              (Git/Syncthing)
```

---

## Demo Scenario (Minimum Passing Gate)

1. Email arrives while Local is offline
2. Cloud drafts reply + writes approval file
3. Local returns → user approves
4. Local executes send via MCP
5. Logs → moves to `/Done/`

---

## Implementation Checklist

### Cloud Infrastructure
- [ ] Set up Oracle/AWS free VM
- [ ] Install Python, Node.js, Odoo
- [ ] Configure HTTPS
- [ ] Set up backups
- [ ] Health monitoring

### Coordination
- [ ] Git-based vault sync OR Syncthing
- [ ] Claim-by-move rules
- [ ] Single-writer Dashboard pattern
- [ ] Security: exclude secrets from sync

### Cloud Odoo
- [ ] 24/7 Odoo Community
- [ ] HTTPS configuration
- [ ] Backup automation
- [ ] Health checks
- [ ] MCP for draft-only actions

### Monitoring
- [ ] Health endpoint
- [ ] Alert system
- [ ] Log aggregation
- [ ] Auto-restart

### Optional A2A Upgrade (Phase 2)
- [ ] Direct agent-to-agent messages
- [ ] Keep vault as audit record

---

## Getting Started

1. Complete Gold Tier first
2. Set up cloud VM (Oracle Free Tier recommended)
3. Install and configure all components
4. Set up vault sync
5. Test delegation protocol

---

## Production Considerations

- **Security**: Cloud never stores WhatsApp sessions or banking creds
- **Reliability**: Health monitoring + auto-restart
- **Performance**: Offload read-heavy tasks to Cloud
- **Cost**: Use free tiers where possible

---

*Built for Personal AI Employee Hackathon 0*
