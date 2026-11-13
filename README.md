# Kannect

A relaxed connecting-wall word game: sort sixteen tiles into four hidden groups of four, then reveal each link.
One self-contained page, `kannect.html`.

## Layout

| Path | What it is |
| --- | --- |
| `kannect.html` | The game. The `LEVELS` block inside it is generated; do not edit it by hand. |
| `levels/core.json` | The first ten walls. Always kept, always first, in this order. |
| `levels/batch_NN.json` | Further walls, one file per batch. Add new files here. |
| `levels/BRIEF.md` | How to write a good wall, and the exact file format. |
| `tools/validate.py` | Checks one level file. |
| `tools/build.py` | Merges every level file into `kannect.html`. |

## Adding walls

1. Create a new `levels/batch_NN.json` (next free number) in the format described in `levels/BRIEF.md`.
2. `python3 tools/validate.py levels/batch_NN.json` and fix anything it reports.
3. `python3 tools/build.py --dry` to see what would be kept, then `python3 tools/build.py` to write the game.

The build drops any wall that fails validation, repeats a link already used by an earlier wall, or would use
the same tile word a third time across the whole game. It orders walls from gentle to hard using each wall's
`difficulty`, alternating between batch files so subjects stay mixed.

Progress is saved on the player's device by wall number. Adding a batch can change which wall has which
number, so completed ticks may shift after a rebuild.
