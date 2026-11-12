# Lecture 10 — group code inspection of the tic-tac-toe program

This folder is a group submission for the Lecture 10 code-inspection activity. The
group reviewed the 65-line tic-tac-toe program distributed with the lecture
(`src/tictactoe_v1.py`, the same listing that is added by the open pull request
"Add Tic-Tac-Toe game implementation"), reported eleven findings, and produced a
corrected implementation (`src/tictactoe_v2.py`) with tests and evidence.

## What is here

| Path | What it is |
|---|---|
| `src/tictactoe_v1.py` | The program as submitted, reproduced unchanged (only trailing whitespace removed) so the evidence transcripts can be replayed. |
| `src/tictactoe_v2.py` | The corrected implementation, 113 lines, standard library only. |
| `tests/test_tictactoe_v2.py` | 21 `unittest` cases: 11 for `is_win`, 10 for the game loop. Standard library only. |
| `evidence/b1..b4` | Sessions that reproduce the defects on v1 (drawn game that prints `Win!` and `Tie!`, `IndexError`, `ValueError`, overwritten cell). |
| `evidence/s1..s4` | Sessions of v2 that show the corrected behaviour. |
| `INT6181_L10_Group_Code_Inspection_Report.docx` | The full record: roles, ground rules, briefing, moderator's checklist, three private review logs, the meeting's decisions, the fixes, and the verification. |

## Run it

```bash
cd lecture10-code-inspection

# the corrected program
python3 src/tictactoe_v2.py

# the tests
python3 -m unittest discover -s tests -v
```

No `pip install` is needed; everything uses the Python standard library.

## Findings

Severity follows the group's own scale (Blocker / Major / Minor / Nit).

| ID | Lines (v1) | Type | Finding | Fix in v2 |
|---|---|---|---|---|
| F-01 | 44, 47, 49 | Blocker | The prompt asks for 1..3 but the numbers are used directly as list indices, so `1 1` marks the centre and `3 3` raises `IndexError`. | Validate the range, then subtract 1. |
| F-02 | 51–56 | Blocker | After a win on the ninth move `n == 8`, so the separate tie test prints `Tie!` as well. | The win path prints and returns; `Tie!` is printed only after the loop. |
| F-03 | 44–49 | Major | Nothing checks that the target cell is empty, so a player can overwrite an opponent's mark. | Reject occupied cells inside the input loop. |
| F-04 | 44 | Major | Input is trusted: `abc` raises `ValueError`, `3 3` raises `IndexError`, `0 0` and `-1 -1` are accepted. | Two-token check, `int()` in `try`, 1..3 check, `EOFError` handling. |
| F-05 | 55 | Minor | The tie test reads the loop variable after `break`. | Removed together with F-02. |
| F-06 | 30 | Minor | The comment says `False` is Player 1, but the flag starts as `True` and is inverted before use. | Comment replaced. |
| F-07 | 4–21 | Minor | Eight near-identical blocks, 32 comparisons, no early return. | The eight lines are data (`WIN_LINES`) and one loop. |
| F-08 | 28–29 | Minor | `player1` / `player2` are assigned but never read. | Named constants `PLAYER_1`, `PLAYER_2`. |
| F-09 | 38, 46 | Nit | `if turn == False` twice (PEP 8 E712), and the flag is inverted twice per iteration. | The player follows from the move number. |
| F-10 | 43, 59–61 | Minor | `Win!` does not say who won, and the prompt is printed separately from `input()`. | `Win!` kept exactly, winner on the next line; prompt passed to `input()`; rows joined. |
| F-11 | 1–21 | Minor | No docstring, and nothing states the coordinate convention. | Module and function docstrings. |

## Verification

The tests were also run against `src/tictactoe_v1.py` to confirm they are not
vacuous: eight of the game-loop tests fail there, which is the expected result
for the defect areas F-01 to F-04. On v2 all 21 tests pass.
