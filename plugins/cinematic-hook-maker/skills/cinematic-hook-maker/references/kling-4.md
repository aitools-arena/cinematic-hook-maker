# Directing Kling 4.0

How to write prompts that Kling 4.0 follows. Read this before any video prompt.

## Contents
1. How the model reads a prompt
2. The four-block prompt
3. Stating what each asset is for
4. Timing a shot
5. Mode recipes
6. Dialogue in one paragraph
7. Text on screen
8. Negatives
9. Flash versus full
10. Prompt self-check

## 1. How the model reads a prompt

Kling 4.0 renders what is described and fills every gap with its own choice. So the craft is not adding adjectives; it is closing the gaps that matter and leaving the rest alone.

- **Describe what the camera sees, not what it means.** "Premium" is a wish. "Low side light traces the bottle's edge, the background falls to soft black, fine condensation beads on the glass" is a picture.
- **One main action per shot.** Two actions in one shot blur into each other. Split them into two shots or put them on a timeline.
- **Give motion an ending.** "She turns to the window and stops, hand on the frame" ends. "She turns" drifts.
- **Say what the camera does, every time.** With no camera instruction the camera improvises. "Static camera" is a valid instruction.
- **Fix geography.** Where each person stands, which way they face, which side of them the camera stays on.
- **Lock the count.** "Exactly one woman and one dog in frame for the whole shot" prevents duplicates far better than "no extra people".
- **Realism comes from the first frame and from physical words.** In image-to-video the frame already sets the look, so make it photographic (`gpt-image-2-5.md`, section 2). In the prompt, name the capture and the light ("handheld documentary footage, hard light from the open door on the left, no colour grading") rather than "cinematic" or "realistic". Real camera behaviour also helps: slight handheld drift, a focus that breathes, motion blur on fast hands, noise in the dark.
- **Short first.** Start with one sentence of subject, place, action and feeling. Add camera, timing, sound and what must be preserved only where they change the result. A long prompt is not a better prompt.

## 2. The four-block prompt

Use this shape for any shot with references or more than one beat. For a simple shot, the middle two blocks in a few sentences are enough.

```
ASSETS
The first reference image is <who/what>; keep <face, hair, clothing> exactly.
The second reference image is <place>; keep its layout and lighting.
The reference video supplies only <camera path | movement | timing>; do not carry over its people or setting.

LOOK
<capture: e.g. "documentary footage shot on a digital cinema camera">, <lens>, <one named light source, its direction and hardness>, <neutral or stated colour, no grading>, <texture: grain, noise in shadows>.

ACTION
0–3 s: <what we see, what moves, what the camera does>
3–7 s: <next beat, how the camera gets there>
7–10 s: <final beat and where it holds>

SOUND
<who speaks, how, the line in quotes> / <ambience> / <effects> / no background music, no subtitles
```

Leave out any block that has nothing to say. Never pad.

## 3. Stating what each asset is for

This matters more than any style word. An image or clip handed over with no job gets used however the model likes.

- Number assets by the order they are passed and say it in words: "the first reference image", "the second reference video". Through Artlist, positional wording is what works; do not rely on handles or file names.
- Give each asset one job and name what to keep: identity, wardrobe, layout, light, camera path, body movement, pacing, style.
- When an asset should contribute only one thing, say what must not carry over: "Use only the camera path from the reference video. Do not copy its people, clothing or location."
- A turnaround sheet or a grid of views can be a single reference image. Add: "This image is a design sheet. Do not render the sheet, its grid or its labels."
- Limits: up to 10 images and 5 videos in one request. Fewer, clearer references beat many. Three is a comfortable number; past six, identities start to blend.

## 4. Timing a shot

- A timeline in seconds is the most reliable way to order events: `0–2 s`, `2–5 s`, `5–8 s`. Keep beats at two seconds or longer; a beat under a second and a half rarely lands.
- Durations are whole seconds from 3 to 30. Choose the shortest length that plays the beat. Long shots cost more and give the model more room to wander.
- Rule of thumb for spoken lines: about two and a half words per second, plus half a second before and after. A twelve-word line needs a six-second shot.
- One camera idea per beat. A push-in that becomes an orbit that becomes a tilt is three shots.

