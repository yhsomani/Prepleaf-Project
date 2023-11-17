import pickle

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def search(self, word):
        node = self._search_node(word)
        return node is not None and node.is_end_of_word

    def _search_node(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return None
            node = node.children[char]
        return node

    def _collect_words_from_trie(self, node, current_word):
        words = []
        if node.is_end_of_word:
            words.append(current_word)
        for char, child_node in node.children.items():
            words.extend(self._collect_words_from_trie(child_node, current_word + char))
        return words

    def load_dictionary(self, file_path):
        with open(file_path, 'rb') as file:
            saved_data = pickle.load(file)
        self.root = saved_data['root']

    def save_dictionary(self, file_path):
        with open(file_path, 'wb') as file:
            data_to_save = {'root': self.root}
            pickle.dump(data_to_save, file)

    def add_to_dictionary(self, word):
        if not self.search(word):
            self.insert(word)

    def remove_from_dictionary(self, word):
        if self.search(word):
            self._remove_from_dictionary(word, self.root, 0)

    def _remove_from_dictionary(self, word, node, index):
        if index == len(word):
            node.is_end_of_word = False
        else:
            char = word[index]
            child_node = node.children[char]
            self._remove_from_dictionary(word, child_node, index + 1)
            if not child_node.children and not child_node.is_end_of_word:
                del node.children[char]

def levenshtein_distance(s1, s2):
    len_s1, len_s2 = len(s1), len(s2)

    matrix = [[0] * (len_s2 + 1) for _ in range(len_s1 + 1)]

    for i in range(len_s1 + 1):
        matrix[i][0] = i
    for j in range(len_s2 + 1):
        matrix[0][j] = j

    for i in range(1, len_s1 + 1):
        for j in range(1, len_s2 + 1):
            cost = 0 if s1[i - 1] == s2[j - 1] else 1
            matrix[i][j] = min(
                matrix[i - 1][j] + 1,
                matrix[i][j - 1] + 1,
                matrix[i - 1][j - 1] + cost
            )

    return matrix[len_s1][len_s2]

def damerau_levenshtein_distance(s1, s2):
    len_s1, len_s2 = len(s1), len(s2)

    matrix = [[0] * (len_s2 + 1) for _ in range(len_s1 + 1)]

    for i in range(len_s1 + 1):
        matrix[i][0] = i
    for j in range(len_s2 + 1):
        matrix[0][j] = j

    for i in range(1, len_s1 + 1):
        for j in range(1, len_s2 + 1):
            cost = 0 if s1[i - 1] == s2[j - 1] else 1
            matrix[i][j] = min(
                matrix[i - 1][j] + 1,
                matrix[i][j - 1] + 1,
                matrix[i - 1][j - 1] + cost
            )

            if i > 1 and j > 1 and s1[i - 1] == s2[j - 2] and s1[i - 2] == s2[j - 1]:
                matrix[i][j] = min(matrix[i][j], matrix[i - 2][j - 2] + cost)

    return matrix[len_s1][len_s2]

class SpellChecker:
    def __init__(self, language='english', dictionary_path='dictionary.txt'):
        self.language = language
        self.trie = Trie()
        self.load_dictionary(dictionary_path)

    def load_dictionary(self, dictionary_path):
        try:
            self.trie.load_dictionary(dictionary_path)
            print(f"Dictionary for {self.language} language loaded successfully.")
        except FileNotFoundError:
            print(f"Dictionary file for {self.language} not found. Creating a new one.")
            self.trie.save_dictionary(dictionary_path)
        except EOFError:
            print(f"Error loading dictionary for {self.language}. Creating a new one.")
            self.trie.save_dictionary(dictionary_path)

    def change_language(self, language):
        self.language = language
        print(f"Language changed to {self.language}.")

    def display_suggestions(self, word):
        suggestions = self._suggest_corrections(word)
        if suggestions:
            print("Suggestions:")
            for suggestion in suggestions:
                print(f"  - {suggestion}")
        else:
            print("No suggestions found.")

    def _suggest_corrections(self, input_word):
        suggestions = []
        current_word = ""
        node = self.trie.root
        self._suggest_corrections_recursive(input_word, current_word, node, suggestions)
        return suggestions

    def _suggest_corrections_recursive(self, input_word, current_word, node, suggestions):
        if node.is_end_of_word:
            suggestions.append(current_word)

        for char, child_node in node.children.items():
            self._suggest_corrections_recursive(input_word, current_word + char, child_node, suggestions)

    def modify_dictionary(self, word):
        if not self.trie.search(word):
            print(f"'{word}' is not in the dictionary.")
            response = input("Do you want to add it to the dictionary? (yes/no): ").lower()
            if response == 'yes':
                self.trie.insert(word)
                self.trie.save_dictionary("dictionary.txt")
                print(f"'{word}' added to the dictionary.")
            else:
                print("No modifications made.")
        else:
            print(f"'{word}' is already in the dictionary.")

def get_user_input():
    user_input = input("Enter a potentially misspelled word: ")
    return user_input

def validate_input(word):
    return word.isalpha()

def display_suggestions(suggestions):
    if suggestions:
        print("Suggestions:")
        for suggestion in suggestions:
            print(f"  - {suggestion}")
    else:
        print("No suggestions found.")

def confirm_modifications():
    response = input("Do you want to confirm the modifications? (yes/no): ").lower()
    return response == 'yes'

def run_tests(spell_checker):
    user_input = get_user_input()

    if not validate_input(user_input):
        print("Input must consist of alphabetic characters.")
        return

    suggestions = spell_checker._suggest_corrections(user_input)
    display_suggestions(suggestions)

    if confirm_modifications():
        spell_checker.trie.insert(user_input)
        spell_checker.trie.save_dictionary("dictionary.txt")
        print("Dictionary modified and saved.")

def main():
    
    spell_checker = SpellChecker(language='english', dictionary_path='english_dictionary.txt')

    while True:
        print("\n===== Spell Checker Application =====")
        print("1. Check Spelling")
        print("2. Modify Dictionary")
        print("3. Change Language")
        print("4. Exit")

        choice = input("Enter your choice (1/2/3/4): ")

        if choice == '1':
            run_tests(spell_checker)
        elif choice == '2':
            word_to_modify = input("Enter the word to modify: ")
            spell_checker.modify_dictionary(word_to_modify)
        elif choice == '3':
            new_language = input("Enter the new language: ")
            spell_checker.change_language(new_language)
        elif choice == '4':
            print("Exiting Spell Checker. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    main()
