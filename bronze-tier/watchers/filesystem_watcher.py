#!/usr/bin/env python3
"""
File System Watcher for Personal AI Employee

Monitors a drop folder (/Inbox) for new files and creates
actionable markdown files in /Needs_Action for Claude Code.

Usage:
    python filesystem_watcher.py

Requirements:
    pip install watchdog
"""

import shutil
import time
from pathlib import Path
from datetime import datetime
from typing import List, Any
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileCreatedEvent

from base_watcher import BaseWatcher


class DropFolderHandler(FileSystemEventHandler):
    """
    Handles file system events in the monitored drop folder.

    When a new file is detected, it's copied to Needs_Action
    with a corresponding markdown metadata file.
    """

    def __init__(self, vault_path: str, processed_ids: set):
        """
        Initialize the drop folder handler.

        Args:
            vault_path: Path to the Obsidian vault
            processed_ids: Set to track processed files
        """
        super().__init__()
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / 'Needs_Action'
        self.inbox = self.vault_path / 'Inbox'
        self.processed_ids = processed_ids
        self.logger = self._setup_logging()

    def _setup_logging(self):
        import logging
        logger = logging.getLogger('DropFolderHandler')
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - DropFolder - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        return logger

    def on_created(self, event):
        """
        Handle new file creation events.

        Args:
            event: FileSystemEvent from watchdog
        """
        if event.is_directory:
            return

        source = Path(event.src_path)

        # Skip temporary files
        if source.name.startswith('~') or source.name.startswith('.'):
            return

        # Wait for file to be fully written
        time.sleep(0.5)

        # Check if file still exists (might have been temporary)
        if not source.exists():
            return

        self.logger.info(f"New file detected: {source.name}")

        try:
            self.process_file(source)
        except Exception as e:
            self.logger.error(f"Error processing {source.name}: {e}")

    def process_file(self, source: Path) -> None:
        """
        Process a new file: copy to Needs_Action and create metadata.

        Args:
            source: Path to the source file
        """
        file_id = f"FILE_{int(time.time())}_{source.name}"

        # Copy file to Needs_Action
        dest = self.needs_action / f"{file_id}{source.suffix}"
        shutil.copy2(source, dest)

        # Create metadata markdown file
        meta_path = self.needs_action / f"{file_id}.md"

        frontmatter = self.generate_frontmatter(source)
        content = self.generate_content(source)

        meta_path.write_text(frontmatter + content, encoding='utf-8')
        self.processed_ids.add(file_id)

        self.logger.info(f"Created action file: {meta_path.name}")

    def generate_frontmatter(self, source: Path) -> str:
        """Generate YAML frontmatter for the file."""
        now = datetime.now().isoformat()
        size = source.stat().st_size

        return f"""---
type: file_drop
source: FileSystemWatcher
received: {now}
priority: medium
status: pending
original_name: {source.name}
file_size: {size} bytes
file_type: {source.suffix or 'unknown'}
---
"""

    def generate_content(self, source: Path) -> str:
        """Generate content for the action file."""
        size_kb = source.stat().st_size / 1024

        return f"""
# File Drop: {source.name}

## File Information
- **Original Path**: `{source}`
- **Size**: {size_kb:.2f} KB
- **Type**: {source.suffix or 'unknown'}
- **Detected**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Suggested Actions
- [ ] Review file contents
- [ ] Determine processing needed
- [ ] Execute action or move to appropriate folder

## Notes
Add your notes here about how to handle this file.
"""

    def create_log_entry(self, action: str, details: str) -> None:
        """Create an entry in the activity log."""
        logs_dir = self.vault_path / 'Logs'
        logs_dir.mkdir(exist_ok=True)

        today = datetime.now().strftime('%Y-%m-%d')
        log_file = logs_dir / f'{today}.md'

        timestamp = datetime.now().strftime('%H:%M:%S')
        entry = f"\n## [{timestamp}] {action}\n- Source: FileSystemWatcher\n- Details: {details}\n"

        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(entry)


class FileSystemWatcher(BaseWatcher):
    """
    File System Watcher that monitors the /Inbox folder.

    Uses watchdog to detect new files dropped into the inbox
    and creates action files for Claude to process.
    """

    def __init__(self, vault_path: str, check_interval: int = 60):
        """
        Initialize the file system watcher.

        Args:
            vault_path: Path to the Obsidian vault
            check_interval: Not used for watchdog, kept for compatibility
        """
        super().__init__(vault_path, check_interval, name='FileSystemWatcher')
        self.inbox = self.vault_path / 'Inbox'
        self.inbox.mkdir(parents=True, exist_ok=True)

        self.observer = None
        self.handler = None

    def check_for_updates(self) -> List[Any]:
        """
        Not used for watchdog-based monitoring.
        The handler processes events in real-time.
        """
        return []

    def get_item_id(self, item: Any) -> str:
        """Get ID for an item (not used for watchdog mode)."""
        return str(item)

    def create_action_file(self, item: Any) -> None:
        """Not used for watchdog mode (handler creates files directly)."""
        return None

    def run(self) -> None:
        """
        Start monitoring the inbox folder using watchdog.

        Press Ctrl+C to stop.
        """
        self.is_running = True
        self.logger.info("Starting FileSystemWatcher (watchdog mode)")
        self.logger.info(f"Monitoring: {self.inbox}")

        # Set up watchdog observer
        self.observer = Observer()
        self.handler = DropFolderHandler(str(self.vault_path), self.processed_ids)
        self.observer.schedule(self.handler, str(self.inbox), recursive=False)
        self.observer.start()

        try:
            while self.is_running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.logger.info("Stopping FileSystemWatcher...")
            self.observer.stop()
        finally:
            self.observer.join()
            self.is_running = False


def main():
    """Entry point for running the file system watcher."""
    import sys

    # Default vault path is current directory + AI_Employee_Vault
    default_vault = Path(__file__).parent.parent / 'AI_Employee_Vault'
    vault_path = Path(sys.argv[1]) if len(sys.argv) > 1 else default_vault

    if not vault_path.exists():
        print(f"Error: Vault path does not exist: {vault_path}")
        print(f"Creating vault structure...")
        vault_path.mkdir(parents=True, exist_ok=True)
        (vault_path / 'Inbox').mkdir(exist_ok=True)
        (vault_path / 'Needs_Action').mkdir(exist_ok=True)
        (vault_path / 'Done').mkdir(exist_ok=True)

    print(f"Starting FileSystemWatcher...")
    print(f"Vault: {vault_path}")
    print(f"Drop files in: {vault_path / 'Inbox'}")
    print(f"Press Ctrl+C to stop\n")

    watcher = FileSystemWatcher(str(vault_path))
    watcher.run()


if __name__ == '__main__':
    main()
