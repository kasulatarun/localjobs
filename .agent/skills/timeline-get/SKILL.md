---
name: timeline-get
description: "Generic read: serialize a Timeline object via ReflectorNet — the `TimelineAsset` itself, a `TrackAsset` (by name/index), or a clip's `PlayableAsset` (track + clipIndex). Pair with 'timeline-modify' to write changes back. Read-only."
metadata:
  generated-by: mcp-plugin-dotnet
---

# Timeline / Get Object

Serialize a Timeline object via ReflectorNet. This is the generic escape hatch for fields not covered by the dedicated tools (e.g. an `AnimationPlayableAsset`'s settings or a track's mixer properties).

## Inputs

- `assetPath` — required `.playable` TimelineAsset path.
- `trackName` / `trackIndex` — when set, target a track instead of the whole asset.
- `clipIndex` — when >= 0 (and a track is selected), target that clip's `PlayableAsset`.
- `deepSerialization` — when `true`, recurse through nested objects.

## Behavior

Resolves the target object (asset / track / clip asset), serializes it via ReflectorNet, and returns the serialized member plus the resolved type name. Read-only. Runs on the Unity main thread.

## How to Call

```bash
unity-mcp-cli run-tool timeline-get --input '{
  "assetPath": "string_value",
  "trackName": "string_value",
  "trackIndex": 0,
  "clipIndex": 0,
  "deepSerialization": false
}'
```

> For complex input (multi-line strings, code), save the JSON to a file and use:
> ```bash
> unity-mcp-cli run-tool timeline-get --input-file args.json
> ```
>
> Or pipe via stdin (recommended):
> ```bash
> unity-mcp-cli run-tool timeline-get --input-file - <<'EOF'
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
| `trackName` | `string` | No | Optional track name to target a track instead of the asset. |
| `trackIndex` | `integer` | No | Root-track index used when trackName is null and a track target is wanted (-1 = asset only). |
| `clipIndex` | `integer` | No | Clip index to target that clip's PlayableAsset (-1 = the track/asset itself). |
| `deepSerialization` | `boolean` | No | Performs deep serialization including nested objects. Otherwise only top-level members. |

### Input JSON Schema

```json
{
  "type": "object",
  "properties": {
    "assetPath": {
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
    },
    "deepSerialization": {
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

