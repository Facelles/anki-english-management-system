# CLAUDE.md — anki-english

Version-controlled source of truth for Anki flashcard decks. Cards, note types, and media are pulled from Anki via AnkiConnect and stored as YAML/HTML/CSS in git.

---

## AnkiConnect

Plugin code: `2055492159`. Runs at `http://localhost:8765`.
Anki must be open for any script to work.

---

## Scripts

All scripts live in `scripts/`, require `.venv` activated, use `requests` + `yaml`.

| script                          | what it does                                                                                                                             |
| ------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| `bootstrap_models.py`         | pulls note types →`models/` (fields, templates, CSS)                                                                                  |
| `bootstrap_decks.py`          | pulls card data →`decks/` (_meta.yaml + cards.yaml)                                                                                   |
| `bootstrap_media.py`          | pulls media files →`media/` (interactive, confirms before downloading)                                                                |
| `validate.py`                 | lints repo: structure, duplicates, media refs, HTML noise — exit 1 on errors                                                            |
| `sync.py`                     | pushes YAML → Anki: add/update notes, upload media, write back new ids                                                                  |
| `sync_back.py`                | pulls changes from Anki back into YAML (reverse sync)                                                                                    |
| `generate_audio.py`           | generates MP3 audio for cards via ElevenLabs TTS (interactive session)                                                                   |
| `import_backlog.py`           | imports new lines from a deck's`backlog.md` into `cards.yaml` with an auto-translated `Front` (interactive, or `--auto`)                |
| `generate_handwriting_pdf.py` | generates a printable PDF of today's due cards (`Back` field) in a dotted handwriting-practice font (`kg_primary_dots/`) for tracing |

Bootstrap scripts are **idempotent** — safe to re-run.
`bootstrap_media.py` reads `mediaFields` from `models/*/_meta.yaml` to know which fields contain filenames.

### sync.py flags

```
python scripts/sync.py --dry-run             # preview plan, no changes
python scripts/sync.py                       # apply with confirmation
python scripts/sync.py --check-media-hashes  # also compare MD5 of media files
python scripts/sync.py --prune               # remove orphaned notes from Anki (with confirmation)
```

`sync.py` writes new `id` values back into `cards.yaml` after `addNote`.

### sync_back.py flags

```
python scripts/sync_back.py --dry-run             # preview plan, no changes
python scripts/sync_back.py                       # apply with confirmation
python scripts/sync_back.py --add-new             # also write new Anki cards to YAML
python scripts/sync_back.py --download-media      # also download missing media files
python scripts/sync_back.py --add-new --download-media  # full pull
```

Cards deleted in Anki are reported but NOT removed from YAML — resolve manually.

### generate_audio.py

Generates MP3 audio for cards where the `Audio` field is empty. Reads the `Back` field (English text), sends it to ElevenLabs TTS, plays back the result, and on confirmation saves the file to `media/` and updates `cards.yaml` immediately. Does not require Anki to be running.

```
python scripts/generate_audio.py --deck interview   # process interview deck
python scripts/generate_audio.py --deck l2-vocab    # process any other deck
```

**Interactive keys:**

| key   | action                                                                           |
| ----- | -------------------------------------------------------------------------------- |
| `y` | accept — save MP3 to`media/`, write `[sound:…]` into cards.yaml, next card |
| `p` | replay — play the same audio again without a new API call                       |
| `r` | regenerate — new ElevenLabs call with a fresh random voice, play again          |
| `s` | skip — leave this card's Audio empty, move to next                              |
| `q` | quit — save progress so far and exit                                            |

**Voice pool:** a random voice is picked from `DEFAULT_VOICES` for each new card (and on `r`). The pool is defined in the script. On `p` replay the already-generated audio plays unchanged.

**Config (`.env`):**

```
ELEVENLABS_API_KEY=...          # required
ELEVENLABS_VOICE_IDS=id1,id2   # optional — replaces the built-in voice pool
ELEVENLABS_VOICE_ID=...        # optional — single voice (used if VOICE_IDS not set)
ELEVENLABS_MODEL_ID=...        # optional — defaults to eleven_multilingual_v2
```

**Workflow after a session:**

```bash
python scripts/generate_audio.py --deck interview   # fill in Audio fields
python scripts/validate.py                          # check media refs are valid
python scripts/sync.py                              # push to Anki
```

Video decks (`video-by-movies`) are automatically rejected — they use `VideoFilename`, not `Audio`.

### import_backlog.py

