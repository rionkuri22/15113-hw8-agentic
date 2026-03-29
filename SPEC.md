Create a command-line Python quiz app that is connected to a pre-determined JSON file. 

# Required features explained in order of user flow: 
- When loaded, display a welcome message and a local login page that prompts users for a username and password or prompts to enter new username and password for first time users. Both options should be made availble each time. Username can be shown as typed but for password, use something like asterisks to hide each character.
- Ask user how many questions they want. Based on integer input by user in the terminal, ramdomly select that many from the default JSON file. Max selection is 5 questions and minimum 1 question.
- Ask user if they want to practice questions from a specific category. There should be 3 options: ”Python Basics", "Data Structures", "All" and these should all have an assigned key input eg) a, s, d or 1, 2, 3.
- Quiz users by asking 1 question at a time. When get wrong, show that report is wrong and make sure to also share correct answer. When correct, report that it was correct. 
There are 3 types of questions. 
For multiple choice, present user with all options and let them use up/down arrow keys to select their answer. Enter should submit their answer. 
For true or false, run it the same way as multiple choice but where the options are always just these 2: "true" and "false". 
For short answer, provide a space for the user to type in their answer. 
- After each question is answered and marked, prompt user to either press Enter to continue to next question or press "n" to flag the question as a bad question that needs rewriting. When flaged as "n", take out of pool of questions to be used in future rounds until manually undisliked in the JSON file.
- In a sepearete file, record score history to track performance and other useful statistics over time for each user. The usernames should be human-readable but the password and score should not be.
- When done with all questions, display final score and give option to retake quiz or quit. 

# Error handling
- If JSON for questions does not exist when quiz is loaded, print error message that specifies that the questions file is missing and exit the program.
- If user types in non-integer for number of questions or a number that is not between 1 and 5, print error message that specifies that the input is invalid and ask user to try again by typing a number is betwen 1 and 5. Continue this until input is something that is expected.
- If user types in non-valid option when selecting categories like 4 or f, print error message that specifies that the input is invalid and ask user to try again by typing a valid option. Make sure to specify what the valid options are again. Continue this until input is something that is expected.
- If user selects category for questions but there are no questions in that category, print error message that specifies that there are no questions in that category and ask user to try again by typing a valid option or by adding questions to that category in the JSON. Continue this until input is something that is expected.

# Acceptance criteria
- The app launches in the terminal and automatically starts with prompt to login or create an account.
- None of the follwing should be used: HTML, CSS, a graphical user interface or any APIs. 
- All passwords are hidden at all times and in all places. 
- All errors are tested and handles with relevant error messages that follow the instructions in the error handling section above.
- Instructions are given clearly at each step to guide the user through the quiz: how to submit choices, quit etc.
- No input is taken from user unless it is followed by the Enter input. In other words, only the last input before the Enter key is pressed should be taken as the user's input.

# The questions 
Put the folliwung 3 questions in a dedicated JSON file.
Based on them, create 3 more questions: 1 true false quesiton about Python Basics, 1 multiple choice question about Data Structures, and 1 short answer question about Data Strucutres. Add these to the same JSON file.

{
  "questions": [
    {
      "question": "What keyword is used to define a function in Python?",
      "type": "multiple_choice",
      "options": ["func", "define", "def", "function"],
      "answer": "def",
      "category": "Python Basics"
    },
    {
      "question": "A list in Python is immutable.",
      "type": "true_false",
      "answer": "false",
      "category": "Data Structures"
    },
    {
      "question": "What built-in function returns the number of items in a list?",
      "type": "short_answer",
      "answer": "len",
      "category": "Python Basics"
    }
  ]
}