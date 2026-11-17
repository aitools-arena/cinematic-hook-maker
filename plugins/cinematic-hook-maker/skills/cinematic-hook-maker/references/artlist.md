# Artlist connector for hooks

Limits were read from the connector on 2026-11-17. `get_model_config` is the authority and may have changed.

## Contents
1. Setup
2. Models and limits
3. Tool map
4. The generation loop
5. Cost and confirmation
6. When something goes wrong

## 1. Setup

If no Artlist tools are available, give exactly this and stop:

1. In Claude, open Settings → Connectors → Add custom connector.
2. Name it Artlist, paste `https://mcp.artlist.io/mcp`, connect, sign in to Artlist and authorise.

## 2. Models and limits

Find models by display name with `list_models` (`kind: "image"` or `"video"`, narrow with `feature`). Never show IDs to the user.

| Model | Use | Limits |
|---|---|---|
| GPT Image 2.5 | first frame, cover, thumbnail, edits | ratios 16:9, 9:16, 1:1, 2:3, 3:4, 4:3, 3:2 (no 21:9, no 4:5); quality low to max; output 1K, 2K, 4K; 1–10 images per call; edit by passing images as `input`. Seen at 80 credits (medium, 1K) and 140 (high, 2K) per image. |
| Kling 4.0 Flash | hook drafts | 3–20 s, 720p, first frame only, audio on by default. |
| Kling 4.0 | final hooks, start and end frames | 3–30 s, 720p or 1080p, start and end frame, up to 10 image and 5 video references, audio on by default, prompt up to 11,000 characters. Seen at 175 credits per second at 720p. |

Image-to-video takes its ratio from the first frame, so make the still in the platform's render ratio. Clips have come back at 24 fps with audio.

Through the connector, `generate_video` accepts a start frame and an end frame (`input: { startFrame, endFrame }`); an array of images is always treated as references, not keyframes.

## 3. Tool map

| Task | Tool |
|---|---|
| Read a model's settings | `get_model_config` |
| Price something without making it | `get_generation_cost` |
| Credits left | `get_balance` |
| First frame, edits, covers | `generate_image` (`settings.num_images` for takes) |
| The hook clip | `generate_video` |
| Several different jobs at once | `generate_batch` (max 20) |
| Wait for results | `get_generation_status` (one ID or an array of up to 12; call again at once while pending) |
| The user's photos or footage | `upload_image`, `upload_video`, then `confirm_upload` for presigned uploads; `upload_widget` if the client can't upload |
| Saved characters or products | `list_references`, then `input: { referenceId }` |
| Keep a look across hooks | `create_style_kit`, `add_style_kit_item` (not combinable with start/end frames) |
| Save the files | `download_generation` |
| Folders | `folderName` on the first generation, then the returned `folderId` |

A `ref` is `{ generationId }` for something Artlist made, `{ assetId }` for an upload, or `{ referenceId }` for a saved reference. Reuse results by `generationId`; never download and re-upload them.

## 4. The generation loop

1. `get_model_config` once per model per session.
2. Generate. If the answer is `queued`, call `get_generation_status` immediately and again while pending. Videos can take minutes.
3. If the status result has no file link, call `download_generation` for one.
4. Log it: `hookmaker.py log <concept> --stage … --gen … --credits …`.
5. Look at it and say what you see.

Never resend a batch or a job reported as `unknown`; it may already have been made and charged.

## 5. Cost and confirmation

- Quote first with `get_generation_cost` (same arguments as the generate call; image-to-video quotes need the first frame as `input`).
- State the stage total in one line: for example "three first-frame takes at 140 each, 420 credits; one 4-second Flash draft after that".
- `confirmation_required` means nothing was spent. Show the cost and wait. Add `confirmCost: true` (and `approvedPrice` for a batch) only after the user says yes in a new message.

## 6. When something goes wrong

| Result | Do |
|---|---|
| `confirmation_required` | Show the cost, wait for approval |
| `wrong_feature` | The input shape doesn't match the pinned variant: pass the model group instead, or the shape that variant takes (image-to-video needs a first frame) |
| `invalid_settings` / pinned variant | Pass `modelGroupId` without `modelId` and let Artlist route |
| `project_required` | Ask which project, pass `projectId` |
| `batch_invalid` | Fix the named job; nothing was spent |
| Failed generation | Often moderation or an unreadable reference: simplify or replace it |
| `download_unavailable` | Relay the message |
