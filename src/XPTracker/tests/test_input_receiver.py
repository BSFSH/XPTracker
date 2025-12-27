from XPTracker.core.input_receiver import InputReceiver

RAW_MSG = "[0;37mYou attack a slimey-skinned black balrog with a glowing mithril heavy platinum fists for[0;0m[0;37m[1;31m 106[0;0m[0;37m damage!"
CLEAN_MSG = "You attack a slimey-skinned black balrog with a glowing mithril heavy platinum fists for 106 damage!"


class TestInputReceiver:
    def test_receive(self):
        """
        When a packet from the target IP/src port is detected, extract the payload in plain text
        """
        input_line = "Test input line"
        ir = InputReceiver()
        ir.receive(input_line)
        assert ir.get_last_received() == input_line

    def test_clean_message(self):
        """
        Take any packet from the server and remove the trash/flags from it
        """
        cleaned = InputReceiver.clean_message(RAW_MSG)
        assert cleaned == CLEAN_MSG
        pass

    def test_queue_line(self):
        """
        Take a cleaned string and add it to our stack of queued lines
        """
        ir = InputReceiver()
        ir.receive(CLEAN_MSG)
        assert ir.remove_from_top() == CLEAN_MSG
        pass

    def test_get_line(self):
        """
        When requested, return the line from the top of the queue, and remove it from the queue
        Make sure what goes in first, comes out first
        """
        ir = InputReceiver()
        input_line1 = "First input line"
        input_line2 = "Second input line"
        ir.receive(input_line1)
        ir.receive(input_line2)
        top_item = ir.remove_from_top()
        assert top_item == input_line1
