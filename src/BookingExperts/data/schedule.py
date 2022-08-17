class Schedule:
    def __init__(self):
        self.schedule = {}

    def __contains__(self, item):
        return item in self.schedule and self.schedule[item] is not None

    def __setitem__(self, key, value):
        pass
