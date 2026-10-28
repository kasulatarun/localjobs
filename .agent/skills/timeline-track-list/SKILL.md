---
name: timeline-track-list
description: List the tracks of a `TimelineAsset` — name, type, mute/lock state, clip count, and each track's clips (with timing). Read-only.
metadata:
  generated-by: mcp-plugin-dotnet
---

# Timeline / List Tracks

List the tracks of a `TimelineAsset`. For each output track returns its name, type, muted / locked flags, clip count, and (optionally) the clips with their timing.

## Inputs

- `assetPath` — required path to the `.playable` TimelineAsset.
- `includeClips` — when `true` (default) include each track's clip list; when `false`, counts only.

## Behavior

Enumerates `TimelineAsset.GetOutputTracks()` and reports each track. Read-only. Runs on the Unity main thread.

## How to Call

```bash
unity-mcp-cli run-tool timeline-track-list --input '{
  "assetPath": "string_value",
  "includeClips": false
}'
```

> For complex input (multi-line strings, code), save the JSON to a file and use:
> ```bash
> unity-mcp-cli run-tool timeline-track-list --input-file args.json
> ```
>
> Or pipe via stdin (recommended):
> ```bash
> unity-mcp-cli run-tool timeline-track-list --input-file - <<'EOF'
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
| `includeClips` | `boolean` | No | If true (default), include each track's clips and their timing; if false, only counts. |

### Input JSON Schema

```json
{
  "type": "object",
  "properties": {
    "assetPath": {
      "type": "string"
    },
    "includeClips": {
      "type": "boolean"
    }
  },
  "required": [
    "assetPath"
  ]
}
```

## Output

This tool does not return structured output.

