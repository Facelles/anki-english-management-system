# Note Types

Human-readable summary. Authoritative schema is in `models/*/_meta.yaml`.

---

## Basic (type in the answer) + audio

Dir: `models/basic-type-in-the-answer-audio/`

| field | description |
|-------|-------------|
| Front | Ukrainian translation (shown as the prompt) |
| Back | English sentence or word (typed as the answer) |
| Audio | Audio file reference, e.g. `[sound:filename.mp3]` |

Used by: `book`, `it-deck`, `l2-vocab`, `medicine`, `test-english`

---

## Basic (with typing)+audio+state

Dir: `models/basic-with-typing-audio-state/`

| field | description |
|-------|-------------|
| Front | Ukrainian translation of Back — typed as a translation hint (filled manually) |
| Back | English answer to produce |
| Audio | Audio file reference |
| State | Interview question / situation that prompted this answer (in Ukrainian) |

Used by: `interview`

---

## Video (type in the answer)

Dir: `models/video-type-in-the-answer/`

| field | description |
|-------|-------------|
| Front | English sentence from the video |
| Back | Ukrainian translation |
| VideoFilename | Video clip filename, e.g. `00001.webm` |

Used by: `video-by-movies`
