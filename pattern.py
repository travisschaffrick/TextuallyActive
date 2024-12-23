class Pattern():
    def __init__(self, beginning: list[str], end: str):
        self.begins_with: list[str] = beginning
        self.ends_with: str = end
        self.occurrences: int = 0

    def __len__(self):
        return len(self.begins_with)

    def __eq__(self, other):
        return self.begins_with == other.begins_with and self.ends_with == other.ends_with

    def __str__(self):
        return f"{self.begins_with} -> {self.ends_with}, {self.occurrences} times"

    def set_begins_with(self, pattern):
        self.begins_with = pattern

    def set_ends_with(self, pattern):
        self.ends_with = pattern

    def get_begins_with(self):
        return self.begins_with

    def get_ends_with(self):
        return self.ends_with

    def increment_occurrences(self):
        self.occurrences += 1