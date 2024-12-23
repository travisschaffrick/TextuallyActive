import pickle

class Database():
    def __init__(self):
        # Loading previous patterns
        try:
            with open('patterns.pkl', 'rb') as file:
                self.data = pickle.load(file)
        except FileNotFoundError:
            self.data = []  # Data will be stored {"first word" + "second word", occurrences}
            print("Database not loaded, created new database")

    def save(self):
        with open('patterns.pkl', 'wb') as file:
            pickle.dump(self.data, file)
            print('Data saved')

    def insert(self, data):
        self.data.append(data)
        self.save()
        return True

    def remove(self, pattern):
        self.data.remove(pattern)
        return True

    def all_patterns(self):
        return self.data