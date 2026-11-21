# Blocking points and conflicts

| # | Blocking point | Effect | How it was solved | Date |
|---|---|---|---|---|
| 1 | MiniLibX could not be installed on the Windows development machines | The planned graphics library was unavailable | Use `pygame`, restricted to operations with an MLX equivalent, behind one wrapper. Staff confirmation: [to fill] | [ ] |
| 2 | Circular import between the maze data classes and the maze generator adapter | The program did not start | Moved `Cell` and `Direction` to the maze side. The adapter imports them, and the maze classes no longer import the adapter | [ ] |
| 3 | The maze image stayed the same after changing the maze size in the options | A new game showed the old maze | The layout, the sprites and the game screen are rebuilt every time a game starts | [ ] |
| 4 | A direction pressed to turn was sometimes lost | Controls felt unreliable | Store only direction keys as a requested direction, ignore key releases, keep the request until it can be used | [ ] |
| 5 | The engine file imported `pygame` and `Asset`, and used two direction conventions | The engine depended on the interface, and directions were ambiguous | Positions and directions use the shared `Direction` type; sprites are in the interface. The `import pygame` line and one import from `src/ui/sprites.py` are still to remove from the engine | [ ] |
| 6 | The standard Python `.gitignore` ignores `*.spec`, the extension of the PyInstaller packaging file | The packaging spec would not be committed | Remove the `*.spec` line when packaging is set up | [ ] |

## Conflicts inside the team

*[Describe any disagreement (design, workload, schedule), how it was discussed
and how it was resolved. If there was none, say so.]*
