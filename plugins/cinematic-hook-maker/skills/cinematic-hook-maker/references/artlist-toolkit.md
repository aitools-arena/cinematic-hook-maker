# Artlist toolkit

How to drive the Artlist connector for this workflow. Limits below were read from the connector on 2026-11-17; `get_model_config` is the authority and may have changed.

## Contents
1. Setup for a new user
2. Models and verified limits
3. Choosing the Kling 4.0 mode and the input shape
4. Tool map by task
5. The generation loop
6. Cost and confirmation
7. Uploads, folders, saved references, style kits
8. When something goes wrong

## 1. Setup for a new user

If no Artlist tools are available, give exactly this and stop:

1. In Claude, open Settings → Connectors → Add custom connector.
2. Name it Artlist, paste `https://mcp.artlist.io/mcp`, connect, sign in to Artlist and authorise.

Then ask them to start a new message. A free Artlist plan can still use its free generations here.

## 2. Models and verified limits

Find a model by its display name with `list_models` (pass `kind: "video"` or `"image"`; the full list is long, so narrow it with `feature` or a known `modelGroupId`). Never show IDs to the user.

### Kling 4.0 (video)
| Setting | Values |
|---|---|
| Duration | 3 to 30 seconds, whole seconds, default 15 |
| Resolution | 720p or 1080p |
| Aspect ratio | Auto, 16:9, 9:16, 1:1, 21:9 (image-to-video follows the first frame: Auto only) |
| Audio | `generate_audio` on by default; turn off for silent plates |
| Prompt | up to 11,000 characters |
| Frames | start frame and end frame (through the connector) |
| References | up to 10 images and up to 5 videos in one request |
| Price seen 2026-11-17 | 700 credits for 4 s at 720p with start and end frame (175 per second) |

The model lists a middle-frames input, but the connector does not expose it: `generate_video` accepts a start frame and an end frame, and an array of images is always treated as references, not keyframes (checked 2026-11-17: an array sent to the image-to-video variant is refused with `wrong_feature`).

Variants in the group: text-to-video, image-to-video, reference-to-video with images, reference-to-video with video; each at 720p and 1080p.

### Kling 4.0 Flash (draft video)
| Setting | Values |
|---|---|
| Duration | 3 to 20 seconds, default 5 |
| Resolution | 720p only |
| Aspect ratio | Auto, 16:9 (default), 9:16, 1:1, 21:9 |
| Frames | start frame only — no end frame, no middle frames |
| References | up to 10 images and up to 5 videos |

Anything longer than 20 s, or needing an end frame or middle keyframes, cannot be drafted on Flash. Draft those on Kling 4.0 at 720p.

### GPT Image 2.5 (stills)
| Setting | Values |
|---|---|
| Aspect ratio | 16:9 (default), 9:16, 1:1, 2:3, 3:4, 4:3, 3:2 — **no 21:9** |
| Quality (`resolution`) | low, medium (default), high, xhigh, max |
| Output size (`output_resolution`) | 1K (default), 2K, 4K |
| Variant (`arlist_model`) | flare (default), sunburst |
| Background | auto, transparent, opaque |
| Images per call (`num_images`) | 1 to 10 |
| Editing | pass one or more images as `input` |
| Price seen 2026-11-17 | 80 credits for one still at medium quality, 1K (free-plan users can spend their free generations on it) |

For a 21:9 film, generate stills at 16:9 and crop with `studio.py fit <image> --ratio 21:9` before uploading them as frames, or let a reference-to-video shot set 21:9 itself.

## 3. Choosing the Kling 4.0 mode and the input shape

| You have | Mode | `input` to `generate_video` |
|---|---|---|
| Only words | text-to-video | none |
| A designed first frame | image-to-video | `{ generationId }` or `{ assetId }` |
| First and last frame | frames | `{ startFrame: ref, endFrame: ref }` |
| Several keyframes for one long take | a chain of start/end-frame segments | see `onetake-keyframes.md` |
| Character, location, prop sheets to combine | reference-to-video (images) | an array of refs, up to 10 |
| Existing footage for motion, camera or editing | reference-to-video (video) | an array mixing video and image refs, up to 5 videos |

A `ref` is `{ generationId, outputIndex? }` for something Artlist already made, `{ assetId }` for an upload, or `{ referenceId }` for a saved character, prop or location.

Pass the group rather than pinning a variant when you can: the connector routes to the right variant from the input shape. Pin a specific model only to force 720p versus 1080p or Flash versus full.

