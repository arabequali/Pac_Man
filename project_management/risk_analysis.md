# Risk analysis

Likelihood and impact: Low, Medium, High. Status: Open, Mitigated, Closed.

| ID | Risk | Likelihood | Impact | Mitigation | Status |
|---|---|---|---|---|---|
| R1 | The program crashes with a traceback during review, which is judged non-functional | Medium | High | Clean error messages for configuration and maze failures, a single final handler in `pac-man.py`, tests for bad input (empty name, closing the window, bad files) | Open: several crash paths found and listed in `acceptance_tests.md` |
| R2 | The assigned maze package is re-installed or its output differs during review | Medium | High | Only `src/maze/generator.py` knows the package. The output is validated (shape, borders, matching walls, connectivity) and any failure becomes a clear error | Mitigated |
| R3 | The configuration is changed at the defense in ways we did not expect, and the strict loader stops where the subject suggests clamping | Medium | Medium | Strict, documented behaviour with exact messages. Try odd configurations in advance (missing key, wrong type, extreme values, unknown keys). Be ready to switch to clamping | Open |
| R4 | A reviewer judges that the graphics library does not respect the MLX-equivalence rule | Medium | High | One wrapper with an MLX-shaped interface, a mapping table in the README, helpers without an MLX counterpart listed, confirmation asked from staff | Open |
| R5 | Packaging or publication on itch.io is left to the end and fails | Medium | High | Try a minimal packaged build early, keep the packaging script at the root, include data files explicitly, check the `.gitignore` does not exclude the spec file | Open |
| R6 | The interface and the engine drift apart (names, directions, positions in cells or pixels) | Medium | Medium | Written interface contract, engine works in cells only, one shared `Direction` type, regular integration | Mitigated, to review |
| R7 | Lint and type errors pile up and `make lint` fails | High | Medium | Run `make lint` before every commit, fix by file | Open |
| R8 | A team member cannot explain a part of the code at the defense, especially AI-assisted code | Medium | High | Each person walks the other through their modules, AI-generated parts are read and tested before being kept, recode exercise rehearsed | Open |
| R9 | The highscore file cannot be written (read-only install folder) or is corrupted | Low | Medium | Tolerant loader, atomic saving, errors logged without stopping the game | Mitigated |
| R10 | Performance drops on large mazes (up to 99 by 99) | Low | Medium | Maze and sprites drawn once per level and cached, sprite size capped, measured at the largest size | To verify |
| R11 | Keyboard layout (for example AZERTY) breaks name entry | Medium | Low | Letters work on every layout. Test digit entry on the layouts used in review | Open |
| R12 | Deadline pressure: required parts (pause, instructions, cheat mode) are missing at the end | Medium | High | Track every subject requirement on the Kanban board, do the mandatory items before polishing | Open |
