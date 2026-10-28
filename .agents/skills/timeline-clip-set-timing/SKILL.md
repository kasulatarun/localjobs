---
name: timeline-clip-set-timing
description: "Set the timing of a clip on a Timeline track: start, duration, clip-in (trim), blend-in / blend-out durations, ease-in / ease-out durations, and time scale. Only the values you supply are changed."
metadata:
  generated-by: mcp-plugin-dotnet
---

# Timeline / Set Clip Timing

Adjust the timing of an existing clip identified by track + clip index. Any value left null is untouched, so this tool can tweak a single property or several at once.

## Inputs

- `assetPath` — required path to the `.playable` TimelineAsset.
- `trackName` / `trackIndex` — which track holds the clip (name wins; index default 0).
- `clipIndex` — required zero-based index of the clip on its track.
- `start` — optional new start time (seconds).
- `duration` — optional new duration (seconds).
- `clipIn` — optional clip-in / trim offset into the source asset (seconds).
- `blendInDuration` / `blendOutDuration` — optional crossfade blend durations (seconds).
- `easeInDuration` / `easeOutDuration` — optional ease (fade) durations (seconds).
- `timeScale` — optional playback time scale of the clip.

## Behavior

Resolves the clip, applies each supplied value, saves the asset, and returns the resulting timing. Runs on the Unity main thread.

## How to Call

```bash
unity-mcp-cli run-tool timeline-clip-set-timing --input '{
  "assetPath": "string_value",
  "clipIndex": 0,
  "trackName": "string_value",
  "trackIndex": 0,
  "start": 0,
  "duration": 0,
  "clipIn": 0,
  "blendInDuration": 0,
  "blendOutDuration": 0,
  "easeInDuration": 0,
  "easeOutDuration": 0,
  "timeScale": 0
}'
```

> For complex input (multi-line strings, code), save the JSON to a file and use:
> ```bash
> unity-mcp-cli run-tool timeline-clip-set-timing --input-file args.json
> ```
>
> Or pipe via stdin (recommended):
> ```bash
> unity-mcp-cli run-tool timeline-clip-set-timing --input-file - <<'EOF'
> {"param": "value"}
> EOF
> ```


### Troubleshooting

If `unity-mcp-cli` is not found, either install it globally (`npm install -g unity-mcp-cli`) or use `npx unity-mcp-cli` instead.
Read the /unity-initial-setup skill for detailed installation instructions.

## Input

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `assetPath` | `string` | Yes | Assets-rooted path to the TimelineAsset (.playable). |
| `clipIndex` | `integer` | Yes | Zero-based index of the clip on its track. |
| `trackName` | `string` | No | Name of the track holding the clip. Takes precedence over trackIndex. |
| `trackIndex` | `integer` | No | Zero-based root-track index, used when trackName is null/empty. |
| `start` | `number` | No | Optional new start time in seconds. |
| `duration` | `number` | No | Optional new duration in seconds. |
| `clipIn` | `number` | No | Optional clip-in (trim offset into the source asset) in seconds. |
| `blendInDuration` | `number` | No | Optional blend-in (crossfade) duration in seconds. |
| `blendOutDuration` | `number` | No | Optional blend-out (crossfade) duration in seconds. |
| `easeInDuration` | `number` | No | Optional ease-in (fade) duration in seconds. |
| `easeOutDuration` | `number` | No | Optional ease-out (fade) duration in seconds. |
| `timeScale` | `number` | No | Optional playback time scale of the clip. |

### Input JSON Schema

```json
{
  "type": "object",
  "properties": {
    "assetPath": {
      "type": "string"
    },
    "clipIndex": {
      "type": "integer"
    },
    "trackName": {
      "type": "string"
    },
    "trackIndex": {
      "type": "integer"
    },
    "start": {
      "type": "number"
    },
    "duration": {
      "type": "number"
    },
    "clipIn": {
      "type": "number"
    },
    "blendInDuration": {
      "type": "number"
    },
    "blendOutDuration": {
      "type": "number"
    },
    "easeInDuration": {
      "type": "number"
    },
    "easeOutDuration": {
      "type": "number"
    },
    "timeScale": {
      "type": "number"
    }
  },
  "required": [
    "assetPath",
    "clipIndex"
  ]
}
```

## Output

This tool does not return structured output.

