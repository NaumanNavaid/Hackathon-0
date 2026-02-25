#!/usr/bin/env python3
"""
LinkedIn Poster for Personal AI Employee

Automatically posts business updates to LinkedIn.

Usage:
    python linkedin_poster.py --post "Your content here"

Requirements:
    pip install playwright
    playwright install chromium
"""

import argparse
import logging
from pathlib import Path
from datetime import datetime

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("Playwright not installed. Run: pip install playwright")
    exit(1)


class LinkedInPoster:
    """
    Posts content to LinkedIn using browser automation.
    """

    def __init__(self, session_path: str = None):
        """
        Initialize LinkedIn Poster.

        Args:
            session_path: Path to store browser session
        """
        self.session_path = session_path or Path.home() / '.linkedin_session'
        self.session_path.mkdir(parents=True, exist_ok=True)

        self.playwright = None
        self.browser = None
        self.page = None

    def _start_browser(self):
        """Start browser."""
        self.playwright = sync_playwright().start()

        self.browser = self.playwright.chromium.launch_persistent_context(
            user_data_dir=str(self.session_path),
            headless=False
        )

        self.page = self.browser.new_page()

    def login(self):
        """Navigate to LinkedIn and ensure logged in."""
        if not self.page:
            self._start_browser()

        self.page.goto('https://www.linkedin.com/login')

        # Check if already logged in (redirected to feed)
        if 'feed' in self.page.url or 'linkedin.com/in/' in self.page.url:
            print("✓ Already logged in to LinkedIn")
            return True

        print("Please log in to LinkedIn...")
        input("Press Enter after logging in...")

        return True

    def create_post(self, content: str, schedule_time: str = None):
        """
        Create a LinkedIn post.

        Args:
            content: Post content
            schedule_time: Optional ISO format datetime to schedule

        Returns:
            True if successful, False otherwise
        """
        try:
            if not self.page:
                self.login()

            # Go to LinkedIn home
            self.page.goto('https://www.linkedin.com/feed/')
            self.page.wait_for_load_state('networkidle')

            # Click post button
            post_button = self.page.query_selector('button[aria-label*="Start a post"], button[aria-label*="Create a post"]')

            if not post_button:
                # Try alternative selector
                post_button = self.page.query_selector('.share-box-feed-entry__trigger, .share-button')

            if post_button:
                post_button.click()
                self.page.wait_for_timeout(2000)

            # Find text area
            text_area = self.page.query_selector('div[contenteditable="true"][role="textbox"], .ql-editor')

            if text_area:
                text_area.fill(content)
                self.page.wait_for_timeout(1000)

                # Save as draft (require approval before posting)
                print("✓ Post drafted (requires manual review before posting)")

                # For Silver Tier, we save draft info
                draft_info = f"""
# LinkedIn Post Draft

## Content
{content}

## Created
{datetime.now().isoformat()}

## Status
Draft - Ready for review and approval

## To Post
1. Review the post in LinkedIn
2. Click "Post" to publish
"""
                return draft_info

            else:
                print("✗ Could not find text area")
                return False

        except Exception as e:
            print(f"✗ Error: {e}")
            return False

    def close(self):
        """Close browser."""
        try:
            if self.browser:
                self.browser.close()
            if self.playwright:
                self.playwright.stop()
        except:
            pass


def main():
    """Entry point for LinkedIn poster."""
    parser = argparse.ArgumentParser(description='Post to LinkedIn')
    parser.add_argument('--post', type=str, help='Content to post')
    parser.add_argument('--file', type=str, help='Read content from file')
    parser.add_argument('--setup', action='store_true', help='Setup/login to LinkedIn')

    args = parser.parse_args()

    poster = LinkedInPoster()

    try:
        if args.setup:
            print("LinkedIn Setup")
            print("=" * 40)
            poster.login()
            print("\nSetup complete! You can now use --post to create posts.")
            return

        content = ""

        if args.post:
            content = args.post
        elif args.file:
            content = Path(args.file).read_text()
        else:
            print("Error: Provide --post or --file")
            return

        print("Creating LinkedIn post...")
        result = poster.create_post(content)

        if result:
            print("\nPost draft created!")

    except KeyboardInterrupt:
        print("\nCancelled")
    finally:
        poster.close()


if __name__ == '__main__':
    main()