## 5. Mode recipes

### Text-to-video
Use for establishing shots, abstract or environmental shots, and anything without a character who must match elsewhere. Describe place, light, the one thing that moves, the camera.

```
Wide static shot of a flooded rice terrace at dawn. Mist lifts from the water in slow layers while a single white egret walks left to right along the nearest bank and stops. Cool blue light with the first warm rim on the far hills. Ambient: water, distant birds. No background music, no subtitles.
```

### Image-to-video (the default for story shots)
The first frame already holds identity, wardrobe, composition and light. So the prompt describes **only what changes**: movement, camera, sound. Re-describing the frame invites the model to redraw it.

```
She lowers the letter, looks up toward the door on the right and exhales. Slow push-in from medium shot to close-up over the whole shot, ending on her eyes. Her hair and clothing stay exactly as in the first frame. Ambient: a clock, rain on the window. No background music, no subtitles.
```

### First and last frame
Use when the shot must arrive somewhere exact: a reveal, a transformation, a match cut, a loop. Describe the journey between the two frames and how the camera travels. Matching the first and last composition gives a clean loop.

### Reference-to-video with images
Use when a shot combines approved elements that have never appeared together: the character sheet, the location plate, a prop. State each one's job (section 3), then direct the action. This is also the route to a 21:9 frame, because the ratio is set by the request and not by a first frame.

### Reference-to-video with video
Use when existing footage should supply movement, camera work or pacing, or when the footage itself is being edited. See `vfx-mode.md`. The word that starts the prompt decides the result: "Edit the reference video…" changes that clip; "Use the camera path of the reference video…" makes a new one.

### Long single take with keyframes
Built as a chain of start/end-frame segments that share frames. See `onetake-keyframes.md`.

## 6. Dialogue in one paragraph

Name the speaker by a visible trait, describe the voice (age, tone, pace, emotion), then give the line in quotation marks in the language it is spoken in. Keep everything else in English. With two speakers, state that each has a distinct voice, that they do not overlap, and who speaks first. Full guidance in `dialogue-audio.md`.

```
The older man in the grey coat speaks in a low, tired voice, slowly: "You should have told me." A pause. The young woman answers quietly without looking at him: "I tried."
```

## 7. Text on screen

Kling 4.0 can render legible text. Give the exact words in quotation marks, where they sit, how they are aligned, when they appear and for how long. Keep it short; long sentences degrade.

```
At 6 s the words "COMING HOME" fade in, centred in the lower third, white sans-serif capitals, and hold until the end.
```

## 8. Negatives

Long negative lists make results worse with this model. Use them sparingly:

- Add **"no subtitles"** and **"no background music"** whenever you do not want them, because the model may add either by default.
- For a non-photographic look, pair the positive style with one exclusion: "hand-painted 2D animation, not photorealistic".
- Turn every other "don't" into a positive fact. Not "don't show her face" but "she is seen from behind throughout".

## 9. Flash versus full

Draft on **Kling 4.0 Flash** when the shot is 20 s or shorter and needs only a first frame. It is 720p, faster and cheaper, and it answers the questions that matter in a draft: does the action read, is the camera right, does the line fit the time.

Use **Kling 4.0** for the final, for anything over 20 s, and for any shot with an end frame or middle keyframes.

A final re-render is a new take. Hold it close to the approved draft by reusing the identical first frame, prompt and references, and by changing nothing else at the same time.

## 10. Prompt self-check

Before spending credits, read the prompt once as if you were the model:

- Does every reference have a stated job and a stated limit?
- Is there exactly one main action, with an ending?
- Is the camera told what to do?
- Would a stranger know where everyone stands?
- Do the beats fit the seconds, and does any spoken line fit its beat?
- Is the sound block there, with "no subtitles, no background music" if wanted?
- Is anything abstract ("cinematic", "epic", "beautiful") that could be replaced by something visible?
- Is anything in the prompt already fixed by the first frame and therefore removable?
