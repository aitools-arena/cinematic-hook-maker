# Review and fix

How to judge a render and what to change when it is wrong. The aim is to reach an approved shot in the fewest paid attempts.

## Contents
1. Looking at a result
2. The review checklist
3. Re-roll, rewrite or redesign
4. Defect catalogue
5. The revision loop
6. Extending and repairing a finished film

## 1. Looking at a result

Say what you actually see. If you can view the clip, describe it against the shot card: what matched, what did not. If you cannot view video in this environment, say so, show the link and ask the user two or three specific questions ("Does she stop at the window? Is the jacket still olive at the end?") rather than announcing success.

Judge against the shot's job first. A technically clean shot that fails its job is a failed shot; a slightly imperfect shot that delivers the beat may be the one to keep.

## 2. The review checklist

Go in this order. Stop at the first failure and fix that; later items often resolve with it.

1. **Job** — does the shot deliver its beat?
2. **Action** — did the described action happen, in order, and end?
3. **Identity** — face, hair, wardrobe match the sheet from first frame to last.
4. **Camera** — the move asked for, at the right speed, ending where it should.
5. **Geography** — screen positions and direction of travel match neighbouring shots.
6. **Light** — source and colour match the location.
7. **Hands, faces, text** — no extra fingers, no melting, no gibberish lettering.
8. **Sound** — line complete and in sync, right speaker, no unwanted music or captions.
9. **Cut points** — usable first and last second; action in progress at both ends where a cut on movement is planned.

Record the verdict: `studio.py review S03 --version 2 --verdict fix --note "jacket turns grey after 5 s"`.

## 3. Re-roll, rewrite or redesign

Choosing the wrong kind of retry is how credits disappear.

| Situation | Do |
|---|---|
| Right idea, one random glitch (a hand, a flicker) | **Re-roll**: same prompt, same inputs, once |
| Same failure twice | **Rewrite**: the prompt is causing it; change one thing |
| The model ignores an instruction repeatedly | **Simplify**: shorter shot, one action, fewer references |
| Identity or composition wrong from frame one | **Redesign the still**: fix the first frame, not the video prompt |
| The idea does not work as one shot | **Re-plan**: split into two shots or change the mode |

Never re-roll more than twice. Two identical failures are information.

## 4. Defect catalogue

| What you see | Usual cause | Change this one thing |
|---|---|---|
| Face changes during the shot | No identity anchor, or shot too long | Use image-to-video from an approved first frame; attach the character sheet; shorten the shot |
| Face differs between shots | Each shot designed from words | Build every first frame from the same sheet |
| Two characters blend into each other | Similar look, positions not stated | Differentiate silhouette and colour; state "man on the left, woman on the right"; or shoot singles |
| Extra person or duplicate appears | Count not locked | "Exactly one … in frame for the whole shot" |
| Hands deform | Hands doing fine work, or cropped at the wrist | Simplify the hand action; reframe so hands are fully in or fully out; shorten |
| Nothing much happens | Action described as a state | Use verbs with an endpoint: "walks to the door and stops" |
| Too much happens, chaotic | Several actions in one shot | One action; move the rest to the next shot |
| Camera wanders | No camera instruction | State the move, or "locked-off static camera" |
| Camera ignores the move | Move buried in a long prompt, or two moves | Put the camera sentence first in the action block; one move |
| Shot cuts when it should not | Prompt reads as a list of shots | "One continuous take, no cuts"; describe travel between beats |
| Shot does not cut when a multi-shot was wanted | Model merged the beats | Render the beats as separate shots |
| Light or colour shifts mid-shot | Light not anchored | Name the source and direction; "lighting stays constant" |
| Light differs between shots of one scene | Light sentence varies | Reuse the identical light sentence in every shot of the scene |
| Object disappears or changes | Not named as persistent | "The red umbrella stays in her right hand throughout" |
| Wardrobe changes colour | Described loosely | Exact colour and garment in every prompt; attach the sheet |
| Motion smears on fast action | Too fast for the frame | Slow the action or the camera; widen the shot; shorten the duration |
| Looks artificial or waxy | Abstract style words | Replace with concrete texture: skin pores, fabric weave, lens grain, a named light source |
| Unwanted music | Model default | "no background music" |
| Burned-in captions | Model default | "no subtitles" |
| Line cut short or mumbled | Too long for the shot | Fewer words or more seconds |
| Wrong person speaks | Speaker not identified | Identify by position and clothing; or singles |
| Reference image ignored | No stated job | "The first reference image is …; keep …" |
| Reference sheet appears in the video | Sheet treated as content | "This is a design sheet; do not render the sheet, grid or labels" |
| Edit produced a different video | Prompt said "reference" | Begin with "Edit the reference video" and list what stays |
| Added element looks pasted on | No integration instruction | "Lighting and shadows match the scene, natural contact shadows" |
| Garbled on-screen text | Text too long or unspecified | Exact words in quotes, short, position and duration stated |
| Final differs from approved draft | Re-render is a new take | Same first frame, prompt and references; change nothing else; accept small differences or pick the better take |
| Request rejected | Outside limits, or moderation | `studio.py validate`; simplify wording; replace the reference |

## 5. The revision loop

1. Name the defect in one sentence.
2. Pick the single change from the catalogue.
3. Quote the cost if it is a paid render.
4. Render that shot only, as a new version (`studio.py log S03 --stage draft …` creates version N+1).
5. Compare with the previous version and say which is better and why.
6. Approve one: `studio.py approve S03 --version N`.

When the user gives a note ("make it more dramatic"), translate it into something visible before acting: closer framing, harder light, a slower push-in, a longer hold. Tell them the translation in a line so they can correct it.

After three failed versions of one shot, stop and offer a different approach (another mode, a split, a simpler action) instead of a fourth attempt.

## 6. Extending and repairing a finished film

- **Add a shot between two existing ones**: use the last frame of the earlier shot as the start frame and the first frame of the later one as the end frame.
- **Lengthen an ending**: start a new shot from the final frame of the last one and describe only what happens next.
- **Replace one shot in a locked cut**: keep its duration identical so the edit and the music do not move.
- **Change one thing in an approved shot**: use it as a reference video and edit it (`vfx-mode.md`) rather than regenerating from scratch.
- **Reformat for another platform**: re-render from references at the new ratio; do not crop a 16:9 final to 9:16 if faces or text sit near the edges.
