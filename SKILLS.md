IT Deck Term Cards
Generates new sentence-card content for the it-deck Anki deck in the anki-english project (a version-controlled Anki repo where cards live in decks/<deck>/cards.yaml, synced to Anki via AnkiConnect scripts).

When to use
Trigger: the user names one or more IT/software-engineering terms or phrases and asks for new card content, backlog entries, or sentences for the it-deck deck (e.g. "згенеруй картки для терміна rollback", "add sentences for 'technical debt'").

Per-term output
For each term, produce a block of sentences:

One definition sentence — dictionary-style, plain English, present tense, explains the term in an IT/software-engineering context (pattern: "X means...", "X is/are...", "To X means..."). Always an affirmative statement.
4–6 example sentences using the term naturally in an IT/software-engineering context (releases, code review, sprints, deployments, testing, infrastructure, incidents, on-call, architecture, etc.). For each example sentence:
Randomly pick one grammar structure from the pool below. Do not repeat a structure within the same term's block.
Randomly pick a sentence type: affirmative statement / negative statement / yes-no question / wh-question. Weight toward variety — don't let every example in a block be an affirmative statement.
Write a Ukrainian translation for every sentence (definition included), following the translation rule below.
Target difficulty: B2/C1. Challenging but not requiring C2/native-level vocabulary.

Grammar structure pool (rotate randomly, avoid repeats within one term's block)
Tenses & aspects: Present Perfect, Present Perfect Continuous, Past Perfect, Past Perfect Continuous, Future Perfect, Future Perfect Continuous, "going to" future, "be about to"

Conditionals & hypothetical: Conditional Type 0, Type 1, Type 2, Type 3, Mixed Conditionals, Wish / If only, Suppose / What if, Unless / provided that / as long as / in case, Subjunctive mood

Inversion & emphasis: Rarely/Seldom + inversion, Never (before) + inversion, Not only... but also, Hardly... when, No sooner... than, Under no circumstances, Only then/by/after + inversion, Little did..., It-cleft ("It was X that..."), What-cleft ("What Y did was..."), Emphatic do/does/did

Passive & causative: Passive voice (various tenses), Passive with modal verbs, Causative (have/get something done), Passive reporting ("It is believed that...")

Modal perfect & obligation: should/could/must/might/may + have + past participle, had to / was allowed to (past obligation/permission)

Reported speech: Reported statements, Reported questions, Reported commands, Reporting verbs + subjunctive (suggest, insist, recommend that...)

Relative & participle clauses: Defining relative clauses, Non-defining relative clauses, Reduced relative clauses, Participle clauses (present/past/perfect participle), Absolute constructions ("With the deployment complete, ...")

Gerund/infinitive & connectors: Gerund vs infinitive, Perfect gerund/infinitive, Concession (although/despite/even though), Purpose (so that/in order to), Result (so...that/such...that), Complex connectors (in light of, with regard to, notwithstanding, insofar as, in the event that)

Other structures: Nominalization, Fronting/topicalization, Double comparatives (the more... the more...), Existential "there" + complex modification, Correlatives (both...and, either...or, neither...nor), Ellipsis/substitution (so do I / neither did she), Rhetorical questions

Translation rule — structurally anchored, not free
The Ukrainian translation must preserve the grammatical/temporal/negation marker of the English sentence at the same functional position in the sentence, even when the rest is translated naturally rather than word-for-word. Never paraphrase away the marker — the Ukrainian sentence is what the learner reads to produce the English one, so the structural cue must survive translation.

Confirmed examples from existing it-deck cards:

"If we had committed to that deadline..." → "Якби ми взяли на себе зобов'язання щодо того дедлайну..." (conditional marker "Якби" kept)
"Rarely does a team commit..." → "Рідко яка команда бере на себе зобов'язання..." (inversion opener "Рідко" kept at sentence start)
"By the end of the sprint, we will have committed..." → "До кінця спринту ми візьмемо на себе зобов'язання..." (time-anchor phrase kept, even though Future Perfect is naturally simplified to simple future in Ukrainian)
Where the output goes
Locate the anki-english project (ask the user for its path if not already accessible). Append new entries directly to decks/it-deck/cards.yaml, one entry per sentence, in this format:

- fields:
    Front: <Ukrainian translation>
    Back: <English sentence>
    Audio: ''
  tags: []
Omit the id field for new cards — sync.py assigns and writes back the real Anki note ID after addNote. Do not touch Audio; it stays empty until filled by generate_audio.py.

After appending cards for a term (or batch of terms), tell the user to run, in order:

python scripts/validate.py
python scripts/generate_audio.py --deck it-deck
python scripts/validate.py
python scripts/sync.py
Presenting the batch before writing
Before writing to cards.yaml, show the user the generated block (definition + examples, English + Ukrainian, with the grammar structure used labeled next to each sentence) so they can review or request changes before it's committed to the file.