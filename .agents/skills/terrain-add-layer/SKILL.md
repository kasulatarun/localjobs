---
name: terrain-add-layer
description: Add a `TerrainLayer` to a `Terrain`. Provide either the asset path of an existing `.terrainlayer` asset, or a texture asset path to build a new TerrainLayer from. Returns the index of the added layer.
metadata:
  generated-by: mcp-plugin-dotnet
---

# Terrain / Add Layer

Append a `TerrainLayer` to a `Terrain`'s `TerrainData.terrainLayers`.

## Inputs

- `gameObjectRef` — the GameObject hosting the `Terrain` (required).
- `terrainLayerAssetPath` — optional project path to an existing `.terrainlayer` asset to add.
- `diffuseTextureAssetPath` — optional project path to a `Texture2D`. When `terrainLayerAssetPath` is omitted, a new `TerrainLayer` is created in-memory with this diffuse texture and added.
- `tileSizeX` / `tileSizeY` — tile size (world units) for a newly-created layer (default 15,15).

## Behavior

Loads or creates the `TerrainLayer`, appends it to `TerrainData.terrainLayers`, marks the asset + scene dirty, repaints, and returns the new layer index. Runs on the Unity main thread.

## How to Call

```bash
unity-mcp-cli run-tool terrain-add-layer --input '{
  "gameObjectRef": "string_value",
  "terrainLayerAssetPath": "string_value",
  "diffuseTextureAssetPath": "string_value",
  "tileSizeX": 0,
  "tileSizeY": 0
}'
```

> For complex input (multi-line strings, code), save the JSON to a file and use:
> ```bash
> unity-mcp-cli run-tool terrain-add-layer --input-file args.json
> ```
>
> Or pipe via stdin (recommended):
> ```bash
> unity-mcp-cli run-tool terrain-add-layer --input-file - <<'EOF'
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
| `terrainLayerAssetPath` | `string` | No | Optional project path to an existing .terrainlayer asset to add. |
| `diffuseTextureAssetPath` | `string` | No | Optional project path to a Texture2D used to build a new TerrainLayer (when no asset path is given). |
| `tileSizeX` | `number` | No | Tile size X (world units) for a newly-created layer. |
| `tileSizeY` | `number` | No | Tile size Y (world units) for a newly-created layer. |

### Input JSON Schema

```json
{
  "type": "object",
  "properties": {
    "gameObjectRef": {
      "type": "string"
    },
    "terrainLayerAssetPath": {
      "type": "string"
    },
    "diffuseTextureAssetPath": {
      "type": "string"
    },
    "tileSizeX": {
      "type": "number"
    },
    "tileSizeY": {
      "type": "number"
    }
  },
  "required": [
    "gameObjectRef"
  ]
}
```

## Output

This tool does not return structured output.

