class CPathChange:
    def __init__(self, max_changes=2, interval=2.0):
        self.max_changes = max_changes
        self.changes_done = 0
        self.time_until_next = interval