Picks up lines from `decks/<deck>/backlog.md` (plain text, one English sentence per line) that aren't cards yet, proposes a Ukrainian translation (Google Translate via `deep-translator`), and on confirmation appends a new card to `cards.yaml` immediately — `Back` = the English line, `Front` = the translation, `Audio`/`State` left empty. Dedup is by exact match against existing `Back` values, so `backlog.md` can just keep growing and re-running the script only processes what's new. Does not require Anki or any API key. A translation attempt is retried automatically a few times before being treated as failed (the Google Translate backend occasionally returns nothing) — lines that still fail are skipped and reported at the end, and just get picked up again on the next run.

```
python scripts/import_backlog.py --deck interview
python scripts/import_backlog.py --deck interview --auto   # accept every translation automatically, no per-line approval
```

**Interactive keys (ignored in `--auto` mode):**

| key   | action                                                |
| ----- | ----------------------------------------------------- |
| `y` | accept the proposed translation, save card, next line |
| `e` | edit the translation before saving                    |
| `s` | skip this line (leave it for a future run)            |
| `q` | quit — save progress so far and exit                 |

**Workflow after a session:**

```bash
python scripts/import_backlog.py --deck interview   # fill in Front/Back from backlog.md
python scripts/generate_audio.py --deck interview   # fill in Audio fields
python scripts/validate.py                          # sanity check
python scripts/sync.py                              # push to Anki
```

### generate_handwriting_pdf.py

Queries AnkiConnect for the cards a deck's reviewer would show today (`is:due`), and
renders the English `Back` field repeated a few times per card in a dotted tracing font
from `kg_primary_dots/`, as a printable PDF. Read-only — never writes back to Anki or
`cards.yaml`. Requires Anki running. Not applicable to `video-by-movies` (no `Back` text
field to trace).

```
python scripts/generate_handwriting_pdf.py --deck interview
python scripts/generate_handwriting_pdf.py --deck l2-vocab --repeat 3 --font lined-alt
python scripts/generate_handwriting_pdf.py --deck interview --limit 5   # quick layout test
```

| flag            | default                                    | description                                                                                          |
| --------------- | ------------------------------------------ | ---------------------------------------------------------------------------------------------------- |
| `--deck`      | required                                   | deck directory name under`decks/`                                                                  |
| `--repeat`    | `2`                                      | times to repeat each sentence (= lines per card)                                                     |
| `--font`      | `lined`                                  | `dotted` / `lined` / `lined-alt` / `lined-nospace` — maps to a file in `kg_primary_dots/` |
| `--font-size` | `26`                                     | font size in pt                                                                                      |
| `--intensity` | `1.0`                                    | text darkness:`0.0` (white) .. `1.0` (full black) — lower prints a fainter guide to trace over  |
| `--limit`     | none                                       | cap number of cards, for quick layout tests                                                          |
| `--output`    | `handwriting_practice/<deck>_<date>.pdf` | output PDF path                                                                                      |

Output goes to `handwriting_practice/` (gitignored — printouts, not tracked content).

---

## Note types (models)

Stored in `models/<safe-name>/`. `safe-name` is the Anki name lowercased, non-alphanum replaced with `-`.

| Anki name                          | dir                                | fields                     | media field   |
| ---------------------------------- | ---------------------------------- | -------------------------- | ------------- |
| Basic (type in the answer) + audio | `basic-type-in-the-answer-audio` | Front, Back, Audio         | Audio         |
| Basic (with typing)+audio+state    | `basic-with-typing-audio-state`  | Front, Back, Audio, State  | Audio         |
| Video (type in the answer)         | `video-type-in-the-answer`       | Front, Back, VideoFilename | VideoFilename |

**Field semantics for `basic-with-typing-audio-state` (interview deck):**

| field     | role                                                                                                 |
| --------- | ---------------------------------------------------------------------------------------------------- |
| `Front` | Ukrainian translation of the English answer — typed by user as a translation hint (filled manually) |
| `Back`  | English answer to produce                                                                            |
| `State` | Interview question / situation that prompted this answer (in Ukrainian)                              |
| `Audio` | MP3 of the`Back` text — generated via `generate_audio.py`                                       |

`_meta.yaml` in each model dir is the authoritative schema. `mediaFields` key tells `bootstrap_media.py` which fields hold filenames.

---

## Decks

Stored in `decks/<safe-name>/`. Each deck has `_meta.yaml` (deckName + noteType) and `cards.yaml`.

