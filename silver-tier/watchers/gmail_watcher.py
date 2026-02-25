#!/usr/bin/env python3
"""
Gmail Watcher for Personal AI Employee

Monitors Gmail for important emails and creates action files.

Usage:
    1. First time: python gmail_watcher.py --setup
    2. Run: python gmail_watcher.py

Requirements:
    pip install google-api-python-client google-auth-oauthlib
"""

import os
import json
import time
import logging
from pathlib import Path
from datetime import datetime

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import sys
sys.path.insert(0, str(Path(__file__).parent))
from base_watcher import BaseWatcher


# Gmail API scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


class GmailWatcher(BaseWatcher):
    """
    Watches Gmail for important emails and creates action files.
    """

    def __init__(self, vault_path: str, credentials_path: str = None, token_path: str = None):
        """
        Initialize Gmail Watcher.

        Args:
            vault_path: Path to Obsidian vault
            credentials_path: Path to OAuth credentials.json
            token_path: Path to store token.json
        """
        super().__init__(vault_path, check_interval=120, name='GmailWatcher')

        self.credentials_path = credentials_path or Path.home() / '.gmail_credentials.json'
        self.token_path = token_path or Path.home() / '.gmail_token.json'

        self.service = None
        self.creds = None

    def authenticate(self):
        """Authenticate with Gmail API."""
        creds = None

        # Load existing token
        if self.token_path.exists():
            creds = Credentials.from_authorized_user_file(str(self.token_path), SCOPES)

        # If no valid credentials, get new ones
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not self.credentials_path.exists():
                    self.logger.error(f"Credentials file not found: {self.credentials_path}")
                    self.logger.error("Download from: https://console.cloud.google.com/apis/credentials")
                    raise FileNotFoundError("Gmail credentials not found")

                flow = InstalledAppFlow.from_client_secrets_file(
                    str(self.credentials_path), SCOPES
                )
                creds = flow.run_local_server(port=0)

            # Save credentials
            with open(self.token_path, 'w') as token:
                token.write(creds.to_json())

        self.creds = creds
        self.service = build('gmail', 'v1', credentials=creds)
        self.logger.info("Gmail authentication successful")

    def check_for_updates(self):
        """
        Check for new important unread emails.

        Returns:
            List of message objects
        """
        if not self.service:
            self.authenticate()

        try:
            # Search for important unread emails
            results = self.service.users().messages().list(
                userId='me',
                q='is:unread is:important OR is:unread label:important'
            ).execute()

            messages = results.get('messages', [])

            # Filter out already processed
            new_messages = [
                m for m in messages
                if m['id'] not in self.processed_ids
            ]

            return new_messages

        except HttpError as error:
            self.logger.error(f"Gmail API error: {error}")
            return []

    def get_item_id(self, item):
        """Get message ID."""
        return item['id']

    def get_item_priority(self, item):
        """Determine priority based on labels/sender."""
        try:
            msg = self.service.users().messages().get(
                userId='me',
                id=item['id'],
                metadataHeaders=['From', 'Subject']
            ).execute()

            headers = {h['name']: h['value'] for h in msg['payload']['headers']}
            labels = msg.get('labelIds', [])

            # Check for urgent indicators
            subject = headers.get('Subject', '').lower()
            from_ = headers.get('From', '').lower()

            if 'urgent' in subject or 'asap' in subject:
                return 'critical'
            elif 'invoice' in subject or 'payment' in subject:
                return 'high'
            elif 'important' in labels:
                return 'high'
            else:
                return 'medium'

        except:
            return 'medium'

    def create_action_file(self, message):
        """
        Create action file for email.

        Args:
            message: Gmail message object

        Returns:
            Path to created file
        """
        try:
            # Get full message details
            msg = self.service.users().messages().get(
                userId='me',
                id=message['id'],
                format='full'
            ).execute()

            # Extract headers
            headers = {}
            for h in msg['payload'].get('headers', []):
                headers[h['name']] = h['value']

            # Extract body
            body = self._get_email_body(msg)

            # Get priority
            priority = self.get_item_priority(message)

            # Create frontmatter
            frontmatter = f"""---
type: email
source: GmailWatcher
received: {datetime.now().isoformat()}
priority: {priority}
status: pending
message_id: {message['id']}
from: {headers.get('From', 'Unknown')}
subject: {headers.get('Subject', 'No Subject')}
---
"""

            # Create content
            content = f"""# Email: {headers.get('Subject', 'No Subject')}

## Email Details
- **From**: {headers.get('From', 'Unknown')}
- **To**: {headers.get('To', 'Unknown')}
- **Date**: {headers.get('Date', 'Unknown')}
- **Subject**: {headers.get('Subject', 'No Subject')}

## Email Content
{body}

## Suggested Actions
- [ ] Read and understand email
- [ ] Determine response needed
- [ ] Draft reply if needed (requires approval)
- [ ] Move to /Done when processed

## Notes
Add your notes here about how to handle this email.
"""

            # Write file
            filename = f"EMAIL_{message['id']}.md"
            filepath = self.needs_action / filename

            filepath.write_text(frontmatter + content, encoding='utf-8')

            # Also copy the original to Inbox
            inbox_file = self.vault_path / 'Inbox' / filename
            inbox_file.write_text(frontmatter + content, encoding='utf-8')

            return filepath

        except Exception as e:
            self.logger.error(f"Error creating action file: {e}")
            return None

    def _get_email_body(self, message):
        """Extract email body from message."""
        try:
            payload = message['payload']

            if 'parts' in payload:
                # Multipart message
                for part in payload['parts']:
                    if part['mimeType'] == 'text/plain':
                        data = part['body']['data']
                        import base64
                        return base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
            else:
                # Single part
                if 'body' in payload and 'data' in payload['body']:
                    data = payload['body']['data']
                    import base64
                    return base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')

            return "(Could not extract email body)"

        except:
            return "(Error extracting email body)"


def main():
    """Entry point for Gmail watcher."""
    import sys

    vault_path = Path(__file__).parent.parent / 'AI_Employee_Vault'

    # Check for setup flag
    if '--setup' in sys.argv:
        print("Gmail Watcher Setup")
        print("1. Go to: https://console.cloud.google.com/apis/credentials")
        print("2. Create OAuth 2.0 credentials")
        print("3. Download credentials.json")
        print(f"4. Save to: {Path.home()/.gmail_credentials.json}")
        print("\nThen run: python gmail_watcher.py")
        return

    watcher = GmailWatcher(str(vault_path))

    print("Starting Gmail Watcher...")
    print(f"Vault: {vault_path}")
    print("Press Ctrl+C to stop\n")

    watcher.run()


if __name__ == '__main__':
    main()
