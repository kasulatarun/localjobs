---
name: timeline-modify
description: "Generic write: apply a `SerializedMember` diff to a Timeline object (the `TimelineAsset`, a `TrackAsset`, or a clip's `PlayableAsset`) via ReflectorNet `TryModify`. Use 'timeline-get' first to inspect the structure. Remember: object *fields* must be supplied through the `fields` channel and *properties* through `props` — there is no cross-fallback."
metadata:
  generated-by: mcp-plugin-dotnet
---

# Timeline / Modify Object

Modify a Timeline object by applying a `SerializedMember` diff via ReflectorNet. This is the generic escape hatch for members not covered by the dedicated tools.

## Inputs

- `assetPath` — required `.playable` TimelineAsset path.
- `data` — the `SerializedMember` diff to apply. Put C# *fields* in the `fields` array and *properties* in the `props` array; ReflectorNet resolves them on separate channels with no fallback.
- `trackName` / `trackIndex` — when set, target a track instead of the whole asset.
- `clipIndex` — when >= 0 (and a track is selected), target that clip's `PlayableAsset`.

## Behavior

Resolves the target, applies the diff via `Reflector.TryModify`, and on success marks the asset dirty and saves. The applied logs are returned. Runs on the Unity main thread.

## How to Call

```bash
unity-mcp-cli run-tool timeline-modify --input '{
  "assetPath": "string_value",
  "data": "string_value",
  "trackName": "string_value",
  "trackIndex": 0,
  "clipIndex": 0
}'
```

> For complex input (multi-line strings, code), save the JSON to a file and use:
> ```bash
> unity-mcp-cli run-tool timeline-modify --input-file args.json
> ```
>
> Or pipe via stdin (recommended):
> ```bash
> unity-mcp-cli run-tool timeline-modify --input-file - <<'EOF'
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
| `data` | `string` | Yes | The SerializedMember diff to apply. Fields go in 'fields', properties in 'props'. RQL: SerializedMember |
| `trackName` | `string` | No | Optional track name to target a track instead of the asset. |
| `trackIndex` | `integer` | No | Root-track index used when trackName is null and a track target is wanted (-1 = asset only). |
| `clipIndex` | `integer` | No | Clip index to target that clip's PlayableAsset (-1 = the track/asset itself). |

### Input JSON Schema

```json
{
  "type": "object",
  "properties": {
    "assetPath": {
      "type": "string"
    },
    "data": {
      "type": "string"
    },
    "trackName": {
      "type": "string"
    },
    "trackIndex": {
      "type": "integer"
    },
    "clipIndex": {
      "type": "integer"
    }
  },
  "required": [
    "assetPath",
    "data"
  ]
}
```

## Output

This tool does not return structured output.

