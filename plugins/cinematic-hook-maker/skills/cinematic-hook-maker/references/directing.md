# Directing: camera, light, blocking, continuity

The vocabulary and the rules for turning a shot's job into a picture the model can render and an editor can cut.

## Contents
1. Choosing the shot size
2. Camera movement, and when to use it
3. Angle and lens
4. Light
5. Blocking
6. Continuity between shots
7. Rhythm
8. The shot card

## 1. Choosing the shot size

Size decides how much the audience is asked to feel.

| Size | Shows | Use it to |
|---|---|---|
| Extreme wide | place, scale | open a scene, isolate someone |
| Wide | whole body in the space | show geography and movement |
| Medium | waist up | play behaviour and exchanges |
| Medium close-up | chest up | hold a conversation |
| Close-up | face | deliver emotion or a decision |
| Extreme close-up | an eye, a hand, an object | point at the detail that matters |
| Insert | an object alone | plant or pay off information |
| Over-the-shoulder | one person past another | tie two people together |
| Point of view | what a character sees | put the audience inside them |

Change size or angle noticeably between neighbouring shots. Two medium shots of the same person from nearly the same place read as a mistake.

## 2. Camera movement, and when to use it

A move needs a reason. If you cannot say why the camera moves, hold it still.

| Move | Words to use | Reason |
|---|---|---|
| Static | "locked-off static camera" | let the performance or composition work |
| Push-in | "slow push-in from medium to close-up" | realisation, growing pressure |
| Pull-back | "camera pulls back to reveal…" | reveal context, leave someone alone |
| Pan / tilt | "camera pans right to follow…" | follow or connect two things |
| Tracking | "camera tracks alongside at walking pace" | travel with a character |
| Orbit | "camera arcs 90 degrees around her, left to right" | a turning point, a hero moment |
| Crane / rise | "camera rises from ground level to above the rooftops" | open out, end a sequence |
| Handheld | "handheld, slight natural shake" | urgency, intimacy, documentary feel |
| Whip pan | "fast whip pan right" | energy, a hidden cut between two shots |
| Rack focus | "focus shifts from the letter in the foreground to her face" | redirect attention inside one frame |
| Dolly zoom | "background stretches while she stays the same size" | vertigo, a shock |

State start, path and end: "Camera starts low behind the wheel, tracks forward along the car, and stops level with the driver's window." One move per beat.

## 3. Angle and lens

- **Eye level** is neutral. **Low angle** gives power or threat. **High angle** shrinks someone. **Overhead** turns people into pattern. **Dutch tilt** signals something wrong; use once.
- Describe the lens by its effect: "wide-angle look, deep focus, exaggerated space" for place and unease; "50 mm look, natural perspective" for people; "long-lens look, compressed background, shallow focus" for isolation and intimacy.
- Shallow depth of field directs the eye and hides background errors. Deep focus needs a clean background.

## 4. Light

Say where the light comes from and what it is. A named source is copied more faithfully than a mood word.

- **Source**: window, lamp, screen, fire, street light, sun position.
- **Direction**: from the left, from behind (rim), from below, overhead.
- **Quality**: hard with sharp shadows, or soft and wrapping.
- **Colour**: warm practical against cool ambient is the workhorse contrast.
- **Level**: bright and even (comedy, product), low with deep shadow (drama, thriller).

Keep the light of a location identical in every shot set there, using the same sentence. Changing light between shots is the most common reason a cut looks wrong.

## 5. Blocking

Where people stand tells the story before anyone speaks.

- Distance between two people is their relationship. Change it when the relationship changes.
- Whoever moves has the energy; whoever stays still has the power.
- Put the thing that matters in the clear, not behind another object.
- Give a character something to do with their hands. Business makes behaviour.
- Describe positions in screen terms: "on the left of frame", "in the doorway at the back", "seated, facing right".

### More rules that save renders

- **A still freezes one moment.** A first-frame prompt describes a single instant ("the moment before she opens the door"), never a sequence. Movement belongs in the video prompt.
- **Camera direction is not subject direction.** "The camera tracks right" and "she walks right" are different instructions. Say both only when both are meant.
- **Effects need a physical cause.** Dust shows only in a beam of light, sparks need an impact, reflections need a wet or glossy surface, wind moves only loose and light things. A random effect reads as an error.
- **Atmosphere is written differently for stills and video.** In a still it is a frozen state ("snowflakes hanging in the air"); in the video it is behaviour ("light snow drifts down and settles"). `references/film-language.md` gives both wordings for every atmosphere.
- **A close-up cannot establish a space.** Use a wide or medium shot first, then go in.
- **The full vocabulary** of sizes, angles, moves, lenses, light, colour, atmosphere, pace, intent and transitions, each with when to use it and its prompt words, is in `references/film-language.md`. Choose from it by the shot's job.

## 6. Continuity between shots

Each shot is generated separately, so continuity must be written in.

- **The line.** Keep the camera on one side of two people. If A is on the left facing right in one shot, A stays on the left facing right in the next. State it in every prompt of the scene.
- **Eyelines.** A character looking off right must be answered by a shot of what is to the right, or of a person looking left.
- **Direction of travel.** Someone moving left to right keeps moving left to right until a shot shows them turn.
- **Wardrobe, hair, props.** The same sentence in every prompt, and the same reference sheet attached. Track which hand holds what.
- **Light and time of day.** One sentence per location, never varied.
- **Hand-off frames.** The safest cut between two shots of the same action: make the last frame of shot A the first frame of shot B (pass the earlier result as the start frame).
- **Cut on movement.** End a shot during an action and begin the next one already in it. Cuts hide inside motion.

Run `studio.py validate` to check lengths and limits, then read the shot list once only for these six points.

## 7. Rhythm

Length is feeling. Long shots build pressure or calm; short shots release energy.

| Feeling | Shape |
|---|---|
| Slow-burn drama | 6–10 s shots, few moves, one long hold near the end |
| Rising tension | each shot a little shorter than the last, then one long silent hold |
| Action or impact | 3–4 s shots, cut on movement, one wide to keep geography clear |
| Product or brand | 3–5 s shots with one 6–8 s hero shot |
| Wonder | one long moving shot, then a still close-up of a face reacting |

Vary it. A film made only of five-second shots feels mechanical however good each one is.

## 8. The shot card

Fill one per shot before writing its prompt. If a field is empty, the shot is not ready.

```
ID / seconds:
Job (what the audience gets):
Size and angle:
Who is where (screen left / right, facing):
Action, with its ending:
Camera: start → path → end
Light: source, direction, colour
The one detail:
Sound: line / ambience / effect
Carries over from previous shot:
Mode and references:
```
