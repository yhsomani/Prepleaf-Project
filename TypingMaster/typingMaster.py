import random
import time
import json

# Constants
WORDS_FILE = "./Prepleaf/words.json"
LEADERBOARD_FILE = "./Prepleaf/leaderboard.json"
WORD_COUNT = 10  # Number of words in each test

# Load words from a JSON file into a Python list
def load_words_from_json(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)
    return data

# Update and sort the leaderboard stored in a JSON file
def update_leaderboard(username, wpm):
    leaderboard = load_leaderboard()
    leaderboard.append({"username": username, "wpm": wpm})
    leaderboard = sorted(leaderboard, key=lambda x: x["wpm"], reverse=True)[:10]
    with open(LEADERBOARD_FILE, "w") as file:
        json.dump(leaderboard, file)

# Load leaderboard from a JSON file
def load_leaderboard():
    try:
        with open(LEADERBOARD_FILE, "r") as file:
            leaderboard = json.load(file)
    except FileNotFoundError:
        leaderboard = []
    return leaderboard

# Get user input from the terminal
def get_user_input(prompt):
    while True:
        user_input = input(prompt)
        if user_input.lower() == "ctrl+q":
            exit()
        else:
            return user_input

# Main game logic
def main():
    words_data = load_words_from_json(WORDS_FILE)
    leaderboard = load_leaderboard()

    while True:
        print("Welcome to the Terminal Typing Master!")
        username = get_user_input("Enter your username: ")

        while True:
            option = get_user_input("Select an option: (1) Start Test, (2) Show Leaderboard, (3) Exit\n")
            if option == "1":
                test_words = random.sample(words_data, WORD_COUNT)
                input("Press Enter to start the test...")
                start_time = time.time()

                typed_words = []
                for word in test_words:
                    typed_word = input(f"Type the word: {word}\n")
                    typed_words.append(typed_word)

                end_time = time.time()
                time_taken = end_time - start_time
                words_typed = len(typed_words)
                wpm = int(words_typed / (time_taken / 60))

                print(f"Words Typed: {words_typed}")
                print(f"Time Taken: {time_taken:.2f} seconds")
                print(f"Words Per Minute: {wpm}")

                update_leaderboard(username, wpm)
            elif option == "2":
                print("Leaderboard:")
                for entry in leaderboard:
                    print(f"{entry['username']}: {entry['wpm']} WPM")
            elif option == "3":
                print("Goodbye!")
                exit()
            else:
                print("Invalid option. Please select a valid option (1, 2, or 3).")

if __name__ == "__main__":
    main()
