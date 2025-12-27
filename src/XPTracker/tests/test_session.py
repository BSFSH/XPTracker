import pytest
import time
from XPTracker.core.session import GameSession
from XPTracker.core.input_receiver import InputReceiver


class TestGameSession:

    def test_process_queue_updates_xp(self):
        """
        Push a mix of valid XP messages and garbage text into the receiver.
        Verify that the session processes them and updates the total_xp correctly.
        """
        # 1. Setup
        receiver = InputReceiver()
        session = GameSession(receiver)

        # 2. Inject Data (Mocking the game server)
        # Total expected XP: 100 + (50+50) = 200
        receiver.receive("You gain 100 experience points.")
        receiver.receive("Global Chat: Hello everyone!")  # Garbage - should be ignored
        receiver.receive("You gain 50 (+50) experience points.")
        receiver.receive("Combat: You took 5 damage.")  # Garbage - should be ignored

        # 3. Action: Trigger the processing loop
        session.process_queue()

        # 4. Assertion
        assert session.total_xp == 200

    def test_xp_per_hour_calculation(self):
        """
        Verify XP/hr math.
        If we gained 3600 XP in 1 second, that is 3600 * 3600 = ~12.9M/hr (unrealistic but easy math)
        Let's try a realistic case: 1000 XP in 3600 seconds (1 hour) = 1000 XP/hr
        """
        receiver = InputReceiver()
        session = GameSession(receiver)

        # Override start time to be 1 hour ago
        session.start_time = time.time() - 3600
        session.total_xp = 1000

        assert session.get_xp_per_hour() == 1000