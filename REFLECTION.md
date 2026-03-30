## 1. How far did the agent get?
- It built the entire app in a way that guides the user smoothly from start to end, but just with a few small issues. 

## 2. Where did you intervene?
- Corrected the max number of questions to 6 (not 5). I had specified that 3 additional questions be made in "the question" section of the spec= 6 total, but forgot to update this. 
- Removed the word "cumulative" from instructions regarding score reporting because it was creating confusion. I made sure that scores are now only + always reported per session (a session = completing the selected number of questions). Retakes are treated as new sessions and given a fresh score.
- Reworded how score reported to user: "Your cumulative score is now: {new_total}" -> "Your score: {score}/{num_questions}."
- Added salt along with password hashing to make it more secure.
- Added new error message for when user chooses question number that is larger than what is in the category: "Error: Only {num_questions} questions available in this category. Continue? (y/n)" and if user presses y, continue with quiz. If user presses n, go back to category selection. 
- All of these interventions could have been avoided by making sure spec has the most up to date info regarding things like number of questions, uses keywords consistently like "session" instead of introducing new ones like "cumulative", and includes example text for what the score reporting should actually look like.

## 3. How useful was the AI review
- Medium to low. It provided me with some confidence, but mainly only caught issues I had already identified with a quick manual test. 
- It missed a key issue: error handling for when user selects more questions than are available in a category existed but this wasn’t explicitly defined in the acceptance criteria...

## 4. How I could have improved my spec
- I didn't include instructions about file structure in the spec because I wasn't sure how it should look myself. The agent inferred it correctly, but it would definately have been safer to specify. 
- As pointed out in the implementation plan in the first round, the following instructions were confusing: 
1. "Requirement 28 states "No input is taken from user unless it is followed by the Enter input." Requirement 9 states "use up/down arrow keys to select their answer. Enter should submit." I will implement this by capturing arrow keys to update the visual state (moving a cursor/highlight) but only "submitting" the final choice once the user presses Enter."
2. "Password Visibility: The spec says "passwords should be hidden at all times and in all places". Does this mean even the storage file shouldn't show them (using a hash)? I'll assume YES and use SHA-256.
3. Score Obfuscation: The spec says "score should not be [human-readable]". Does this mean per-run scores or cumulative? I will obfuscate the entire history for each user."
- Should have included security considerations as an acceptance criteria from the beginning, instead of just in the prompt for agent 2.

## 5. When would you use this workflow?
- For most non–speed-build projects, especially given my go-to IDE (Antigravity) supports agentic workflows natively.
- I can see it being especially useful for complex, user-facing systems where defining acceptance criteria and error handling upfront helps prevent UX issues.