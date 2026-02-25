#!/usr/bin/env python3
"""
WhatsApp Watcher for Personal AI Employee

Monitors WhatsApp Web for messages with keywords and creates action files.

Usage:
    python whatsapp_watcher.py

Requirements:
    pip install playwright
    playwright install chromium
"""

import time
import logging
from pathlib import Path
from datetime import datetime

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("Playwright not installed. Run: pip install playwright")
    exit(1)

import sys
sys.path.insert(0, str(Path(__file__).parent))
from base_watcher import BaseWatcher


class WhatsAppWatcher(BaseWatcher):
    """
    Watches WhatsApp Web for messages with specific keywords.
    """

    # Keywords to monitor for
    KEYWORDS = [
        'urgent', 'asap', 'invoice', 'payment', 'help',
        'meeting', 'call', 'please', 'thank'
    ]

    def __init__(self, vault_path: str, session_path: str = None):
        """
        Initialize WhatsApp Watcher.

        Args:
            vault_path: Path to Obsidian vault
            session_path: Path to store browser session
        """
        super().__init__(vault_path, check_interval=60, name='WhatsAppWatcher')

        self.session_path = session_path or Path.home() / '.whatsapp_session'
        self.session_path.mkdir(parents=True, exist_ok=True)

        self.browser = None
        self.page = None
        self.playwright = None

    def _start_browser(self):
        """Start browser and load WhatsApp Web."""
        if self.page:
            return  # Already running

        self.playwright = sync_playwright().start()

        # Launch with persistent context for session
        self.browser = self.playwright.chromium.launch_persistent_context(
            user_data_dir=str(self.session_path),
            headless=False,  # Need to scan QR code first time
            args=['--no-sandbox', '--disable-setuid-sandbox']
        )

        self.page = self.browser.new_page()

        # Navigate to WhatsApp Web
        self.page.goto('https://web.whatsapp.com')

        # Wait for chat list to load
        try:
            self.page.wait_for_selector('[data-testid="chat-list"]', timeout=60000)
            self.logger.info("WhatsApp Web loaded successfully")
        except:
            self.logger.warning("WhatsApp Web not fully loaded - may need QR code scan")

    def check_for_updates(self):
        """
        Check for new unread messages with keywords.

        Returns:
            List of message objects
        """
        try:
            if not self.page:
                self._start_browser()

            # Find all unread chats
            unread_chats = self.page.query_selector_all('[aria-label*="unread"]')

            messages = []

            for chat in unread_chats:
                try:
                    # Get chat text
                    text = chat.inner_text().lower()

                    # Check for keywords
                    if any(kw in text for kw in self.KEYWORDS):
                        # Get sender name
                        try:
                            sender_elem = chat.query_selector('[title]')
                            sender = sender_elem.get_attribute('title') if sender_elem else 'Unknown'
                        except:
                            sender = 'Unknown'

                        messages.append({
                            'sender': sender,
                            'text': text,
                            'chat': chat
                        })

                except:
                    continue

            return messages

        except Exception as e:
            self.logger.error(f"Error checking for updates: {e}")
            # Reset page to force reconnection
            self.page = None
            return []

    def get_item_id(self, item):
        """Get unique ID for message."""
        return f"{item['sender']}_{int(time.time())}"

    def get_item_priority(self, item):
        """Determine priority based on keywords."""
        text = item['text'].lower()

        if 'urgent' in text or 'asap' in text:
            return 'critical'
        elif 'invoice' in text or 'payment' in text:
            return 'high'
        else:
            return 'medium'

    def create_action_file(self, item):
        """
        Create action file for WhatsApp message.

        Args:
            item: Message dict with sender and text

        Returns:
            Path to created file
        """
        try:
            priority = self.get_item_priority(item)
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            frontmatter = f"""---
type: whatsapp
source: WhatsAppWatcher
received: {datetime.now().isoformat()}
priority: {priority}
status: pending
sender: {item['sender']}
---
"""

            content = f"""# WhatsApp Message from {item['sender']}

## Message Details
- **From**: {item['sender']}
- **Detected**: {timestamp}

## Message Preview
{item['text'][:200]}...

## Suggested Actions
- [ ] Read full message in WhatsApp
- [ ] Determine response needed
- [ ] Draft reply if needed (requires approval)
- [ ] Move to /Done when processed

## Notes
Full message available in WhatsApp Web.
"""

            filename = f"WHATSAPP_{self.get_item_id(item)}.md"
            filepath = self.needs_action / filename

            filepath.write_text(frontmatter + content, encoding='utf-8')

            # Also copy to Inbox
            inbox_file = self.vault_path / 'Inbox' / filename
            inbox_file.write_text(frontmatter + content, encoding='utf-8')

            return filepath

        except Exception as e:
            self.logger.error(f"Error creating action file: {e}")
            return None

    def run(self):
        """Main loop with browser management."""
        self.is_running = True
        self.logger.info(f"Starting {self.name}")
        self.logger.info(f"Vault: {self.vault_path}")
        self.logger.info("First run will require QR code scan")

        try:
            # Start browser once
            self._start_browser()

            while self.is_running:
                try:
                    self.run_once()
                    time.sleep(self.check_interval)
                except Exception as e:
                    self.logger.error(f"Error in loop: {e}")
                    time.sleep(10)  # Wait before retry

        except KeyboardInterrupt:
            self.logger.info("Stopping...")
        finally:
            self._cleanup()

    def _cleanup(self):
        """Clean up browser resources."""
        try:
            if self.browser:
                self.browser.close()
            if self.playwright:
                self.playwright.stop()
        except:
            pass

    def stop(self):
        """Stop the watcher."""
        super().stop()
        self._cleanup()


def main():
    """Entry point for WhatsApp watcher."""
    vault_path = Path(__file__).parent.parent / 'AI_Employee_Vault'

    watcher = WhatsAppWatcher(str(vault_path))

    print("Starting WhatsApp Watcher...")
    print(f"Vault: {vault_path}")
    print("First time: Scan QR code in browser")
    print("Press Ctrl+C to stop\n")

    try:
        watcher.run()
    except KeyboardInterrupt:
        print("\nStopping WhatsApp Watcher...")


if __name__ == '__main__':
    main()
