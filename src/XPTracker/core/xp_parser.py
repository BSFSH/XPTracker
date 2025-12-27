import re


def parse_xp_message(line: str) -> int:
    """
    Parses a log line to extract experience points.
    Supports formats:
    1. "You gain X experience points."
    2. "You gain X (+Y) experience points."

    Returns the total integer XP (X + Y), or 0 if no XP found.
    """
    # Regex Breakdown:
    # You gain\s+       -> Matches literal "You gain" followed by whitespace
    # (\d+)             -> Group 1: The base XP amount (digits)
    # (?:\s+\(\+(\d+)\))? -> Non-capturing group for the optional bonus part:
    #     \s+\(\+       -> whitespace, literal '(', literal '+'
    #     (\d+)         -> Group 2: The bonus XP amount (digits)
    #     \)            -> literal ')'
    # .*experience      -> Matches rest of line to ensure context

    xp_pattern = re.compile(r'You gain\s+(\d+)(?:\s+\(\+(\d+)\))?.*experience', re.IGNORECASE)

    match = xp_pattern.search(line)

    if match:
        base_xp = int(match.group(1))
        bonus_xp = 0

        # If Group 2 exists (the bonus part), add it
        if match.group(2):
            bonus_xp = int(match.group(2))

        return base_xp + bonus_xp

    return 0