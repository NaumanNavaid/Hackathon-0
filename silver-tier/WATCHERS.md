# Silver Tier - Quick Start Guide

## Run All Watchers

### Windows (cmd)
```batch
# Open 3 terminal windows and run:

# Terminal 1 - File System
cd silver-tier\watchers
python filesystem_watcher.py

# Terminal 2 - Gmail
cd silver-tier\watchers
python gmail_watcher.py

# Terminal 3 - WhatsApp
cd silver-tier\watchers
python whatsapp_watcher.py
```

### Or Run Setup Script
```batch
cd silver-tier
setup-all.bat
```

---

## Status Checklist

| Watcher | Status | Command |
|---------|--------|---------|
| File System | ✅ Working | `python filesystem_watcher.py` |
| Gmail | 🔧 Needs Setup | See below |
| WhatsApp | 🔧 Needs Setup | See below |
| Email MCP | ✅ Installed | `node index.js` |
| LinkedIn | 🔧 Needs Setup | See below |

---

## Quick Setup

### Gmail (5 min)
1. Go to: https://console.cloud.google.com/apis/credentials
2. Create OAuth 2.0 credentials
3. Download and save to: `C:\Users\YourName\.gmail_credentials.json`
4. Run: `python gmail_watcher.py`

### WhatsApp (2 min)
1. Run: `python whatsapp_watcher.py`
2. Scan QR code in browser

### LinkedIn (2 min)
1. Run: `python linkedin_poster.py --setup`
2. Log in to LinkedIn

---

## Test File System Watcher (Already Running!)

```batch
# Drop a test file
echo "urgent message from client" > silver-tier\AI_Employee_Vault\Inbox\test.txt

# Check the action file created
dir silver-tier\AI_Employee_Vault\Needs_Action\
```
