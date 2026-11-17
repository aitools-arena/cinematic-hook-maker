# One-takes and keyframes

A single unbroken shot of up to thirty seconds is the most striking thing Kling 4.0 does, and the easiest to waste. Keyframes are how you keep control of it.

## Contents
1. When a one-take is the right choice
2. Designing the journey
3. Keyframe timing
4. Making the keyframes
5. Sending them through Artlist
6. The chained fallback
7. Transitions that hide the joins
8. Common failures

## 1. When a one-take is the right choice

Use one when the unbroken movement is itself the idea: a journey through connected spaces, a transformation, a reveal that depends on the camera arriving somewhere. Do not use one for a conversation, or for anything that needs a cut to a reaction. If the user wants "thirty seconds" but the story has cuts, make shots.

## 2. Designing the journey

Write the take as a path with stations:

1. **Start**: where the camera is and what it sees.
2. **Three to five stations**: each a new space, state or discovery.
3. **Arrival**: the image the whole move was heading for.

Keep one constant through the entire shot: a character walking at a steady pace, a continuous forward camera, an object that is followed. The constant is what lets the audience read change. Keep the direction of travel the same from start to finish.

## 3. Keyframe timing

Through Artlist a long take is built as a **chain of segments**: each segment runs from one keyframe to the next, and every segment is its own render of 3 seconds or more, in whole seconds. That sets the arithmetic:

- Keyframes sit **3 seconds apart or more**, on whole seconds.
- Up to ten keyframes; a thirty-second take can hold at most eleven stations at 3 s spacing, so ten is the practical ceiling.
- Fewer, wider-spaced keyframes move more fluidly. Six keyframes over thirty seconds (five 6-second segments) is a good default.
- Every segment is paid for separately. Five segments of six seconds cost the same as thirty seconds of video.

`studio.py keyplan --dur 30 --keys 6` prints the keyframe times and the segment list.

| Keyframe | Time | Station | Segment that leaves it |
|---|---|---|---|
| 1 | 0 s | Start | 1 → 2, 6 s |
| 2 | 6 s | Station A | 2 → 3, 6 s |
| 3 | 12 s | Station B | 3 → 4, 6 s |
| 4 | 18 s | Station C | 4 → 5, 6 s |
| 5 | 24 s | Station D | 5 → 6, 6 s |
| 6 | 30 s | Arrival | — |

## 4. Making the keyframes

Generate them with GPT Image 2.5 as a **set**, each edited from or referencing the one before, so the constant element stays identical:

- Same aspect ratio for all of them (the take follows the first frame).
- Same character sheet attached to every one.
- The constant element in a consistent place and scale: if the protagonist is centre frame at the same size in every keyframe, the result reads as one continuous follow shot.
- Each keyframe composed to connect to the next: an open doorway on the side the camera will travel toward, the next space visible through it.

Show the set to the user as a strip before rendering. Fixing a keyframe is free; fixing the take is not.

## 5. Sending them through Artlist

The connector's `generate_video` takes a start frame and an end frame. It does not take middle frames, and an array of images is treated as references rather than keyframes (checked 2026-11-17). So render the take as segments that share frames:

1. Segment 1: `input: { startFrame: keyframe 1, endFrame: keyframe 2 }`
2. Segment 2: `input: { startFrame: keyframe 2, endFrame: keyframe 3 }`
3. Continue to the last keyframe.

Each segment ends on exactly the image the next one begins on, so the joins are frame-accurate. Pin the image-to-video variant at the resolution you want, set `duration` to the segment's whole seconds, and send all segments in one `generate_batch`: they depend only on stills that already exist, so they render in parallel.

Write every segment's prompt with the same opening sentence, so pace and direction match across joins, then describe only that segment's travel:

```
One continuous unbroken take, no cuts. The camera follows a woman in a long black coat from behind and slightly to the side at a constant walking pace, always moving left to right, keeping her centred at the same size.

0–3 s: she walks across the bright white room toward the open doorway on the right; the camera glides beside her.
3–6 s: she passes through the doorway and the door frame wipes across the lens; the room beyond is deep blue with rippling water-light. She keeps the same pace and is still mid-stride at the end.

Her hair, coat, trousers and boots stay exactly the same throughout.
Sound: boot heels on wood, then a soft underwater hum. No background music, no subtitles.
```

Rules for clean joins:
- End every segment except the last **mid-movement**, and say so. A segment that settles before its end frame makes the take stutter at the join.
- Same camera height, distance and speed words in every segment.
- Let sound carry across: end one segment's ambience where the next begins.
- Only the last segment gets "and holds".

Assemble with `studio.py assemble --chain --keep-audio` (or give the edit list). `--chain` drops the one repeated frame at each join, which otherwise shows as a tiny hitch. Tell the user plainly that the take is several renders joined on shared frames.

Tested 2026-11-17: three stills edited from one another and two 4-second segments at 720p gave a take in which the character, coat and scale held from first frame to last and the join was not visible. Clips come back at 24 frames per second and about 0.04 s longer than the requested seconds.

## 6. When one render is better

If the journey does not need exact pictures at exact times, a single reference-to-video render can be smoother and cheaper to iterate: pass the station stills as **references** (up to ten) and write the timeline in the prompt, stating that the images are the look of each station in order. The model then decides exactly when each station arrives. Use this for drafts of the idea and the chain for the version that must hit its marks.

## 7. Transitions that hide the joins

Whether the take is one render or a chain of segments, these make the passage between stations feel deliberate:

- **Through a doorway or window**: the frame edge wipes the old space away.
- **Past a foreground object**: a pillar, a passer-by, a wall fills the frame for a few frames.
- **Into darkness or light**: a tunnel, a flare, a flash.
- **Match on shape**: a round window becomes a moon, a spinning coin becomes a wheel.
- **Whip pan**: fast lateral blur.

Name the transition in the prompt at the moment it happens.

## 8. Common failures

| Symptom | Likely cause | Fix |
|---|---|---|
| Morphing between stations instead of moving | Keyframes too different in composition for the seconds given | Lengthen the segment; add a physical passage (doorway) between them |
| A visible hitch at a join | The earlier segment came to rest before its end frame | Say "still mid-stride at the end"; keep pace words identical in both segments |
| Character changes mid-take | Constant element not held across keyframes | Regenerate keyframes from the same sheet at the same scale |
| The take cuts | Prompt reads like a shot list | Start with "One continuous unbroken take, no cuts" and describe travel between every pair |
| Camera reverses direction | Direction not stated in each beat | Repeat "moving left to right" in each beat |
| Ending drifts | No end frame, or no instruction to hold | Provide the last keyframe and end the prompt with "and holds" |
| Pace surges | Uneven segment lengths | Even out the times, or state "constant pace throughout" |
