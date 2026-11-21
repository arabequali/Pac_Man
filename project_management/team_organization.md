# Team organization

## Members and responsibilities

| Member | Main responsibility | Modules |
|---|---|---|
| avally | Interface | `src/ui/` (graphics, renderer, sprites, screens, application), `src/config/`, `src/maze/`, `src/scores/` |
| dazema | Gameplay | `src/engine/` (engine, level, game objects, ghost behaviour) |

*[Check this table against reality. Add who wrote the Makefile, the README and
each document in this folder, and who handles packaging and publication.]*

## Working rules

- **Layering:** the interface may read the engine, the engine does not know the
  interface. The engine works in maze cells and never in pixels.
- **Interface contract:** the engine exposes, read-only, the current level and
  maze, the positions and facing of Pac-Man and the ghosts, the ghost states,
  the pellets left, score, lives, level number and remaining time. The
  interface sends in a requested direction and the elapsed time. Changes to
  these names are agreed before either side codes against them.
- **Directions:** one shared `Direction` type (`NORTH`, `EAST`, `SOUTH`,
  `WEST`), no numbers standing for directions.
- **Quality gate:** `make lint` before each commit. *[Add: branch rules, review
  rules, commit message convention.]*
- **Reviews:** each person reads the other's merge before it is accepted, so
  both can explain the whole project at the defense.

## How decisions were made

*[Describe: meetings or chat, who decided in case of disagreement, how often
you synchronised.]*

## Decision log

| Date | Decision | Reason | Alternatives |
|---|---|---|---|
| [ ] | Use `pygame` limited to MLX-equivalent operations | MiniLibX not usable on Windows machines | WSL, virtual machine |
| [ ] | All graphics calls go through one `Graphics` wrapper | Makes the equivalence checkable and the library replaceable | Direct calls |
| [ ] | Strict configuration validation | Exact error messages, no silent defaults | Clamping to defaults |
| [ ] | Validate the maze package output | The package is third party and replaceable | Trust its output |
| [ ] | Screens return the next screen name | Avoid circular imports and coupling | Screens call the application |
| [ ] | Sprites built pixel by pixel | MLX cannot resize images | Image files in several sizes |
| [ ] | Layout object created per level | No stale cell size after a level change | Renderer attributes |
| [ ] | Movement on a 0.15 s grid step, interpolated when drawing | Simple rules and smooth look | Pixel movement |
| [ ] | Level timer and level change decided by the engine | Rules belong to the engine | Decided by the screen |
| [ ] | Highscore loader tolerates damaged files | The file is not critical | Strict failure |

## Issue handling

*[Describe how bugs and blocked tasks were reported and assigned, for example an
issue list or the Kanban board.]*
