# Stills with GPT Image 2.5

Stills are where the film is designed. They are quick, they cost a small fraction of video, and every one of them removes a guess from the video stage. Kling 4.0 copies what it is given: a plastic first frame becomes a plastic shot. Realism is won or lost here.

## Contents
1. Settings that matter
2. Photographic realism
3. Character sheet (casting photos)
4. Location plate
5. Prop sheet
6. Keyframes
7. Editing instead of regenerating
8. Holding a look across a production
9. Checks before approval

## 1. Settings that matter

| Need | Setting |
|---|---|
| Exploring ideas | quality `medium`, `num_images` 3 or 4 |
| An approved sheet or keyframe | quality `high`, output `2K` |
| Skin, hair and fabric must hold up close | quality `xhigh` or `max`, output `2K` (quote first; it costs more) |
| A frame that will be cropped to 21:9 | 16:9 at `2K` or `4K`, then `studio.py fit --ratio 21:9` |
| A cut-out prop or title element | background `transparent` |
| Vertical film | 9:16 for keyframes, 2:3 or 3:4 for sheets |

Two variants exist, Flare (default) and Sunburst. If a look is not landing on one, try the same prompt on the other before rewriting it. Match the keyframe's aspect ratio to the film's; image-to-video takes its ratio from the first frame.

## 2. Photographic realism

The model's default person is airbrushed, symmetrical, evenly lit and graded like a poster. Words like "realistic", "natural skin texture" or "cinematic" do not move it off that default; they are labels, and the model already believes its default matches them. What moves it is describing **a photograph that was actually taken**: one physical light, one real camera, and the small faults real things have.

### Real, and good-looking

AI imagery that people watch and share shows attractive people. Realism is not the same as plainness: the target is **a good-looking person in a real photograph**, the way a professional model looks in an unretouched editorial or street-style shot. Keep the two jobs separate:

- **Appeal comes from casting, grooming and flattering light.** Describe it concretely: striking, well-proportioned features, defined jaw and cheekbones, full lips, groomed brows, clear healthy skin, styled hair, and light makeup when it fits the character (thin eyeliner, mascara, soft blush, tinted lips). Put the face in open shade or bounced light even when the sun is hard on the background.
- **Realism comes from the capture, the light physics and the materials.** Fine skin texture and pores visible up close, a few flyaway hairs, real fabric creases, a real wall, neutral colour.
- **Keep the faults small and away from the face's appeal.** Texture yes; oily shine, blotches, puffiness, under-eye bags and a tired expression no, unless the story asks for them. Scars, dirt, sweat and exhaustion are story choices for a specific shot, not the default.

A fearful or exhausted character in a scene is still an attractive actor playing fear; write the emotion in the expression, not into the skin.

### The six parts of a realistic prompt

1. **The capture.** Name how the picture was made, and keep it plain. "Unedited photo taken on a phone camera", "35 mm film photograph, Portra 400 scan", "frame grab from a documentary shot on a digital cinema camera, ungraded log converted to Rec.709". A plain capture beats a glamorous one.
2. **One physical light.** Name the source, its direction, its hardness and what its shadows do. "Hard direct afternoon sun from the upper left; a sharp diagonal shadow of the window frame falls across the wall behind her; the shadow side of her face is lit only by light bouncing off the wall." No fill, no rim, no "studio lighting" unless the scene is in a studio.
3. **Plain framing.** Eye level, subject roughly centred or casually off-centre, real depth of field for the lens and distance. Avoid "dramatic angle", "bokeh", "epic composition".
4. **Fine skin and hair detail.** Fine natural skin texture with pores visible up close, a faint natural sheen on the nose and cheekbones, a few fine flyaway hairs catching the light, tiny natural asymmetry. Name two or three. Stronger faults (oily shine, redness, uneven tone, blemishes) make the person look unwell and should appear only when the story asks for them.
5. **Material faults.** Fabric creases where the body bends and at the seams, a loose thread, a cuff slightly turned; a plaster wall with hairline cracks and uneven paint; a scuffed floor. Real surfaces are never clean.
6. **Neutral colour.** "Neutral, true-to-life colour, no colour grading, highlights slightly clipped on the brightest skin, soft natural contrast." Teal-and-orange, crushed blacks and glowing skin read as AI before anything else does.

