#!/usr/bin/env python3
"""
Base Watcher Template for Personal AI Employee

All watchers should inherit from BaseWatcher and implement:
- check_for_updates(): Returns list of new items to process
- create_action_file(item): Creates .md file in Needs_Action folder
"""

import time
import logging
from pathlib import Path
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Any, Optional


class BaseWatcher(ABC):
    """
    Abstract base class for all AI Employee watchers.

    Watchers monitor external sources (Gmail, WhatsApp, files, etc.)
    and create actionable markdown files in the Needs_Action folder
    for Claude Code to process.
    """

    def __init__(
        self,
        vault_path: str,
        check_interval: int = 60,
        name: Optional[str] = None
    ):
        """
        Initialize the watcher.

        Args:
            vault_path: Path to the Obsidian vault
            check_interval: Seconds between checks (default: 60)
            name: Optional custom name for logging
        """
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / 'Needs_Action'
        self.check_interval = check_interval
        self.name = name or self.__class__.__name__
        self.logger = self._setup_logging()

        # Ensure Needs_Action folder exists
        self.needs_action.mkdir(parents=True, exist_ok=True)

        # State tracking
        self.processed_ids: set = set()
        self.is_running = False

    def _setup_logging(self) -> logging.Logger:
        """Configure logging for this watcher."""
        logger = logging.getLogger(self.name)
        logger.setLevel(logging.INFO)

        # Console handler
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger

    @abstractmethod
    def check_for_updates(self) -> List[Any]:
        """
        Check for new updates from the monitored source.

        Returns:
            List of new items to process (items not in processed_ids)
        """
        pass

    @abstractmethod
    def create_action_file(self, item: Any) -> Optional[Path]:
        """
        Create a markdown action file in the Needs_Action folder.

        Args:
            item: The item to create an action file for

        Returns:
            Path to the created file, or None if creation failed
        """
        pass

    @abstractmethod
    def get_item_id(self, item: Any) -> str:
        """
        Get a unique identifier for an item.

        Args:
            item: The item to get an ID for

        Returns:
            Unique string identifier for this item
        """
        pass

    def get_item_priority(self, item: Any) -> str:
        """
        Determine priority level for an item.

        Args:
            item: The item to prioritize

        Returns:
            Priority level: 'critical', 'high', 'medium', or 'low'
        """
        return 'medium'

    def generate_frontmatter(self, item: Any, item_type: str) -> str:
        """
        Generate YAML frontmatter for action files.

        Args:
            item: The item being processed
            item_type: Type of item (email, whatsapp, file, etc.)

        Returns:
            YAML frontmatter string
        """
        priority = self.get_item_priority(item)
        now = datetime.now().isoformat()

        return f"""---
type: {item_type}
source: {self.name}
received: {now}
priority: {priority}
status: pending
item_id: {self.get_item_id(item)}
---
"""

    def create_log_entry(self, action: str, details: str) -> None:
        """
        Create an entry in the activity log.

        Args:
            action: Action performed (e.g., 'created', 'skipped')
            details: Additional details about the action
        """
        logs_dir = self.vault_path / 'Logs'
        logs_dir.mkdir(exist_ok=True)

        today = datetime.now().strftime('%Y-%m-%d')
        log_file = logs_dir / f'{today}.md'

        timestamp = datetime.now().strftime('%H:%M:%S')
        entry = f"\n## [{timestamp}] {action}\n- Source: {self.name}\n- Details: {details}\n"

        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(entry)

    def process_item(self, item: Any) -> bool:
        """
        Process a single item: create action file and log.

        Args:
            item: The item to process

        Returns:
            True if successful, False otherwise
        """
        try:
            filepath = self.create_action_file(item)
            if filepath:
                self.processed_ids.add(self.get_item_id(item))
                self.logger.info(f"Created action file: {filepath.name}")
                self.create_log_entry('action_created', str(filepath))
                return True
            return False
        except Exception as e:
            self.logger.error(f"Error processing item: {e}")
            return False

    def run_once(self) -> int:
        """
        Run a single check cycle.

        Returns:
            Number of items processed
        """
        try:
            items = self.check_for_updates()
            count = 0

            for item in items:
                item_id = self.get_item_id(item)
                if item_id not in self.processed_ids:
                    if self.process_item(item):
                        count += 1

            if count > 0:
                self.logger.info(f"Processed {count} new item(s)")

            return count

        except Exception as e:
            self.logger.error(f"Error in check cycle: {e}")
            return 0

    def run(self) -> None:
        """
        Main loop: continuously check for updates.
        Press Ctrl+C to stop.
        """
        self.is_running = True
        self.logger.info(f"Starting {self.name}")
        self.logger.info(f"Vault: {self.vault_path}")
        self.logger.info(f"Check interval: {self.check_interval}s")

        try:
            while self.is_running:
                self.run_once()
                time.sleep(self.check_interval)

        except KeyboardInterrupt:
            self.logger.info(f"Stopping {self.name}...")
            self.is_running = False

    def stop(self) -> None:
        """Stop the watcher gracefully."""
        self.is_running = False
        self.logger.info(f"{self.name} stopped")


if __name__ == '__main__':
    # Example usage
    print("BaseWatcher is an abstract class.")
    print("Inherit from it to create specific watchers.")
