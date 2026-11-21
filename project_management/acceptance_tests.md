# Acceptance test plan

Status values: **Pass** (checked), **Fail** (checked, broken), **To run** (not
checked yet). The statuses below come from a review of the code and
automated checks on [date]. Update them each time you test, and add the date
and the tester.

## Test cases

### Launch and configuration

| ID | Feature | Steps | Expected result | Status |
|---|---|---|---|---|
| T01 | Valid launch | `python3 pac-man.py config.json` | Main menu appears | To run |
| T02 | Wrong argument count | Launch with no argument, then with two | Usage message, no traceback | Pass |
| T03 | Missing file | Launch with a file that does not exist | Clear message, no traceback | Pass |
| T04 | Invalid JSON | File with a syntax error | Message with line and column | Pass |
| T05 | Comments | Add `# comment` and `// comment` lines | File accepted | Pass |
| T06 | Unknown key | Add an extra key | Ignored | Pass |
| T07 | Missing or invalid value | Remove `lives`, then set it to `"three"` | Message naming the key (the program stops: documented choice) | Pass |
| T08 | Extreme values | Sizes 11 and 99, 0 and huge times, level count 10 and 43 | Accepted if valid, clear message otherwise | To run |
| T09 | Config file unchanged | Run and quit, then compare the file | File identical, comments kept | Fail (the game rewrites it) |

### Maze

| ID | Feature | Steps | Expected result | Status |
|---|---|---|---|---|
| T10 | Fixed first level | Start twice with seed 42 | Same maze | To run |
| T11 | Random later levels | Reach level 2 in two games | Different mazes | To run |
| T12 | Maze validity | Automated checks on generated mazes (borders, matching walls, connectivity) | All pass | Pass |
| T13 | Generator failure | Make the package raise during Start | Clear message, back to the menu, no traceback | Fail (traceback) |
| T14 | Level growth | Play levels 1 to 10 | Size grows by `level_size_increase` | To run |

### Game

| ID | Feature | Steps | Expected result | Status |
|---|---|---|---|---|
| T20 | Start positions | Start a game | Pac-Man in the middle, ghosts in the 4 corners, super-pacgums in the corners | To run |
| T21 | Movement and turns | Press a direction against a wall, then a free one | Pac-Man turns when possible | To run |
| T22 | Pacgum score | Eat a pacgum | Score grows by `points_per_pacgum` | To run |
| T23 | Super-pacgum | Eat one | Score grows, ghosts become edible for `power_duration` | To run |
| T24 | Eat an edible ghost | Touch an edible ghost | Score grows by `points_per_ghosts`, ghost returns to its corner after `ghost_respawn_time` | Fail (no points, no respawn) |
| T25 | Lose a life | Touch a normal ghost | One life less, Pac-Man back to the middle | To run |
| T26 | Game over | Lose every life | Game-over screen with the final score | To run |
| T27 | Level complete | Eat every pacgum | Next level, score and lives kept | To run |
| T28 | Victory | Finish the last level | Victory screen with a congratulation and the score | To run |
| T29 | Time limit | Let the countdown reach 0 | Game ends, uses `level_max_time` | Fail (fixed at 120 seconds) |
| T30 | HUD | During play | Score, lives, level, remaining time visible | To run |
| T31 | Pause | Press the pause key | Pause menu: Resume and Return to main menu | Fail (not implemented) |
| T32 | Close the window | Click the close button or press Alt+F4 | Clean exit | Fail (traceback) |

### Menus and highscores

| ID | Feature | Steps | Expected result | Status |
|---|---|---|---|---|
| T40 | Main menu | Navigate with the keys | Start, Highscores, Instructions, Exit | Fail (Instructions missing) |
| T41 | Instructions | Open it | Controls and rules shown | Fail (not implemented) |
| T42 | New highscore | Finish a game with a top-10 score, type a name | Saved, visible in the table, still there after a restart | To run |
| T43 | Not in the top 10 | Finish with a low score | No name prompt, back to the menu | To run |
| T44 | Name rules | Empty name, 11 letters, symbols, only spaces | Refused or limited, no crash | Fail (traceback) |
| T45 | Damaged score file | Empty file, invalid JSON, wrong structure | Game runs, empty or partial table | Pass |
| T46 | Read-only score file | Make the file or folder read-only | Game continues, warning only | Pass |

### Cheat mode

| ID | Feature | Steps | Expected result | Status |
|---|---|---|---|---|
| T50 | Cheat off | `cheat_mode` false | No cheat key works | To run |
| T51 | Level skip | Cheat on, press the skip key | Level completes | Fail (the key is never read) |
| T52 | Invincibility | Cheat on, touch a ghost | No life lost | Fail (not implemented) |
| T53 | Ghost freeze | Cheat on | Ghosts stop moving | Fail (not implemented) |
| T54 | Extra lives, faster Pac-Man | Cheat on | Lives added, speed increased | Fail (not implemented) |

### Code quality

| ID | Check | Command | Expected result | Status |
|---|---|---|---|---|
| T60 | flake8 | `make lint` | No warning | Fail (275 warnings) |
| T61 | mypy | `make lint` | No error | Fail (83 errors) |
| T62 | Unit tests | `make test` | All pass | To run |
| T63 | Packaged build | Install from the public platform and launch | Works | To run |

## Bugs found and fixed

| ID | Bug | How found | Status |
|---|---|---|---|
| B01 | The game crashed on the first frame (time measured by a method that no longer existed) | Run | Fixed |
| B02 | The maze did not change after changing the size in the options | Run | Fixed (everything is rebuilt at each Start) |
| B03 | The highscore screen did not show a new score | Run | Fixed (table reloaded when the screen opens) |
| B04 | A turn was sometimes ignored (key releases overwrote the request) | Play-testing | Fixed |
| B05 | Closing the window raised `UnboundLocalError` in `handle_events` | Automated check | Open |
| B06 | Name entry raised `ValueError` for an empty name, 11 characters or a symbol | Automated check | Open |
| B07 | A generator failure at Start gave a traceback | Automated check | Open |
| B08 | The cheat key was never read | Code review and check | Open |
| B09 | The level timer ignored `level_max_time`, and the last level was fixed at 10 | Code review | Open |
| B10 | The game rewrote the config file at exit, losing its comments | Code review | Open |
| B11 | Eating an edible ghost gave no points, and eaten ghosts never came back | Code review | Open |
