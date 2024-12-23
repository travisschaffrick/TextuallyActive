import os
import re
from pattern import Pattern
from database import Database


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
                for stored_pattern in db.all_patterns():
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
    for pattern in db.all_patterns():
        if pattern.get_ends_with() == input_words[-1]:
            continue
        match_score = get_match_score(pattern, input_words)
        occurrences = pattern.occurrences

        if match_score > best[1] or match_score == best[1] and occurrences > best[2]:
            best = (pattern.get_ends_with(), match_score, occurrences)
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
