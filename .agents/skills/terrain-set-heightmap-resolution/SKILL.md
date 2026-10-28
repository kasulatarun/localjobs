---
name: terrain-set-heightmap-resolution
description: Set the heightmap resolution of a `Terrain`'s `TerrainData`. The value is rounded up to a valid `2^n + 1`. Changing resolution resamples the existing heightmap.
metadata:
  generated-by: mcp-plugin-dotnet
---

# Terrain / Set Heightmap Resolution

Set the heightmap resolution of a `Terrain`'s `TerrainData`.

## Inputs

- `gameObjectRef` — the GameObject hosting the `Terrain` (required).
- `heightmapResolution` — requested resolution; rounded up to a valid `2^n + 1` value (clamped to Unity's [33, 4097] range).

## Behavior

Assigns `TerrainData.heightmapResolution`. This is destructive: Unity resamples the existing heightmap to the new resolution. Marks the asset + scene dirty and repaints. Runs on the Unity main thread.

## How to Call

```bash
unity-mcp-cli run-tool terrain-set-heightmap-resolution --input '{
  "gameObjectRef": "string_value",
  "heightmapResolution": 0
}'
```

> For complex input (multi-line strings, code), save the JSON to a file and use:
> ```bash
> unity-mcp-cli run-tool terrain-set-heightmap-resolution --input-file args.json
> ```
>
> Or pipe via stdin (recommended):
> ```bash
> unity-mcp-cli run-tool terrain-set-heightmap-resolution --input-file - <<'EOF'
> {"param": "value"}
> EOF
> ```


### Troubleshooting

If `unity-mcp-cli` is not found, either install it globally (`npm install -g unity-mcp-cli`) or use `npx unity-mcp-cli` instead.
Read the /unity-initial-setup skill for detailed installation instructions.

## Input

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `gameObjectRef` | `string` | Yes | Reference to the GameObject containing the Terrain component. RQL: GameObjectRef |
| `heightmapResolution` | `integer` | Yes | Requested heightmap resolution. Rounded up to a valid (2^n + 1) value. |

### Input JSON Schema

```json
{
  "type": "object",
  "properties": {
    "gameObjectRef": {
      "type": "string"
    },
    "heightmapResolution": {
      "type": "integer"
    }
  },
  "required": [
    "gameObjectRef",
    "heightmapResolution"
  ]
}
```

## Output

This tool does not return structured output.

