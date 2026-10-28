---
name: terrain-remove-layer
description: Remove a `TerrainLayer` from a `Terrain` by its index. Returns the remaining layer count.
metadata:
  generated-by: mcp-plugin-dotnet
---

# Terrain / Remove Layer

Remove a `TerrainLayer` from a `Terrain`'s `TerrainData.terrainLayers` by index.

## Inputs

- `gameObjectRef` — the GameObject hosting the `Terrain` (required).
- `layerIndex` — index of the layer to remove (required).

## Behavior

Validates the index against the current layer count, removes the layer, reassigns `TerrainData.terrainLayers`, marks the asset + scene dirty, repaints, and returns the remaining layer count. Destructive. Runs on the Unity main thread.

## How to Call

```bash
unity-mcp-cli run-tool terrain-remove-layer --input '{
  "gameObjectRef": "string_value",
  "layerIndex": 0
}'
```

> For complex input (multi-line strings, code), save the JSON to a file and use:
> ```bash
> unity-mcp-cli run-tool terrain-remove-layer --input-file args.json
> ```
>
> Or pipe via stdin (recommended):
> ```bash
> unity-mcp-cli run-tool terrain-remove-layer --input-file - <<'EOF'
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
| `layerIndex` | `integer` | Yes | Index of the TerrainLayer to remove. |

### Input JSON Schema

```json
{
  "type": "object",
  "properties": {
    "gameObjectRef": {
      "type": "string"
    },
    "layerIndex": {
      "type": "integer"
    }
  },
  "required": [
    "gameObjectRef",
    "layerIndex"
  ]
}
```

## Output

This tool does not return structured output.

