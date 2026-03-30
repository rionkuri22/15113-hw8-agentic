## 1. How far did the agent get?
- Made entire thing in a way that guides user smoothly from start to end of program but just with some small issues. 

## 2. Where did you intervene?
- Fix max questions to 6 instead of 5. My mistake. Forgot that I had written instructions to create 3 additional questions= 6 total. 
- No need for cumulative score reporting. Just report total score after each session where session= if asked for 3 questioins and finished 3 questions. If user retakes quiz, consider new session and give new score at end of it. 
- Reword how score reported to user: "Your cumulative score is now: {new_total}" -> "Your score: {score}/{num_questions}."
- Added salt along with password hashing to make it more secure.
- Added new error message for when user chooses question number that is larger than what is in the category: "Error: Only {num_questions} questions available in this category. Continue? (y/n)" and if user presses y, continue with quiz. If user presses n, go back to category selection. 
- All could have been prevented by making sure spec has most up to date correct info like number of questions, is easy to understand and even includes example text for what the score reporting should look like.

## 3. How useful was the AI review
- Medium to low. Gave me confidence but only caught problems that I noticed in 1 few minute check run right after agent output
- Dropped issue where but technically failed to specify it as acceptance criteria in spec. 

## 4. How I could have improved my spec
- Failed to include file strucutre and instrucitons in spec because was not sure how it should look but agent was able to figure it out. Probs safer to add it though.
- As pointed out by implemnetaiton plan in first round, some confusing instructions. AI was able to interpret correctly so did not have to intervene to correct but could have caused problems. 
1. "Requirement 28 states "No input is taken from user unless it is followed by the Enter input." Requirement 9 states "use up/down arrow keys to select their answer. Enter should submit." I will implement this by capturing arrow keys to update the visual state (moving a cursor/highlight) but only "submitting" the final choice once the user presses Enter."
2. "Password Visibility: The spec says "passwords should be hidden at all times and in all places". Does this mean even the storage file shouldn't show them (using a hash)? I'll assume YES and use SHA-256.
3. Score Obfuscation: The spec says "score should not be [human-readable]". Does this mean per-run scores or cumulative? I will obfuscate the entire history for each user."
- Include instructions to make secure from beginning
- 

## 5. When would you use this workflow?
- Probs for anything that is not a speed build. Especially since availability of agents on Antigravity= my current go to IDE, will probs use this workflow for most projects going forward: specify accepance criteria, error handling etc. 
- Is espcially useful for projects that are more complex and are used by other users because it helps catch bugs before they inconvenience anybody else. 