Finish with the expression, stated as a behaviour: "relaxed, unposed, lips softly closed, looking straight into the lens with a calm, confident, slightly serious expression." A forced model smile is the fastest way to lose realism; a tired or blank face is the fastest way to lose appeal.

### Words that make it worse

Leave these out of every realistic prompt: *perfect, flawless, cinematic, epic, masterpiece, 8K, ultra-detailed, hyper-realistic, photorealistic, award-winning, dramatic lighting, glowing skin, smooth skin, porcelain skin*. Each one pushes toward the airbrushed default. Words like *beautiful* or *stunning* alone do little; replace them with the concrete features, grooming and makeup listed above.

### Template

```
Unretouched editorial photo taken on a phone camera. A strikingly attractive woman in her early twenties, model features: defined cheekbones and jaw, full lips, groomed straight brows, large dark-brown eyes. She stands against a rough white plaster wall with hairline cracks, framed from the waist up at eye level, centred.

Light: hard afternoon sun from the upper left falls on the wall behind her, casting a sharp diagonal shadow of a window frame; her face is in soft open shade, lit evenly by light bouncing off the wall.

Her: long glossy black hair in a high ponytail with a few fine flyaway strands catching the sun, clear healthy skin with fine natural texture visible up close, a faint natural sheen on the nose and cheekbones. Light makeup: thin black eyeliner, mascara, soft blush, rosy tinted lips. She wears a fitted short-sleeved white cotton shirt with natural creases at the waist.

Relaxed and unposed, lips softly closed, looking straight into the lens with a calm, confident, slightly serious expression.

Neutral true-to-life colour, no colour grading. No text, no watermark.
```

### When the user has a realism reference

If the user supplies a picture whose realism they like, use it. Upload it, pass it as an `input` image and state its job: "The first image is a reference for lighting, skin texture, camera and colour only. Do not copy the person's face, hair, clothing or the setting." Add it to the production's style kit as a reference image so every still inherits it. Before using it, ask once whether it shows a real person; if it does, use it only for light and texture, never for identity.

### Night, darkness and effects

Low light is where realism breaks most often, because the model brightens faces and smooths noise. Write the darkness in physical terms: "the only light is the phone screen held at chest height, lighting her face from below; everything beyond arm's length falls to near black; visible sensor noise in the shadows; slight motion blur on her hand." For coloured light from a fantastical source (a ship, a portal, a beam), describe it as if it were a real lamp: its colour, how hard it is, which surfaces it hits and what it leaves in shadow.

## 3. Character sheet (casting photos)

One image that defines a person so every later shot can refer to it. Do not ask for a "character design sheet": that phrase pulls toward concept art and flat 3D-looking people. Ask for **casting photos** instead: real photographs of one person taken at a casting session.

```
Four casting photographs of the same person arranged in a 2x2 grid, each a separate unedited photo on a plain grey seamless paper backdrop: front, three-quarter left, side profile facing right, back. Full body, standing naturally with weight on one leg, arms relaxed. A single large softbox from the front left, a soft shadow on the backdrop, otherwise neutral light.

The person: a strikingly attractive woman in her early twenties, model features (defined cheekbones, full lips, groomed brows), slim build, long glossy black hair in a high ponytail with a few flyaway strands, a small mole under the left eye, clear skin with fine natural texture, light natural makeup. She wears an oversized faded mustard-yellow cotton hoodie with a stretched neckline and creased sleeves, black track pants, worn white sneakers with grey scuffs.

Shot on a digital camera, 50 mm lens, neutral true-to-life colour, no retouching, no colour grading. Each photo shows exactly one person. No text, no labels.
```

Then make a second image from the first: a row of six head-and-shoulders **expressions** (neutral, slight smile, anger, fear, grief, surprise) as casting close-ups, with the instruction to keep face, hair, skin texture and clothing identical. Expressions are what drift first in video; a sheet of them gives you a reference to pass.

What makes a sheet usable:
- **Three to five distinctive, visible traits** (hair shape, a mark on the face, a garment, a colour). These are what survive into video.
- **One costume per sheet.** A costume change is a new sheet edited from the first.
- **Plain backdrop and simple light**, so the model copies the person and not the mood. Simple light still has one direction and real shadow; "even studio light with no shadows" is what produces mannequins.
- **Original people only.** No real individuals or celebrity likenesses.

