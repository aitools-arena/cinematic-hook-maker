# VFX mode: working from existing footage

For when the user already has a clip — phone footage, a 3D previs, a stock shot, an earlier generation — and wants to change part of it, or borrow its movement for something new. The footage does the directing; you decide what stays and what changes.

## Contents
1. Two different jobs
2. Preparing the footage
3. The keep / change plan
4. Recipes
5. Making it look real
6. Limits and costs
7. Review points

## 1. Two different jobs

Decide which one this is before writing anything, because the first words of the prompt select it.

| Job | Result | Prompt begins |
|---|---|---|
| **Edit** | The same clip with something changed | "Edit the reference video. …" |
| **Borrow** | A new clip that takes camera, movement or pacing from the footage | "Use only the camera path of the reference video. …" |

"Reference the video and change the jacket" is ambiguous and tends to produce a new, different video. Say "Edit" when you mean edit.

## 2. Preparing the footage

- Up to five clips per request. Keep each between 3 and 30 seconds and keep the combined length of all clips at 30 seconds or less; shorter references follow more reliably.
- Trim to the part that matters with `studio.py trim <file> --start 2 --dur 8` (needs ffmpeg) before uploading. Length is cost.
- Upload with `upload_video` and pass the video itself. Never extract a frame as a substitute.
- Steady, clearly lit footage with a readable subject works best. A grey 3D previs or a rough animatic is an excellent motion reference: it carries camera and blocking with no appearance to leak.
- If real people are visible, confirm the user has the right to use them, and do not turn a real person into someone else's likeness.

## 3. The keep / change plan

Write this down before the prompt and show it to the user in one line each. It is the whole brief.

```
KEEP    camera path and speed, framing, the walk, timing, the street layout
CHANGE  the walker → the armoured knight (first reference image)
        the sky → storm clouds
ADD     blue sparks around the sword from 3 s to 6 s
SOUND   keep original ambience; add crackling
```

One clear intent per render. Replace the character in one pass and add the effect in the next if both together do not hold.

## 4. Recipes

Number assets by position. Adapt the nouns; keep the structure.

**Replace a person**
```
Edit the reference video. Replace the person walking in the centre with the character in the first reference image: keep that character's face, armour and proportions exactly. Keep everything else unchanged: the camera movement, framing, the walk and its timing, the street, the lighting and the video's length.
```

**Change only the outfit**
```
Edit the reference video. Change the woman's clothing to the outfit in the first reference image. Keep her face, hair, body and movement exactly as they are, and keep the background, camera and lighting unchanged.
```

**Replace the background**
```
Edit the reference video. Replace the environment behind the dancers with the location in the first reference image. Keep the dancers, their movement, the camera and the timing unchanged. Match the light on the dancers to the new location.
```

**Add an effect at a moment**
```
Edit the reference video. From 3 s to 6 s, add crackling blue electrical arcs around the sword blade that follow its movement, casting blue light on his hands and face. Keep everything else unchanged.
```

**Remove something**
```
Edit the reference video to remove the parked car on the left. Keep everything else unchanged, including the background behind it, the other people, the camera movement, the lighting and the video's length.
```

**Restyle**
```
Edit the reference video. Change its visual style to the hand-painted watercolour style of the first reference image. Preserve the original composition, shots, actions and timing. Change only the style.
```

**Borrow the camera move**
```
Use only the camera path and pacing of the reference video; do not carry over its people, objects or setting. The subject is the red sports car in the first reference image, on the coastal road in the second reference image at golden hour.
```

**Borrow the performance**
```
Use the body movement and timing of the reference video for the robot in the first reference image. Keep the robot's design exactly. The setting is the workshop in the second reference image. Static camera, medium-wide.
```

**Previs to final**
```
Use the reference video as the approved blocking and camera plan: follow its camera path, character positions and timing exactly. Render it as finished live-action footage. The grey figure is the woman in the first reference image; the room is the second reference image. Do not show any grey previs surfaces, grids or guide lines.
```

**Recreate a format with a new subject**
```
Edit the reference video. Replace the product in it with the bottle in the first reference image, keeping its label exactly. Keep the pacing, camera movement, lighting style and shot structure unchanged.
```

## 5. Making it look real

Anything composited in needs to belong to the light it is in. Add one sentence when replacing or adding:

> Lighting and shadows on the new element match the scene; it sits naturally in the shot with correct contact shadows and reflections.

Other things that help:
- Name the light the plate already has ("overcast daylight from above") so the new element is lit the same way.
- For effects, describe the light they give off and what it lands on.
- Say whether the original sound stays: "Keep the original audio" or describe the new sound.
- Lengths can differ slightly from the source after processing; do not promise frame-exact duration.

## 6. Limits and costs

- Video references are billed differently from plain image-to-video and usually cost more; quote before rendering.
- Kling 4.0 Flash accepts video references too, at 720p and up to 20 s, which makes it a sensible draft for edits.
- Output is 720p or 1080p. If the user needs higher, say that it is not available here.
- A reference video shares the request with image references: up to 5 videos and 10 images together.

## 7. Review points

Compare the result with the source side by side and check, in this order:

1. Did the things in KEEP actually stay — camera path, timing, framing?
2. Does the changed element hold its identity for the whole clip, including when it turns or is partly hidden?
3. Do edges, contact shadows and reflections belong to the scene?
4. Did anything outside the brief change (a sign, a background person, the colour of the sky)?
5. Is the sound what was asked for?

Report what changed that should not have. The usual fix is a stricter KEEP sentence listing the exact things that drifted, not a longer description of the change.
