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
| `levels/order.json` | Generated. The permanent play order, by wall id. |
| `tools/validate.py` | Checks one level file. |
| `tools/build.py` | Merges every level file into `kannect.html`. |

## Adding walls

1. Create a new `levels/batch_NN.json` (next free number) in the format described in `levels/BRIEF.md`.
2. `python3 tools/validate.py levels/batch_NN.json` and fix anything it reports.
3. `python3 tools/build.py --dry` to see what would be kept, then `python3 tools/build.py` to write the game.

Wall numbers are permanent. `levels/order.json` records the play order: walls already listed keep their
number, and new walls are appended to the end. Walls added in the same build are mixed among themselves,
gentle to hard, alternating between their batch files so subjects do not clump. Commit `order.json` with
every build, and do not delete or change the words of a wall that is already listed.

Words may recur across walls. A new wall is dropped only if it fails validation or repeats a group already
in the game (the same four tiles, or three of the same four).