Offer two or three candidates, let the user pick, then save the choice (and add it to the style kit).

## 4. Location plate

A wide, empty view of the setting with the light the scene will use, written as a photograph of a real place:

```
Unedited wide photo of a narrow family kitchen at night, empty of people, taken at eye level from the doorway with a 28 mm lens. Wood-grain cabinets on the left wall with a chipped corner, a small table with two mismatched chairs under a window on the right, a kettle with a limescale ring and a stack of unopened letters on the counter. The only lights: one warm pendant lamp over the table, cold blue streetlight through the window. Corners beyond the lamp fall into deep shadow with visible grain. Neutral colour, no grading.
```

Make a second angle (reverse view) by editing the first, so that shots facing the other way still match. Note where the light comes from; you will repeat it in every prompt set here.

## 5. Prop sheet

For anything that reappears: a weapon, a vehicle, a product, a letter. Three views on a plain background, exact colours and markings described, with wear stated (scratches, fingerprints, a bent corner). For a real product the user owns, edit from their photo rather than inventing it, and keep every label exactly as supplied.

## 6. Keyframes

A keyframe is the first (or last, or a middle) frame of a shot. Build it by **combining the approved sheets**, not from words alone: pass the character sheet and the location plate as `input` and describe the moment, then the capture and light (section 2).

```
Using the first image for the woman's face, hair, skin and clothing and the second image for the kitchen: she stands at the counter on the left, back half-turned to camera, holding one opened letter in both hands, head lowered. Medium shot from the doorway, eye level. The pendant lamp lights her shoulder and the side of her face warm and hard; the window throws cold blue light on the far wall; the rest of the room is in shadow. Frame grab from a digital cinema camera, 35 mm lens, natural shallow depth of field, neutral colour, visible grain in the shadows, no grading. No text.
```

Compose for motion: leave space in the direction something will move, keep hands and faces unobstructed and fully in frame, and avoid cropping at joints. A keyframe that already implies its movement (weight on one foot, a hand reaching) animates better than a posed one.

For a shot that must end somewhere exact, make the **last frame** by editing the first: "Same frame. She has turned to face the door on the right; the letter is on the counter. Keep everything else identical."

## 7. Editing instead of regenerating

When a still is nearly right, edit it. Pass it as `input` and name **only the change**, then say everything else stays identical. Re-describing the whole image makes the model redraw the whole image, and the parts the user approved are lost.

```
Change only the jacket colour to dark navy. Keep the face, hair, pose, background and lighting exactly the same.
```

When a still is right in content but looks artificial, fix the realism with one edit: "Keep the person, pose, framing and light exactly the same. Make it look like an unretouched photograph: restore visible pores and slight shine on the skin, add fine flyaway hairs, add natural creases to the clothing, remove any colour grading."

Keep editing from the newest result's `generationId`. One change per edit.

## 8. Holding a look across a production

- Write the look as five facts and reuse the same wording in every prompt: capture, lens, light, colour, texture. Example: "frame grab from a digital cinema camera, 35 mm lens, hard practical light from one named source, neutral ungraded colour, visible grain in the shadows."
- Put those facts, the palette, the approved hero stills and any realism reference from the user in an Artlist style kit and attach it to every still.
- Pass the character sheet as a reference on every keyframe that contains the character, even when the prompt also describes them.
- When two characters share a frame, give them clearly different silhouettes, hair and colours, and state their positions ("the taller man on the left, the woman on the right"). Similar-looking characters blend.

## 9. Checks before approval

Look at each still before showing it and say what you see:

- **Realism and appeal:** fine skin texture, a few stray hairs, creased fabric, light from one direction with real shadows, no grading; and a face that is attractive and well groomed, not oily, blotchy, puffy or tired unless the shot calls for it. If it looks airbrushed, use the realism edit in section 7; if it looks plain or unwell, edit the grooming, makeup or face light, one change at a time.
- Face and hair match the sheet; the distinctive traits are present.
- Hands: five fingers, natural pose, not hidden awkwardly.
- No stray text, watermark, border or duplicated person.
- Light direction matches the location plate.
- Composition leaves room for the planned movement.
- Aspect ratio is the film's.

If a check fails, fix it with an edit before the user spends attention on it.
