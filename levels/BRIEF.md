# Brief for writing Kategories walls

Kategories is a relaxed phone game for a British adult who enjoys the "connecting wall" style of quiz puzzle.
A wall is 16 tiles that sort into 4 hidden groups of 4. The player taps four tiles; a correct group locks.
When all are sorted she guesses each group's link and reveals it. No timer, unlimited guesses.
A "Pictures" switch replaces some word tiles with an emoji the player must translate back into the word.

You are one of eleven writers working in parallel. Each writer has their own subject area and letter range
(given in your task message) so that the combined set has no repeated groups. Stay inside yours.

## What makes a good wall

1. **Exactly one solution.** There must be only one way to split the 16 tiles into four valid groups.
2. **Real red herrings.** At least three tiles (ideally five or more) must genuinely fit a second group in the
   same wall, so a group has five or six candidates and the player must work out which one belongs elsewhere.
   The classic shape: group A has exactly four possible members, one of which also fits group B; group B
   has five candidates, so the shared tile is forced into A. Chains of these make a wall satisfying.
   Also good: a "phantom" theme, where three or four tiles from different groups look like a fifth category.
3. **Mix of group types in each wall.** Usually two or three knowledge categories and one or two wordplay
   groups. Wordplay types: `FIRE ___` / `___ BOARD` compounds, hidden words (piRATe), homophones,
   words that become another word when a letter is added/removed, anagrams, words sharing a sound or spelling
   pattern, things that follow or precede a word, famous pairs missing a half, and so on.
4. **Fair.** General knowledge a British adult would have. UK spelling and UK names for things. No obscure
   trivia, nothing offensive, no brand-new slang. Every member of a group must clearly and uncontroversially
   belong. Check spellings. For hidden-word groups, check letter by letter that the hidden word is really
   there, and check that no tile in the other three groups accidentally contains a hidden word of that kind.
   For `X ___` groups, check that no other tile in the wall also makes a common compound with X.
5. **Variety.** Do not lean on the same trick every wall. Spread difficulty 1 (gentle) to 5 (hard), roughly
   evenly, and set the `difficulty` field honestly.

## Pictures

Give 3 to 7 tiles per wall a picture: a single, common emoji (in phones since about 2020; avoid very new ones,
flags, and text-like symbols). The emoji must let a player get to the exact word, but the best ones mislead at
first glance: a 🦇 for BAT in a sports-equipment group, a 📅 for DATE in a fruit group, a 🏏 for CRICKET in an
insects group. Never use an emoji that gives away the group's link. A wall must still be solvable with
pictures on, so do not put pictures on tiles whose word could not be recovered from the image.

## Hard format rules

Write one JSON file: a list of walls.

```json
[
 {"difficulty": 2,
  "groups": [
   {"link": "Fire ___", "note": "Firefly, firework, firearm, fireplace",
    "tiles": [["FLY","🪰"],["WORK"],["ARM","💪"],["PLACE"]]},
   {"link": "Insects", "tiles": [["BEETLE","🪲"],["WASP"],["MOTH"],["CRICKET","🏏"]]},
   {"link": "Vegetables", "tiles": [["LEEK"],["SWEDE"],["MARROW"],["SQUASH"]]},
   {"link": "Sports", "tiles": [["GOLF","⛳"],["DARTS","🎯"],["BOWLS","🥣"],["POLO"]]}],
  "overlaps": {"FLY": ["Insects"], "CRICKET": ["Sports"], "SQUASH": ["Sports"]}}
]
```

- Each tile word: ONE word, 2 to 9 capital letters A–Z only. No spaces, hyphens, apostrophes, digits or accents.
- `link`: short (under about 30 characters), the answer the player sees. Use `___` for a blank.
- `note`: optional, only for wordplay groups, to show the working (e.g. `piRATe, grAPE, whEEL, BEARd`).
- `overlaps`: every tile that could also reasonably be placed in another group of this wall, mapped to the
  exact `link` text of those other groups. Be honest and complete here: list every real overlap, because the
  checker uses this to prove the wall has exactly one solution. At least three words per wall.
- No group may repeat one already used (the same four tiles, or three of the same four), in your file or in
  the existing walls. Individual words may recur in different walls, ideally in a different sense.

## Checking

Run `python3 /home/user/kannect/tools/validate.py <your file>` and fix until it reports 0 problems.
The checker only proves what you declare. Before you finish, re-read every wall as an adversarial solver:
for each tile ask "could this defensibly go in any other group here?" and for each group ask "is there a
different set of four from this wall that fits the link?". Fix the wall or declare the overlap, and re-run.

Only write your one file. Do not edit any other file, and do not run git commands.
Your final message should be short: the file path, the number of walls, and the checker's last line.

## Already used (do not reuse)

Links: Batman characters, Birds, Building site machines, Chess pieces, Chocolate bars, Crockery, Disney
characters, Drinks, English rivers, Facial hair, Fire ___, Fish, Fruit, Hidden animals, Hidden numbers,
Honey ___, Insects, Medieval weapons, Members of Queen, Old British coins, One-name singers, Parts of a car,
Parts of a shoe, Parts of the face, Peoples who invaded Britain, Planets, Playing card suits, Punctuation,
Shipping forecast areas, Singing voices, Sound like letters, Sports, Sports equipment, Teeth, Text styles,
Units of weight, Vegetables, Young animals, ___ bird, ___ board.

Words: ALTO ANGLE ARM AVON AXE BAMBI BASS BAT BEARD BEE BEETLE BISHOP BLACK BLUE BOLD BONE BONNET BOOT BOUNTY
BOWLS BRACKET BROW BUMPER CALF CANINE CARD CARP CHEEK CHIN CIDER CLUB CLUTCH COCOA COFFEE COLA COLON COMB COMMA
CRANE CRICKET CROWN CUB CUE CUP DARTS DASH DATE DEACON DEW DIAMOND DIGGER DOGGER DUMBO DUMPER EARTH EWE EYE FIG
FINCH FISHER FLORIN FLY FOAL GALAXY GOLF GOOFY GRAM GRAPE GUINEA HEART HEEL HYPHEN INCISOR ITALIC JAIL JOKER JUG
JUTE KITE KITTEN KNIGHT LACE LADY LANCE LEEK LIME MACE MARROW MARS MAY MERCURY MERSEY MILK MOLAR MOON MOTH
MOUSTACHE MUG NEPTUNE NORMAN NOSE OUNCE PAWN PENGUIN PERCH PIKE PINK PIRATE PLACE PLATE PLUM PLUTO POLO POT POUND
PRINCE PUCK PUPPY RACKET RAY RIDDLER ROBIN ROLLER ROMAN ROOK SATURN SAUCER SAXON SEAL SEVERN SIDEBURNS SKATE SOLE
SONG SOPRANO SOVEREIGN SPADE SQUASH STING STONE STUBBLE SWEDE SWIFT TAYLOR TEA TENOR THAMES TONGUE TRENT TWIRL
UNDERLINE VENUS VIKING WASP WEIGHT WHEEL WHISKERS WISDOM WORK WREN
