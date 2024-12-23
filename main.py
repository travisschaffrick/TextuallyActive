import pickle
import os
import re


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


def main():
    db = Database()
    # Polling for input
    while True:
        line = input()

        if line == '!quit':
            db.save()
            print('See ya!')
            break

        if line == '!clear':
            os.remove('data.json')
            print('Data cleared')
            break

        sentences = re.split(r'[.,;!?]', line)
        # Process each sentence
        for sentence in sentences:
            tokens = sentence.split()  # Split sentence into words
            for i in range(len(tokens)):
                # Stripping words of capitals and punctuation
                tokens[i] = tokens[i].lower()
                punc = '''!()-[]{};:'"\\,<>./?@#$%^&*_~'''
                tokens[i] = "".join([char if char not in punc else "" for char in tokens[i]])

            # Turning each sentence into an array of all contiguous combinations of words
            all_patterns_final_word = words_to_patterns(tokens)
            # Adding/Incrementing new/pre-existing entries in the database
            for pattern in all_patterns_final_word:
                new_pattern = Pattern(pattern[:-1], pattern[-1])
                # Check if the pattern already exists in the database
                existing_pattern = None
                for stored_pattern in db.data:
                    if stored_pattern == new_pattern:
                        existing_pattern = stored_pattern
                        break

                # If pattern exists, increment occurrences, otherwise, insert new pattern
                if existing_pattern:
                    existing_pattern.increment_occurrences()
                else:
                    db.insert(new_pattern)
        print("Type more or use '!quit' to exit, or use !clear to clear the entire database")

    guess_word(db)


def guess_word(db):
    """
    Guess word based on user input by accessing database.
    :return:
    :param db: Database of user-generated contextual sentences
    """
    input_words = input("Input some context and I will try to predict the next word: ").lower().split()
    best = ("", 0, 0)  # (most likely word, match score, number of occurrences)
    print(db.all_patterns())
    for pattern in db.all_patterns():
        if pattern.get_ends_with() == input_words[-1]:
            continue
        match_score = get_match_score(pattern, input_words)
        occurrences = pattern.occurrences

        if match_score > best[1] or match_score == best[1] and occurrences > best[2]:
            best = (pattern.get_ends_with(), match_score, occurrences)
            print(best)
    if best[0]:
        print(f'''I predict you'll say "{best[0]}" next''')
    else:
        print("My vision is hazy... try again later.")


def words_to_patterns(words):
    """
    :param words: String of user-generated words
    :return: All possible combinations of words with order maintained, returning context and the next word
    """
    # Examples:
    # >>> words_to_patterns(["a", "b", "c"])
    # [['a', 'b'], ['a', 'b', 'c'], ['b', 'c']]
    # >>> words_to_patterns(["a"])
    # []
    # >>> words_to_patterns([])
    # []
    res = []
    for start in range(0, len(words) - 1):
        for end in range(start + 2, len(words) + 1):
            res.append(words[start:end])
    return res


def get_match_score(pattern: Pattern, input_words: list[str]):
    '''

    :param pattern:
    :param input_words:
    :return int: Match score
    '''
    # Calculating match score
    # pattern: this is a phrase that ends
    # input: what is a phrase that ____
    # unweighted match_score should be 4
    match_length = 0
    for i in range(len(input_words)):
        if i < len(pattern.get_begins_with()):
            if pattern.get_begins_with()[-i] == input_words[-i]:
                match_length += 1
            else:
                return 2 ** match_length
    return 2 ** match_length


if __name__ == "__main__":
    main()
