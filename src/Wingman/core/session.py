import time
import re
from Wingman.core.input_receiver import InputReceiver
# Ensure parse_group_status is imported from your parser refactor
from Wingman.core.parser import parse_xp_message, parse_group_status


class GameSession:
    def __init__(self, receiver: InputReceiver):
        self.receiver = receiver
        self.total_xp = 0
        self.start_time = time.time()

        # New: Store the latest snapshot of group members
        self.latest_group_data = []

    def get_xp_per_hour(self):
        if self.total_xp == 0: return 0
        elapsed_seconds = time.time() - self.start_time
        if elapsed_seconds < 1: return 0
        hours = elapsed_seconds / 3600
        return int(self.total_xp / hours)

    def reset(self):
        self.total_xp = 0
        self.start_time = time.time()
        self.latest_group_data = []

    def get_duration_str(self):
        elapsed = int(time.time() - self.start_time)
        hours = elapsed // 3600
        minutes = (elapsed % 3600) // 60
        seconds = elapsed % 60
        return f"{hours:02}:{minutes:02}:{seconds:02}"

    def get_latest_group_data(self):
        """Returns the current list of party members for the GUI."""
        return self.latest_group_data

    def process_queue(self):
        """
        Pops items, calculates XP, and parses Group stats.
        Returns a list of text logs for the GUI.
        """
        logs = []

        # Process everything currently in the stack
        while True:
            line = self.receiver.remove_from_top()
            if line is None:
                break

            # --- Logic 1: Group Detection ---
            # If we see "Someone's group:", we assume a fresh list is coming.
            # We clear the current data so we don't hold onto stale members.

            # OLD:
            # if "group:" in line and re.search(r"^\S+'s group:", line):

            # NEW: Remove the '^' to allow timestamps before the name
            if "group:" in line and re.search(r"\S+'s group:", line):
                self.latest_group_data = []

            # Check for member rows in this line
            found_members = parse_group_status(line)
            if found_members:
                # Add found members to our "dashboard" list
                self.latest_group_data.extend(found_members)

            # --- Logic 2: XP Detection ---
            xp_gain = parse_xp_message(line)

            if xp_gain > 0:
                print(f"DEBUG: XP FOUND: {xp_gain}")
                self.total_xp += xp_gain
                timestamp = time.strftime("%H:%M:%S", time.localtime())
                log_entry = f"[{timestamp}] +{xp_gain:,} XP"
                logs.append(log_entry)

        return logs