# Dialogue and sound

Kling 4.0 generates picture and sound together: speech with lip movement, ambience and effects. This covers how to ask for speech that fits, how to make the same scene in several languages, and when to bring in Artlist's voice, music and sound-effect tools.

## Contents
1. The sound block
2. Writing a line that fits
3. Two or more speakers
4. Languages and localised versions
5. Silent plates
6. Voice-over, music and effects from Artlist
7. Common problems

## 1. The sound block

End every video prompt with a short sound block. Four possible layers, in this order; include only the ones the shot needs:

```
Sound: <speech> / <ambience> / <effects> / <music or "no background music">, no subtitles.
```

The model may add music or burned-in subtitles unless told otherwise. If the film will be scored in the edit, say "no background music" on every shot so the clips cut together cleanly, and always say "no subtitles" unless the user wants them.

## 2. Writing a line that fits

Give four things: who, what the voice is like, how the line is delivered, and the words.

```
The older woman behind the counter speaks in a warm, slightly hoarse voice, unhurried, with a small smile: "You're early today."
```

- **Identify the speaker by something visible** (position, clothing, age), not by a name the model has never seen.
- **Describe the voice**: age, pitch, texture, accent if it matters.
- **Describe the delivery**: pace, volume, emotion, and where a pause falls.
- **Put the words in quotation marks**, in the language they are spoken in. Keep the rest of the prompt in English.
- **Fit the time.** About two and a half words per second, plus half a second of air either side. Count the words; lengthen the shot or cut the line.
- **One or two lines per shot.** Longer speeches drift out of sync. Split a speech across shots and cut to a listener between them.
- **Mouth visible and unobstructed** in the first frame, face at medium close-up or closer, for lines that must read.

## 3. Two or more speakers

State, in this order: who speaks first, that each has a distinct voice, that they do not talk over each other, and that lip movement matches each speaker.

```
Two people at a table, the man on the left and the woman on the right. They have clearly different voices and never overlap; lips move only for the person speaking.
The man, low and tense: "Did you read it?"
A beat of silence.
The woman, flat, not looking up: "Twice."
```

If a two-shot keeps giving the line to the wrong person, cut it as two singles: each speaker alone in frame for their own line. It is also better filmmaking.

## 4. Languages and localised versions

Write the spoken line in the target language inside the quotation marks and name the language in the delivery: "She says in natural, clear Spanish: «¿Dónde está la estación?»". The Kling 4.0 brief on Artlist states dialogue in nine languages; treat the exact list as something to confirm on the day, and run a short test line before committing a whole scene in a language you have not tried.

**Making one scene in several languages**

1. Approve the scene in the first language.
2. For each further language, keep the first frame, references and every non-speech sentence identical; change only the quoted line and the named language.
3. Check the translated line still fits the shot length; languages differ in length. Shorten the wording before lengthening the shot, so all versions cut the same.
4. Send the versions together with `generate_batch` and label them in the project (`studio.py add-shot --id S03-es --variant-of S03`).
5. Have a speaker of the language listen if the film will be published. Say so to the user; do not vouch for pronunciation you cannot judge.

Each language version is a separate take, so performance and small details will differ between them. Holding the first frame fixed keeps them close.

## 5. Silent plates

Set `generate_audio` to off when the clip will be fully re-sounded in the edit (music videos cut to a track, shots under voice-over, VFX plates). It removes one source of error.

## 6. Voice-over, music and effects from Artlist

Use these when the film needs sound that does not come from inside the shot.

**Voice-over.** `list_voices` to choose a voice; present candidates by name and character, never by ID. `generate_voiceover` takes only the words to be spoken: no stage directions, no speaker labels, no quotation marks. Shape the tone with the voice choice and its settings (`get_model_config` with the `voiceId` shows the languages, accents, emotions and speeds that voice supports).

**Music.** `search_music` finds existing catalogue tracks by mood, genre, tempo and length; use it when the user wants a real licensed track. `generate_music` writes a new one from a description. For a film cut to music, choose the track before the shot list and plan shot lengths in bars.

**Sound effects.** `search_sfx` with a plain description ("heavy door slam in a stone hall"). Refine only with categories or tags copied from a previous result.

Record what was chosen in the project file and include it in the edit list (`deliverables.md`) with timings, so the user can lay it in.

## 7. Common problems

| Problem | Cause | Fix |
|---|---|---|
| Line cut off or rushed | Too many words for the seconds | Count words; shorten the line or add seconds |
| Wrong person speaks | Speaker not identified visibly | Name position and clothing; or cut to singles |
| Lips move on the listener | Overlap not excluded | Add "lips move only for the person speaking" |
| Unwanted music under dialogue | Model default | "no background music" in the sound block |
| Burned-in captions | Model default | "no subtitles" |
| Flat delivery | No delivery direction | Add pace, emotion, where the stress falls |
| Accent wanders | Voice not described | State the accent and age each time the character speaks |
| Mouth hidden, sync unreadable | Framing | Reframe closer and frontal in the first frame |
| Different voice in each shot | Voice re-invented per render | Reuse the identical voice sentence in every shot; keep lines short; for narration use Artlist voice-over instead |
