# Look: realism, camera and motion for hooks

How to write the first-frame prompt (GPT Image 2.5) and the motion prompt (Kling 4.0) so the hook looks like a real, well-shot, good-looking video and not like AI.

## Contents
1. Real and good-looking
2. The first-frame prompt
3. Camera choices that stop a scroll
4. The motion prompt
5. Text inside the shot
6. Self-check before spending

## 1. Real and good-looking

AI content that performs shows attractive people and beautiful things. Realism is not plainness. The target is **an attractive subject in a real, unretouched photograph**, like a professional model in a street-style shot or a product in an honest, well-lit photo. Keep the two jobs apart:

- **Appeal** comes from casting, grooming and flattering light: striking well-proportioned features, groomed brows, clear healthy skin, styled hair, light makeup when it fits (thin eyeliner, mascara, soft blush, tinted lips); for products, clean surfaces, crisp edges and one beautiful highlight. Keep faces in open shade or bounced light even when the sun is hard on the background.
- **Realism** comes from capture, light physics and materials: one named light source with real shadows, fine skin texture visible up close, a few stray hairs, natural fabric creases, real walls and floors, neutral colour without grading.
- **Keep faults small.** Texture yes; oily shine, blotches, puffiness and a tired face no, unless the hook is about exactly that.
- **Expression as a behaviour, not a pose.** "Relaxed and unposed, lips softly closed, looking into the lens with a calm, confident expression." A posed model smile is the fastest way to lose realism; a blank or tired face the fastest way to lose appeal. A smile belongs only where the motion earns it (a reaction in the hook), never as the default.

**The full recipe** (six parts of a realistic prompt, a tested template, realism references, night and effects) is in `references/gpt-image-2-5.md`, section 2. Read it before every still with a person in it; character sheets and casting photos are in section 3 of the same file.

**Words that make it worse:** perfect, flawless, cinematic, epic, masterpiece, 8K, ultra-detailed, hyper-realistic, photorealistic, award-winning, dramatic lighting, glowing skin, smooth skin. Replace them with physical facts. "Beautiful" alone does nothing; describe the features, grooming and light.

## 2. The first-frame prompt

Write it in this order and keep each part short:

1. **Capture**: "Unretouched photo taken on a phone camera", "frame grab from a digital cinema camera", "35 mm film photograph".
2. **Subject and moment**: who or what, doing what, at the instant just before or just as the hook's action starts. A frozen instant, never a sequence.
3. **Framing**: size, angle, lens (section 3).
4. **Light**: one source, its direction and hardness, what it leaves in shadow.
5. **Appeal and detail**: the features, grooming or product finish; two or three real-world details (texture, creases, a scuff).
6. **Space for text**: "clean, uncluttered space in the upper third for a caption", inside the platform's safe zone.
7. **Colour**: "neutral true-to-life colour, no colour grading" unless the look calls for a stated palette.
8. **Exclusions**: "No text, no watermark" (the text is added later and exact).

Example (vertical, tutorial, result first):

```
Unretouched photo taken on a phone camera. A strikingly attractive woman in her mid-twenties, defined cheekbones, groomed brows, light makeup, sits at a wooden desk at night holding a phone that shows a finished vertical film frame. Medium close-up at eye level, 35 mm. The only light is a warm desk lamp from the left, the right side of her face in soft shadow, the room beyond falling to dark. Fine skin texture, a few stray hairs catching the lamp, a creased linen shirt. Clean dark space in the upper third for a caption; her face and the phone stay away from the bottom quarter and the right edge. Neutral colour, no grading. No text, no watermark.
```

For the user's face, product or place, pass their photo as `input` and write: "The first image is the person (or product); keep the face, hair and skin tone (or the shape, colours, label and logo) exactly." Then describe only the new moment.

Make two to four takes with `num_images`, choose, then **edit** small faults: "Keep everything identical. Change only …". When a frame looks artificial, one edit usually fixes it: "Keep the person, pose, framing and light the same. Make it an unretouched photograph: restore fine pores, a few flyaway hairs, natural fabric creases, remove colour grading."

## 3. Camera choices that stop a scroll

Choose by the hook's job, not by taste. One choice per row.

| Choose | When the hook needs | Prompt words |
|---|---|---|
| Extreme close-up | a detail that raises a question | "extreme close-up on …" |
| Close-up | emotion, a face reacting | "close-up on the face" |
| Medium close-up | a person talking to camera | "medium close-up, face and shoulders" |
| Top-down | hands demo, product layout | "top-down overhead view" |
| POV | the viewer inside the moment | "first-person point of view from the eye line" |
| Low angle | power, scale, a product as hero | "low angle looking up" |
| Wide with a small subject | scale, isolation, an impossible event | "wide frame, subject small and off-centre" |
| 85 mm | flattering faces, product separation | "85 mm portrait lens, soft background" |
| 24–35 mm | place plus person, energy | "28 mm lens" |
| Macro | texture, satisfaction, scale shift | "100 mm macro lens" |

Light that reads instantly on a phone: **hard sun with a sharp shadow** (graphic, real), **one practical lamp in the dark** (intimate, cinematic), **screen glow on a face** (night, secrets), **rim backlight** (separation, product edges), **window light** (soft, flattering). Name the source every time.

Atmosphere needs a physical cause: dust shows only in a beam, sparks need an impact, reflections need a wet or glossy surface, wind moves only light things.

## 4. The motion prompt

The first frame already fixes the look, so the motion prompt describes only what changes. For hooks:

- **Action from frame one.** "The action is already underway in the first frame; something visibly changes within the first second." No fade in, no slow establishing.
- **One main action with an ending.** "The glass tips, falls and shatters on the tiles", not "things happen".
- **One camera move, starting immediately.** Push-in for realisation, pull-back for reveal, handheld for urgency, orbit for a product hero, static for a face talking.
- **The line, if spoken.** Who speaks (by something visible), the voice (age, tone, pace), the words in quotes in their language: `The woman at the desk says in a calm, low voice, in English: "This took me one afternoon."` About seven words for three seconds.
- **The end.** "End on a clean beat that cuts straight into the main video", or for loops on Shorts, "end on a frame that matches the first".
- **Sound block.** `Sound: <line> / <ambience> / <one effect> / no background music, no subtitles.`

Length: 3–6 s. Draft on Kling 4.0 Flash (3–20 s, first frame only); final on Kling 4.0 (3–30 s, 720p or 1080p, start and end frames). A Flash draft and a Kling 4.0 final are different takes; keep the same first frame and prompt to hold them close.

For **Before/After** and **Transformation** formats, make the end frame by editing the first frame ("Same frame. Now …"), then render with both frames on Kling 4.0.

## 5. Text inside the shot

- **Hook captions**: add them after rendering with `hookmaker.py overlay`; they are exact and inside the safe zone.
- **Text that belongs to the scene** (a phone notification, a sign, a label): Kling 4.0 renders short text. Give the exact words in quotes, where it is, and when it appears. Check the spelling in the render.
- Keep captions to six words, high contrast (white with a dark outline, or dark on a white box), in the upper third on vertical video.

## 6. Self-check before spending

- Would the first frame stop you as a still, at thumbnail size?
- Is the subject attractive and the picture still clearly a real photograph?
- Is there one light source named, and space for the text?
- Does something change in the first second?
- One action, one camera move, an ending?
- Does the line fit the seconds, and is the text different from the line?
- Can the video keep the promise this hook makes?
