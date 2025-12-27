import pytest
from XPTracker.core.xp_parser import parse_xp_message

class TestXPParser:

    def test_parse_compound_xp(self):
        """
        Case: User provided example with Base + Bonus XP.
        'You gain 17325 (+43312) experience points.'
        Should return sum: 60637
        """
        log_line = "You gain 17325 (+43312) experience points."
        xp_amount = parse_xp_message(log_line)
        assert xp_amount == 60637

    def test_parse_simple_xp(self):
        """
        Case: Standard XP gain with no bonus.
        'You gain 150 experience points.'
        Should return: 150
        """
        log_line = "You gain 150 experience points."
        xp_amount = parse_xp_message(log_line)
        assert xp_amount == 150

    def test_ignore_irrelevant_lines(self):
        """
        Case: A combat line or chat message containing numbers but no XP.
        Should return 0 (or None, depending on design preference).
        """
        log_line = "You hit the dragon for 150 damage."
        xp_amount = parse_xp_message(log_line)
        assert xp_amount == 0

    def test_parse_strange_formatting(self):
        """
        Case: Handling potential extra spaces or formatting quirks.
        """
        log_line = "   You gain    10 (+5)    experience points.   "
        xp_amount = parse_xp_message(log_line)
        assert xp_amount == 15