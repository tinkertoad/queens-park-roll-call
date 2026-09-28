# Queen's Park Roll Call

A study tool for learning the 124 members of the 44th Parliament of Ontario and
the cabinet: faces, names, ridings, parties and portfolios. Built for a
legislative page getting ready for a session at Queen's Park.

**Use it:** https://tinkertoad.github.io/queens-park-roll-call/

It is one self-contained HTML file with no server, account or install. It works
on a phone, and progress is saved in the browser you use it in.

## What's in it

- **Quiz**: four-choice questions: face → name, face → riding, name → riding,
  riding → name, and for the cabinet, minister ↔ portfolio. Wrong answers are
  chosen to be hard (other Scarborough ridings, other Stephens).
- **Flashcards**: see a face, say the name, flip, mark "Got it" or "Again".
- **Browse**: every member by party, searchable.
- **Small batches**: the guided path goes party by party in fixed batches of 8.
  You stay on a batch until you choose to move on, and each new person is
  introduced before you're quizzed on them.
- **Read aloud**: a speaker button beside each name and riding uses the
  browser's built-in voice.

## Data

From the member and cabinet lists dated September 2026. The source PDFs are not
included here.

- `data/mpps.json`: name, riding, party and photo for all 124 members, in riding
  order. Donna Skelly is listed as Speaker, as the source lists her.
- `data/cabinet.json`: 29 ministers and 7 associate ministers, keyed by riding.
- `photos/`: member headshots taken from the members list.

Two spellings differ from the source list and follow the Legislature's own:
Tyler **Allsopp**, Vijay **Thanigasalam**.

## Pronunciation

The read-aloud voice guesses from spelling, so unusual names may come out wrong.
To fix one, add a sounds-like spelling to `SAY_AS` in `src/app.html`, then
rebuild.

## Editing

`index.html` is generated: edit `src/app.html` or `data/`, then run:

    python3 build.py

`tools/extract_photos.py` regenerates `photos/` from the members-list PDF if a
new one is issued.