| dir                 | Anki deck name  | note type                          | purpose                                                                                      |
| ------------------- | --------------- | ---------------------------------- | -------------------------------------------------------------------------------------------- |
| `it-deck`         | IT_deck         | Basic (type in the answer) + audio | IT professional vocab — sentence production                                                 |
| `video-by-movies` | Video_by_movies | Video (type in the answer)         | Listening + fluency — clips from shows                                                      |
| `interview`       | Interview       | Basic (with typing)+audio+state    | Interview prep — State = question, Front = ukr. translation (manual), Back = English answer |
| `l2-vocab`        | L2_vocab        | Basic (type in the answer) + audio | ESOL L2 course vocabulary                                                                    |
| `medicine`        | Medicine        | Basic (type in the answer) + audio | Medical vocab for GP visits                                                                  |
| `book`            | Book            | Basic (type in the answer) + audio | Phrases from English books                                                                   |
| `test-english`    | test-english    | Basic (type in the answer) + audio | Grammar & vocabulary from test-english.com — sentence production                            |

See `docs/decks-overview.md` for full context on each deck.

`cards.yaml` format — default convention (`Front` = Ukrainian prompt, `Back` = English answer to type; see `video-by-movies specifics` below for the one deck that reverses this):

```yaml
- id: 1756166410321       # Anki noteId (integer)
  fields:
    Front: Ukrainian translation
    Back: English sentence
    Audio: filename.mp3             # or VideoFilename: 00001.webm
  tags: []
```

If a deck has multiple note types, bootstrap creates `cards.<safe-type>.yaml` files instead of a single `cards.yaml`.

### video-by-movies specifics

Clips are short video fragments (max 5 sec, 320px) cut from shows in Final Cut Pro.
Front = English transcript (what the user types). Back = Ukrainian translation (secondary).
This is the reverse of every other deck's Front/Back convention.

Produced via the staging pipeline in `video_prepare/` (see its own README for the
full cut → convert → merge workflow) — one episode worked on at a time, merged
into this deck when done.

**Current content:**

- `sherlok_*.webm` — Sherlock BBC, Season 1 complete (660 clips)
- `silicon_valley_*.webm` — Silicon Valley HBO, Season 1 in progress (529 clips)
- `pets_*.webm` — The Secret Life of Pets, complete (273 clips)
- 19 legacy `NNNNN.webm` clips predating the per-show naming convention

**Next candidates:** finish Silicon Valley S1, then House MD / Suits / Sherlock S2.

---

## Media

All files are flat in `media/`. Video cards use `.webm`, audio cards use `.mp3`.
Filenames in cards reference media directly (e.g. `00001.webm`, not a full path).
`media/` is committed to git (files are checked in).

---

## Python environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install requests pyyaml deep-translator reportlab
```

`.venv/` is gitignored.

---

## Environment config (`.env`)

`.env` lives in the project root and is gitignored. Never read, print, or commit it.

| key                      | required                       | description                                           |
| ------------------------ | ------------------------------ | ----------------------------------------------------- |
| `ELEVENLABS_API_KEY`   | yes (for`generate_audio.py`) | ElevenLabs API key                                    |
| `ELEVENLABS_VOICE_IDS` | no                             | comma-separated voice ID pool for random selection    |
| `ELEVENLABS_VOICE_ID`  | no                             | single voice override (fallback if VOICE_IDS not set) |
| `ELEVENLABS_MODEL_ID`  | no                             | TTS model, defaults to`eleven_multilingual_v2`      |

---

## Docs

| file                       | what it contains                                                            |
| -------------------------- | --------------------------------------------------------------------------- |
| `docs/decks-overview.md` | why each deck exists, motivation, content details                           |
| `docs/word-lists.md`     | vocabulary roadmap — IT terms, phrases, phrasal verbs not yet in cards     |
| `docs/hint-dsl.md`       | planned hint system for card Front fields (HTML-based, not implemented yet) |
| `docs/note-types.md`     | human-readable summary of note type models                                  |
| `docs/ielts-roadmap.md`  | IELTS Writing skill roadmap for`l2-vocab` — what's covered, what's next  |
| `docs/ielts-trends.md`   | IELTS Task 1 trend-description vocab reference for`l2-vocab`              |
| `docs/ielts-vocab.md`    | IELTS Task 2 topic vocab/collocations reference for`l2-vocab`             |

---

## Gitignore

- `.venv/` — Python venv
- `__pycache__/` — bytecode
- `backups/` — `.colpkg` snapshots (kept locally, not in git)
- `handwriting_practice/` — generated PDFs from `generate_handwriting_pdf.py` (printouts, not tracked content)
- `.env` — API keys and secrets (never commit)
- `.DS_Store`, `node_modules/` — OS/tooling noise
- `*.srt`, `video_prepare/tracks`, `video_prepare/converted_webm` — clip-production scratch state (see `video_prepare/README.md`)
