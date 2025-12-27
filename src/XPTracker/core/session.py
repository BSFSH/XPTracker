import time
from XPTracker.core.input_receiver import InputReceiver
from XPTracker.core.xp_parser import parse_xp_message


class GameSession:
    def __init__(self, receiver: InputReceiver):
        self.receiver = receiver
        self.total_xp = 0
        self.start_time = time.time()

    def process_queue(self):
        """
        Pops ALL items from the receiver's stack.
        - If it's XP, add to total.
        - If it's not, discard it.
        """
        while True:
            # 1. Get the next line from the stack (FIFO)
            line = self.receiver.remove_from_top()

            # 2. If stack is empty, we are done for now
            if line is None:
                break

            # 3. Check if it is an XP message
            # parse_xp_message returns 0 if it's "garbage" or chat
            xp_gain = parse_xp_message(line)

            if xp_gain > 0:
                self.total_xp += xp_gain

    def get_xp_per_hour(self):
        """
        Calculates XP per hour based on total_xp and elapsed time.
        """
        if self.total_xp == 0:
            return 0

        elapsed_seconds = time.time() - self.start_time

        # Avoid division by zero
        if elapsed_seconds < 1:
            return 0

        hours = elapsed_seconds / 3600
        return int(self.total_xp / hours)