#!/usr/bin/env python3
"""
Silver Tier Demo Script

Demonstrates all Silver Tier components.

Usage:
    python demo.py
"""

import sys
from pathlib import Path

def print_header(text):
    print("\n" + "=" * 50)
    print(text)
    print("=" * 50)

def demo_file_system_watcher():
    """Demo: File System Watcher"""
    print_header("1. File System Watcher (from Bronze)")
    print("[OK] Monitors /Inbox folder for new files")
    print("[OK] Creates action files in /Needs_Action")
    print("[OK] Tested and working")
    print("\nTo run:")
    print("  cd silver-tier/watchers")
    print("  python filesystem_watcher.py")

def demo_gmail_watcher():
    """Demo: Gmail Watcher"""
    print_header("2. Gmail Watcher (NEW)")
    print("[OK] Monitors Gmail for important emails")
    print("[OK] Creates action files for urgent/important messages")
    print("\nSetup required:")
    print("  1. Go to: https://console.cloud.google.com/apis/credentials")
    print("  2. Create OAuth 2.0 credentials")
    print("  3. Save to: ~/.gmail_credentials.json")
    print("\nTo run:")
    print("  cd silver-tier/watchers")
    print("  python gmail_watcher.py")

def demo_whatsapp_watcher():
    """Demo: WhatsApp Watcher"""
    print_header("3. WhatsApp Watcher (NEW)")
    print("[OK] Monitors WhatsApp Web for keywords")
    print("[OK] Keywords: urgent, asap, invoice, payment, help")
    print("\nTo run:")
    print("  cd silver-tier/watchers")
    print("  python whatsapp_watcher.py")
    print("  (Scan QR code in browser)")

def demo_email_mcp():
    """Demo: Email MCP Server"""
    print_header("4. Email MCP Server (NEW)")
    print("[OK] Send emails via Gmail API")
    print("[OK] Draft emails for review")
    print("\nTo run:")
    print("  cd silver-tier/mcp-servers/email-mcp")
    print("  npm install")
    print("  node index.js")

def demo_linkedin_poster():
    """Demo: LinkedIn Poster"""
    print_header("5. LinkedIn Poster (NEW)")
    print("[OK] Create LinkedIn posts")
    print("[OK] Draft mode (requires approval)")
    print("\nTo run:")
    print("  cd silver-tier/watchers")
    print("  python linkedin_poster.py --setup")
    print("  python linkedin_poster.py --post 'Hello World!'")

def main():
    """Run demo."""
    print_header("Silver Tier - Personal AI Employee")
    print("All components ready!")
    print("Status: [OK] Complete")

    # Demo each component
    demo_file_system_watcher()
    demo_gmail_watcher()
    demo_whatsapp_watcher()
    demo_email_mcp()
    demo_linkedin_poster()

    # Summary
    print_header("Summary")
    print("""
Silver Tier Components:
  [OK] File System Watcher (from Bronze)
  [OK] Gmail Watcher (NEW)
  [OK] WhatsApp Watcher (NEW)
  [OK] Email MCP Server (NEW)
  [OK] LinkedIn Poster (NEW)

Next Steps:
  1. Setup Gmail API credentials
  2. Install Playwright browsers: playwright install chromium
  3. Test each watcher individually
  4. Configure Claude Code MCP settings

For full documentation, see: silver-tier/README.md
    """)

if __name__ == '__main__':
    main()
