# Deliverables

What the user walks away with, and how to produce each item. Everything here comes from the project file, so it stays correct as long as generations are logged.

## Contents
1. The storyboard board
2. The one-image pitch board
3. Shot list, edit list and cost report
4. Downloading the clips
5. Assembling a cut
6. Platform formats
7. Handoff for the next episode or conversation
8. Without code execution

## 1. The storyboard board

`studio.py board` writes `board.html`, a client-ready storyboard page that prints cleanly to A4 (browser → Print → Save as PDF):

- **Header:** title, logline, and an information bar with duration, format and ratio, style (from the Style Lock), target audience, music direction and progress in shots approved and credits.
- **Why this style works:** one sentence from `studio.py set style_note=…`. Write it as the reason the look serves this story, not as praise.
- **Cast and locations** with their pictures and traits.
- **One card per shot:** numbered circle and duration badge on the frame, the shot's job, camera (size, angle, move, lens), picture, action, line, on-screen text, sound, the transition into the next shot, status and version, and the prompts folded away.
- **Footer:** total running time, ratio, format, style.

- Attach a picture to a shot with `studio.py log S03 --gen <id> --thumb <image-url-or-path>` (use the still's URL from the generation result). Clips are linked, not embedded.
- Rebuild the board after each stage and show it: in a desktop or web conversation present the HTML file so it renders; otherwise give the file path.
- Result links from Artlist can expire. For a board that must last, download the stills into the project folder and log the local paths.

The board is the user's overview. It answers "where are we?" without scrolling the conversation.

## 2. The one-image pitch board

For a pitch or a social post before anything is rendered, `studio.py pitchboard` writes `exports/pitchboard-prompt.txt`: a GPT Image 2.5 prompt for a single A4 portrait image that lays out the whole film as a printed presentation board (title, information bar, why-this-style box, up to eight panels in a grid with scene number, duration, camera, action and line, and a footer).

- Render it at 3:4 or 2:3, quality high, 2K. Quote the cost first.
- Pass the approved character sheets and keyframes as `input` images and add `--with-refs`, so the panel pictures show the real cast. Without them the panels are illustrations of the plan, not of the film.
- Small text can come out misspelled. Read every word before the user shares it; fix with an edit, or point them to `board.html`, which is always exact.
- The panel pictures follow the realism rules in `gpt-image-2-5.md`, section 2.

## 3. Shot list, edit list and cost report

`studio.py export` writes three files into `exports/`:

| File | Contents | For |
|---|---|---|
| `shotlist.csv` | Every shot: ID, seconds, job, picture, action, camera, transition, dialogue, on-screen text, mode, status, approved version, generation ID, both prompts | Spreadsheet, client approval |
| `edit-list.md` | Approved shots in order with in and out times on the timeline, total running time, the sound notes for each | Whoever cuts the film |
| `cost-report.md` | Credits per shot and per stage, attempts versus approved, total | Budgeting, honest reporting |

The cost report counts what was logged. Say so if any generation was not logged, and prefer the user's Artlist usage page as the final word on charges.

## 4. Downloading the clips

Call `download_generation` for each approved shot (it returns a link and records the download in the user's Artlist history). When you can run code, save the files into `<project>/clips/` named by shot ID and version, for example `S03_v2.mp4`, and record each path with `studio.py log S03 --file clips/S03_v2.mp4 --version 2`.

Ask before downloading a large set; say how many files there are.

## 5. Assembling a cut

`studio.py assemble` joins the approved clips in shot order into `exports/cut.mp4`. It needs ffmpeg and local clip files.

- Clips are re-encoded to one common size at their own frame rate so mixed sources join cleanly.
- `--chain` is for segments of one take that share frames: it drops the repeated frame at each join.
- `--music <file>` lays a track under the cut, `--keep-audio` keeps each clip's own sound, and both together mix them with the music lowered.
- It makes straight cuts only. It is a rough cut for review, not a finished edit; tell the user that titles, grading and precise sound work belong in an editor.

If ffmpeg is missing, say so and give the edit list instead.

## 6. Platform formats

| Destination | Ratio | Notes |
|---|---|---|
| YouTube, web, presentations | 16:9 | 1080p |
| Cinematic showcase | 21:9 | Letterboxed on 16:9 players; keep titles inside the centre |
| Reels, TikTok, Shorts | 9:16 | Keep faces and text clear of the top 12% and bottom 20%, where interface elements sit |
| Feed posts | 1:1 | Centre the subject |

Decide the ratio at the start; it sets every keyframe. To deliver a second ratio, re-render the hero shots from references at the new ratio. Output tops out at 1080p; do not promise more.

## 7. Handoff for the next episode or conversation

`studio.py handoff` prints a compact brief: the bible, the cast with their saved references, the look in five facts, the style kit, the user's recorded preferences, open story threads and where production stopped. Give it to the user as a file and tell them to attach or paste it when they come back.

In the next conversation, read it first, confirm in one line what you are continuing, and carry on. Do not ask them to re-explain anything the handoff already holds.

Also save, where you have a memory, the durable facts about how this user works: preferred ratio and length, favourite look, how many options they like to see, how much explanation they want.

## 8. Without code execution

Everything above can be done by hand:

- **Board** → a table in the conversation with shot ID, picture, seconds, status.
- **Shot list and edit list** → write them as tables and offer them as a document.
- **Cost report** → sum the prices the generate tools echoed; state that it is a running tally.
- **Handoff** → write the brief yourself in the same structure.
- **Assembly** → provide the edit list and the download links in order.

Tell the user once that the automated versions exist when the skill runs somewhere that can execute code.