With two or more references the model cannot tell them apart by name. State in the prompt which is which **by position**: "The first reference image is the heroine; the second is the kitchen; the reference video supplies only the camera move."

A style kit cannot be combined with start/end-frame input. For framed shots, write the look rules into the prompt instead.

## 4. Tool map by task

| Task | Tool |
|---|---|
| Find a model, read its settings | `list_models`, `get_model_config` |
| Price something before making it | `get_generation_cost` |
| Check the user's credits | `get_balance` |
| Make or edit a still | `generate_image` |
| Make a video | `generate_video` |
| Several different generations at once (max 20) | `generate_batch` |
| More takes of one still | `generate_image` with `settings.num_images` |
| Wait for results | `get_generation_status` (one ID or up to 12) |
| Bring in the user's own image or footage | `upload_image`, `upload_video`, then `confirm_upload` when a presigned upload is used |
| Reuse a saved character, prop, location | `list_references`, then `input: { referenceId }` |
| Hold the look across a production | `create_style_kit`, `add_style_kit_item`, `get_style_kit` |
| Keep things tidy | `create_folder`, or `folderName` on the first generation then reuse `folderId` |
| Find earlier work | `list_generations` |
| Voice-over | `list_voices`, `generate_voiceover` |
| Music | `search_music` for catalogue tracks, `generate_music` for new ones |
| Sound effects | `search_sfx` |
| Save a file | `download_generation`, `download_track` |

## 5. The generation loop

1. `get_model_config` once per model per session; build `settings` only from keys and values it lists.
2. `generate_image` / `generate_video` / `generate_batch`.
3. If the answer is `queued`, call `get_generation_status` immediately with the returned ID, and again while `pending`. Do not wait between calls; the tool already blocks for about fifty seconds. Videos can take several minutes.
4. Record the ID against the shot: `studio.py log <shot> --gen <id> …`.
5. Show the result and say plainly what you see.

For a batch, poll all queued IDs together (twelve at most per call) with the same array each time. Never resend a batch, and never resend a job reported as `unknown`; it may already have been made and charged.

## 6. Cost and confirmation

- Quote first. `get_generation_cost` takes the same arguments as the generate call and makes nothing.
- Cost grows with video duration. Use the length the shot needs, not the maximum.
- Reference-to-video is priced differently from plain image-to-video; the queued response echoes the price.
- `confirmation_required` means nothing was spent. Show the cost and wait. Add `confirmCost: true` (and `approvedPrice` for a batch) only after the user says yes in a new message.
- Keep a running total with `studio.py log … --credits N` and report it at each stage.

## 7. Uploads, folders, saved references, style kits

**Uploads.** A public https link is the easy path (`imageUrl` / `videoUrl`). For a file on the user's machine, request a presigned URL with `mimeType` and the real `fileName`, PUT the bytes, then `confirm_upload`. If the upload cannot complete in the user's client, call `upload_widget`. Never send base64. Pass a video itself as a reference; do not extract a frame from it.

**Folders.** One folder per production. The first generation sets it with `folderName`; every later call passes the `folderId` that came back.

**Saved references.** When the user says "use Mara" or "my character", call `list_references`, show the matches by name and picture, and let them choose. Do not guess between two matches. If you name a model that cannot hold a saved identity, the call returns `reference_unsupported_model` and spends nothing; drop the model and let routing choose.

**Style kit.** Create one per production: a text item with the look rules, one palette item with every colour, and the approved hero images. Attach it with `styleKitId` on stills and on reference-style video shots. Use `styleKitItemIds` to send only the items a shot needs.

## 8. When something goes wrong

| Result | Meaning | Do |
|---|---|---|
| `confirmation_required` | Above the cost gate (a two-clip batch at 1,400 credits triggered it) | Show cost, wait for approval |
| `wrong_feature` | The input shape does not match the pinned variant | Pass the group instead of a variant, or use the shape that variant takes |
| `project_required` | User has several projects | Ask which, pass `projectId` |
| `reference_unsupported_model` | Pinned model cannot hold a saved reference | Remove the model, let routing pick |
| `batch_invalid` | A job failed validation; nothing spent | Fix the named job, resend the whole batch |
| `batch_too_large` | More than 20 jobs | Split by priority, tell the user |
| Settings rejected | Key or value not in the model config | Re-read `get_model_config`, rebuild `settings` |
| Still `pending` after many polls | Long video | Keep polling; do not regenerate |
| Failed generation | Often moderation or an unreadable reference | Read the message; simplify the prompt or replace the reference |
| `download_unavailable` | Plan has no AI credits | Relay the message |
