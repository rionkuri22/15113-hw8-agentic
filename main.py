import json
import os
import sys
import hashlib
import base64
import random
import tty
import termios

# --- Configuration ---
QUESTIONS_FILE = "questions.json"
USERS_FILE = "users.json"

# --- Utility Functions ---

def load_data(file_path):
    if not os.path.exists(file_path):
        return None
    with open(file_path, "r") as f:
        return json.load(f)

def save_data(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def obfuscate_score(score):
    # Requirement: "The scores should not be human-readable". Using base64 to store the string representation.
    return base64.b64encode(str(score).encode()).decode()

def deobfuscate_score(obfuscated):
    try:
        return int(base64.b64decode(obfuscated).decode())
    except:
        return 0

def get_char():
    """Reads a single character from stdin without echoing, but handles arrow keys."""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
        if ch == '\x1b':
            ch += sys.stdin.read(2)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def input_with_asterisks(prompt=""):
    """Reads input while displaying asterisks for each character."""
    print(prompt, end="", flush=True)
    password = ""
    while True:
        ch = get_char()
        if ch in ('\r', '\n'):
            print()
            break
        elif ch == '\x7f': # Backspace
            if len(password) > 0:
                password = password[:-1]
                print("\b \b", end="", flush=True)
        else:
            password += ch
            print("*", end="", flush=True)
    return password

def wait_for_enter_or_n():
    """Wait for Enter or 'n' to flag/continue."""
    while True:
        print("\nPress Enter to continue or 'n' to flag this question: ", end="", flush=True)
        inp = input().strip().lower()
        if inp == "" or inp == "n":
            return inp
        print("Invalid input. Press Enter or 'n'.")

def interactive_select(options, question_text):
    """Multiple choice / True-False selection using arrow keys and Enter."""
    selected_idx = 0
    while True:
        # Clear screen (terminal specific, using ANSI escapes for macOS)
        print("\033[H\033[2J", end="")
        print(f"Question: {question_text}\n")
        print("Use Up/Down arrows to select, Enter to submit:\n")
        
        for i, opt in enumerate(options):
            prefix = "> " if i == selected_idx else "  "
            print(f"{prefix}{opt}")
        
        ch = get_char()
        if ch == '\x1b[A': # Up
            selected_idx = (selected_idx - 1) % len(options)
        elif ch == '\x1b[B': # Down
            selected_idx = (selected_idx + 1) % len(options)
        elif ch in ('\r', '\n'): # Enter
            return options[selected_idx]

# --- Main Application Classes ---

class QuizApp:
    def __init__(self):
        self.questions = []
        self.users = {}
        self.current_user = None

    def initialize(self):
        data = load_data(QUESTIONS_FILE)
        if data is None:
            print(f"Error: The questions file '{QUESTIONS_FILE}' is missing.")
            sys.exit(1)
        self.questions = data.get("questions", [])
        
        users_data = load_data(USERS_FILE)
        if users_data:
            self.users = users_data
        else:
            self.users = {}

    def login_page(self):
        print("Welcome to the Python Quiz App!")
        while True:
            print("\n1. Login")
            print("2. Create New Account")
            choice = input("Select an option (1 or 2): ").strip()
            
            if choice not in ('1', '2'):
                print("Invalid option. Please enter 1 or 2.")
                continue

            username = input("Username: ").strip()
            password = input_with_asterisks("Password: ")
            hashed_pw = hash_password(password)

            if choice == '1':
                if username in self.users and self.users[username]["password"] == hashed_pw:
                    self.current_user = username
                    print(f"\nWelcome back, {username}!")
                    break
                else:
                    print("\nInvalid username or password.")
            else:
                if username in self.users:
                    print("\nUsername already exists. Please login or pick another name.")
                else:
                    self.users[username] = {
                        "password": hashed_pw,
                        "score": obfuscate_score(0)
                    }
                    save_data(USERS_FILE, self.users)
                    self.current_user = username
                    print(f"\nAccount created! Welcome, {username}!")
                    break

    def get_settings(self):
        # Number of questions
        while True:
            try:
                num_input = input("\nHow many questions would you like? (1-5): ").strip()
                count = int(num_input)
                if 1 <= count <= 5:
                    break
                print("Invalid. Please type a number between 1 and 5.")
            except ValueError:
                print("Invalid. Please type a number between 1 and 5.")
        
        # Category
        while True:
            print("\nSelect a category:")
            print("1. Python Basics")
            print("2. Data Structures")
            print("3. All")
            cat_choice = input("Enter choice (1, 2, or 3): ").strip()
            
            if cat_choice == '1':
                category = "Python Basics"
            elif cat_choice == '2':
                category = "Data Structures"
            elif cat_choice == '3':
                category = "All"
            else:
                print("Invalid option. Please select 1, 2, or 3.")
                continue
            
            # Check if questions exist for this category
            available = [q for q in self.questions if (category == "All" or q["category"] == category) and not q.get("disliked", False)]
            if not available:
                print(f"Error: There are no available questions in category '{category}'. Please select another or add questions to '{QUESTIONS_FILE}'.")
                continue
            
            return min(count, len(available)), category, available

    def run_quiz(self):
        while True:
            count, category, pool = self.get_settings()
            selected_questions = random.sample(pool, count)
            
            round_score = 0
            for q in selected_questions:
                print("\033[H\033[2J", end="") # Clear screen
                
                if q["type"] == "multiple_choice":
                    user_answer = interactive_select(q["options"], q["question"])
                elif q["type"] == "true_false":
                    user_answer = interactive_select(["true", "false"], q["question"])
                else: # short_answer
                    print(f"Question: {q['question']}")
                    user_answer = input("Your answer: ").strip().lower()

                if user_answer.lower() == q["answer"].lower():
                    print("\nCorrect!")
                    round_score += 1
                else:
                    print(f"\nWrong. The correct answer was: {q['answer']}")
                
                flag = wait_for_enter_or_n()
                if flag == "n":
                    # Flag question as bad
                    for original_q in self.questions:
                        if original_q["question"] == q["question"]:
                            original_q["disliked"] = True
                            break
                    save_data(QUESTIONS_FILE, {"questions": self.questions})
                    print("Question flagged and removed from future rounds.")

            # Update cumulative score
            current_total = deobfuscate_score(self.users[self.current_user]["score"])
            new_total = current_total + round_score
            self.users[self.current_user]["score"] = obfuscate_score(new_total)
            save_data(USERS_FILE, self.users)

            print("\033[H\033[2J", end="")
            print(f"Quiz Complete!")
            # Final score per round is HIDDEN as per user feedback: "Per-run scores should not be reported"
            print(f"Your cumulative score is now: {new_total}")
            
            while True:
                choice = input("\nWould you like to (r)etake the quiz or (q)uit? ").strip().lower()
                if choice == 'r':
                    break
                elif choice == 'q':
                    print("Goodbye!")
                    sys.exit(0)
                else:
                    print("Invalid option. Enter 'r' or 'q'.")

if __name__ == "__main__":
    app = QuizApp()
    app.initialize()
    app.login_page()
    app.run_quiz()
