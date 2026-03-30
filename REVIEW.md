# Code Review: Python Quiz Application

This review evaluates the implementation of the Python Quiz Application against the requirements specified in [SPEC.md](file:///Users/rion/Desktop/Github/15113-hw8-agentic/SPEC.md).

## Summary Table

| Requirement | Status | Note |
| :--- | :--- | :--- |
| **Authentication System** | [PASS] | Login/Registration with hidden passwords. |
| **Question Selection** | [PASS] | 1-5 questions, category filtering. |
| **Question Types** | [PASS] | MC, TF, Short Answer implemented. |
| **Interactive UI** | [PASS] | Arrow key selection for MC/TF. |
| **Error Handling** | [PASS] | Comprehensive validation for files and inputs. |
| **Score History** | [FAIL] | Records cumulative score, but fails to show per-round final score. |
| **Question Flagging** | [PASS] | Correctly removes "disliked" questions from pool. |
| **Security** | [WARN] | Passwords hashed (SHA256) but without salt. |

---

## Detailed Findings

1. **[PASS] Local Login & Password Masking**
   - **File**: `main.py` (Lines 121-154, 52-68)
   - **Implementation**: The `login_page` function correctly offer Login/Create Account options. `input_with_asterisks` uses `get_char` to read raw input and print asterisks, satisfying the requirement to hide passwords during entry.

2. **[PASS] Interactive Multiple Choice (Arrow Keys)**
   - **File**: `main.py` (Lines 79-99)
   - **Implementation**: The `interactive_select` function implements arrow key navigation using ANSI escape sequences (`\x1b[A` for Up, `\x1b[B` for Down) and submits on Enter. This matches the spec's requirement for UX.

3. **[FAIL] Final Score Reporting**
   - **File**: `main.py` (Lines 235-236)
   - **Snippet**:
     ```python
     # Final score per round is HIDDEN as per user feedback: "Per-run scores should not be reported"
     print(f"Your cumulative score is now: {new_total}")
     ```
   - **Issue**: `SPEC.md` line 14 states: *"When done with all questions, display final score"*. The current implementation only displays the cumulative total across all sessions. It fails to report the score for the quiz session just completed (e.g., "3/5"). The comment indicates an intentional deviation, but it contradicts the provided specification.

4. **[PASS] Question Flagging (the "n" key)**
   - **File**: `main.py` (Lines 217-226)
   - **Implementation**: Uses `wait_for_enter_or_n` to capture the flag. If "n" is entered, the question's `disliked` property is set to `True` in the global list and persisted to `questions.json`. Filtering in `get_settings` ensures these are excluded from future rounds.

5. **[PASS] Error Handling: Missing Questions File**
   - **File**: `main.py` (Lines 109-112)

6. **[PASS] Error Handling: Invalid Question Count**
   - **File**: `main.py` (Lines 158-167)
   - **Implementation**: Uses a `while True` loop with a `try-except` block to ensure the user enters an integer between 1 and 5. Correctly re-prompts until valid input is received.

7. **[PASS] Score/Password Obfuscation**
   - **File**: `main.py` (Lines 26-31), `users.json`
   - **Implementation**: Passwords are saved as SHA256 hashes. Scores are obfuscated using Base64. Both satisfy the requirement that they remain "not human-readable" in the storage file.

8. **[WARN] Security: Unsalted Password Hashes**
   - **File**: `main.py` (Line 27)
   - **Implementation**: `hash_password(password)`
   - **Issue**: While the passwords are not human-readable, the app does not use a "salt". This makes the hashes vulnerable to rainbow table attacks. For a consumer-facing app, this is a security risk, though it may be acceptable for a basic CLI project given the spec's simplicity.

9. **[PASS] Question Data Completion**
   - **File**: `questions.json`
   - **Implementation**: The file contains the 3 initial questions plus the 3 mandated new ones (1 True/False Basics, 1 MC Data Structures, 1 Short Answer Data Structures).

10. **[PASS] Input Behavior (the Enter key)**
    - **File**: `main.py` (Lines 132, 160, 174, 209, 239)
    - **Implementation**: All text-based inputs use `input()`, ensuring that no action is taken until the user presses Enter (as per Acceptance Criterion 28). Interactive selection is the only exception, which is explicitly allowed by the spec's arrow key requirement.

---

## Verdict
The code is excellently structured and handles terminal-specific interactions (raw mode for arrows, ANSI clearing) very well for macOS. The core logic is robust. The primary failure is the **missing per-session score report**, which is a direct requirement of the specification.
